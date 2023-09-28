from fastapi import APIRouter , Query , HTTPException , Body , Path
from models.Product import Product
from config.database import collections
from schema.schemas import list_serial_product
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
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
async def post_product(product: Product, image: UploadFile = File(...)):

    image_data = base64.b64encode(await image.read()).decode("utf-8")
    product.image_base64 = image_data
    
    # Insert the product into the MongoDB collection
    
    collections["product"].insert_one(dict(product))
    
    return dict(product)


@router.put("/{id}")
async def put_product(id: str, product: Product):
    # Assuming 'collections' is a MongoDB collection
    # Use the 'update_one' method to update the document
    result = collections["product"].update_one(
        {"_id": ObjectId(id)},
        {"$set": dict(product)}
    )

    # Check if the update was successful
    if result.modified_count == 1:
        # Return the updated product
        return dict(product)
    else:
        # Product not found or update failed
        return {"message": "Product not found or update failed"}


@router.delete("/{id}")
async def delete_product(id: str):
    # Convert the ID to ObjectId
    object_id = ObjectId(id)

    # Try to find and delete the product
    result = collections["product"].find_one_and_delete({"_id": object_id})

    if result:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.get("/search/product")
async def search_product_by_name_or_type(product_name_or_type: str):
    # Access the 'product' collection
    products = list_serial_product(collections["product"].find())

    # Use linear search to find products with matching names
    matching_products = linear_search(products, product_name_or_type)
    
    # Sort the matching products by price using Quick Sort
    sorted_products = quick_sort(matching_products)
    
    # You can further process 'sorted_products' as needed
    return sorted_products


    



