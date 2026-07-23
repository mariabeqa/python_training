from pony.orm import *
from datetime import datetime
from model.group import Group
from model.contact import Contact

class ORMFixture:

    db = Database()


    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        contacts = Set(lambda: ORMFixture.ORMContact, table="address_in_groups", column="id", reverse="groups", lazy=True)


    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        deprecated = Optional(datetime, column='deprecated')
        groups = Set(lambda: ORMFixture.ORMGroup, table="address_in_groups", column="group_id", reverse="contacts", lazy=True)


    def __init__(self, host, name, user, password):
        self.db.bind(provider='mysql', host=host, user=user, password=password, database=name)
        self.db.generate_mapping()
        sql_debug(True)


    def convert_groups_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))


    @db_session
    def get_group_list(self):
        return self.convert_groups_to_model(select(g for g in ORMFixture.ORMGroup))


    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), first_name=contact.firstname, last_name=contact.lastname)
        return list(map(convert, contacts))


    @db_session
    def get_contact_list(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))


    @db_session
    def get_contacts_in_group(self, group):
        contacts = list(
            select(
            c for c in ORMFixture.ORMContact if exists(g for g in c.groups if g.id == group.id)
            ))
        return contacts


    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(
            select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group not in c.groups))

    @db_session
    def get_group_to_remove_contact(self):
        return list(self.convert_groups_to_model(
            select(
                g for g in ORMFixture.ORMGroup if exists(contact.deprecated is None for contact in g.contacts)
            )
        ))


    @db_session
    def get_contacts_without_any_group(self):
        return list(self.convert_contacts_to_model(
            select(
                c for c in ORMFixture.ORMContact if not exists(g for g in c.groups)
            )
        ))



