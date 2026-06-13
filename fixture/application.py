from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver

from fixture.session import SessionHelper
from fixture.group import  GroupHelper
from fixture.contact import ContactHelper
from fixture.navigation import NavigationHelper


class Application:

    def __init__(self):
        self.wd = WebDriver()
        self.wd.implicitly_wait(10)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)
        self.navigation = NavigationHelper(self)


    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False                    


    def destroy(self):
        self.wd.quit()