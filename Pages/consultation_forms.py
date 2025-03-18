from Utils.user_actions import (
    fill_personal_details,
    fill_academic_details,
    navigate_to_date_page,
    select_available_timeslot,
    is_time_slot_unavailable,
)
from playwright.async_api import Page

class ConsultationForms:
    def __init__(self, page: Page):
        self.page = page
        self.selectors = {
            "first_name": "//input[@name='First_Name']",
            "last_name": "//input[@name='Last_Name']",
            "email_address": "//input[@name='Email0']",
            "mobile": "//input[@name='Mobile']",
            "interested_course": "//select[@name='CaseStudyInterest']",
            "interested_course_dom":"//select[@id='select-123']",
            "study_level": "//select[@name='CaseStudyLevel']",
            "location": "//select[@name='Campus_Interest0']",
            "course_name": "//input[@name='Course_Name']",
            "details_textbox": "//input[@id='input-101']",
            "details_textbox_dom": "//input[@id='input-120']",
            "next_button": "//button[@type='button']",
            "appointment_type_dom": "//span[contains(text(),'Face to Face at our Melbourne (Bundoora) Campus')]",
            "appointment_type_next": "//button[normalize-space()='Next']",
            "time_slots": "//label[contains(@for, 'radio')]/span[contains(@class, 'slds-radio_faux')]",
            "review_details": "//u[normalize-space()='Review Consultation Details']",
            "final_message": "//u[normalize-space()='We look forward to seeing you']",
            "finish_button": "//button[@type='button']",
            "thank_you_text": "//h1[normalize-space()='Thank you']",
            "date_next_button": "//button[@title='Next calendar page']",
        }

    def proceed_to_appointment_selection(self):
        """Click Next button to proceed to appointment type selection."""
        self.page.click(self.selectors["next_button"])

    def select_appointment_type(self):
        """Select Face-to-Face appointment type and proceed."""
        self.page.check(self.selectors["appointment_type_dom"])
        self.page.click(self.selectors["appointment_type_next"])

    def confirm_booking(self):
        """Confirm the consultation booking."""
        self.page.click(self.selectors["appointment_type_next"])
        self.page.locator(self.selectors["review_details"]).wait_for(timeout=15000)

    def confirm_final_message(self):
        """Confirm the final message."""
        self.page.click(self.selectors["appointment_type_next"])
        self.page.locator(self.selectors["final_message"]).wait_for(timeout=15000)

    def click_finish_button(self):
        """Click finish Button."""
        self.page.click(self.selectors["finish_button"])

    def validate_thank_you_message(self):
        """Validates the Thank You message."""
        self.page.locator(self.selectors["thank_you_text"]).wait_for(timeout=5000)