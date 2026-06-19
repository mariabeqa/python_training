from model.contact import Contact

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
        self.fill_contact_form(contact)
        # submit contact info
        wd.find_element_by_css_selector("input[name='submit']").click()
        self.to_main_page()
        self.contact_cache = None


    def edit_first_contact(self, new_contact_data):
        wd = self.app.wd
        self.select_first_contact()
        wd.find_element_by_css_selector("img[title=Edit]").click()
        self.fill_contact_form(new_contact_data)
        wd.find_element_by_name("update").click()
        self.to_main_page()
        self.contact_cache = None


    def delete_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()
        wd.find_element_by_name("delete").click()
        self.to_main_page()
        self.contact_cache = None


    def select_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_css_selector("input[name='selected[]']").click()


    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)


    def fill_contact_form(self, contact):
        self.change_field_value("firstname", contact.first_name)
        self.change_field_value("lastname", contact.last_name)
        self.change_field_value("email", contact.email)
        self.change_field_value("mobile", contact.mobile_phone)


    def count(self):
        wd = self.app.wd
        return  len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.contact_cache = []
            for el in wd.find_elements_by_name("entry"):
                firstname = el.find_element_by_xpath(".//td[3]").text
                lastname = el.find_element_by_xpath(".//td[2]").text
                id = el.find_element_by_xpath(".//td[1]/input").get_attribute("id")
                self.contact_cache.append(Contact(first_name=firstname, last_name=lastname, id=id))
        return list(self.contact_cache)