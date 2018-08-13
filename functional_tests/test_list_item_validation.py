from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Alice tries to add an empty item in the list and press Enter.
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # The home page refreshes: it has an error message saying empty items can't be added.
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector(".has-error").text, "You can't have an empty list item"))

        # She decides to add an item with some text. It works.
        self.browser.find_element_by_id("id_new_item").send_keys("Buy milk")

        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # She tries to add another blank item.
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # It still doesn't work and she get the same error message.
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector(".has-error").text, "You can't have an empty list item"))

        # She corrects her mistake and enter text.
        self.browser.find_element_by_id("id_new_item").send_keys("Make tea")

        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")
