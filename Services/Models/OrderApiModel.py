class OrderApiModel:
    name: str
    address: str
    item_name: str
    price: int
    storefront: str

    def __init__(self, name: str, address: str, item_name: str, price: int, storefront: str) -> None:
        self.name = name
        self.address = address
        self.item_name = item_name
        self.price = price
        self.storefront = storefront


"""
Order API JSON Example:
{
   "name" : "Natalie Portman",
   "address" : "12 Russell Square, London",
   "item" : "Xiaomi Mi Note 10",
   "price" : 250
}
"""
