"""
ShopLens 种子数据脚本。

故意制造的业务"坑"（用于验证 Agent 鲁棒性）：
1. "销量"有歧义：order_items.quantity 是件数，orders.total_amount 是金额
2. 8% 的 order_items.refunded = 1：销量是否排除退款
3. 10% 的 products.is_active = 0：下架商品不应出现在排行
4. 存在 orders_archive：Schema 路由的干扰项
5. 时间相对 now() 生成：保证"最近 7 天"永远有数据
"""
import json
import random
from datetime import datetime, timedelta

from faker import Faker
from app.db.base import engine, SessionLocal
from app.db.models import (
    Base, Product, Order, OrderItem, User, OrdersArchive, TableMetadata,
)

fake = Faker("zh_CN")
random.seed(42)  # 可复现

CATEGORIES = ["美妆", "数码", "家居", "服饰", "食品", "母婴", "运动", "图书", "宠物", "汽车用品"]
PRODUCT_SUFFIX = ["水乳", "耳机", "收纳盒", "连衣裙", "零食礼包", "奶瓶", "瑜伽垫", "小说", "猫粮", "车载支架"]
REGIONS = ["广东", "浙江", "江苏", "上海", "北京", "四川", "山东", "福建"]
CHANNELS = ["App", "小程序", "Web", "线下"]


def seed() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    now = datetime.now()
    try:
        # users
        db.bulk_save_objects([
            User(id=i + 1, region=random.choice(REGIONS),
                 register_date=now - timedelta(days=random.randint(30, 500)))
            for i in range(500)
        ])

        # products（10% 下架）
        db.bulk_save_objects([
            Product(
                id=i + 1,
                name=f"{random.choice(['轻奢','经典','新款','限定'])}{fake.word()}{random.choice(PRODUCT_SUFFIX)}",
                category=random.choice(CATEGORIES),
                price=(p := round(random.uniform(10, 800), 2)),
                cost=round(p * random.uniform(0.3, 0.7), 2),
                created_at=now - timedelta(days=random.randint(10, 400)),
                is_active=random.random() > 0.1,
            )
            for i in range(300)
        ])

        # orders（90 天跨度）+ order_items（每单 1~5 条，8% 退款）
        orders, items, item_id = [], [], 1
        for i in range(8000):
            days_ago = random.randint(0, 89)
            oid = i + 1
            total = 0.0
            orders.append(Order(
                id=oid, user_id=random.randint(1, 500),
                order_date=now - timedelta(days=days_ago, hours=random.randint(0, 23)),
                status=random.choice(["paid", "paid", "paid", "shipped", "refunded"]),
                total_amount=0.0,  # 稍后回填
                channel=random.choice(CHANNELS),
            ))
            for _ in range(random.randint(1, 5)):
                pid = random.randint(1, 300)
                qty = random.choice([1, 1, 1, 2, 2, 3, 4, 5])
                unit = round(random.uniform(10, 800), 2)
                total += qty * unit
                items.append(OrderItem(
                    id=item_id, order_id=oid, product_id=pid,
                    quantity=qty, unit_price=unit,
                    refunded=random.random() < 0.08,
                ))
                item_id += 1
            orders[-1].total_amount = round(total, 2)

        db.bulk_save_objects(orders)
        db.bulk_save_objects(items)

        # orders_archive：仅建表 + 少量历史数据，作为 Schema 路由干扰项
        db.bulk_save_objects([
            OrdersArchive(
                id=i + 1, user_id=random.randint(1, 500),
                order_date=now - timedelta(days=random.randint(365, 730)),
                status="paid", total_amount=round(random.uniform(50, 2000), 2),
                channel=random.choice(CHANNELS),
            )
            for i in range(200)
        ])

        # table_metadata（Schema 路由的种子）
        meta = [
            ("products", "商品表，包含商品名称、品类、价格、成本、是否上架。销量排行时必须过滤 is_active=1。",
             ["name", "category", "price", "is_active"]),
            ("orders", "订单主表，包含下单时间、订单状态、总金额、渠道。total_amount 是金额不是件数。",
             ["order_date", "status", "total_amount", "channel"]),
            ("order_items", "订单明细表，quantity 是件数，refunded=1 表示该明细已退款。计算销量时应排除退款。",
             ["product_id", "quantity", "unit_price", "refunded"]),
            ("users", "用户表，包含注册地区和注册时间。",
             ["region", "register_date"]),
            ("orders_archive", "历史归档订单表（一年前），不用于近期经营分析。",
             ["order_date", "total_amount"]),
        ]
        db.bulk_save_objects([
            TableMetadata(table_name=n, description=d, key_fields=json.dumps(f, ensure_ascii=False))
            for n, d, f in meta
        ])

        db.commit()
        print(f"✅ seed done: users=500 products=300 orders=8000 items={len(items)}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
