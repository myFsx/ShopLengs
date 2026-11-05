"""验证数据能回答核心问数场景：近 7 天销量 TOP5（排除退款、排除下架商品）。"""
from sqlalchemy import text
from app.db.base import SessionLocal

SQL = """
SELECT p.name, p.category, SUM(oi.quantity) AS sales
FROM order_items oi
JOIN orders o        ON oi.order_id = o.id
JOIN products p      ON oi.product_id = p.id
WHERE o.order_date >= datetime('now', '-7 days')
  AND oi.refunded = 0
  AND p.is_active = 1
GROUP BY p.id
ORDER BY sales DESC
LIMIT 5;
"""

def main() -> None:
    db = SessionLocal()
    try:
        rows = db.execute(text(SQL)).fetchall()
        print("近 7 天销量 TOP5（已排除退款与下架）：")
        for i, (name, cat, sales) in enumerate(rows, 1):
            print(f"  {i}. {name} [{cat}] — {sales} 件")
        assert len(rows) == 5, "结果不足 5 条，检查数据分布"
        print("✅ check passed")
    finally:
        db.close()

if __name__ == "__main__":
    main()
