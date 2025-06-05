from django.core.management.base import BaseCommand
from django_seed import Seed
from user_fitapp.models import FitnessClass
import random

class Command(BaseCommand):
    help = "Seed database with demo fitness classes"

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        class_names = ['Yoga', 'Zumba', 'HIIT']

        seeder.add_entity(FitnessClass, 3, {
            'name': lambda x: random.choice(class_names),
            'date_time': lambda x: seeder.faker.date_time_this_year(),
            'instructor': lambda x: seeder.faker.name(),
            'description': lambda x: seeder.faker.text(),
            'total_slots': lambda x: seeder.faker.random_int(min=2, max=5),
            'available_slots': lambda x: seeder.faker.random_int(min=2, max=5),
        })

        inserted_pks = seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded data: {inserted_pks}'))
