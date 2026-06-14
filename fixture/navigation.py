
class NavigationHelper:

    def __init__(self, app):
        self.app = app


    def open_login_page(self):
        wd = self.app.wd
        wd.get("http://localhost/addressbook/group.php")


    def open_contacts_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_link_text("Last name")) > 0):
            wd.find_element_by_link_text("home").click()