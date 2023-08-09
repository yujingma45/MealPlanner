import sqlite3
import random
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

# may add a class for gredient, so some gredient can alter users to prepare earlier 
class Dish:
    def __init__(self, name, meal_type, ingredients, extra_instructions= ''):
        self._name = name
        self._meal_type = meal_type 
        self._ingredients = ingredients #.split(',') we don't split here, it will be easier to store in db
        self._extra_instructions = extra_instructions

    def __repr__(self) -> str:
        return f'Dish(name = {self._name}, meal_type ={self._meal_type}, ingredients = {self._ingredients}, extra_instruction = {self._extra_instructions})'

class MealPlannerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = sqlite3.connect('mealplanner.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dishes (name TEXT, meal_type TEXT, ingredients TEXT, extra_instructions TEXT)''')
        self.conn.commit()

        self.dishes = []

        self.main_layout = BoxLayout(orientation='vertical')

        self.scroll_view = ScrollView()
        self.grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        self.scroll_view.add_widget(self.grid_layout)
        self.main_layout.add_widget(self.scroll_view)


    def build(self):
        self.load_dishes()

        
        self.dish_input = MDTextField(hint_text='Enter Dish')
        self.dish_type_input = MDTextField(hint_text='Enter Its Meal Type')
        self.ingredients_input = MDTextField(hint_text='Enter Ingredients (comma-separated)')
        self.extra_instructions_input = MDTextField(hint_text='Enter Extra Instructions (Optional)')
        self.add_dish_button = MDRaisedButton(text='Add Dish', on_release=self.add_dish)
        self.generate_button = MDRaisedButton(text='Generate Meal Plan', on_release=self.generate_meal_plan)
        self.meal_plan_label = OneLineListItem(text='Meal Plan will appear here')

        self.main_layout.add_widget(self.dish_input)
        self.main_layout.add_widget(self.dish_type_input)
        self.main_layout.add_widget(self.ingredients_input)
        self.main_layout.add_widget(self.extra_instructions_input)
        self.main_layout.add_widget(self.add_dish_button)
        self.main_layout.add_widget(self.generate_button)
        self.main_layout.add_widget(self.meal_plan_label)
        return self.main_layout

    def load_dishes(self):
        self.cursor.execute('SELECT * FROM dishes')
        rows = self.cursor.fetchall()
        print(rows)
        self.dishes = [Dish(row[0], row[1], row[2], row[3]) for row in rows]
        for dish in self.dishes:
            print(dish)
            dish_label = OneLineListItem(text=dish._name)
            self.grid_layout.add_widget(dish_label)
    
    def add_dish(self, instance):
        dish_name = self.dish_input.text
        dish_type = self.dish_type_input.text
        ingredients = self.ingredients_input.text
        extra_instructions = self.extra_instructions_input.text
        if dish_name and dish_type and ingredients:
            dish = Dish(dish_name, dish_type, ingredients)
            self.cursor.execute('INSERT INTO dishes (name, meal_type, ingredients, extra_instructions) VALUES (?, ?, ?, ?)', 
                                (dish_name, dish_type, ingredients, extra_instructions))
            self.conn.commit()
            self.dishes.append(dish)
            self.dish_input.text = ''
            self.dish_type_input.text = ''
            self.ingredients_input.text = ''
            self.extra_instructions_input.text = ''  # Clear the extra_instructions input
            self.main_layout.add_widget(OneLineListItem(text=dish._name))

    def generate_meal_plan(self, instance):
        breakfast = random.choice(self.dishes)
        lunch = random.choice(self.dishes)
        dinner = random.choice(self.dishes)
        self.meal_plan_label.text = f"Breakfast: {breakfast._name}\nLunch: {lunch._name}\nDinner: {dinner._name}"

if __name__ == '__main__':
    app = MealPlannerApp()
    app.run()


     