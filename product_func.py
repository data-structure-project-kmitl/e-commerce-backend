def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]['price']  # Assuming 'price' is a field in your product documents
        less_than_pivot = [item for item in arr[1:] if item['price'] < pivot]
        greater_than_pivot = [item for item in arr[1:] if item['price'] >= pivot]
        return quick_sort(less_than_pivot) + [arr[0]] + quick_sort(greater_than_pivot)



def quick_sort_high_low(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]['price']  # Assuming 'price' is a field in your product documents
        less_than_pivot = [item for item in arr[1:] if item['price'] < pivot]
        greater_than_pivot = [item for item in arr[1:] if item['price'] >= pivot]
        return quick_sort(greater_than_pivot) + [arr[0]] + quick_sort(less_than_pivot)
    

def linear_search(products, search_name):
    matching_products = []
    for product in products:
        if search_name.lower() in product['name'].lower() or search_name.lower() in product.get('type', '').lower():
            matching_products.append(product)
    return matching_products

