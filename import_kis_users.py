import csv
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group

with open('kis_users.csv', 'r') as f:
    records = list(csv.DictReader(f))

csrs_group = Group.objects.get(name='CSRs')

for record in records:
    # Get the user's group or create it if it doesn't yet exist
    group, group_created = Group.objects.get_or_create(name=record['group'])
    if group_created:
        print("Created group {0}.".format(record['group']))

    username = record['user.user_name']
    first_name = record['user.first_name']
    last_name = record['user.last_name']
    email = record['user.email']

    user, user_created = User.objects.get_or_create(
                            username=username, 
                            first_name=first_name, 
                            last_name=last_name, 
                            email=email)
    if user_created:
        print("Created user {0}.".format(username))
    else:
        print("User {0} already exists.".format(username))
    user.set_password('')
    print("Adding {0} to group {1}".format(user.username, group.name))
    user.groups.add(group)
    # Make everyone a member of the CSRs group, for good measure
    print("Adding {0} to group {1}".format(user.username, csrs_group.name))
    user.groups.add(csrs_group)
    user.save()
