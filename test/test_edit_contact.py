from model.contact import Contact
from random import randrange

def test_edit_some_contact(app):
    app.navigation.open_contacts_page()
    if app.contact.count() == 0:
        app.contact.create(first_name="Vasya", last_name="Pupkin")
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact = Contact(first_name="Vasya", last_name="Pupkin")
    contact.id = old_contacts[index].id
    app.contact.edit_some_contact(index, contact)
    new_contacts = app.contact.get_contact_list()
    assert len(old_contacts) == len(new_contacts)
    old_contacts[index] = contact
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)