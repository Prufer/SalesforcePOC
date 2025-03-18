import pytest
from playwright.async_api import Page, expect

from Utils.user_actions import UserActions


@pytest.mark.asyncio
async def test_open_app_launcher(page: Page):
    """Verify that the app launcher opens successfully."""
    user_actions = UserActions(page)
    await page.goto("https://example.com")  # Replace with your target URL

    # Test open_app_launcher
    await user_actions.open_app_launcher()

    # Verify that the search input is visible
    search_input = page.locator(user_actions.selectors['app_launcher_search_input'])
    await expect(search_input).to_be_visible()
    print("✅ App launcher opened successfully")

@pytest.mark.asyncio
async def test_search_in_app_launcher(page: Page):
    """Verify that searching in the app launcher works."""
    user_actions = UserActions(page)
    await page.goto("https://example.com")  # Replace with your target URL

    # Test search_in_app_launcher
    search_text = "PRIME Ethics"
    await user_actions.search_in_app_launcher(search_text)

    # Verify that the search input contains the entered text
    search_input = page.locator(user_actions.selectors['app_launcher_search_input'])
    await expect(search_input).to_have_value(search_text)
    print(f"✅ Successfully searched for '{search_text}' in app launcher")

@pytest.mark.asyncio
async def test_search_in_main_search(page: Page):
    """Verify that searching in the main search bar works."""
    user_actions = UserActions(page)
    await page.goto("https://example.com")  # Replace with your target URL

    # Test search_in_main_search
    search_text = "PRIME Ethics"
    await user_actions.search_in_main_search(search_text)

    # Verify that the main search input contains the entered text
    main_search_input = page.locator(user_actions.selectors['main_search_bar'])
    await expect(main_search_input).to_have_value(search_text)
    print(f"✅ Successfully searched for '{search_text}' in main search")