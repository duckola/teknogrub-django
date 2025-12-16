from django.core.management.base import BaseCommand
from Canteen.models import Canteen
from Menu.models import Category, MenuItem, Inventory
from User.models import Role
from Promo.models import Promo

class Command(BaseCommand):
    help = 'Seeds initial data'

    def handle(self, *args, **kwargs):
        Role.objects.get_or_create(role_name='Student')
        Role.objects.get_or_create(role_name='Staff')
        Role.objects.get_or_create(role_name='Admin')

        main, _ = Canteen.objects.get_or_create(name="Main Canteen", location="Main")
        shs, _ = Canteen.objects.get_or_create(name="SHS Canteen", location="SHS")
        jhs_canteen, _ = Canteen.objects.get_or_create(name="JHS Canteen", location="JHS Building")

        cats = ["Rice Meals", "Snacks", "Drinks", "Desserts", "Pasta"]
        cat_objs = {c: Category.objects.get_or_create(category_name=c)[0] for c in cats}

        items = [
            ("Chicken Adobo", 60, "Rice Meals", main), ("Pork Sinigang", 70, "Rice Meals", main),
            ("Beef Caldereta", 85, "Rice Meals", main), ("Spaghetti", 50, "Pasta", main),
            ("Burger Steak", 55, "Rice Meals", shs), ("Tuna Sandwich", 30, "Snacks", shs),
            ("Coke Mismo", 25, "Drinks", main), ("Halo-Halo", 45, "Desserts", main),
            ("Siomai Rice", 35, "Rice Meals", shs), ("Fried Chicken", 65, "Rice Meals", main),
        ]

        for name, price, cat, cant in items:
            mi, _ = MenuItem.objects.get_or_create(
                name=name, canteen=cant,
                defaults={'price': price, 'category': cat_objs[cat], 'description': f'Delicious {name}'}
            )
            Inventory.objects.get_or_create(item=mi, defaults={'current_stock': 100})

            self.stdout.write('Creating Promos...')

        spaghetti = MenuItem.objects.get(name="Spaghetti")
        caldereta = MenuItem.objects.get(name="Beef Caldereta")
        promo_1, created = Promo.objects.get_or_create(
                title="Spaghetti & Drink Combo",
                discount_percent=15,
                defaults={'is_active': True}
            )
        if created:
            promo_1.applicable_items.add(spaghetti)
            promo_2, created = Promo.objects.get_or_create(
                title="Caldereta Weekend Special",
                discount_percent=20,
                defaults={'is_active': True}
        )
            if created:
                promo_2.applicable_items.add(caldereta)

        self.stdout.write(self.style.SUCCESS('Data Seeded Successfully!'))