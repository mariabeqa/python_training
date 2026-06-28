import re


def test_phones_on_home_page(app):
    app.navigation.open_contacts_page()
    contact_from_home_page = app.contact.get_contact_list()[0]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    assert contact_from_home_page.first_name == contact_from_edit_page.first_name
    assert contact_from_home_page.last_name == contact_from_edit_page.last_name
    assert contact_from_home_page.address == contact_from_edit_page.address
    assert contact_from_home_page.all_phones_from_home_page == merge_homes_like_on_home_page(contact_from_edit_page)
    assert contact_from_home_page.all_emails_from_home_page == merge_emails_like_on_home_page(contact_from_edit_page)


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