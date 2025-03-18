from playwright.sync_api import Page

from Utils.data_generator import generate_random_org_name
from Utils.user_actions import select_random_dropdown_option


class OrganisationsPage:
    def __init__(self, page: Page):
        self.page = page  # Store the page instance

        # New button
        self.new_button = page.get_by_role("button", name="New")

        # Create New Org Pop Up
        self.organisation_name_text = page.get_by_label("*Organisation Name")

        # Domestic/International dropdown
        self.organisation_org_int = page.get_by_role('combobox', name="Domestic/International")
        self.organisation_org_int_dropdown_options = page.get_by_role('option')  # Locator for all options

        # Organisation Type dropdown
        self.organisation_type = page.get_by_role('combobox', name="Organisation Type")
        self.organisation_type_dropdown_options = page.get_by_role('option')  # Locator for all options

        # Partnership Tier dropdown
        self.partnership_tier = page.get_by_role('combobox', name="Partnership Tier")
        self.partnership_tier_dropdown_options = page.get_by_role('option')  # Locator for all options

        # Save button
        self.save_button = page.get_by_role('button', name="Save", exact=True)

        #Edit Page
        self.org_name_text = page.locator("//lightning-formatted-text[@slot='primaryField']")


    def click_on_new(self):
        """Click on the 'New' button to create an organization."""
        self.new_button.click()

    def fill_org_name_text(self):
        """Fill the organisation name field with a random name."""
        org_name = generate_random_org_name()
        self.organisation_name_text.fill(org_name)
        return org_name  # Return the generated name for logging or assertions

    def fill_org_details(self):
        """Fill organisation details and save."""
        # Select 'Domestic/International'
        select_random_dropdown_option(
            dropdown_locator=self.organisation_org_int,
            dropdown_list_locator=self.organisation_org_int_dropdown_options
        )

    def fill_org_type_details(self):
        # Select 'Organisation Type'
        select_random_dropdown_option(
            dropdown_locator=self.organisation_type,
            dropdown_list_locator=self.organisation_type_dropdown_options
        )
    def fill_org_tier_details(self):
        # Select 'Partnership Tier'
        select_random_dropdown_option(
            dropdown_locator=self.partnership_tier,
            dropdown_list_locator=self.partnership_tier_dropdown_options
        )
    def click_save(self):
        # Click Save button
        self.save_button.click()