from django.core.management.base import BaseCommand
from resturantapp.models import MenuItem


MENU_DATA = [
    # Buff
    dict(name='Buff Steam Momo',  category='buff',    momo_type='steam',  price=120, is_featured=True,
         description='Juicy buff filling steamed to perfection in thin dough.'),
    dict(name='Buff Fried Momo',  category='buff',    momo_type='fried',  price=130,
         description='Crispy pan-fried buff momos with golden crust.'),
    dict(name='Buff Chilly Momo', category='buff',    momo_type='chilly', price=200, is_featured=True,
         description='Spicy tossed buff momos with bell peppers & sauce.'),
    # Chicken
    dict(name='Chicken Steam Momo',  category='chicken', momo_type='steam',  price=150,
         description='Tender chicken filling with aromatic herbs, steamed fresh.'),
    dict(name='Chicken Fried Momo',  category='chicken', momo_type='fried',  price=180,
         description='Crispy fried chicken momos – a crowd favourite.'),
    dict(name='Chicken Chilly Momo', category='chicken', momo_type='chilly', price=200, is_featured=True,
         description='Fiery chicken momos tossed in our special chilly sauce.'),
    # Veg
    dict(name='Veg Steam Momo',  category='veg', momo_type='steam',  price=100,
         description='Garden-fresh vegetables wrapped in handmade dough.'),
    dict(name='Veg Fried Momo',  category='veg', momo_type='fried',  price=110,
         description='Light and crispy fried veg momos.'),
    dict(name='Veg Chilly Momo', category='veg', momo_type='chilly', price=110,
         description='Spicy vegetarian momos tossed with onions and chilies.'),
]


class Command(BaseCommand):
    help = 'Seed the database with initial menu items'

    def handle(self, *args, **options):
        created = 0
        for data in MENU_DATA:
            _, is_new = MenuItem.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if is_new:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} menu items (skipped existing).'))