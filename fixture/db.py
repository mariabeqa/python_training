import pymysql.cursors
from model.group import Group
from model.contact import Contact


class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password, autocommit=True)

    def get_group_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                list.append(Group(id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return list


    def get_contact_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select firstname, lastname, address, email, email2, email3, home, mobile, work, id from addressbook")
            for row in cursor:
                (firstname, lastname, address, email, email2, email3, home, mobile, work, id) = row
                list.append(Contact(first_name=firstname, last_name=lastname, email=email, email2=email2,
                                    email3=email3, home_phone=home, mobile_phone=mobile, work_phone=work,
                                    id=str(id), address=address))
        finally:
            cursor.close()
        return list


    def destroy(self):
        self.connection.close()
