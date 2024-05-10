import json
from product import Product
from cart import Cart
from store import Store


def main():
    # Set up store and create a new shopping cart
    store = Store()
    products = [
        Product("A", 50, 3, 140),
        Product("B", 35, 2, 60),
        Product("C", 25),
        Product("D", 12)
    ]
    for product in products:
        store.add_product(product)
    cart = Cart(store)

    # Ask the user for the file name
    file_name = input("Please enter the file name or press Enter to use the default data file (data-set-1.json): ")
    if not file_name:
        file_name = 'data-set-1.json'

    # Open data file and take order
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
            cart.take_order(data)
            print(f"\nData: {data}\n")
            print(f"Shopping cart content: {cart.get_cart()}\n")
            print(f"Subtotal: {cart.get_subtotal()}")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except json.JSONDecodeError:
        print(f"The file {file_name} is not a valid JSON file.")
    except PermissionError:
        print(f"Permission denied when trying to open {file_name}.")
    except IsADirectoryError:
        print(f"{file_name} is a directory, not a file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()    