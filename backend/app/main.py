from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text

from .db.base import SessionLocal

app = FastAPI(title="ShopLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

# P0 阶段验证过的 SQL
HARDCODED_SQL = """
SELECT p.name, SUM(oi.quantity) AS sales
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

@app.post("/api/chat")
def chat(req: ChatRequest):
    # 注意：这里先忽略 req.message，不管用户问什么，都返回这条 SQL 的结果
    db = SessionLocal()
    try:
        rows = db.execute(text(HARDCODED_SQL)).fetchall()
        data = [{"name": row[0], "sales": row[1]} for row in rows]

        return {
            "chart_type": "bar",
            "x_field": "name",
            "y_field": "sales",
            "title": "近7天销量TOP5（硬编码）",
            "data": data
        }
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}
