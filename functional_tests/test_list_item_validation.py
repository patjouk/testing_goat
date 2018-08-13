from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Alice tries to add an empty item in the list and press Enter.

        # The home page refreshes: it has an error message saying empty items can't be added.

        # She decides to add an item with some text. It works.

        # She tries to add another blank item.

        # It still doesn't work and she get the same error message.

        # She corrects her mistake and enter text.
        self.fail("WRITE ME!")
