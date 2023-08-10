import sqlite3
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import ScreenManager, Screen
from dishes import Dish
from kivymd.theming import ThemeManager

class TitleScreen(Screen):
    pass

class NewDishScreen(Screen):
    pass

class DishListScreen(Screen):
    pass

class MealPlannerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.theme_cls = ThemeManager()  # Initialize ThemeManager

        self.conn = sqlite3.connect('mealplanner.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dishes (name TEXT, meal_type TEXT, ingredients TEXT, extra_instructions TEXT)''')
        self.conn.commit()
        self.dishes = []

    def build(self):
        self.theme_cls.primary_palette = 'Red' #  'Cyan', 'Teal'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        
        self.screen_manager = ScreenManager()

        self.title_screen = TitleScreen(name="title")
        self.screen_manager.add_widget(self.title_screen)

        self.new_dish_screen = NewDishScreen(name="new_dish")
        self.screen_manager.add_widget(self.new_dish_screen)

        self.dish_list_screen = DishListScreen(name="dish_list")  
        self.screen_manager.add_widget(self.dish_list_screen) 

        return self.screen_manager

    def switch_to_dish_list_screen(self):
        self.root.current = 'dish_list'  # Transition to the dish list screen
        self.load_dishes_in_list_screen()  # Load and display the list of dishes

    def load_dishes_in_list_screen(self):
        self.dish_list_screen.ids.dish_grid.clear_widgets()
        self.cursor.execute("SELECT * FROM dishes")
        loaded_dishes = self.cursor.fetchall()
        self.dishes = [Dish(*row) for row in loaded_dishes]
        for dish in self.dishes:
            dish_label = OneLineListItem(text=dish._name)
            dish_label.bind(on_release=lambda instance: self.modify_dish(instance.text))
            self.dish_list_screen.ids.dish_grid.add_widget(dish_label)

    def modify_dish(self, dish_name):
        # Find the Dish object based on dish_name
        selected_dish = next((dish for dish in self.dishes if dish._name == dish_name), None)
        if selected_dish:
            # Transition to a new screen to modify the selected_dish
            # You need to create a new screen class for dish modification
            # and implement the necessary UI and logic for it.
            pass

if __name__ == '__main__':
    app = MealPlannerApp()
    app.run()