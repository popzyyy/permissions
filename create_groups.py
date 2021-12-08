from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group, Permission
import logging

#TO CREATE PERMISSIONS GROUPS, RUN THE COMMAND 'python manage.py create_groups'
GROUPS = {

    "Referee": {
        # django app model specific permissions
        "match": ["add", "delete", "change", "view"],
    },
    "Coach": {
        # django app model specific permissions
        "team": ["add", "delete", "change", "view"],
    },
    "Nothing_Test": {
        # django app model specific permissions
        "team": ["view"],
    },

}

USERS = {
    "spqr": ["Referee", "spress@unomaha.edu", "spqr"], #last one is password, it's supposed to be a test password that they later change
    "spqr1": ["Coach", "spress61@live.com", "spqr1"],

}


class Command(BaseCommand):
    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):

        for group_name in GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for app_model in GROUPS[group_name]:

                # Loop permissions in group/model
                for permission_name in GROUPS[group_name][app_model]:

                    # Generate permission name as Django would generate it
                    name = "Can {} {}".format(permission_name, app_model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

            for user_name in USERS:

                new_user = None
                if user_name == "Admin":
                    new_user, created = User.objects.get_or_create(username=user_name, is_staff=True, is_superuser=True,
                                                                   email=USERS[user_name][1])
                else:
                    new_user, created = User.objects.get_or_create(username=user_name, is_staff=True,
                                                                   email=USERS[user_name][1])

                new_user.set_password(USERS[user_name][2])
                new_user.save()

                if USERS[user_name][0] == str(new_group):
                    new_group.user_set.add(new_user)

                    print("Adding {} to {}".format(user_name, new_group))
