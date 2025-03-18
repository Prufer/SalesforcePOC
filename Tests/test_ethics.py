import re
import pytest
from playwright.sync_api import expect
from Pages.home_page import HomePage

@pytest.mark.user_type("Ethics")
class TestEthics:
    def test_open_prime_ethics(self, authenticated_page):
        """Verify PRIME Ethics can be searched and opened from App Launcher."""
        page = authenticated_page["page"]
        home_page = HomePage(page)  # Create HomePage instance

        home_page.click_app_launcher()
        home_page.search_in_app_launcher("PRIME Ethics")
        home_page.click_on_app_search_result("PRIME Ethics")

        # ✅ Verify navigation happened successfully
        expect(page).to_have_url(re.compile(".*lightning/page/home.*"), timeout=10000)





