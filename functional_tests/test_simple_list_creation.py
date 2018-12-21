from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        # Can reach the homepage
        self.browser.get(self.live_server_url)

        # WebApp has correct name and header mentioning to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # Can enter item in to-do list straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # Can enter content in a text box
        inputbox.send_keys("Buy peacock feathers")

        # When user press enter, the page updates and list the added item in the to-do list table
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # Can add more items in the to-do list
        self.add_list_item("Use peacock feathers to make a fly")

        # When the page is updated, both items are listed
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Bob starts a new to-do list
        self.browser.get(self.live_server_url)
        self.add_list_item("Buy peacock feathers")

        # Bob to-do list has a unique URL
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, "/lists/.+")

        # Alice also wants a to-do list!

        # Closing Bob's browser and opening a new one for Alice
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Alice's homepage doesn't have Bob's content
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Alice creates her list
        self.add_list_item("Buy milk")

        # Alice gets her own URL
        alice_list_url = self.browser.current_url
        self.assertRegex(alice_list_url, "/lists/.+")
        self.assertNotEqual(alice_list_url, bob_list_url)

        # Bob's list is not there
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)
