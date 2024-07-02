from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create a superuser and add to custom group.'

    def handle(self, *args, **options):
        username = options.get('username')
        interactive = options.get('interactive')

        # Call the original createsuperuser command
        super().handle(*args, **options)

        # Your custom group name
        group_name = 'administrateur'

        # Add superuser to custom group if group exists
        try:
            group = Group.objects.get(name=group_name)
            user = User.objects.get(username=username)
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {username} to {group_name} group.'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'Group {group_name} does not exist.'))
        except User.DoesNotExist:
            if interactive:
                self.stdout.write(self.style.WARNING(f'User {username} does not exist.'))
            else:
                self.stderr.write(self.style.ERROR(f'User {username} does not exist.'))
