from kivy.uix.textinput import TextInput
from .DynamicList import *

import autocomplete
autocomplete.load()

class LabTextInput(TextInput):

    active_textinput = None
    instances = []

    def __init__(self, **kwargs):
        super(LabTextInput, self).__init__(**kwargs)
        LabTextInput.instances.append(self)

    def get_labhelper(self):
        return self.parent.parent.parent.parent.parent

    def switch_to_suggestions(self):
        if self.get_labhelper().ids.sm.current == 'suggestions':
            pass
        else:
            self.get_labhelper().ids.sm.current = 'suggestions'

    def switch_to_checkboxes(self):
        if self.get_labhelper().ids.sm.current == 'checkboxes':
            pass
        else:
            self.get_labhelper().ids.sm.current = 'checkboxes'

    def on_text(self, instance, value):
        try:
            if self.get_labhelper().ids.substance_name.text == "":
                pass
            else:
                print("csdvjbchknohuicgyvjg hkbhbj")
                self.get_labhelper().ids.suggestions_list.remove_widget(self.get_labhelper().ids.suggestions_list.character_list)
                suggestion_list = []
                predicted_values = autocomplete.predict(value, ' ')
                print (predicted_values)
                for sv in predicted_values:
                    print (sv[0])
                    print("-_-")
                    suggestion_list.append(sv[0])

                print(suggestion_list)
                character_list = CharacterList(suggestion_list)
                self.get_labhelper().ids.suggestions_list.add_widget(character_list)
                print("didne")
        except:
            pass


        if instance == LabTextInput.instances[0]:
            pass
        elif self.get_labhelper().ids.substance_name.text == "":
            pass
        else:
            self.switch_to_suggestions()

    def on_focus(self, instance, value):

        if LabTextInput.instances[0].focus==True or LabTextInput.instances[1].focus==False:
            self.switch_to_checkboxes()

        if LabTextInput.instances[1].background_normal == './src/assets/back.png' and LabTextInput.instances[1].focus==False:
            self.switch_to_checkboxes()
        if value == False and LabTextInput.active_textinput == instance :
            self.background_normal= './src/assets/active.png'

        if value == True:
            LabTextInput.active_textinput = instance
            for i in LabTextInput.instances:
                if i != instance:
                    i.background_normal= './src/assets/back.png'
