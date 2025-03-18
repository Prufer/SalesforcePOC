import pytest
import logging
from typing import Dict, Any

from pages.scripts import args
from playwright.sync_api import Browser, Page, sync_playwright
from pathlib import Path

from Pages import LoginPage
from Utils.load_user import USERS  # Import the pre-loaded users

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_TIMEOUT = 15000
SALESFORCE_BASE_URL = "https://latrobe--uat.sandbox.lightning.force.com/"
CONSULTATION_BOOKINGS_DOMESTIC_STUDENTS_URL="https://latrobe--uat.sandbox.my.site.com/s/"
CONSULTATION_BOOKINGS_INTERNATIONAL_STUDENTS_URL="https://latrobe--uat.sandbox.my.site.com/s/home-international"


class BrowserConfig:
    """Browser configuration settings."""
    HEADLESS = False  # Toggle for CI/CD
    VIEWPORT = {"width": 1920, "height": 1080}
    SLOW_MO = 50  # Milliseconds between actions

# Use sync_playwright for sync browser handling
@pytest.fixture(scope="session")
def browser() -> Browser:
    """Session-scoped fixture that provides a browser instance."""
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(
                headless=BrowserConfig.HEADLESS,
                slow_mo=BrowserConfig.SLOW_MO,
                args=['--deny-permission-prompts']
            )
            logger.info("Browser launched successfully")
            yield browser
        except Exception as e:
            logger.error(f"Failed to launch browser: {str(e)}")
            raise
        finally:
            browser.close()
            logger.info("Browser closed")

# Page fixture
@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    """Function-scoped fixture that provides a page instance."""
    context = browser.new_context(viewport=BrowserConfig.VIEWPORT)
    page = context.new_page()
    logger.info("New page created")

    yield page

    try:
        context.close()
        logger.info("Browser context closed")
    except Exception as e:
        logger.error(f"Error closing browser context: {str(e)}")

# Fixture to get a user by key from the pre-loaded users
@pytest.fixture(scope="session")
def get_user():
    """Fixture to get a user by key from the pre-loaded users."""
    def _get_user(user_key: str):
        user = USERS.get(user_key)
        if not user:
            available_users = ", ".join(USERS.keys())
            raise ValueError(f"User '{user_key}' not found. Available users: {available_users}")
        return user
    return _get_user

# Fixture to log in as a specific user
@pytest.fixture(scope="function")
def login_as_user(page: Page, get_user):
    """Fixture to log in as a specific user."""
    def _login_as_user(user_key: str):
        user = get_user(user_key)
        login_page = LoginPage(page)
        login_page.navigate_to_login()
        login_page.login(user["email"], user["password"])

        # Wait for Salesforce redirect
        page.wait_for_url(f"{SALESFORCE_BASE_URL}**", timeout=DEFAULT_TIMEOUT)

        # Verify URL
        assert SALESFORCE_BASE_URL in page.url, f"Login failed. Unexpected URL: {page.url}"

        logger.info(f"Successfully logged in as {user['role']}")
        return user

    return _login_as_user

# Fixture to provide an authenticated page
@pytest.fixture(scope="function")
def authenticated_page(request, page: Page, login_as_user) -> Dict[str, Any]:
    """Function-scoped fixture that provides an authenticated page."""
    try:
        if not hasattr(request.cls, 'pytestmark'):
            raise ValueError("Test class must specify a user_type marker")

        user_type = request.cls.pytestmark[0].args[0]
        user = login_as_user(user_type)
        logger.info(f"Authenticated as user type: {user_type}")

        return {"page": page, "user": user}

    except Exception as e:
        logger.error(f"Failed to set up authenticated page: {str(e)}")
        raise

# # Fixture for creating UserActions instance
# @pytest.fixture(scope="function")
# def user_actions(page) -> UserActions:
#     """Fixture for creating UserActions instance."""
#     return UserActions(page)

#Fixture to return URLS
@pytest.fixture(scope="session")
def salesforce_urls():
    """Fixture to provide Salesforce URLs"""
    return {
        "base_url": SALESFORCE_BASE_URL,
        "consultation_domestic_booking_url": CONSULTATION_BOOKINGS_DOMESTIC_STUDENTS_URL,
        "consultation_international_booking_url": CONSULTATION_BOOKINGS_INTERNATIONAL_STUDENTS_URL,
    }


pytest_plugins = "pytest_asyncio"

def pytest_configure():
    pytest.asyncio_mode = "auto"


