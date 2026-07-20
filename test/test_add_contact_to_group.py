from model.group import Group
from model.contact import Contact
import random

def test_add_some_contact_to_group(app, orm):
    if len(orm.get_group_list()) == 0:
        app.group.create(Group(name="Contact to add to group"))
    if len(orm.get_contact_list()) == 0:
        app.contact.create(Contact(first_name="Group to test contact adding"))
    app.navigation.open_contacts_page()
    contacts = orm.get_contact_list()
    random_contact = random.choice(contacts)
    groups = orm.get_group_list()
    random_group = random.choice(groups)
    app.contact.add_contact_to_group(random_contact, random_group)
    assert str(orm.get_contacts_in_group(random_group)[0].id) == random_contact.id