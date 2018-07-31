import time
from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Can reach the homepage
        self.browser.get("http://localhost:8000")

        # WebApp has correct name and header mentioning to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element("h1").text
        self.assertIn("To-Do", header_text)

        # Can enter item in to-do list straight away
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do iten")

        # Can enter content in a text box
        inputbox.send_keys("Buy peacock feathers")

        # When user press enter, the page updates and list the added item in the to-do list table
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows))

        # Can add more item in the to-do list
        self.fail("Finish the test!")

        # If update the page, the items are still there

        # Each to-do has it's own URL, as explain to users

        # URL return the corresponding to-do list


if __name__ == "__main__":
    unittest.main()
