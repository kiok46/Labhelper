# -*- coding: utf-8 -*-

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, \
                            BooleanProperty, OptionProperty, ListProperty, \
                            DictProperty

from collections import OrderedDict
import json

import autocomplete
autocomplete.load()

from src.components.LabTextInput import LabTextInput


__all__ = ('KeyboardToggleButton', 'NumericKeyboard', 'KeyboardButton')


class KeyboardButton(Button):
    '''
    Track Keyboard buttons.
    Color and other styles defined in `settings.kv`.
    '''
    pass


class KeyboardToggleButton(ToggleButton):
    '''
    Shift Button.
    Color and other styles defined in `settings.kv`.
    '''
    pass


class NumericKeyboard(BoxLayout):
    '''
    Numeric Keyboard class
    Color and other styles defined in `settings.kv`.
    '''

    NumericKeyboard_dict = OrderedDict([('1', '!'), ('2', '@'), ('3', '#'),
                                        ('4', '$'), ('5', '%'), ('6', '^'),
                                        ('7', '&'), ('8', '*'), ('9', '-'),
                                        ('=', '+'), ('0', '_'), ('`', '~')])

    shift_pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(NumericKeyboard, self).__init__(**kwargs)
        self.box_buttons = []

        to_alpha = BoxLayout(orientation='vertical', size_hint_x=.2,
                             padding= (3, 3), spacing= 3)
        to_alpha.add_widget(Label())
        to_alpha.add_widget(KeyboardToggleButton(text='shift',
                                                 on_release=self.key_released))

        to_alpha.add_widget(KeyboardButton(text='abc', on_release=self.key_released,
                                           background_color= (123/255.0, 123/255.0, 123/255.0, 1)))

        self.add_widget(to_alpha)
        self.numeric_grid = GridLayout(cols=3, padding= (3, 3), spacing= 5)
        for i in self.NumericKeyboard_dict.keys():
            kb = KeyboardButton(text=i, on_release=self.key_released)
            self.box_buttons.append(kb)
            self.numeric_grid.add_widget(kb)
        self.add_widget(self.numeric_grid)

        change_box = BoxLayout(orientation='vertical', size_hint_x=.2,
                               padding= (3, 3), spacing= 3)
        change_box.add_widget(Label())
        change_box.add_widget(KeyboardButton(text='⌫',
                                             on_release=self.key_released))
        change_box.add_widget(KeyboardButton(text='space',
                                             on_release=self.key_released))

        self.add_widget(change_box)

    def shift_buttons(self):
        '''
        This method handles the shifting of the keys in the track keyboard,
        making upper case and lower case buttons.
        '''

        for i in self.box_buttons:
            if self.shift_pressed:
                i.text = self.NumericKeyboard_dict[i.text]
            else:
                i.text = {v:k for k, v in self.NumericKeyboard_dict.items()}[i.text]

    def key_released(self, button):
        '''
        Decides which method to call after a button is released/pressed.
        '''

        track_name = LabTextInput.active_textinput
        if button.text == 'abc':
            self.parent.parent.current = 'keyboard_buttons'
        elif button.text == 'shift':
            if self.shift_pressed:
                self.shift_pressed = False
                self.shift_buttons()
            else:
                self.shift_pressed = True
                self.shift_buttons()
        if track_name != None:
            if button.text == 'space':
                track_name.text += ' '
            elif button.text in ['123', 'abc', 'shift']:
                pass
            elif button.text == '⌫':
                track_name.text = track_name.text[:-1]
            else:
                track_name.text += button.text


class KeyboardLayout(BoxLayout):
    '''
    The keyboard widget.
    Color and other styles defined in `settings.kv`.
    '''

    # For lower case to be default.

    top_line = ListProperty(['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'])
    middle_line = ListProperty(['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'])
    bottom_line = ListProperty(['z', 'x', 'c', 'v', 'b', 'n', 'm'])

    '''

    # For upper case to be default.

    top_line = ListProperty(['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '(', ')', "\\"])
    middle_line = ListProperty(['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '\''])
    bottom_line = ListProperty(['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/'])
    '''

    shift_pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(KeyboardLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        top_box = BoxLayout()
        inner_top_box = BoxLayout(spacing=3, padding=(5, 1))
        middle_box = BoxLayout(spacing=3, padding=(5, 1))
        inner_middle_box = BoxLayout(spacing=3, padding=(5, 1))
        lower_box = BoxLayout(spacing=3)
        inner_lower_box = BoxLayout(spacing=3, padding=(5, 1))

        self.box_buttons = []

        for i in self.top_line:
            kb = KeyboardButton(text=i, on_release=self.key_released)
            self.box_buttons.append(kb)
            inner_top_box.add_widget(kb)
        top_box.add_widget(inner_top_box)
        top_box.add_widget(KeyboardButton(text='⌫', on_release=self.key_released,
                                          size_hint_x=.1))

        for i in self.middle_line:
            kb = KeyboardButton(text=i, on_release=self.key_released)
            self.box_buttons.append(kb)
            inner_middle_box.add_widget(kb)
        middle_box.add_widget(inner_middle_box)
        middle_box.add_widget(KeyboardToggleButton(text='shift',
                                                   on_release=self.key_released,
                                                   size_hint_x=.125))


        lower_box.add_widget(KeyboardButton(text='123',
                                            on_release=self.key_released,
                                            size_hint_x=.15,
                                            background_color= (123/255.0, 123/255.0, 123/255.0, 1)))
        for i in self.bottom_line:
            kb = KeyboardButton(text=i, on_release=self.key_released)
            self.box_buttons.append(kb)
            inner_lower_box.add_widget(kb)
        lower_box.add_widget(inner_lower_box)
        lower_box.add_widget(KeyboardButton(text='space', on_release=self.key_released,
                                            size_hint_x=.175))


        self.add_widget(top_box)
        self.add_widget(middle_box)
        self.add_widget(lower_box)

    def shift_buttons(self):
        '''
        This method handles the shifting of the keys in the track keyboard,
        making upper case and lower case buttons.
        '''
        for i in self.box_buttons:
            if self.shift_pressed:
                i.text = i.text.upper()
            else:
                i.text = i.text.lower()

    def key_released(self, button):
        '''
        Decides which method to call after a button is released/pressed.
        '''

        track_name = LabTextInput.active_textinput
        if button.text == '123':
            self.parent.parent.current = 'numeric_keyboard'
            self.parent.parent.transition.direction='left'
        elif button.text == 'shift':
            if self.shift_pressed:
                self.shift_pressed = False
                self.shift_buttons()
            else:
                self.shift_pressed = True
                self.shift_buttons()
        if track_name != None:
            if button.text == 'space':
                track_name.text += ' '
            elif button.text in ['123', 'abc', 'shift']:
                pass
            elif button.text == '⌫':
                track_name.text = track_name.text[:-1]
                try:
                    print (autocomplete.predict(track_name.text, ' '))
                except:
                    pass
            else:
                track_name.text += button.text
                try:
                    print (autocomplete.predict(track_name.text, button.text))
                except:
                    pass
