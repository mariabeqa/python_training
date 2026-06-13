

def test_edit_first_contact(app):
    app.navigation.open_contacts_page()
    app.contact.edit_first_contact()