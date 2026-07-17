import re
from model.contact import Contact


def test_phones_on_home_page(app, db):
    app.navigation.open_contacts_page()
    main_page_contacts = sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
    db_contacts = sorted(db.get_contact_list(), key=Contact.id_or_max)
    for i in range(len(main_page_contacts)):
        assert main_page_contacts[i].first_name == db_contacts[i].first_name
        assert main_page_contacts[i].last_name == db_contacts[i].last_name
        assert main_page_contacts[i].address == db_contacts[i].address
        assert main_page_contacts[i].all_phones_from_home_page == merge_homes_like_on_home_page(db_contacts[i])
        assert main_page_contacts[i].all_emails_from_home_page == merge_emails_like_on_home_page(db_contacts[i])


def test_phones_on_contact_view_page(app):
    app.navigation.open_contacts_page()
    contact_from_view_page = app.contact.get_contact_from_view_page(0)
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    assert contact_from_view_page.home_phone == contact_from_edit_page.home_phone
    assert contact_from_view_page.mobile_phone == contact_from_edit_page.mobile_phone
    assert contact_from_view_page.work_phone == contact_from_edit_page.work_phone

def clear(s):
    return re.sub("[() -]", "", s)


def merge_homes_like_on_home_page(contact):
    return "\n".join(
        filter(lambda x: x != "",
               map( lambda x: clear(x),
                    filter(lambda x: x is not None,
                           [contact.home_phone,  contact.mobile_phone, contact.work_phone]))))


def merge_emails_like_on_home_page(contact):
    return "\n".join(
        filter(lambda x: x != "",
               map(lambda x: x,
                    filter(lambda x: x is not None,
                           [contact.email, contact.email2, contact.email3]))))