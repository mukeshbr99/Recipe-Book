from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Category, Recipe


class Command(BaseCommand):
    help = 'Seed demo categories, users, and recipes for quick testing'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        if user.pk and not user.has_usable_password():
            user.set_password('password123')
            user.save()

        categories = ['Dessert', 'Main Course', 'Salad', 'Vegan', 'Drinks', 'Breakfast', 'Appetizers', 'Non-Veg']
        cat_objs = {}
        for name in categories:
            cat, _ = Category.objects.get_or_create(name=name)
            cat_objs[name] = cat

        recipes = [
            {
                'title': 'Classic Chocolate Cake',
                'category': cat_objs['Dessert'],
                'ingredients': '2 cups flour, 1 cup sugar, 3/4 cup cocoa powder, 2 eggs, 1 cup milk, 1 tsp vanilla, 1.5 tsp baking powder, 1/2 tsp salt, 1/2 cup butter',
                'instructions': '1. Preheat oven to 350°F\n2. Mix dry ingredients together\n3. Cream butter and sugar, beat in eggs\n4. Alternate adding dry mix and milk\n5. Pour into greased pan\n6. Bake 30-35 minutes until golden\n7. Cool and frost with chocolate icing',
                'is_featured': True
            },
            {
                'title': 'Spaghetti Bolognese',
                'category': cat_objs['Main Course'],
                'ingredients': '400g spaghetti, 500g minced meat, 1 onion, 4 garlic cloves, 2 cans tomato sauce, 2 tbsp olive oil, Salt, pepper, parmesan cheese',
                'instructions': '1. Boil spaghetti in salted water until al dente\n2. Heat olive oil and sauté onion and garlic\n3. Add minced meat and cook until brown\n4. Pour tomato sauce and simmer 20 minutes\n5. Drain pasta and toss with sauce\n6. Serve with grated parmesan',
                'is_featured': True
            },
            {
                'title': 'Greek Salad',
                'category': cat_objs['Salad'],
                'ingredients': '4 tomatoes, 1 cucumber, 1 red onion, 200g feta cheese, 100g olives, 3 tbsp olive oil, 1 tbsp lemon juice, oregano, salt, pepper',
                'instructions': '1. Chop tomatoes, cucumber, and onion\n2. Cut feta into chunks\n3. Combine all vegetables in large bowl\n4. Add olives\n5. Whisk olive oil with lemon juice and oregano\n6. Drizzle dressing over salad\n7. Toss gently and serve immediately',
                'is_featured': True
            },
            {
                'title': 'Vegan Buddha Bowl',
                'category': cat_objs['Vegan'],
                'ingredients': '1 cup quinoa, 1 sweet potato, 1 avocado, 200g chickpeas, 2 cups spinach, 3 tbsp tahini, 2 tbsp lemon juice, garlic, salt, pepper',
                'instructions': '1. Cook quinoa according to package instructions\n2. Roast diced sweet potato at 400°F for 25 minutes\n3. Mix tahini, lemon juice, and water for dressing\n4. Arrange quinoa, sweet potato, chickpeas, and spinach in bowl\n5. Top with sliced avocado\n6. Drizzle tahini dressing\n7. Serve warm or cold',
                'is_featured': False
            },
            {
                'title': 'Masala Chai',
                'category': cat_objs['Drinks'],
                'ingredients': '2 cups water, 1 cup milk, 2 tbsp tea leaves, 4-5 cloves, 1 cinnamon stick, 1 tsp ginger, sugar to taste',
                'instructions': '1. Crush cloves, cinnamon, and ginger slightly\n2. Boil water with spices for 2 minutes\n3. Add tea leaves and boil for 1 minute\n4. Pour milk and bring to boil\n5. Strain into cups\n6. Add sugar as desired\n7. Serve hot with snacks',
                'is_featured': False
            },
            {
                'title': 'Fluffy Pancakes',
                'category': cat_objs['Breakfast'],
                'ingredients': '1.5 cups flour, 1 tbsp sugar, 2 tsp baking powder, 1/2 tsp salt, 1 cup milk, 1 egg, 2 tbsp butter (melted), blueberries (optional)',
                'instructions': '1. Mix flour, sugar, baking powder, and salt\n2. Whisk milk, egg, and melted butter together\n3. Combine wet and dry ingredients gently\n4. Heat griddle or pan over medium-high heat\n5. Pour 1/4 cup batter per pancake\n6. Cook until bubbles form on top\n7. Flip and cook until golden brown\n8. Serve with maple syrup and berries',
                'is_featured': False
            },
            {
                'title': 'Crispy Spring Rolls',
                'category': cat_objs['Appetizers'],
                'ingredients': '12 spring roll wrappers, 2 cups cabbage (shredded), 1 cup carrots (julienned), 1 cup mushrooms (chopped), 2 tbsp soy sauce, 1 tbsp sesame oil, garlic, ginger, oil for frying',
                'instructions': '1. Heat sesame oil and stir-fry garlic and ginger\n2. Add vegetables and soy sauce, cook 3 minutes\n3. Let filling cool slightly\n4. Wet spring roll wrapper edges with water\n5. Place filling in center and roll tightly\n6. Heat oil to 350°F\n7. Fry rolls until golden and crispy\n8. Serve with sweet chili or soy sauce',
                'is_featured': False
            },
            {
                'title': 'Tandoori Chicken',
                'category': cat_objs['Non-Veg'],
                'ingredients': '800g chicken pieces, 1 cup yogurt, 3 tbsp tandoori masala, 2 tbsp lemon juice, 3 cloves garlic, 1 tbsp ginger, salt, pepper, oil',
                'instructions': '1. Make marinade with yogurt, tandoori masala, garlic, and ginger\n2. Marinate chicken pieces for at least 2 hours\n3. Preheat oven to 450°F or use grill\n4. Place chicken on greased baking tray\n5. Bake for 25-30 minutes until golden and cooked through\n6. Brush with oil midway\n7. Serve hot with lemon wedges and mint chutney\n8. Pair with basmati rice or naan',
                'is_featured': True
            },
            {
                'title': 'Green Smoothie Bowl',
                'category': cat_objs['Breakfast'],
                'ingredients': '2 cups spinach, 1 banana, 1 mango, 1 cup almond milk, 1 tbsp almond butter, granola, coconut flakes, berries',
                'instructions': '1. Blend spinach, banana, mango, and almond milk until smooth\n2. Pour into bowl\n3. Top with granola for crunch\n4. Add coconut flakes\n5. Arrange fresh berries on top\n6. Drizzle with almond butter\n7. Eat with spoon and enjoy immediately',
                'is_featured': False
            },
            {
                'title': 'Mushroom Risotto',
                'category': cat_objs['Main Course'],
                'ingredients': '1.5 cups arborio rice, 500ml vegetable broth, 300g mushrooms, 1 onion, 100ml white wine, 50g parmesan, 2 tbsp butter, garlic, salt, pepper',
                'instructions': '1. Slice mushrooms and sauté in butter and garlic\n2. Sauté diced onion until translucent\n3. Add rice and toast for 2 minutes\n4. Pour white wine and stir until absorbed\n5. Add warm broth one ladle at a time, stirring constantly\n6. Cook for 18-20 minutes until creamy\n7. Fold in cooked mushrooms and parmesan\n8. Season and serve immediately',
                'is_featured': False
            },
        ]

        for data in recipes:
            recipe, created = Recipe.objects.get_or_create(
                title=data['title'],
                defaults={
                    'author': user,
                    'category': data['category'],
                    'ingredients': data['ingredients'],
                    'instructions': data['instructions'],
                    'is_featured': data['is_featured'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created recipe: {recipe.title}"))

        self.stdout.write(self.style.SUCCESS('Seeding complete - 10 recipes + 8 categories added!'))
