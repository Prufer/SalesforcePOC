class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator('xpath=//input[@id="username"]')
        self.password_input = page.locator('xpath=//input[@id="password"]')
        self.login_button = page.locator('xpath=//input[@id="Login"]')


    def navigate_to_login(self):
        self.page.goto("https://latrobe--uat.sandbox.my.salesforce.com/")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()