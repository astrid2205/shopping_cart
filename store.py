from product import Product

class Store:
    """
    A class representing a store with a shelf of products.

    Attributes:
        shelf (dict): A dictionary where the keys are product names and the values are Product instances.
    """

    def __init__(self):
        """ Initialize an empty store. """
        self.shelf = {}


    def add_product(self, product: Product):
        """
        Add a product to the shelf.

        Raises:
            TypeError: If the product is not an instance of Product.
            ValueError: If the product is already on the shelf.
        """
        if not isinstance(product, Product):
            raise TypeError("You should only add the product to the shelf.")
        product_name = product.get_item_code()
        if product_name in self.shelf:
            raise ValueError(f"The product {product_name} is already on the shelf.")
        self.shelf[product_name] = product


    def get_shelf(self):
        """
        Returns the shelf of the store.

        Returns:
            dict: The shelf of the store, where the keys are product names and the values are Product instances.
        """
        return self.shelf
