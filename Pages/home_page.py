import logging
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.app_launcher_button = page.locator("//div[@class='slds-icon-waffle']")
        self.app_launcher_search = page.locator("//input[@placeholder='Search apps and items...']")
        self.main_search = page.get_by_label("Search", exact=True)  # Fixed locator
        self.main_search_textbox = page.locator("//input[@placeholder='Search...']")


    def click_app_launcher(self):
        """Clicks on the App Launcher button."""
        self.app_launcher_button.click()
        logger.info("Clicked on the App Launcher button")

    def search_in_app_launcher(self, search_text: str):
        """Search for an app or item inside the App Launcher."""
        # Ensure search input is visible before typing
        expect(self.app_launcher_search).to_be_visible(timeout=5000)

        # Fill the search box
        self.app_launcher_search.fill(search_text)
        self.page.wait_for_timeout(2000)  # Wait for results to appear
        logger.info(f"Searched for '{search_text}' in App Launcher")

    def click_on_app_search_result(self, search_text: str):
        """Click on the desired app search result in the App Launcher."""
        try:
            # Wait for the search results to be visible
            search_result_locator = self.page.locator(f"role=option >> text={search_text}").first

            # Ensure it's visible
            expect(search_result_locator).to_be_visible(timeout=10000)

            # Click on the search result
            search_result_locator.click()
            logger.info(f"Clicked on '{search_text}' in the App Launcher")

            # Wait for navigation
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)

        except Exception as e:
            logger.error(f"Failed to click search result: {str(e)}")
            logger.error(f"Current URL: {self.page.url}")
            self.page.screenshot(path="error-screenshot.png")
            raise

    def search_on_global_search(self, search_text: str):
        """Search for a term in the global search bar."""
        expect(self.main_search_textbox).to_be_visible(timeout=15000)

        self.main_search_textbox.click()

        # Fill the search box
        self.main_search_textbox.fill(search_text)
        self.page.wait_for_timeout(2000)  # Wait for results to appear
        logger.info(f"Searched for '{search_text}' in global search")

    def search_and_click_result(self, search_text: str, result_title: str):
        """
        Generic method to search for a term in the global search and click on a specific result.
        :param search_text: The text to search for.
        :param result_title: The title of the result to click on.
        """
        try:
            # Step 1: Click on the global search bar
            self.main_search.click()
            logger.info("Clicked on the global search bar")

            # Step 2: Fill the search term
            self.main_search_textbox.fill(search_text)
            self.page.wait_for_timeout(2000)  # Wait for results to appear
            logger.info(f"Filled '{search_text}' in the global search bar")

            # Step 3: Click on the search result with the specified title
            self.page.get_by_title(result_title).click()
            logger.info(f"Clicked on '{result_title}' in the search results")

            # Step 4: Wait for navigation and log the URL and title
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            logger.info(f"Current URL after navigation: {self.page.url}")
            logger.info(f"Current Title after navigation: {self.page.title()}")

        except Exception as e:
            logger.error(f"Failed during search and click: {str(e)}")
            logger.error(f"Current URL: {self.page.url}")
            self.page.screenshot(path="search-error-screenshot.png")
            raise