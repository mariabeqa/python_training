from model.group import Group
from model.contact import Contact
import random

def test_add_some_contact_to_group(app, orm):
    if len(orm.get_contacts_without_any_group()) == 0:
        app.contact.add(Contact(first_name="Contact to add to group"))
    if len(orm.get_group_list()) == 0:
        app.group.create(Group(name="Group to test contact adding"))
    app.navigation.open_contacts_page()
    contact_without_group = orm.get_contacts_without_any_group()[0]
    groups = orm.get_group_list()
    random_group = random.choice(groups)
    app.contact.add_contact_to_group(contact_without_group, random_group)
    assert any(str(c.id) == contact_without_group.id for c in orm.get_contacts_in_group(random_group))