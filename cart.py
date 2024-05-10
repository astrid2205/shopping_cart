from store import Store
from product import Product

class Cart:
    """
    A class representing a shopping cart in a store.

    Attributes:
        cart: A dictionary where the keys are product names and the values are quantities.
        subtotal: The current subtotal of the shopping cart.
        store: The store where the cart is shopping.
    """
    def __init__(self, store: Store):
        """
        Initialize an empty shopping cart with a subtotal of 0 in a given store.

        Args:
            store (Store): The store where the cart is shopping.
        """
        self.cart = {}
        self.subtotal = 0
        self.store = store

    def get_cart(self):
        """
        Returns the current products and their quantities in the shopping cart 
        as a dictionary, sorted by the product name in ascending order.
        """
        return dict(sorted(self.cart.items()))
    
    def get_subtotal(self):
        """ Returns the current subtotal of the shopping cart. """
        return self.subtotal

    def update_subtotal(self, price):
        """ Add the `price` to the subtotal of the cart. """
        self.subtotal += price

    def add_product(self, product: str, quantity: int):
        """ 
        Adds a `product` with a given `quantity` to the shopping cart.

        Raises:
            TypeError: If the `product` is None or empty.
            TypeError: If the `quantity` is not a non-negative integer.
            ValueError: If the `product` is not in the store.

        >>> store = Store()
        >>> product_A = Product("A", 50, 3, 140)
        >>> store.add_product(product_A)
        >>> cart = Cart(store)
        >>> cart.add_product("A", 3)
        >>> cart.get_cart()
        {'A': 3}
        """
        if not product:
            raise TypeError(f"Invalid product {product}.")
        if not isinstance(quantity, int) or quantity < 0:
            raise TypeError(f"The quantity of {product} should be a non-negative integer.")
        if product not in self.store.get_shelf():
            raise ValueError(f"We don't have {product} in our store.")
        if quantity != 0:
            product = str(product)
            quantity_before = self.cart.get(product, 0)
            quantity_after = quantity_before + quantity
            self.cart[product] = quantity_after
            product_instance = self.store.get_shelf().get(product)
            price_difference = product_instance.price_difference(quantity_before, quantity_after)
            self.update_subtotal(price_difference)
    

    def take_order(self, data: list):
        """ 
        Takes an order from the `data` and adds the products in the data to the shopping cart.
        The shopping cart only handles valid products and quantities. 
        Invalid products or quantities will be printed to the terminal.
        
        Args:
            data (list): The order, represented as a list of dictionaries. Each dictionary should have a 'code' key and a 'quantity' key.
        
        Example of data:
        ```
        [{"code":"A","quantity":3}, {"code":"B","quantity":3}, {"code":"C","quantity":1}, {"code":"D","quantity":2}]

        ```
        """
        if not data or not isinstance(data, list):
            print(f"The data {data} is not a valid list.")
            return
        for order_item in data:
            if not isinstance(order_item, dict):
                print(f"The order item {order_item} is not a dictionary.")
                continue
            try:
                product = order_item['code']
                quantity = order_item['quantity']
                self.add_product(product, quantity)
            except KeyError as e:
                print(f"An error occurred: Cannot retrieve {e} from the order item: {order_item}.")
            except Exception as e:
                print(f"An error occurred: {e}")
