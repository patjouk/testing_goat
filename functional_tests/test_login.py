from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = "alex@example.com"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):
    def test_can_email_link_to_log_in(self):
        # Alex can enter their email in the login section of the navbar
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling them an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                "Check your email", self.browser.find_element_by_tag_name("body").text
            )
        )

        # They check their email and find a message
        email = mail.outbox[0]
        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # They click the link
        self.browser.get(url)

        # They're logged in
        self.wait_for(lambda: self.browser.find_element_by_link_text("Log out"))
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)
