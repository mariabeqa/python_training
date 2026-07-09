from selenium.webdriver.common.by import By


class NavigationHelper:

    def __init__(self, app):
        self.app = app


    def open_login_page(self):
        wd = self.app.wd
        wd.get(self.app.base_url)


    def open_contacts_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements(By.LINK_TEXT, "Last name")) > 0):
            wd.find_element(By.LINK_TEXT, "home").click()