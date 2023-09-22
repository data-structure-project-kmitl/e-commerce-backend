def individual_serial_product(Product) -> dict:
    return {
        "id": str(Product["_id"]),
        "name": Product["name"],
        "price": Product["price"],
        "type": Product["type"],
        "quantity": Product["quantity"]
    }


def list_serial_product(product) -> list:
    return [individual_serial_product(product) for product in product]
