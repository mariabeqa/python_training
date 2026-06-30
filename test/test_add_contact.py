# -*- coding: utf-8 -*-

from model.contact import Contact
import pytest
import random
import string

def random_name():
    return "".join([random.choice(string.ascii_letters) for i in range(random.randint(2, 20))])

def random_email(postfix):
    return "".join([random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 20))]) + postfix

def random_phone():
    return "+7" + "".join(random.choice(string.digits) for i in range(10))

def random_postal_code():
    return "".join(random.choice(string.digits) for i in range(6))

def random_number_for_address():
    return "".join(random.choice(string.digits) for i in range(2))

test_data = [Contact(first_name="", last_name="", email="", email2="", email3="", home_phone="", mobile_phone="", work_phone="", address="")] + [
    Contact(
        first_name=random_name(), last_name=random_name(), email=random_email("@mail.ru"), email2=random_email("@gmail.com"),
        email3=random_email("@yandex.com"),
        home_phone=random_phone(),
        mobile_phone=random_phone(),
        work_phone=random_phone(),
        address=random_postal_code() + " г. Омск, ул Ленина, д. " + random_number_for_address() + ", кв. " + random_number_for_address()
        )
    for i in range(3)
]

@pytest.mark.parametrize("contact", test_data, ids=[repr(x) for x in test_data])
def test_add_contact(app, contact):
    app.navigation.open_contacts_page()
    old_contacts = app.contact.get_contact_list()
    app.contact.add(contact)
    assert len(old_contacts) + 1 == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) ==  sorted(new_contacts, key=Contact.id_or_max)
