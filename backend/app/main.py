from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ShopLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发期放开，部署前收紧
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}
