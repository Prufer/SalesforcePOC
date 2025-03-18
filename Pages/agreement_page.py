class AgreementsPage:
    def __init__(self, page):
        self.page = page
        self.search_input = page.locator("input[placeholder='Search apps and items...']")
        self.agreements_link = page.locator("text=Agreements")
        self.new_agreement_button = page.locator("button:has-text('New Agreement')")
        self.save_button = page.locator("button:has-text('Save')")

    def search_for_agreements(self, agreement_name):
        self.search_input.fill(agreement_name)
        self.agreements_link.click()

    def create_new_agreement(self, agreement_details):
        self.new_agreement_button.click()
        # Fill in agreement details here
        self.save_button.click()