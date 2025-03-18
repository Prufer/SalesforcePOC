import pytest
from pages.scripts import logger
from Pages import HomePage
from Pages.organisations_all import OrganisationsPage
from Tests.conftest import authenticated_page
from Utils.user_actions import get_mandatory_field_errors


@pytest.mark.user_type("PRMGeneralUser")
class TestPRMOrganisation:
    def test_create_prm_organisation(self, authenticated_page):
        """
        Test case to create a PRM organisation by searching for a term and clicking on a result.
        """
        page = authenticated_page["page"]
        home_page = HomePage(page)

        # Step 1: Search for "organisations" and click on the "All Organisations" result
        home_page.search_and_click_result(search_text="organisations", result_title="All Organisations")

        # Step 2: Debugging - Print the current URL and title
        logger.info(f"Current URL: {page.url}")
        logger.info(f"Current Title: {page.title()}")

        # Step 3: Wait for the expected title or a specific element on the target page
        expected_title = "All Organisations | Organisations | Salesforce"
        try:
            page.wait_for_function(f'document.title === "{expected_title}"', timeout=10000)
            logger.info(f"Found expected title: {expected_title}")
        except Exception as e:
            logger.error(f"Expected title not found: {str(e)}")
            logger.error(f"Current URL: {page.url}")
            page.screenshot(path="title-error-screenshot.png")
            raise

        # Step 4: Assert the presence of the expected title
        assert expected_title in page.title(), f"Expected title '{expected_title}', but got '{page.title()}'"

        # Step 5: Create a PRM organisation
        organisations_page = OrganisationsPage(page)

        logger.info("Clicking on 'New' button to start organisation creation")
        organisations_page.click_on_new()

        logger.info("Filling organisation name")
        org_name = organisations_page.fill_org_name_text()  # Fill the organisation name
        logger.info(f"Generated organisation name: {org_name}")

        logger.info("Filling organisation details")
        organisations_page.fill_org_details()
        organisations_page.fill_org_type_details()
        organisations_page.fill_org_tier_details()
        organisations_page.click_save()
        logger.info(f"{org_name} created successfully")

        # Step 6: Add assertions to validate the creation of the organisation
        assert organisations_page.org_name_text.inner_text() == org_name, f"Expected organisation name '{org_name}', but got '{organisations_page.org_name_text.inner_text()}'"


    def test_prm_organisation_mandatory_fields(self, authenticated_page):
        page = authenticated_page["page"]
        home_page = HomePage(page)

        home_page.search_and_click_result(search_text="organisations", result_title="All Organisations")

        organisations_page = OrganisationsPage(page)
        organisations_page.click_on_new()

        # Intentionally not filling mandatory fields
        organisations_page.click_save()

        # Validate error messages for missing mandatory fields
        mandatory_errors = get_mandatory_field_errors(page)

        assert "Organisation Name" in mandatory_errors, \
            "Expected error message for missing organisation name not found"
        assert "Organisation Type" in mandatory_errors, \
            "Expected error message for missing organisation type not found"

        logger.info(f"{mandatory_errors} are mandatory fields")
