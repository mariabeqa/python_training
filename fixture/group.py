
from selenium.webdriver.common.by import By

from model.group import Group

class GroupHelper:

    def __init__(self, app):
        self.app = app


    def create(self, group):
        # init group creation
        wd = self.app.wd
        self.to_group_page()
        wd.find_element(By.CSS_SELECTOR, "input[name='new']").click()
        self.fill_group_form(group)
        # submit group creation
        wd.find_element(By.NAME, "submit").click()
        self.to_group_page()
        self.group_cache = None


    def to_group_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/group.php") and len(wd.find_elements(By.NAME, "new")) >0):
            wd.find_element(By.LINK_TEXT, "groups").click()


    def select_first_group(self):
        self.select_group_by_index(0)


    def select_group_by_index(self, index):
        wd = self.app.wd
        wd.find_elements(By.NAME, "selected[]")[index].click()


    def edit_first_group(self, new_group_data):
        self.edit_group_by_index(0, new_group_data)


    def edit_group_by_index(self, index, new_group_data):
        wd = self.app.wd
        self.to_group_page()
        self.select_group_by_index(index)
        # open modification form
        wd.find_element(By.NAME, "edit").click()
        self.fill_group_form(new_group_data)
        # submit modification
        wd.find_element(By.NAME, "update").click()
        self.group_cache = None


    def delete_first_group(self):
        self.delete_group_by_index(0)


    def delete_group_by_index(self, index):
        wd = self.app.wd
        self.select_group_by_index(index)
        wd.find_element(By.NAME, "delete").click()
        self.to_group_page()
        self.group_cache = None


    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element(By.NAME, field_name).click()
            wd.find_element(By.NAME, field_name).clear()
            wd.find_element(By.NAME, field_name).send_keys(text)


    def fill_group_form(self, group):
        self.change_field_value("group_name", group.name)
        self.change_field_value("group_header", group.header)
        self.change_field_value("group_footer", group.footer)


    def count(self):
        wd = self.app.wd
        self.to_group_page()
        return len(wd.find_elements(By.NAME, "selected[]"))

    group_cache = None

    def get_group_list(self):
        if self.group_cache is None:
            wd = self.app.wd
            self.to_group_page()
            self.group_cache = []
            for element in wd.find_elements(By.CSS_SELECTOR, "span.group"):
                text = element.text
                id = element.find_element(By.NAME, "selected[]").get_attribute("value")
                self.group_cache.append(Group(name=text, id=id))
        return list(self.group_cache)
