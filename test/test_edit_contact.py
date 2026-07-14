from model.contact import Contact
import random

def test_edit_some_contact(app, db, check_ui):
    app.navigation.open_contacts_page()
    if (len(db.get_contact_list())) == 0:
        app.contact.create(first_name="Vasilisa", last_name="Pupkina")
    old_contacts = db.get_contact_list()
    contact = random.choice(old_contacts)
    contact.first_name="Vasya"
    contact.last_name="Pupkin"
    app.contact.edit_contact_by_id(contact.id, contact)
    new_contacts = db.get_contact_list()
    assert len(old_contacts) == len(new_contacts)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert  sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)