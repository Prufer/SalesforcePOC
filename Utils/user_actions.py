import logging
import random

import page
from faker import Faker
from playwright.async_api import Page
from Utils.data_generator import (
    generate_random_name,
    generate_random_mobile_local,
    generate_random_mobile_international,
    generate_random_word,
    generate_paragraph, generate_random_org_name,
)

fake = Faker()
logger = logging.getLogger(__name__)

async def handle_captcha(page: Page):
    """Handles CAPTCHA detection and allows for manual solving."""
    try:
        captcha_locator = page.locator("//input[@id='input-114']")
        if await captcha_locator.is_visible():
            logger.warning("CAPTCHA detected! Waiting for manual solving...")
            await page.wait_for_timeout(30000)  # Allow time for manual intervention
            logger.info("CAPTCHA resolved manually.")
            return True
        logger.info("No CAPTCHA detected.")
        return False
    except Exception as e:
        logger.error(f"Error handling CAPTCHA: {str(e)}")
        raise ValueError("Failed to handle CAPTCHA.")

def fill_personal_details(page, selectors, is_international=True):
    """Fill out the personal details form."""
    first_name = generate_random_name()
    last_name = fake.last_name()
    email = f"{first_name}.{last_name}@example.com"
    mobile = generate_random_mobile_international() if is_international else generate_random_mobile_local()
    page.fill(selectors["first_name"], first_name)
    page.fill(selectors["last_name"], last_name)
    page.fill(selectors["email_address"], email)
    page.fill(selectors["mobile"], mobile)
    logger.info("Filled personal details.")

def fill_academic_details(page, selectors):
    """Fill out the academic details section."""
    dropdown_interested_course = page.locator(selectors["interested_course"]).locator("..").locator("select")
    dropdown_interested_course.select_option(index=1)
    page.select_option(selectors["interested_course"], index=1)
    page.select_option(selectors["study_level"], index=3)
    page.select_option(selectors["location"], index=4)
    page.fill(selectors["course_name"], generate_random_word())
    page.fill(selectors["details_textbox"], generate_paragraph())
    logger.info("Filled academic details.")

def navigate_to_date_page(page, selectors, attempts: int):
    """Navigate to a specific date page by clicking the date_next_button a given number of times."""
    if attempts == 0:
        logger.info("No navigation required as attempts is 0.")
        return
    for _ in range(attempts):
        logger.info(f"Clicking 'Next' calendar button, attempt {_ + 1}/{attempts}...")
        try:
            page.wait_for_selector(selectors["date_next_button"], state="visible", timeout=10000)
            page.click(selectors["date_next_button"])
            page.wait_for_load_state("networkidle")
        except Exception as e:
            logger.error(f"Failed to click the date_next_button: {str(e)}")
            raise ValueError("Could not navigate to the next date page.")
    logger.info(f"Successfully navigated to date page after {attempts} clicks.")

def select_available_timeslot(page, selectors):
    """
    Navigate through dates until an available time slot is found.
    Returns the selected time slot and the number of clicks on the date_next_button.
    """
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        try:
            page.wait_for_load_state("networkidle")
            logger.info(f"Attempt {attempts + 1}: Waiting for time slots to load...")
            time_slots = page.locator(selectors["time_slots"]).all()
            available_slots = [slot for slot in time_slots if slot.is_visible() and slot.is_enabled()]
            if available_slots:
                selected_slot = available_slots[0].inner_text().strip()
                available_slots[0].click()
                logger.info(f"Selected Time Slot: {selected_slot} on attempt {attempts + 1}")
                return selected_slot, attempts
            logger.info("No available time slots. Moving to the next date...")
        except Exception as e:
            logger.error(f"Error on attempt {attempts + 1}: {str(e)}")
        try:
            logger.info("Clicking date_next_button...")
            page.click(selectors["date_next_button"])
            page.wait_for_load_state("networkidle")
            attempts += 1
        except Exception as e:
            logger.error(f"Failed to click date_next_button: {str(e)}")
            raise ValueError("Could not navigate to the next date page.")
    raise ValueError("No available time slots found after checking multiple dates.")

def is_time_slot_unavailable(page, selectors, selected_slot: str):
    """
    Check if a specific time slot is unavailable.
    :param selected_slot: The text of the previously selected time slot.
    """
    try:
        page.wait_for_selector(selectors["time_slots"], timeout=5000)
        time_slot_locator = page.locator(f"//label/span[contains(text(), '{selected_slot}')]")
        is_disabled = time_slot_locator.get_attribute("disabled") is not None
        return is_disabled or not time_slot_locator.is_visible()
    except Exception:
        return True

import random
from playwright.sync_api import Locator

def select_random_dropdown_option(dropdown_locator: Locator, dropdown_list_locator: Locator):
    """
    Selects a random option from a dropdown.
    """
    try:
        # Click the dropdown to open it
        print("Clicking the dropdown...")
        dropdown_locator.click()

        # Wait for the dropdown options to be visible
        print("Waiting for dropdown options to be visible...")
        dropdown_list_locator.first.wait_for(state="visible", timeout=60000)

        # Retrieve all dropdown options
        print("Retrieving dropdown options...")
        options = dropdown_list_locator.all()

        # Check if there are any options available
        if options:
            # Exclude the first option
            if len(options) > 1:
                options = options[1:]  # Skip the first option
                print(f"Found {len(options)} options (excluding the first one). Selecting a random one...")
                random_option = random.choice(options)
                random_option.click()
                print("Selected option clicked.")
            else:
                raise Exception("No options available after excluding the first one")
        else:
            raise Exception("No options found in the dropdown")
    except Exception as e:
        print(f"Error selecting dropdown option: {e}")
        raise


def get_mandatory_field_errors(page):
    page.wait_for_selector("ul.errorsList.slds-list_dotted.slds-m-left_medium li a")  # Ensure error messages are loaded

    error_elements = page.locator("ul.errorsList.slds-list_dotted.slds-m-left_medium li a").all()  # Select the <a> elements

    error_texts = [error.inner_text().strip() for error in error_elements]  # Extract text
    print(f"Extracted errors: {error_texts}")  # Debugging
    return error_texts









