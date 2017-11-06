#!/bin/python
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.image import Image

class CharacterList(StackLayout):
    def __init__(self, characters_dict_list, **kwargs):
        super(CharacterList, self).__init__(**kwargs)

        self.characters_dict_list = characters_dict_list
        self.list_widget = self.dict_to_label_list()

        self.add_widget(self.list_widget)

    def dict_to_label_list(self):
        list_widget = StackLayout()
        for i in self.characters_dict_list:
            list_widget.add_widget(Button(text=i, size_hint=[1.0,0.10]))
        return list_widget


class SuggestionsList(RelativeLayout):
    def __init__(self, **kwargs):
        super(SuggestionsList, self).__init__(**kwargs)

        self.character_list = CharacterList([ './assets/fred.png' ,
                       'img', './assets/ted.png'] )

        self.add_widget(self.character_list)
