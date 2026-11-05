"""电商业务表结构（ORM 模型）。

用 SQLAlchemy 声明 products / orders / order_items / users /
orders_archive / table_metadata 六张表的字段与关系；
seed 建表、后续 SQL 查询都依赖这里的定义。
"""
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(50), index=True)
    price: Mapped[float] = mapped_column(Float)
    cost: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    status: Mapped[str] = mapped_column(String(20))
    total_amount: Mapped[float] = mapped_column(Float)
    channel: Mapped[str] = mapped_column(String(20))

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)
    refunded: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    region: Mapped[str] = mapped_column(String(20), index=True)
    register_date: Mapped[datetime] = mapped_column(DateTime)

class OrdersArchive(Base):
    """归档表：故意留作 Schema 路由的干扰项，不应被问数选中。"""
    __tablename__ = "orders_archive"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    order_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20))
    total_amount: Mapped[float] = mapped_column(Float)
    channel: Mapped[str] = mapped_column(String(20))

class TableMetadata(Base):
    """Schema 路由的元数据表。"""
    __tablename__ = "table_metadata"
    id: Mapped[int] = mapped_column(primary_key=True)
    table_name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text)
    key_fields: Mapped[str] = mapped_column(Text)  # JSON 字符串
