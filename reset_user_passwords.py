import csv
from django.contrib.auth.models import User
from passgen import passgen

with open('user_passwords.csv', 'w') as f:
    dw = csv.DictWriter(f, fieldnames=('username', 'password'))
    dw.writeheader()

    for user in User.objects.filter(is_superuser=False):
        print("Creating password for user {0}.".format(user.username))
        password = passgen(length=12)
        user.set_password(password)
        user.save()
        dw.writerow(dict(username=user.username, password=password))
