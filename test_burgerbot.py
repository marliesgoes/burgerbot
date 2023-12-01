import unittest
from burgerbot import extract_recipe, execute_recipe
from image_segmentation import get_camera_image, find_center_of


class TestExtractRecipe(unittest.TestCase):

    def setUp(self):
        self.messages = [{'role': 'system', 'content': "You are a robot chef that can prepare a limited set of food items.\n        You have the following items: Burger buns, tomatoes, lettuce, pickles, \n        burger patties, cheese, toast, ham.\n        If prompted to make a dish, first check whether you have the correct ingredients\n        to serve that dish. If you don't have all the ingredients, propose an alternative\n        for the user to order. If there is ambiguity about the person's request, ask follow-up\n        questions to clear things up.\n        If you have all the required information for a certain dish and all the\n        ingredients are available, list all the ingredients you will be using.\n        If the user confirms their order, reply with 'confirmation'."},
                         {'role': 'user', 'content': ' Hi, I will have a burger with ham and cheese please.'},
                         {'role': 'system',
                          'content': "You've requested a burger with ham and cheese. I have all the necessary ingredients to prepare this dish: burger buns, tomatoes, lettuce, pickles, cheese, and ham (which will be used instead of a regular burger patty, if that's okay with you). Please confirm your order."},
                         {'role': 'user', 'content': " Yeah, that's okay."},
                         {'role': 'system', 'content': 'Confirmation. Your burger with ham and cheese will be made with burger buns, tomatoes, lettuce, pickles, cheese, and ham. Enjoy your meal!'}]

    def test_extract_recipe(self):
        ingredients = extract_recipe(self.messages)
        for ingredient in ingredients:
            print('🌼 ', ingredient)

    def test_execute_recipe(self):
        # ingredients = ['bun', 'patty', 'cheese', 'lettuce', 'tomato', 'bun']
        ingredients = ['cheese', 'tomato']
        execute_recipe(ingredients)

    def test_get_camera_image(self):
        get_camera_image()

    def test_find_center_of(self):
        image = get_camera_image()
        camera_coords = find_center_of('Tomato', image, visualize=True)
        print('camera_coords:', camera_coords)


if __name__ == '__main__':
    unittest.main()
