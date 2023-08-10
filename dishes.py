
# may add a class for gredient, so some gredient can alter users to prepare earlier 
class Dish:
    def __init__(self, name, meal_type, ingredients, extra_instructions= ''):
        self._name = name
        self._meal_type = meal_type 
        self._ingredients = ingredients #.split(',') we don't split here, it will be easier to store in db
        self._extra_instructions = extra_instructions

    def __repr__(self) -> str:
        return f'Dish(name = {self._name}, meal_type ={self._meal_type}, ingredients = {self._ingredients}, extra_instruction = {self._extra_instructions})'
