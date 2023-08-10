import sqlite3
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import ScreenManager, Screen
from recipes import Recipe
from kivymd.theming import ThemeManager


class TitleScreen(Screen):
    pass

class NewRecipeScreen(Screen):
    pass

class RecipeListScreen(Screen):
    pass

class MealPlannerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.theme_cls = ThemeManager()  # Initialize ThemeManager

        self.conn = sqlite3.connect('mealplanner.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (name TEXT, meal_type TEXT, ingredients TEXT, extra_instructions TEXT)''')
        self.conn.commit()
        self.recipes = []

    def build(self):
        self.theme_cls.primary_palette = 'Red' #  'Cyan', 'Teal'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        
        self.screen_manager = ScreenManager()

        self.title_screen = TitleScreen(name="title")
        self.screen_manager.add_widget(self.title_screen)

        self.new_recipe_screen = NewRecipeScreen(name="new_recipe")
        self.screen_manager.add_widget(self.new_recipe_screen)

        self.recipe_list_screen = RecipeListScreen(name="recipe_list")  
        self.screen_manager.add_widget(self.recipe_list_screen) 

        return self.screen_manager

    def switch_to_recipes_list_screen(self):
        self.root.current = "recipe_list"
        self.load_recipes_in_list_screen()  

    def switch_to_new_recipe_screen(self):
        self.root.current = "new_recipe"
        self.load_new_recipe_screen()  

    def load_new_recipe_screen(self):
        pass  

    def load_recipes_in_list_screen(self):
        self.recipe_list_screen.ids.recipe_grid.clear_widgets()
        self.cursor.execute("SELECT * FROM recipes")
        self.recipes = [Recipe(*row) for row in self.cursor.fetchall()]
        print(self.recipes)
        for dish in self.recipes:
            dish_label = OneLineListItem(text=dish._name)
            dish_label.bind(on_release=lambda instance: self.modify_recipe(instance.text))
            self.recipe_list_screen.ids.recipe_grid.add_widget(dish_label)

    def modify_recipe(self, selected_name):
        # Find the Recipe object based on recipe name
        selected_recipe = next((r for r in self.recipes if recipe._name == selected_name), None)
        if selected_recipe:
            # Transition to a new screen to modify the selected_dish
            # You need to create a new screen class for dish modification
            # and implement the necessary UI and logic for it.
            pass

if __name__ == '__main__':
    app = MealPlannerApp()
    app.run()