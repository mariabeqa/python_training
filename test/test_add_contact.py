# -*- coding: utf-8 -*-

from model.contact import Contact

def test_add_contact(app):
    app.contact.add(Contact(first_name="Maria", last_name="Murashkina", email="maria@mail.ru", mobile_phone="+79237600757"))


def test_add_empty_contact(app):
    app.contact.add(Contact(first_name="", last_name="", email="", mobile_phone=""))
