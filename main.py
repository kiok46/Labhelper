from kivy.app import App

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from src.components.keyboard import KeyboardLayout
from src.components.DynamicList import *

import os
from fpdf import FPDF
import sys
import datetime

# Loading the KV files from the src/kv/ folder.
from os import listdir
kv_path = './src/kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

from src.constants.colors import keyboard_keys

class LabHelper(BoxLayout):
    def __init__(self, **kwargs):
        super(LabHelper, self).__init__(**kwargs)

    def onPrintReportReleased(self):

        user_name = self.ids.user_name.text
        entry_substance_name = self.ids.substance_name.text

        if self.ids.dangerous_checkbox.active:
            dangerous_value = "Dangerous"
        else:
            dangerous_value = "Non-Dangerous"

        today = datetime.date.today()

        now = datetime.datetime.now()
        entry_date = str(now.day) + " " + str(today.strftime('%B')) + " " + str(now.year)

        pdf = FPDF()
        # compression is not yet supported in py3k version
        pdf.compress = False
        pdf.add_page()
        # Unicode is not yet supported in the py3k version; use windows-1252 standard font
        pdf.set_font('Arial', '', 14)
        pdf.ln(10)
        pdf.cell(100, 10, user_name, 1)
        pdf.cell(70, 10, entry_date, 1)
        pdf.ln(10)
        pdf.cell(100, 10, entry_substance_name, 1)
        pdf.cell(70, 10, dangerous_value, 1)
        pdf.output('lab_report.pdf', 'F')

        os.system("lpr -P DYMO_LabelWriter_4XL -o media=Custom.4x6in -o page-left=0 -o page-right=0 -o page-top=0 -o page-bottom=0 lab_report.pdf")

        """
        lpr -P printer-name -o media=paper-size -o page-left=0 -o page-right=0 -o page-top=0 -o page-bottom=0 img.png
        """


class MainApp(App):
    def build(self):
        return LabHelper()


if __name__ == '__main__':
    MainApp().run()
