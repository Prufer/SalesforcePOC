import random
import string
from playwright.async_api import Page

from Utils.data_generator import generate_random_mobile_local
from Utils.user_actions import generate_random_name, generate_random_mobile_international, generate_random_word, generate_paragraph


class ConsultationDomestic:
    """Common user actions that can be shared across tests."""

    def __init__(self, page: Page):
        """Initialize UserActions with a page instance."""
        self.page = page

        # Common selectors
        self.selectors = {
            # Forms (Consultation Bookings - Domestic Students)
            "first_name": "//input[@id='input-86']",
            "last_name": "//input[@id='input-91']",
            "email_address": "//input[@id='input-96']",
            "mobile": "//input[@id='input-101']",
            "interested_course": "//select[@id='select-121']",
            "study_level": "//select[@id='select-106']",
            "location": "//select[@id='select-109']",
            "course_name": "//input[@id='input-114']",
            "details_textbox": "//textarea[@id='input-118']",
            "next_button":"//button[@type='button']",


            #Appoinment_Types_Selction
            "appointment_type_dom": "//span[contains(text(),'Face to Face')]",
            "appointment_type_next" : "//button[normalize-space()='Next']",

            #Date_Time_Selection
            "Date_Time_next" : "//button[normalize-space()='Next']",

        }

        # Generate random first name, last name, and email
        self.first_name = generate_random_name()
        self.last_name = "Autotest"
        self.email = f"{self.first_name}.{self.last_name}@ltuautotest.com"

    def fill_first_name(self):
        """Fills the first name input with a random name."""
        self.page.fill(self.selectors["first_name"], self.first_name)

    def fill_last_name(self):
        """Fills the last name input with a fixed last name."""
        self.page.fill(self.selectors["last_name"], self.last_name)

    def fill_email(self):
        """Fills the email input with a generated email."""
        self.page.fill(self.selectors["email_address"], self.email)

    def fill_mobile_international(self):
        """Fills the mobile input with a generated mobile number."""
        mobile = generate_random_mobile_international()
        self.page.fill(self.selectors["mobile"], mobile)

    def fill_mobile_local(self):
        """Fills the mobile input with a generated mobile number."""
        mobile = generate_random_mobile_local()
        self.page.fill(self.selectors["mobile"], mobile)

    def select_course(self):
        """Selects the first available course from the dropdown."""
        self.page.select_option(self.selectors["interested_course"], index=1)

    def select_study_level(self):
        """Selects the first available study level from the dropdown."""
        self.page.select_option(self.selectors["study_level"], index=3)

    def select_campus(self):
        """Selects the first available campus from the dropdown."""
        self.page.select_option(self.selectors["location"], index=4)

    def fill_course_interested_called(self):
        """Fills the course I am interested in studying is called."""
        course_name_text = generate_random_word()
        self.page.fill(self.selectors["course_name"], course_name_text)

    def fill_discuss_text(self):
        """Fills the Please outline what you would like to discuss at your consultation."""
        large_text = generate_paragraph()
        self.page.fill(self.selectors["details_textbox"], large_text)


