# import pytest
# from Pages import LoginPage
#
# def test_login(page, user):
#     login_page = LoginPage(page)
#     login_page.navigate_to_login()
#     login_page.login(user["username"], user["password"])
#     #validate the URL pattern
#
#     page.wait_for_url("https://latrobe--uat.sandbox.lightning.force.com/**", timeout=8000)
#     assert "https://latrobe--uat.sandbox.lightning.force.com" in page.url, f"Unexpected URL: {page.url}"
#     print(f"Logged in as {user['role']}")