from Data.DatabaseManager import DatabaseManager
from Data.Models import ProductModel
from Data.Repositories import ProductRepository, StockRepository

if __name__ == '__main__':
    db_manager = DatabaseManager()
    db_manager.initialise_database()
    db_manager.generate_test_data()

    product_repo = ProductRepository(db_manager)
    stock_repo = StockRepository(db_manager, product_repo)
    prod = product_repo.get_product(1)
    print(f"Product with id=1 is: \n{prod}")

    iphone_se = product_repo.create_product("iPhone SE 2", "A cheaper iPhone", 2)
    print(f"Created iphone se: \n{iphone_se}")

    iPad = product_repo.get_product(3)
    iPad.description = "Apple tablet"
    iPad.target_stock = 3
    product_repo.edit_product(iPad)

    all_prods = product_repo.get_all_products()
    print(f"All Products ({len(all_prods)})")
    print("|   id  |      name       |       description        | target stock |")
    print("|-------+-----------------+--------------------------+--------------|")
    for p in all_prods:
        print (f"| {p.id:5} | {p.name:15} | {p.description:24} |  {p.target_stock:11} |")

    print ("All Stock: ")
    all_stock = stock_repo.get_all_stock_items()
    for si in all_stock:
        print (si.id, si.product.name, si.location, si.quantity)

    print ("iPhone Stock")
    iphone_x_stock = stock_repo.get_stock_for_product(1)
    for si in iphone_x_stock:
        print (si.id, si.product.name, si.location, si.quantity)

    total = stock_repo.get_total_product_stock(1)
    print("Total iPhone X stock is: ", total)
