from fastapi import FastAPI
from app.routers import auth, product, category, review, cart, order

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])
app.include_router(review.router, prefix="/reviews", tags=["Reviews"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])

@app.get("/")
def read_root():
    return {"message": "Game PC Store Backend is running!"}