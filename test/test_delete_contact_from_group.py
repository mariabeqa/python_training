from model.group import Group
from model.contact import Contact

def test_delete_some_contact_from_group(app, orm):
    group = orm.get_group_to_remove_contact()[0]
    if group is None:
        new_group = app.group.create(Group(name="Group to test contact adding"))
        new_contact = app.contact.create(Contact(first_name="Group to test contact adding"))
        app.contact.add_contact_to_group(new_contact, new_group)
    app.navigation.open_contacts_page()
    contact = orm.get_contacts_in_group(group)[0]
    app.contact.remove_contact_from_group(contact, group)
    assert not any(c.id == contact.id for c in orm.get_contacts_in_group(group))