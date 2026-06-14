
class ContactHelper:

    def __init__(self, app):
        self.app = app


    def to_main_page(self):
        wd = self.app.wd
        if not(wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_link_text("Last name")) > 0):
            wd.find_element_by_link_text("home page").click()


    def add(self, contact):
        # initiate contact creation
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()
        # enter contact info
        wd.find_element_by_name("firstname").click()
        wd.find_element_by_name("firstname").clear()
        wd.find_element_by_name("firstname").send_keys(contact.first_name)

        wd.find_element_by_name("lastname").click()
        wd.find_element_by_name("lastname").clear()
        wd.find_element_by_name("lastname").send_keys(contact.last_name)

        wd.find_element_by_name("email").click()
        wd.find_element_by_name("email").clear()
        wd.find_element_by_name("email").send_keys(contact.email)

        wd.find_element_by_name("mobile").click()
        wd.find_element_by_name("mobile").clear()
        wd.find_element_by_name("mobile").send_keys(contact.mobile_phone)
        # submit contact info
        wd.find_element_by_css_selector("input[name='submit']").click()
        self.to_main_page()


    def edit_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_css_selector("img[title=Edit]").click()
        wd.find_element_by_name("firstname").click()
        wd.find_element_by_name("firstname").clear()
        wd.find_element_by_name("firstname").send_keys("Edited contact name")
        wd.find_element_by_name("update").click()
        self.to_main_page()


    def delete_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()
        wd.find_element_by_name("delete").click()
        self.to_main_page()


    def count(self):
        wd = self.app.wd
        return  len(wd.find_elements_by_name("selected[]"))