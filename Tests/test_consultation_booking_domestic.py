import pytest
from Pages.consultation_forms import ConsultationForms
from Utils.user_actions import (
    fill_personal_details,
    fill_academic_details,
    navigate_to_date_page,
    select_available_timeslot,
    is_time_slot_unavailable,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def shared_context():
    return {}

def complete_consultation_booking(page, salesforce_urls, consultation_forms, is_international=True):
    """Helper function to complete the consultation booking process."""
    profile_url = salesforce_urls["consultation_domestic_booking_url"]
    page.goto(profile_url)
    page.wait_for_load_state("networkidle")
    logger.info(f"Navigated to {'international' if is_international else 'domestic'} consultation booking page.")

    # Fill personal and academic details
    fill_personal_details(page, consultation_forms.selectors, is_international=False)
    fill_academic_details(page, consultation_forms.selectors)

    # Proceed to appointment selection and select time slot
    consultation_forms.proceed_to_appointment_selection()
    consultation_forms.select_appointment_type()
    selected_slot, attempts = select_available_timeslot(page, consultation_forms.selectors)

    return selected_slot, attempts

@pytest.mark.usefixtures("salesforce_urls", "page")
def test_first_user_booking(salesforce_urls, page, shared_context):
    """Test to book a consultation as the first user."""
    try:
        consultation_domestic = ConsultationForms(page)
        selected_slot, attempts = complete_consultation_booking(page, salesforce_urls, consultation_domestic, is_international=False)
        shared_context["selected_slot"] = selected_slot
        shared_context["attempts"] = attempts

        # Confirm booking and validate thank you message
        consultation_domestic.confirm_booking()

        consultation_domestic.confirm_final_message()
        consultation_domestic.click_finish_button()
        consultation_domestic.validate_thank_you_message()

        logger.info(f"First User Selected Time Slot: {selected_slot} after {attempts} clicks.")
    except Exception as e:
        logger.error(f"Test Failed: {str(e)}")
        raise

@pytest.mark.usefixtures("salesforce_urls", "page")
def test_second_user_validate_time_slot(salesforce_urls, page, shared_context):
    """Test to validate that the selected time slot is unavailable for the second user."""
    selected_slot = shared_context.get("selected_slot")
    attempts = shared_context.get("attempts")
    assert selected_slot, "Shared context does not contain 'selected_slot'."
    assert attempts is not None, "Shared context does not contain 'attempts'."

    try:
        consultation_domestic = ConsultationForms(page)
        profile_url = salesforce_urls["consultation_international_booking_url"]
        page.goto(profile_url)
        page.wait_for_load_state("networkidle")
        logger.info("Navigated to consultation booking page for the second user.")

        # Fill personal and academic details
        fill_personal_details(page, consultation_domestic.selectors, is_international=False)
        fill_academic_details(page, consultation_domestic.selectors)

        # Proceed to appointment selection and navigate to the same date page
        consultation_domestic.proceed_to_appointment_selection()
        consultation_domestic.select_appointment_type()
        navigate_to_date_page(page, consultation_domestic.selectors, attempts)

        # Validate that the previously selected time slot is unavailable
        is_unavailable = is_time_slot_unavailable(page, consultation_domestic.selectors, selected_slot)
        assert is_unavailable, f"Validation failed: The time slot '{selected_slot}' is still available for the second user."
        logger.info(f"The time slot '{selected_slot}' is no longer available for subsequent users.")
    except Exception as e:
        logger.error(f"Test Failed: {str(e)}")
        raise