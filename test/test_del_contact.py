

def test_delete_first_contact(app):
    app.session.login(username="admin", password="secret")
    app.navigation.open_contacts_page()
    app.contact.delete_first_contact()
    app.session.logout()