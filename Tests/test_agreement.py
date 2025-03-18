import pytest
from playwright.sync_api import expect

@pytest.mark.user_type("PRMGeneralUser")  # Use the role directly
class TestAgreements:
    def test_dashboard_visible(self, authenticated_page):
        """Verify the dashboard is visible after login."""
        page = authenticated_page["page"]
        user = authenticated_page["user"]

        print(f"Testing as {user['role']}")

        # Get the iframe
        dashboard_iframe = page.frame_locator("//iframe[@title='dashboard']")
        expect(dashboard_iframe.locator("//span[@title='PRM Dashboard']")).to_be_visible(timeout=10000)

        print("✅ Dashboard visibility verified")