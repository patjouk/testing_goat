from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Can reach the homepage
        self.browser.get('http://localhost:8000')

        # WebApp has correct name
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # Can enter item in to-do list straight away

        # Can enter content in a text box

        # Enter add item in the to-do list

        # Can add more item in the to-do list

        # If update the page, the items are still there

        # Each to-do has it's own URL, as explain to users

        # URL return the corresponding to-do list


if __name__ == '__main__':
    unittest.main()
