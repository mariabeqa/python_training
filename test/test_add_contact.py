# -*- coding: utf-8 -*-

from model.contact import Contact

def test_add_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.add(Contact(first_name="Maria", last_name="Murashkina", email="maria@mail.ru", mobile_phone="+79237600757"))
    app.session.logout()


def test_add_empty_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.add(Contact(first_name="", last_name="", email="", mobile_phone=""))
    app.session.logout()
