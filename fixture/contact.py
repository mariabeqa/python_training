from model.contact import Contact
import re

class ContactHelper:

    def __init__(self, app):
        self.app = app


    def to_main_page(self):
        wd = self.app.wd
        if not(wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_link_text("Last name")) > 0):
            wd.find_element_by_link_text("home").click()


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
        self.edit_some_contact(0, new_contact_data)


    def edit_some_contact(self, index, new_contact_data ):
        wd = self.app.wd
        self.edit_contact_by_index(index)
        self.fill_contact_form(new_contact_data)
        wd.find_element_by_name("update").click()
        self.to_main_page()
        self.contact_cache = None


    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.to_main_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()


    def delete_first_contact(self):
        self.delete_some_contact(0)


    def delete_some_contact(self, index):
        wd = self.app.wd
        self.select_contact_by_index(index)
        wd.find_element_by_name("delete").click()
        self.to_main_page()
        self.contact_cache = None


    def select_first_contact(self):
        self.select_contact_by_index(0)


    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_css_selector("input[name='selected[]']")[index].click()


    def edit_contact_by_index(self, index):
        wd = self.app.wd
        self.to_main_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()


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
            for row in wd.find_elements_by_name("entry"):
                cells = row.find_elements_by_tag_name("td")
                firstname = cells[1].text
                lastname = cells[2].text
                id = cells[0].find_element_by_tag_name("input").get_attribute("value")
                all_phones = cells[5].text
                self.contact_cache.append(Contact(
                    first_name=firstname,
                    last_name=lastname,
                    id=id,
                    all_phones_from_home_page=all_phones
                ))
        return list(self.contact_cache)


    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.edit_contact_by_index(index)
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        homephone = wd.find_element_by_name("home").get_attribute("value")
        mobilephone = wd.find_element_by_name("mobile").get_attribute("value")
        workphone = wd.find_element_by_name("work").get_attribute("value")
        return Contact(
            first_name=firstname,
            last_name=lastname,
            home_phone=homephone,
            mobile_phone=mobilephone,
            work_phone=workphone,
            id=id
        )

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        text = wd.find_element_by_id("content").text
        homephone = re.search("H: (.*)", text).group(1)
        mobilephone = re.search("M: (.*)", text).group(1)
        workphone = re.search("W: (.*)", text).group(1)
        return Contact(
            home_phone=homephone,
            mobile_phone=mobilephone,
            work_phone=workphone,
        )
