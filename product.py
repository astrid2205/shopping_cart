from numbers import Number

class Product:
    def __init__(self, item_code, unit_price: Number, special_quantity: int=None, special_price: Number=None):
        """ 
        Represents a product with a unit price and an optional special price.

        For example, Product A costs 50 per unit, 
        and 3 of product A costs 140 would look like this.
        >>> product_A = Product("A", 50, 3, 140)

        Raises:
            ValueError: If `unit_price` or `special_price` is not a positive number.
            ValueError: If `special_quantity` is not a positive integer.
        """
        validate_product_parameters(unit_price, special_quantity, special_price)    
        self.item_code = item_code
        self.unit_price = unit_price
        self.special_quantity = special_quantity
        self.special_price = special_price


    def get_item_code(self):
        """ Return the product's item code as a string. """
        return str(self.item_code)
    

    def get_unit_price(self):
        """ Return the product's unit price. """
        return self.unit_price
    

    def get_special_price(self):
        """ 
        Return a string describing the product's special price and its quantity, 
        or a message indicating there is no special price.
        """
        if self.special_price and self.special_quantity:
            return f"{self.special_quantity} of {self.get_item_code()} costs {self.special_price}"
        else:
            return f"There is no special price for {self.get_item_code()}"


    def calculate_price(self, quantity: int) -> Number:
        """ 
        Returns and return the total price for a given `quantity` of the product.

        Raises:
            ValueError: If `quantity` is not a non-negative integer.

        """
        if not is_non_negative(int, quantity):
            raise ValueError(f"The quantity of {self.get_item_code()} should be a non-negative integer.")

        if self.special_quantity and self.special_price and quantity >= self.special_quantity:
            special_bundle_count = quantity // self.special_quantity
            remaining_item_count = quantity % self.special_quantity
            price = special_bundle_count * self.special_price + remaining_item_count * self.unit_price
        else:
            price = quantity * self.unit_price
        return price
    
    
    def price_difference(self, quantity_before: int, quantity_after: int) -> Number:
        """ 
        Returns the price difference resulting from a change in the quantity of the product.
        `quantity_before` is the quantity of the product before the change.
        `quantity_after` is the quantity of the product after the change.
        
        Raises:
            ValueError: If `quantity_before` or `quantity_after` is not a non-negative integer.

        >>> product_A = Product("A", 50, 3, 140)
        >>> product_A.price_difference(2, 3)
        40
        >>> product_A.price_difference(3, 4)
        50
        >>> product_A.price_difference(4, 3)
        -50
        >>> product_A.price_difference(3, 2)
        -40
        """
        if not is_non_negative(int, quantity_before) or not is_non_negative(int, quantity_after):
            raise ValueError("The quantity of the product should be a non-negative integer.")
        if quantity_after == quantity_before:
            return 0
        return self.calculate_price(quantity_after) - self.calculate_price(quantity_before)
    

def is_non_negative(number_type, number):
    """ 
    Check if the argument `number` of type `number_type` is non-negative..
    >>> is_non_negative(int, 3)
    True
    >>> is_non_negative(Number, 4.33)
    True
    >>> is_non_negative(Number, -4.33)
    False
    """
    return isinstance(number, number_type) and number >= 0


def validate_product_parameters(unit_price, special_quantity, special_price):
    """ 
    Validate parameters for the Product class. 

    `unit_price` should be a non-negative number.
    `special_quantity` should be a positive integer if it is not None.
    `special_price` should be a non-negative number if it is not None.
    """
    if not is_non_negative(Number, unit_price):
        raise ValueError("Unit price should be a non-negative number.")
    if special_quantity is not None and (not isinstance(special_quantity, int) or special_quantity <= 0):
        raise ValueError("Special quantity should be a positive integer.")
    if special_price and not is_non_negative(Number, special_price):
        raise ValueError("Special price should be a non-negative number.")