from model.contact import Contact


def test_delete_first_contact(app):
    app.navigation.open_contacts_page()
    if app.contact.count() == 0:
        app.contact.create(Contact(first_name="first contact"))
    app.contact.delete_first_contact()