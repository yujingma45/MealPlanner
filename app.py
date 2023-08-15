import sqlite3
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivy.uix.screenmanager import ScreenManager, Screen
from recipes import Recipe
from kivymd.theming import ThemeManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineIconListItem


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
        self.recipes = []


    def build(self):
        self.theme_cls.primary_palette = 'Red' #  'Cyan', 'Teal'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        self.items = [str(i) for i in range(10)]#[u"早餐", u"午餐", u"晚餐",u"加餐"]

        # check if the db exists
        conn = sqlite3.connect('mealplanner.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
                       name TEXT, meal_type TEXT, ingredients TEXT, extra_instructions TEXT)''')
        conn.commit()
        conn.close()

        # Add screens
        self.screen_manager = ScreenManager()

        self.title_screen = TitleScreen(name="title")
        self.screen_manager.add_widget(self.title_screen)

        self.new_recipe_screen = NewRecipeScreen(name="new_recipe")
        self.screen_manager.add_widget(self.new_recipe_screen)

        self.recipe_list_screen = RecipeListScreen(name="recipe_list")  
        self.screen_manager.add_widget(self.recipe_list_screen) 
    
        return self.screen_manager
    
    def return_to_title(self, *args):
        # Access the `ScreenManager` and change the screen.
        self.root.transition.direction = "right"
        self.root.current = "title"
    
    # Recipe List Screen
    def switch_to_recipes_list_screen(self):
        self.root.transition.direction = "left"
        self.root.current = "recipe_list"
        self.load_recipes_in_list_screen()  

    def load_recipes_in_list_screen(self):
        self.recipe_list_screen.ids.recipe_grid.clear_widgets()
        # Get all the recipes from db 
        conn = sqlite3.connect('mealplanner.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes")
        self.recipes = [Recipe(*row) for row in cursor.fetchall()]
        cursor.close()

        # Put it in the list
        for rcp in self.recipes:
            # dish_label = OneLineListItem(text=dish._name)
            rcp_label = TwoLineAvatarIconListItem(
                    IconLeftWidget(
                        icon="plus"
                    ),
                    text=f"[font=assets/DroidSansFallback.ttf]{rcp._name}",
                    secondary_text= f"[font=assets/DroidSansFallback.ttf]{rcp._meal_type}"
                )
            rcp_label.bind(on_release=lambda instance: self.modify_recipe(instance.text))
            self.recipe_list_screen.ids.recipe_grid.add_widget(rcp_label)

    def modify_recipe(self, selected_name):
        # TODO
        # Find the Recipe object based on recipe name
        selected_recipe = next((r for r in self.recipes if r._name == selected_name), None)
        if selected_recipe:
            # Transition to a new screen to modify the selected_dish
            # You need to create a new screen class for dish modification
            # and implement the necessary UI and logic for it.
            pass

    # New recipe screen 
    def switch_to_new_recipe_screen(self):
        self.root.transition.direction = "left"
        self.root.current = "new_recipe"
        self.load_new_recipe_screen()  

    def load_new_recipe_screen(self):
        meal_type_items = [
            {   "text": f"[font=assets/DroidSansFallback.ttf]{i}",
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "font_size": dp(18),
                "on_release": lambda x=i: self.meal_type_menu_callback(x),
                
            } for i in [u"早餐", u"午餐晚餐", u"午餐", u"晚餐", u"加餐", u"无限制"]
        ]
        self.meal_type_menu = MDDropdownMenu(
            max_height=dp(224),
            caller=self.new_recipe_screen.ids.meal_type_button,
            items=meal_type_items,
            position='auto',
            width_mult=5,
        )
        self.meal_type_menu.bind()

    def meal_type_menu_callback(self, text_item):
        self.new_recipe_screen.ids.meal_type_button.text = text_item
        self.meal_type_menu.dismiss() # Close the dropdown menu after selecting an item


    def add_recipe(self, recipe_name, recipe_ingredients, recipe_meal_type, recipe_extra_instructions):
        if not recipe_name or not recipe_ingredients or not recipe_meal_type:
            self.new_recipe_screen.ids.error_label.text = "[font=assets/DroidSansFallback.ttf]错误：食谱名，材料和类型必填"
            self.new_recipe_screen.ids.error_label.text = ""  # Clear the error label

            # Add the recipe to the database or perform other actions
            conn = sqlite3.connect('mealplanner.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO recipes (name,  ingredients, meal_type, extra_instructions) VALUES (?, ?, ?, ?)''', 
                                (recipe_name.strip(" "), 
                                 recipe_ingredients.strip(" "), 
                                 recipe_meal_type, 
                                 recipe_extra_instructions.strip(" ")))
            conn.commit()
            conn.close()

            # Clear the input fields
            self.new_recipe_screen.ids.recipe_name.text = ""
            self.new_recipe_screen.ids.recipe_ingredients.text = ""
            self.new_recipe_screen.ids.meal_type_button.text = "[font=assets/DroidSansFallback.ttf]无限制" # Clear the selected meal type
            self.new_recipe_screen.ids.recipe_extra_instructions.text = ""

if __name__ == '__main__':
    app = MealPlannerApp()
    app.run()