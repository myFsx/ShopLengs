"""数据库连接配置。

负责定位 SQLite 文件路径（backend/shop_lens.db），创建 SQLAlchemy engine，
以及 SessionLocal 会话工厂，供建表、种子脚本和后续查询复用。
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# backend/shop_lens.db
DB_PATH = Path(__file__).resolve().parent.parent.parent / "shop_lens.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
