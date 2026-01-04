# main.py
import json
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Мини-маркет API",
    description="API для получения списка товаров. Поддерживает фильтрацию.",
    version="1.0",
)

# Загружаем товары из JSON
DATA_PATH = Path(__file__).parent / "products.json"
with open(DATA_PATH, encoding="utf-8") as f:
    PRODUCTS = json.load(f)


@app.get("/api/products", summary="Получить список товаров")
async def get_products(
        category: Optional[str] = Query(None, description="Категория (точное совпадение)"),
        min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
        max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
        q: Optional[str] = Query(None, description="Поиск по названию (регистронезависимый)"),
):
    """
    Возвращает список товаров с возможностью фильтрации.

    Примеры:
    - Все товары: `/api/products`
    - Смартфоны до 30 000 ₽: `/api/products?category=Смартфоны&max_price=30000`
    - Что-то с 'mi' в названии: `/api/products?q=mi`
    """
    result = PRODUCTS

    if category is not None:
        result = [p for p in result if p["category"] == category]
    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    if q is not None:
        q_lower = q.lower()
        result = [p for p in result if q_lower in p["name"].lower()]

    return JSONResponse(result)
