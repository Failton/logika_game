from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
)
from kivy.core.window import Window
import random

def get_color(color):
    if color == 0:
        return (0, 1, 0) # GREEN
    elif color == 1:
        return (1, 0, 0) # RED
    elif color == 2:
        return (0, 0, 1) # BLUE
    elif color == 3:
        return (1, 1, 0) # YELLOW
    elif color == 4:
        return (134/256, 1/256, 175/256) # VIOLET
    elif color == 5:
        return (150/256, 75/256, 0) # BROWN

class CenterRectangle(Widget):
    pass

class Cell(Button):
    color_id = 0
    done_flag = False

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (100/256, 118/256, 135/256)
    
    def on_release(self):
        if (self.done_flag == False):
            self.color_id += 1
            if (self.color_id == 6):
                self.color_id = 0
            self.background_color = get_color(self.color_id)

class Container(GridLayout):
    used_colors = []
    before_colors = []
    sorted_answers = []
    used_ids = []
    win_counter = 0

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        while (len(self.before_colors) != 4):
            new_color = random.randint(0, 5)
            if (new_color not in self.used_colors):
                self.before_colors.append(new_color)
                self.used_colors.append(new_color)

    def show_answer(self):
        if (self.children[0].children[6].children[1].text == 'Показать'):
            self.children[0].children[6].children[1].text = 'Скрыть'
            for i in range(4):
                self.children[2].children[6].add_widget(Button(background_normal = '', background_down='', background_color=get_color(self.before_colors[i])))
        else:
            for i in range(4):
                self.children[2].children[6].remove_widget(self.children[2].children[6].children[0])
            self.children[0].children[6].children[1].text = 'Показать'

            

    def reverse_color_id(self, count):
        if (count == 0):
            return 3
        elif (count == 1):
            return 2
        elif (count == 2):
            return 1
        elif (count == 3):
            return 0

    def check_colors(self, count2, child):
        for count1, value in enumerate(self.before_colors):
            if (value == child.color_id and self.reverse_color_id(count1) == count2):
                return 2
            elif (value == child.color_id):
                return 1
        return 0

    def check_doubling(self, children):
        used_colors = []
        for i in children:
            if i.color_id in used_colors:
                return True
            used_colors.append(i.color_id)
        return False
    
    def check_match(self):
        new_id = 0
        for count1, value in enumerate(self.children[2].children):
            if (count1 != 6 and len(value.children) == 4 and count1 not in self.used_ids):
                if (self.check_doubling(value.children) == True):
                    return 0
                new_id = count1
                self.used_ids.append(count1)
                for count2, child in enumerate(value.children):
                    child.done_flag = True
                    color_match = self.check_colors(count2, child)
                    if (color_match == 1):
                        self.sorted_answers.append(1)
                    elif (color_match == 2):
                        self.sorted_answers.append(2)
        self.sorted_answers.sort(reverse=True)

        for i in range(4 - len(self.sorted_answers)):
            self.sorted_answers.append(0)

        for i in self.sorted_answers:
            if (i == 1):
                self.children[0].children[new_id].add_widget(Button(background_normal='', background_down='', background_color=(0, 0, 0)))
            elif (i == 2):
                self.children[0].children[new_id].add_widget(Button(background_normal = '', background_down='', background_color=(1, 1, 1)))
            else:
                self.children[0].children[new_id].add_widget(Label())


        for i in self.sorted_answers:
            if (i == 2):
                self.win_counter += 1

        if (self.win_counter < 4 and new_id != 5):
            for i in range(4):
                self.children[2].children[new_id + 1].add_widget(Cell())
        elif (self.win_counter < 4 and new_id == 5):
            for i in range(2):
                self.children[0].children[6].remove_widget(self.children[0].children[6].children[0])
            self.children[0].children[6].add_widget(Label(text='YOU LOSE :('))
        else:
            for i in range(2):
                self.children[0].children[6].remove_widget(self.children[0].children[6].children[0])
            self.children[0].children[6].add_widget(Label(text='YOU WIN :)'))

        self.sorted_answers = []
        self.win_counter = 0
        



class MyApp(App):
    def build(self):
        return Container()

if __name__ == '__main__':
    # Window.size = (720, 1280)
    Window.clearcolor = (39/256, 68/256, 92/256, 1)
    MyApp().run()
