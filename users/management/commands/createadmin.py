from users.models import CustomUser
from django.core.management.base import BaseCommand
from medicalapp.projconfig import config_dict


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = config_dict.get("DJANGO_SUPERUSER_EMAIL")
        password = config_dict.get("DJANGO_SUPERUSER_PASSWORD")
        surname = config_dict.get("DJANGO_SURNAME")
        other_names = config_dict.get("DJANGO_OTHER_NAMES")
        date_of_birth = config_dict.get("DJANGO_DATE_OF_BIRTH")

        if not CustomUser.objects.filter(email=email).exists():
            print("Creating account for %s (%s)" % (surname, email))
            CustomUser.objects.create_superuser(
                email=email,
                password=password,
                surname=surname,
                other_names=other_names,
                date_of_birth=date_of_birth,
            )
        else:
            print("Admin account has already been initialized.")
