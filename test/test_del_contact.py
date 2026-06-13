

def test_delete_first_contact(app):
    app.navigation.open_contacts_page()
    app.contact.delete_first_contact()