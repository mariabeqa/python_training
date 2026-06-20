from model.contact import Contact
from random import randrange


def test_delete_some_contact(app):
    app.navigation.open_contacts_page()
    if app.contact.count() == 0:
        app.contact.create(Contact(first_name="first contact"))
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    app.contact.delete_some_contact(index)
    new_contacts = app.contact.get_contact_list()
    assert len(old_contacts) - 1 == len(new_contacts)
    old_contacts[index:index+1] = []
    assert old_contacts == new_contacts