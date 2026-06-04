

def test_edit_first_contact(app):
    app.session.login(username="admin", password="secret")
    app.navigation.open_contacts_page()
    app.contact.edit_first_contact()
    app.session.logout()