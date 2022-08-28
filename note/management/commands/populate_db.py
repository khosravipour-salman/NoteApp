from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from random import choice, randint

from note.models import Note, Category
from core.helpers.model_choices import HEX_CHOICES


faker = Faker()


class Command(BaseCommand):
    help = 'Populate database with dummy-data.'

    def add_arguments(self, parser):
        parser.add_argument('--count', help='Object count to insert into database.', type=int)

    def handle(self, *args, **options):
        obj_count = options.get('--count', 30)

        for _ in range(obj_count):
            note_obj = Note.objects.create(title='note' + faker.name(), content=faker.text())
            category_obj = Category.objects.create(name='category' + faker.name(), color=choice([color[1] for color in HEX_CHOICES]))

        for obj in Note.objects.all():
            iteration_count = randint(1, 3)
            obj.categories.set([choice(Category.objects.all()) for _ in range(iteration_count)])
            obj.save()

        self.stdout.write(self.style.SUCCESS('Dummy-data has been generated and inserted to database Successfully.'))