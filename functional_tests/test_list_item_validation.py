from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Alice tries to add an empty item in the list and press Enter.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the list page.
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

        # She start typing some text and the error disappears
        self.get_item_input_box().send_keys("Buy milk")
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:valid")
        )

        # She can submit that new item successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # She tries to add another blank item.
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, it doesn't work and the browser intercepts the request
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

        # She corrects her mistake and enter text.
        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:valid")
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")

    def test_cannot_add_duplicate_items(self):
        # Alice goes to the home page and start a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy chocolate")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy chocolate")

        # She likes chocolate so much se wants to add it a second time
        self.get_item_input_box().send_keys("Buy chocolate")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She sees an error message
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You've already got this in your list",
            )
        )
