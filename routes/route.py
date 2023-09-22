from fastapi import APIRouter
from models.Product import Product
from config.database import collections
from schema.schemas import list_serial_product
from bson import ObjectId
from product_func import quick_sort , quick_sort_high_low , linear_search


router = APIRouter()


@router.get("/")
async def get_products():
    products = list_serial_product(collections["product"].find())
    return products

@router.get("/sort/byPriceToHigh")
async def get_products_sortbyprice():
    products = list_serial_product(collections["product"].find())
    sorted_productsToHigh = quick_sort(products)
    return sorted_productsToHigh

@router.get("/sort/byPriceToLow")
async def get_products_sortbyprice():
    products = list_serial_product(collections["product"].find())
    sorted_productsToLow = quick_sort(products)
    sorted_productsToLow.reverse()
    return sorted_productsToLow

@router.get("/sort/byLimitPrice/{price}")
async def get_product_sortbylimitprice(price: float):
    products = list_serial_product(collections["product"].find())
    products = [product for product in products if product['price'] <= price]
    products = quick_sort(products)
    return products


@router.post("/")
async def post_product(product: Product):
    collections["product"].insert_one(dict(product))
    return dict(product)


@router.put("/{id}")
async def put_product(id: str, product: Product):
    collections.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(product)})
    return dict(product)


@router.delete("/{id}")
async def delete_product(id: str):
    collections.find_one_and_delete({"_id": ObjectId(id)})

@router.get("/search/product")
async def search_product_by_name(product_name: str):
    # Access the 'product' collection
    products = list_serial_product(collections["product"].find())

    # Use linear search to find products with matching names
    matching_products = linear_search(products, product_name)
    
    # Sort the matching products by price using Quick Sort
    sorted_products = quick_sort(matching_products)
    
    # You can further process 'sorted_products' as needed
    return sorted_products