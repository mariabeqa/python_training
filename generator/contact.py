from model.contact import Contact
import random
import string
import jsonpickle
import os.path
import getopt
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of contacts", "file"])
    print("Raw sys.argv:", sys.argv)
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n=5
f="data/contacts.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a

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

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(test_data, keys=True))