# Shopping cart

A simple checkout system that consumes a data source like [this](https://spareroom.github.io/recruitment/docs/cart-kata/data-set-1.json), and returns the subtotal when queried.

## Usage

To use the shopping cart, follow these steps:

1.  Clone the repository:

    ```
    git clone https://github.com/astrid2205/shopping_cart.git
    ```

2.  cd into the directory:

    ```
    cd shopping_cart
    ```

3.  Add your own data files to the current directory (under `shopping_cart/`). The file should be JSON format.

    For example: `data-set-3.json`

    ```
    [
        { "code": "A", "quantity": 3 },
        { "code": "B", "quantity": 4 },
        { "code": "C", "quantity": 2 },
        { "code": "D", "quantity": 3 }
    ]
    ```

4.  Run the project:
    ```
    python main.py
    ```
5.  Follow the instructions on the terminal:

    ```
    Please enter the file name or press Enter to use the default data file (data-set-1.json):
    ```

    Here we enter the file `data-set-3.json` we just added to the directory.

    The program will print out the data from the input file, the content inside the shopping cart, and the subtotal of the shopping cart.

    ```
    Data: [{'code': 'A', 'quantity': 3}, {'code': 'B', 'quantity': 4}, {'code': 'C', 'quantity': 2}, {'code': 'D', 'quantity': 3}]

    Shopping cart content: {'A': 3, 'B': 4, 'C': 2, 'D': 3}

    Subtotal: 346
    ```

    The shopping cart only handles valid products and quantities. Invalid products or quantities will be printed to the terminal.

    For example:

    ```
    An error occurred: Cannot retrieve 'quantity' from the order item: {'code': 'A'}.
    An error occurred: Cannot retrieve 'code' from the order item: {'quantity': 3}.
    An error occurred: The quantity of C should be a non-negative integer.
    The order item ['Not a dictionary'] is not a dictionary.

    Data: [{'code': 'A'}, {'quantity': 3}, {'code': 'C', 'quantity': 'Not integer'}, ['Not a dictionary'], {'code': 'A', 'quantity': 5}, {'code': 'B', 'quantity': 3}, {'code': 'D', 'quantity': 8}, {'code': 'B', 'quantity': 2}, {'code': 'A', 'quantity': 2}, {'code': 'C', 'quantity': 5}]

    Shopping cart content: {'A': 7, 'B': 5, 'C': 5, 'D': 8}

    Subtotal: 706
    ```

## Files

To maintain future scalability and avoid the code becoming overly complex and difficult to manage, I modularize the code into components such as product, store, cart, and implement them using classes.

- `product.py`:

  - This file contains the `Product` class which represents a product with a unit price and an optional special price.
  - `calculate_price` method calculates the total price for a given quantity of the product based on the unit price and the special price (if any).

- `store.py`:

  - This file defines a `Store` class that represents a store with a shelf of products.
  - `add_product` method adds a `Product` instance to the shelf.

- `cart.py`:

  - This file defines a `Cart` class that represents a shopping cart in a store.
  - `Cart` class takes a `Store` instance as an argument when initializing an empty shopping cart in a given store.
  - `take_order` method takes an order from the data and adds the products in the data to the shopping cart. The shopping cart only handles valid products and quantities. Invalid products or quantities will be printed to the terminal.
  - `get_subtotal` method returns the current subtotal of the shopping cart.

- `main.py`

  - This file is the entry point of the shopping cart application.
  - The `main` function does the following:

    1. Sets up a store with four products, each represented by an instance of the `Product` class, and adds these products to the store.
    2. Creates a new shopping cart in the store.
    3. Asks the user for the name of a JSON file that contains an order. If the user doesn't provide a file name, it uses a default file named `data-set-1.json`.
    4. Tries to open the specified file and load the JSON data from it. If successful, it adds the products in the data to the shopping cart, and then prints the order data, the content of the shopping cart, and the subtotal of the shopping cart.
    5. Handles and prints out various exceptions that might occur when opening the file or adding the products to the shopping cart.

- `test.py`

  - This file contains unit tests for the initialization and methods of the `Product`, `Store`, and `Cart` class. It also contains tests for the `main` function in `main.py`.
  - To run the tests, simply run `python test.py`
