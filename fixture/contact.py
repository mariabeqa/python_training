from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from model.contact import Contact
import re

class ContactHelper:

    def __init__(self, app):
        self.app = app


    def to_main_page(self):
        wd = self.app.wd
        if not(wd.current_url.endswith("/addressbook/") and len(wd.find_elements(By.LINK_TEXT, "Last name")) > 0):
            wd.find_element(By.LINK_TEXT, "home").click()


    def add(self, contact):
        # initiate contact creation
        wd = self.app.wd
        wd.find_element(By.LINK_TEXT, "add new").click()
        # enter contact info
        self.fill_contact_form(contact)
        # submit contact info
        wd.find_element(By.CSS_SELECTOR, "input[name='submit']").click()
        self.to_main_page()
        self.contact_cache = None


    def edit_first_contact(self, new_contact_data):
        self.edit_some_contact(0, new_contact_data)


    def edit_some_contact(self, index, new_contact_data ):
        wd = self.app.wd
        self.edit_contact_by_index(index)
        self.fill_contact_form(new_contact_data)
        wd.find_element(By.NAME, "update").click()
        self.to_main_page()
        self.contact_cache = None


    def edit_contact_by_id(self, id, contact):
        wd = self.app.wd
        self.select_contact_to_edit(id)
        self.fill_contact_form(contact)
        wd.find_element(By.NAME, "update").click()
        self.to_main_page()
        self.contact_cache = None


    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.to_main_page()
        row = wd.find_elements(By.NAME, "entry")[index]
        cell = row.find_elements(By.TAG_NAME, "td")[6]
        cell.find_element(By.TAG_NAME, "a").click()


    def delete_first_contact(self):
        self.delete_some_contact(0)


    def delete_some_contact(self, index):
        wd = self.app.wd
        self.select_contact_by_index(index)
        wd.find_element(By.NAME, "delete").click()
        self.to_main_page()
        self.contact_cache = None

    def delete_contact_by_id(self, id):
        wd = self.app.wd
        self.select_contact_by_id(id)
        wd.find_element(By.NAME, "delete").click()
        self.to_main_page()
        self.contact_cache = None

    def select_first_contact(self):
        self.select_contact_by_index(0)


    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements(By.CSS_SELECTOR, "input[name='selected[]']")[index].click()


    def select_contact_by_id(self, id):
        wd = self.app.wd
        wd.find_element(By.CSS_SELECTOR, "input[value='%s']" % id).click()


    def edit_contact_by_index(self, index):
        wd = self.app.wd
        self.to_main_page()
        row = wd.find_elements(By.NAME, "entry")[index]
        cell = row.find_elements(By.TAG_NAME, "td")[7]
        cell.find_element(By.TAG_NAME, "a").click()


    def select_contact_to_edit(self, id):
        wd = self.app.wd
        self.to_main_page()
        wd.find_element(By.XPATH, "//a[@href='edit.php?id=%s']" % id).click()


    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element(By.NAME, field_name).click()
            wd.find_element(By.NAME, field_name).clear()
            wd.find_element(By.NAME, field_name).send_keys(text)


    def fill_contact_form(self, contact):
        self.change_field_value("firstname", contact.first_name)
        self.change_field_value("lastname", contact.last_name)
        self.change_field_value("email", contact.email)
        self.change_field_value("email2", contact.email2)
        self.change_field_value("email3", contact.email3)
        self.change_field_value("home", contact.mobile_phone)
        self.change_field_value("mobile", contact.mobile_phone)
        self.change_field_value("work", contact.mobile_phone)
        self.change_field_value("address", contact.address)


    def count(self):
        wd = self.app.wd
        return  len(wd.find_elements(By.NAME, "selected[]"))


    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.contact_cache = []
            for row in wd.find_elements(By.NAME, "entry"):
                cells = row.find_elements(By.TAG_NAME, "td")
                firstname = cells[2].text
                lastname = cells[1].text
                id = cells[0].find_element(By.TAG_NAME, "input").get_attribute("value")
                all_phones = cells[5].text
                address = cells[3].text
                all_emails_from_home_page=cells[4].text
                self.contact_cache.append(Contact(
                    first_name=firstname,
                    last_name=lastname,
                    id=id,
                    all_phones_from_home_page=all_phones,
                    address=address,
                    all_emails_from_home_page=all_emails_from_home_page
                ))
        return list(self.contact_cache)


    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.edit_contact_by_index(index)
        firstname = wd.find_element(By.NAME, "firstname").get_attribute("value")
        lastname = wd.find_element(By.NAME, "lastname").get_attribute("value")
        address = wd.find_element(By.NAME, "address").get_attribute("value")
        id = wd.find_element(By.NAME,"id").get_attribute("value")
        homephone = wd.find_element(By.NAME, "home").get_attribute("value")
        mobilephone = wd.find_element(By.NAME, "mobile").get_attribute("value")
        workphone = wd.find_element(By.NAME, "work").get_attribute("value")
        email = wd.find_element(By.NAME, "email").get_attribute("value")
        email2 = wd.find_element(By.NAME, "email2").get_attribute("value")
        email3 = wd.find_element(By.NAME, "email3").get_attribute("value")
        return Contact(
            first_name=firstname,
            last_name=lastname,
            home_phone=homephone,
            mobile_phone=mobilephone,
            work_phone=workphone,
            id=id,
            address=address,
            email=email,
            email2=email2,
            email3=email3
        )

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        text = wd.find_element(By.ID, "content").text
        homephone = re.search("H: (.*)", text).group(1)
        mobilephone = re.search("M: (.*)", text).group(1)
        workphone = re.search("W: (.*)", text).group(1)
        return Contact(
            home_phone=homephone,
            mobile_phone=mobilephone,
            work_phone=workphone,
        )


    def add_contact_to_group(self, contact, group):
        wd = self.app.wd
        self.select_contact_by_id(contact.id)
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        dropdown = wd.find_element(By.CSS_SELECTOR, "select[name='to_group']")
        ActionChains(wd).move_to_element(dropdown).perform()
        select_group_dropdown = Select(dropdown)
        select_group_dropdown.select_by_value(group.id)
        wd.find_element(By.CSS_SELECTOR, "input[name='add']").click()


    def select_group_by_id(self, group):
        wd = self.app.wd
        dropdown = wd.find_element(By.CSS_SELECTOR, "select[name='group']")
        select_group_dropdown = Select(dropdown)
        select_group_dropdown.select_by_value(group.id)


    def remove_contact_from_group(self, contact, group):
        wd = self.app.wd
        self.select_group_by_id(group)
        self.select_contact_by_id(contact.id)
        wd.find_element(By.CSS_SELECTOR, "input[name='delete']").click()