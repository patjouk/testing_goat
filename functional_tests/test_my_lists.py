from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from functional_tests.base import FunctionalTest

User = get_user_model()


class MyListTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # To set a cookie, we need to first visit the domain. 404 pages load the quickest :D
        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session.session_key, path="/")
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = "alex@example.com"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Alex is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_saved_as_my_file(self):
        # Alex is a logged-in user
        self.create_pre_authenticated_session("alex@example.com")

        # They go to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticulate splines")
        self.add_list_item("Immanentize eschaton")
        first_list_utl = self.browser.current_url

        # They notice a "My lists" link, for the first time.
        self.browser.find_element_by_link_text("My lists").click()

        # They see that their list is in there, named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Reticulate splines")
        )
        self.browser.find_element_by_link_text("Reticulate splines").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_utl)
        )

        # They decide to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        # Under "my lists", Their new lists appears
        self.browser.find_element_by_link_text("My lists").click()
        self.wait_for(lambda: self.browser.find_element_by_link_text("Click cows"))
        self.browser.find_element_by_link_text("Click cows").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # They log out. The "My lists" option disappears
        self.browser.find_element_by_link_text("Log out").click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_link_text("My lists"), []
            )
        )
