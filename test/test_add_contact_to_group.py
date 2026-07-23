from model.group import Group
from model.contact import Contact
import random

def test_add_some_contact_to_group(app, orm):
    contacts = orm.get_contacts_without_any_group()
    if len(contacts) == 0:
        app.contact.create(Contact(first_name="Contact to add to group"))
    if len(orm.get_group_list()) == 0:
        app.group.create(Group(name="Group to test contact adding"))
    app.navigation.open_contacts_page()
    contact = contacts[0]
    groups = orm.get_group_list()
    random_group = random.choice(groups)
    app.contact.add_contact_to_group(contact, random_group)
    assert str(orm.get_contacts_in_group(random_group)[0].id) == contact.id