import unittest
from product import Product
from store import Store
from cart import Cart
from numbers import Number
from unittest.mock import patch
from io import StringIO
from main import main


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.product_A = Product("A", 50, 3, 140)
        self.product_B = Product("B", 35, 2, 60)
        self.product_C = Product("C", 25)
        self.product_D = Product("D", 12)
        self.product_E = Product("E", 10.5, 3, 29.9)


    def test_product_initialization_with_invalid_values(self):
        message_unit_price = "Unit price should be a non-negative number."
        self.assertRaisesRegex(ValueError, message_unit_price, Product, "E", -8, 12, 20)
        self.assertRaisesRegex(ValueError, message_unit_price, Product, "E", "Hi!", 12, 20)

        message_special_quantity = "Special quantity should be a positive integer."
        self.assertRaisesRegex(ValueError, message_special_quantity, Product, "E", 10, 0, 20)
        self.assertRaisesRegex(ValueError, message_special_quantity, Product, "E", 10, -3, 20)
        self.assertRaisesRegex(ValueError, message_special_quantity, Product, "E", 10, 12.3, 20)
        self.assertRaisesRegex(ValueError, message_special_quantity, Product, "E", 10, "HELLO", 20)

        message_special_price = "Special price should be a non-negative number."
        self.assertRaisesRegex(ValueError, message_special_price, Product, "E", 300, 12, -20)
        self.assertRaisesRegex(ValueError, message_special_price, Product, "E", 300, 12, "YEAH")


    def test_product_property(self):
        self.assertEqual("A", self.product_A.get_item_code())
        self.assertEqual("B", self.product_B.get_item_code())
        self.assertEqual("C", self.product_C.get_item_code())
        self.assertEqual("D", self.product_D.get_item_code())

        self.assertEqual(50, self.product_A.get_unit_price())
        self.assertEqual(25, self.product_C.get_unit_price())
        self.assertEqual(10.5, self.product_E.get_unit_price())

        self.assertEqual("3 of A costs 140", self.product_A.get_special_price())
        self.assertEqual("There is no special price for C", self.product_C.get_special_price())


    def test_valid_quantity_input(self):
        """ Test whether the method `calculate_price` has valid `quantity` input. """
        message = "The quantity of A should be a non-negative integer."
        self.assertRaisesRegex(ValueError, message, self.product_A.calculate_price, -1)
        self.assertRaisesRegex(ValueError, message, self.product_A.calculate_price, 1.35)
        self.assertRaisesRegex(ValueError, message, self.product_A.calculate_price, "ABC")
        self.assertIsInstance(self.product_A.calculate_price(3), Number)

    
    def test_price_calculation(self):
        self.assertEqual(0, self.product_A.calculate_price(0))
        self.assertEqual(50, self.product_A.calculate_price(1))
        self.assertEqual(100, self.product_A.calculate_price(2))
        self.assertEqual(140, self.product_A.calculate_price(3))
        self.assertEqual(190, self.product_A.calculate_price(4))
        self.assertEqual(280, self.product_A.calculate_price(6))
        self.assertEqual(380, self.product_A.calculate_price(8))
        
        self.assertEqual(0, self.product_B.calculate_price(0))
        self.assertEqual(35, self.product_B.calculate_price(1))
        self.assertEqual(60, self.product_B.calculate_price(2))
        self.assertEqual(95, self.product_B.calculate_price(3))
        self.assertEqual(120, self.product_B.calculate_price(4))
        self.assertEqual(3000, self.product_B.calculate_price(100))

        self.assertEqual(25, self.product_C.calculate_price(1))
        self.assertEqual(50, self.product_C.calculate_price(2))

        self.assertEqual(10.5, self.product_E.calculate_price(1))
        self.assertEqual(21, self.product_E.calculate_price(2))
        self.assertEqual(29.9, self.product_E.calculate_price(3))

    
    def test_price_difference(self):
        self.assertEqual(50, self.product_A.price_difference(4, 5))
        self.assertEqual(40, self.product_A.price_difference(5, 6))
        self.assertEqual(0, self.product_A.price_difference(6, 6))
        self.assertEqual(-280, self.product_A.price_difference(6, 0))
        self.assertEqual(240, self.product_A.price_difference(0, 5))
        self.assertEqual(280, self.product_A.price_difference(0, 6))
        self.assertEqual(46390, self.product_A.price_difference(6, 1000))

        message = "The quantity of the product should be a non-negative integer."
        self.assertRaisesRegex(ValueError, message, self.product_A.price_difference, -1, 3)
        self.assertRaisesRegex(ValueError, message, self.product_A.price_difference, 3, -3)
        self.assertRaisesRegex(ValueError, message, self.product_A.price_difference, "A", 3)



class StoreTestCase(unittest.TestCase):
    def test_store(self):
        # Empty store
        store = Store()
        self.assertEqual({}, store.get_shelf())

        product_A = Product("A", 50, 3, 140)
        product_B = Product("B", 35, 2, 60)

        # Add valid products
        store.add_product(product_A)
        store.add_product(product_B)
        self.assertEqual({"A": product_A, "B": product_B}, store.get_shelf())

        # Trying to add a product which is not a Product instance
        message_not_a_product = "You should only add the product to the shelf."
        self.assertRaisesRegex(TypeError, message_not_a_product, store.add_product, "Not a product")
        
        store_B = Store()
        self.assertEqual({}, store_B.get_shelf())

        # Add a product that already exists
        message_already_exist = "The product A is already on the shelf."
        self.assertRaisesRegex(ValueError, message_already_exist, store.add_product, product_A)


class CartTestCast(unittest.TestCase):
    def setUp(self):
        # Set up a store with product A, B, C, D and an empty shopping cart in the store
        self.store = Store()
        self.product_A = Product("A", 50, 3, 140)
        self.product_B = Product("B", 35, 2, 60)
        self.product_C = Product("C", 25)
        self.product_D = Product("D", 12)
        self.store.add_product(self.product_A)
        self.store.add_product(self.product_B)
        self.store.add_product(self.product_C)
        self.store.add_product(self.product_D)
        self.cart = Cart(self.store)

    def test_empty_cart(self):
        self.assertEqual({}, self.cart.get_cart())

    def test_add_product(self):
        # Add valid products
        self.cart.add_product("A", 3)
        self.assertEqual({"A": 3}, self.cart.get_cart())
        self.assertEqual(140, self.cart.get_subtotal())
        self.cart.add_product("A", 4)
        self.assertEqual({"A": 7}, self.cart.get_cart())
        self.assertEqual(330, self.cart.get_subtotal())
        self.cart.add_product("B", 8)
        self.assertEqual({"A": 7, "B": 8}, self.cart.get_cart())
        self.assertEqual(570, self.cart.get_subtotal())


        # Try adding invalid quantities
        message = "The quantity of A should be a non-negative integer."
        self.assertRaisesRegex(TypeError, message, self.cart.add_product, "A", -1)
        self.assertRaisesRegex(TypeError, message, self.cart.add_product, "A", 1.35)
        self.assertRaisesRegex(TypeError, message, self.cart.add_product, "A", "invalid")

        # Try adding products not in the store
        message_not_on_shelf = "We don't have E in our store."
        self.assertRaisesRegex(ValueError, message_not_on_shelf, self.cart.add_product, "E", 1)
    

    def test_add_product_with_zero_quantity(self):
        self.cart.add_product("A", 0)
        self.assertEqual({}, self.cart.get_cart())


    def test_add_product_with_none_product(self):
        self.assertRaisesRegex(TypeError, "Invalid product.", self.cart.add_product, None, 1)
        self.assertRaisesRegex(TypeError, "Invalid product.", self.cart.add_product, "", 1)

            
    def test_add_product_updates_subtotal_correctly(self):
        self.cart.add_product("A", 1)
        self.assertEqual(50, self.cart.get_subtotal())
        self.cart.add_product("A", 2)
        self.assertEqual(140, self.cart.get_subtotal())
        self.cart.add_product("B", 1)
        self.assertEqual(175, self.cart.get_subtotal())
        self.cart.add_product("B", 1)
        self.assertEqual(200, self.cart.get_subtotal())
        self.cart.add_product("C", 1)
        self.assertEqual(225, self.cart.get_subtotal())
        self.cart.add_product("D", 1)
        self.assertEqual(237, self.cart.get_subtotal())
        self.cart.add_product("B", 1)
        self.assertEqual({"A": 3, "B": 3, "C": 1, "D": 1}, self.cart.get_cart())
        self.assertEqual(272, self.cart.get_subtotal())


    @patch('sys.stdout', new_callable=StringIO)
    def test_take_order(self, mock_stdout):
        self.cart.take_order([{'code': 'A', 'quantity': 3}, {'code': 'B', 'quantity': 3}, {'code': 'C', 'quantity': 1}, {'code': 'D', 'quantity': 2}])
        self.assertEqual({"A": 3, "B": 3, "C": 1, "D": 2}, self.cart.get_cart())
        self.cart.take_order([{'code': 'E', 'quantity': 3}, {'code': 'B', 'quantity': 3}, {'code': 'C', 'quantity': 1}, {'code': 'D', 'quantity': 2}, {'code': 'D', 'quantity': 0}])
        self.assertEqual({"A": 3, "B": 6, "C": 2, "D": 4}, self.cart.get_cart())
        self.assertEqual(mock_stdout.getvalue(), "An error occurred: We don't have E in our store.\n")
    

    @patch('sys.stdout', new_callable=StringIO)
    def test_take_order_with_invalid_data(self, mock_stdout):
        self.cart.take_order([])
        self.cart.take_order({'code': 'A', 'quantity': 3})
        print_msg = (
            "The data [] is not a valid list.\n"
            "The data {'code': 'A', 'quantity': 3} is not a valid list.\n"
        )
        self.assertEqual(mock_stdout.getvalue(), print_msg)

        
    @patch('sys.stdout', new_callable=StringIO)
    def test_take_order_with_invalid_product_or_quantity(self, mock_stdout):
        self.cart.take_order([{'code': 'E', 'quantity': 3}, {'code': None, 'quantity': 3}, {'code': 'B', 'quantity': "invalid"}, {'code': 'C', 'quantity': -1}, {'code': 'D', 'quantity': 2.46}])
        self.assertEqual({}, self.cart.get_cart())
        print_msg = (
            "An error occurred: We don't have E in our store.\n"
            "An error occurred: Invalid product None.\n"
            "An error occurred: The quantity of B should be a non-negative integer.\n"
            "An error occurred: The quantity of C should be a non-negative integer.\n"
            "An error occurred: The quantity of D should be a non-negative integer.\n"
        )
        self.assertEqual(mock_stdout.getvalue(), print_msg)


    @patch('sys.stdout', new_callable=StringIO)
    def test_take_order_with_invalid_type(self, mock_stdout):
        self.cart.take_order([["quantity", 3]])
        self.cart.take_order([{"quantity": 3}])
        self.cart.take_order([{"code": "A"}])
        print_msg = (
            "The order item ['quantity', 3] is not a dictionary.\n"
            "An error occurred: Cannot retrieve 'code' from the order item: {'quantity': 3}.\n"
            "An error occurred: Cannot retrieve 'quantity' from the order item: {'code': 'A'}.\n"
        )
        self.assertEqual(mock_stdout.getvalue(), print_msg)


class TestCheckoutSystem(unittest.TestCase):
    @patch('builtins.input', return_value='')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[{"code":"A","quantity":3}, {"code":"B","quantity":3}, {"code":"C","quantity":1}, {"code":"D","quantity":2}]')
    @patch('json.load', return_value=[{"code":"A","quantity":3}, {"code":"B","quantity":3}, {"code":"C","quantity":1}, {"code":"D","quantity":2}])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout, mock_json, mock_open, mock_input):
        main()
        mock_input.assert_called_once_with("Please enter the file name or press Enter to use the default data file (data-set-1.json): ")
        mock_open.assert_called_once_with('data-set-1.json', 'r')
        mock_json.assert_called_once()
        print_msg = (
            "\nData: [{'code': 'A', 'quantity': 3}, {'code': 'B', 'quantity': 3}, {'code': 'C', 'quantity': 1}, {'code': 'D', 'quantity': 2}]\n\n"
            "Shopping cart content: {'A': 3, 'B': 3, 'C': 1, 'D': 2}\n\n"
            "Subtotal: 284\n"
        )
        self.assertEqual(mock_stdout.getvalue(), print_msg)


    data_with_invalid_input = [
        { "code": "A" },
        { "quantity": 3 },
        { "code": "C", "quantity": "Not integer" },
        ["Not a dictionary"],
        { "code": "A", "quantity": 5 },
        { "code": "B", "quantity": 3 },
        { "code": "D", "quantity": 8 },
        { "code": "B", "quantity": 2 },
        { "code": "A", "quantity": 2 },
        { "code": "C", "quantity": 5 }
    ]

    @patch('builtins.input', return_value='data-set-2.json')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=str(data_with_invalid_input))
    @patch('json.load', return_value=data_with_invalid_input)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_some_invalid_input(self, mock_stdout, mock_json, mock_open, mock_input):
        main()
        mock_input.assert_called_once_with("Please enter the file name or press Enter to use the default data file (data-set-1.json): ")
        mock_open.assert_called_once_with('data-set-2.json', 'r')
        mock_json.assert_called_once()
        print_msg = (
            "An error occurred: Cannot retrieve 'quantity' from the order item: {'code': 'A'}.\n"
            "An error occurred: Cannot retrieve 'code' from the order item: {'quantity': 3}.\n"
            "An error occurred: The quantity of C should be a non-negative integer.\n"
            "The order item ['Not a dictionary'] is not a dictionary.\n\n"
            "Data: [{'code': 'A'}, {'quantity': 3}, {'code': 'C', 'quantity': 'Not integer'}, ['Not a dictionary'], {'code': 'A', 'quantity': 5}, {'code': 'B', 'quantity': 3}, {'code': 'D', 'quantity': 8}, {'code': 'B', 'quantity': 2}, {'code': 'A', 'quantity': 2}, {'code': 'C', 'quantity': 5}]\n\n"
            "Shopping cart content: {'A': 7, 'B': 5, 'C': 5, 'D': 8}\n\n"
            "Subtotal: 706\n"
        )
        self.assertEqual(mock_stdout.getvalue(), print_msg)


if __name__ == '__main__':
    unittest.main()    
