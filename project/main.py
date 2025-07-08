# Импорт библиотек

# Kivy
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window
# KivyMD
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.widget import MDWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
# JSON
import json
# OS
import os



path = os.path.dirname(__file__)

with open(os.path.join(path, 'base.json'), 'r', encoding = 'utf-8') as f:

    try:

        notes = json.load(f)

    except json.decoder.JSONDecodeError:

        notes = {}

with open(os.path.join(path, 'settings.json'), 'r', encoding = 'utf-8') as f:

    settings = json.load(f)



def loading(title, text, key = False):

    global notes


    if key is not False:

        notes[key] = [title, text]

    else:

        new_key = max([int(i) for i in notes.keys()], default = -1) + 1
        notes[new_key] = [title, text]

    
    if settings['sort'] == 'alphabet':
            
            notes_sorted = sorted(notes.items(), key = lambda x: x[1][0])
            notes = dict(notes_sorted)

    elif settings['sort'] == 'date':

        notes_sorted = sorted(notes.items(), key = lambda x: int(x[0]))
        notes_sorted.reverse()
        notes = dict(notes_sorted)


    with open(os.path.join(path, 'base.json'), 'w', encoding='utf-8') as f:

        json.dump(notes, f, ensure_ascii=False, indent=4)

def deleting(key):

    global notes


    notes.pop(key)

    if settings['sort'] == 'alphabet':
            
            notes_sorted = sorted(notes.items(), key = lambda x: x[1][0])
            notes = dict(notes_sorted)

    elif settings['sort'] == 'date':

        notes_sorted = sorted(notes.items(), key = lambda x: int(x[0]))
        notes_sorted.reverse()
        notes = dict(notes_sorted)


    with open(os.path.join(path, 'base.json'), 'w', encoding='utf-8') as f:

        json.dump(notes, f, ensure_ascii=False, indent=4)


def update_settings_json():
    with open(os.path.join(path, 'settings.json'), 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)



font_scales = {'very_small': 0.6,
               'small': 0.8,
               'standart': 1.0,
               'large': 1.4,
               'very_large': 1.8}



class BaseMDNavigationItem(MDNavigationItem):

    icon = StringProperty()
    text = StringProperty()


class LoffNotes(MDApp):


    def build(self):

        global settings, notes
        self.root = Builder.load_file('interface.kv')
        self.theme_cls.theme_style = settings['theme']
        self.theme_cls.primary_palette = settings['theme_color']
        self.save_status = False
        self.new_status = False
        self.root.ids['none_for_keyboard'].height = Window.height * 0.6

        if settings['sort'] == 'alphabet':

            notes_sorted = sorted(notes.items(), key = lambda x: x[1][0])
            notes = dict(notes_sorted)

        elif settings['sort'] == 'date':

            notes_sorted = sorted(notes.items(), key = lambda x: int(x[0]))
            notes_sorted.reverse()
            notes = dict(notes_sorted)

        self.update_notes_list()

        return self.root


    def update_notes_list(self):

        self.root.ids['notes_md_list'].clear_widgets()
        self.root.ids['notes_md_list'].cols = settings['cols_number']


        for key, value in notes.items():

            md_list_item = MDCard(on_release=lambda x, k=key: self.open_notes(k),
                                  orientation = 'vertical',
                                  size_hint=(1, None),
                                  radius=[dp(40)],
                                  style='outlined',
                                  padding=dp(20),
                                  height = dp(100))
            
            md_list_item.note_id = key

            md_list_item.add_widget(MDLabel(text=str(value[0]),
                                            role = 'large',
                                            font_style = 'Title',
                                            shorten=True))

            md_list_item.add_widget(MDLabel(text = str(value[1]),
                                            role = 'medium',
                                            shorten = True,
                                            halign = 'left',
                                            font_style = 'Body'))


            self.root.ids['notes_md_list'].add_widget(md_list_item)


        self.root.ids['screen_manager'].current = 'notes_list'


    def open_notes(self, key):

        self.new_status = False
        self.key_note = key
        self.root.ids['title_field'].text = notes[key][0]
        self.root.ids['text_field'].text = notes[key][1]
        self.root.ids['screen_manager'].current = 'note'
        self.root.transition = SlideTransition(direction='right')
        self.save_status = False

        self.root.ids['plus_button'].active = False
        self.root.ids['settings_button'].active = False
        self.root.ids['home_button'].active = False

    def back_to_notes_list(self):

        if self.root.ids['title_field'].text != '' or self.root.ids['text_field'].text != '':
            if self.new_status == False and self.save_status == False:

                loading(self.root.ids['title_field'].text,
                        self.root.ids['text_field'].text,
                        self.key_note)

            elif self.new_status == True and self.save_status == False:

                loading(self.root.ids['title_field'].text,
                        self.root.ids['text_field'].text)


            self.new_status = False


            self.update_notes_list()

        else:

            self.root.ids['screen_manager'].current = 'notes_list'


        self.root.ids['plus_button'].active = False
        self.root.ids['settings_button'].active = False
        self.root.ids['home_button'].active = True


    def save_note(self):

        if self.root.ids['title_field'].text != '' or self.root.ids['text_field'].text != '':
            if self.new_status == False and self.save_status == False:

                loading(self.root.ids['title_field'].text,
                        self.root.ids['text_field'].text,
                        self.key_note)

            elif self.new_status == True and self.save_status == False:

                loading(self.root.ids['title_field'].text,
                        self.root.ids['text_field'].text)


            self.new_status = False


    def delete_note_question(self): 
        
        self.md_dialog_question_delete = MDDialog(
            MDDialogHeadlineText(
                text = f'Удалить заметку «{self.root.ids["title_field"].text}»?'
            ),
            MDDialogSupportingText(
                text = 'Вы более не сможете просматривать и изменять эту заметку.'
            ),
            MDDialogButtonContainer(
                MDWidget(),
                MDButton(
                    MDButtonText(text = 'Отменить'),
                    style = 'text',
                    on_release = lambda *args: self.back_delete_note()
                ),
                MDButton(
                    MDButtonText(text = 'Удалить'),
                    style = 'text',
                    on_release = lambda *args: self.delete_note()
                )
            )
        )


        self.md_dialog_question_delete.open()

    def delete_note(self):

        self.md_dialog_question_delete.dismiss()


        if self.new_status == False:

            deleting(self.key_note)

        else:

            self.root.ids['screen_manager'].current = 'notes_list'


        self.update_notes_list()

        self.root.ids['plus_button'].active = False
        self.root.ids['settings_button'].active = False
        self.root.ids['home_button'].active = True


    def back_delete_note(self):

        self.md_dialog_question_delete.dismiss()
        self.root.ids['screen_manager'].current = 'note'


    def sort_button_press(self):

        menu_items = [
            {
                'text': 'По алфавиту',
                'leading_icon': 'sort-alphabetical-ascending',
                'on_release': lambda *args: self.sort_alphabet()
            },
            {
                'text': 'По дате создания',
                'leading_icon': 'sort-calendar-descending',
                'on_release': lambda *args: self.sort_date()
            }
        ]
        MDDropdownMenu(
            caller=self.root.ids['sort_button'],
            items=menu_items,
            position='bottom',
            pos_hint={'right': 0.90}
        ).open()



    def on_switch_tabs(self, bar, item, *args):

        screen_manager = self.root.ids['screen_manager']

        if item.text == 'Главная':

            if screen_manager.current == 'note':

                self.back_to_notes_list()

            screen_manager.current = 'notes_list'

        elif item.text == 'Настройки':

            if screen_manager.current == 'note':
                self.save_note()

            if self.theme_cls.theme_style == 'Dark':
                self.root.ids['theme_dark_segment'].active = True
            else:
                self.root.ids['theme_light_segment'].active = True

            if self.theme_cls.primary_palette == 'Red':
                self.root.ids['red_theme_button'].active = True
            elif self.theme_cls.primary_palette == 'Green':
                self.root.ids['green_theme_button'].active = True
            else:
                self.root.ids['blue_theme_button'].active = True
            screen_manager.current = 'settings'

            if settings['cols_number'] == 1:
                self.root.ids['col_1_segment'].active = True
            else:
                self.root.ids['col_2_segment'].active = True

        elif item.text == 'Создать':

            self.root.ids['title_field'].text = ''
            self.root.ids['text_field'].text = ''
            self.new_status = True
            self.root.ids['screen_manager'].current = 'note'
            screen_manager.current = 'note'



    def sort_alphabet(self):

        global settings, notes
        settings['sort'] = 'alphabet'
        notes_sorted = sorted(notes.items(), key = lambda x: x[1][0])
        notes = dict(notes_sorted)

        update_settings_json()

        self.update_notes_list()
    
    def sort_date(self):

        global settings, notes
        settings['sort'] = 'date'
        notes_sorted = sorted(notes.items(), key = lambda x: int(x[0]))
        notes_sorted.reverse()
        notes = dict(notes_sorted)

        update_settings_json()

        self.update_notes_list()

    def search_open(self):

        self.root.ids['plus_button'].active = False
        self.root.ids['settings_button'].active = False
        self.root.ids['home_button'].active = False

        self.root.ids['notes_list_search'].cols = settings['cols_number']

        self.root.ids['screen_manager'].current = 'search'

    def back_to_notes_after_search(self):
        self.root.ids['screen_manager'].current = 'notes_list'

        self.root.ids['plus_button'].active = False
        self.root.ids['settings_button'].active = False
        self.root.ids['home_button'].active = True

    def search_notes(self):

        self.root.ids['notes_list_search'].clear_widgets()

        text_search = self.root.ids['field_search'].text

        for key, value in notes.items():

            if text_search != '':

                if text_search in value[0] or text_search in value[1]:

                    md_list_item = MDCard(on_release=lambda x, k=key: self.open_notes(k),
                                          orientation='vertical',
                                          size_hint=(1, None),
                                          radius=[dp(40)],
                                          style='outlined',
                                          padding=dp(20),
                                          height=dp(100))

                    md_list_item.note_id = key

                    md_list_item.add_widget(MDLabel(text=str(value[0]),
                                                    role='large',
                                                    font_style='Title',
                                                    shorten=True))

                    md_list_item.add_widget(MDLabel(text=str(value[1]),
                                                    role='medium',
                                                    shorten=True,
                                                    halign='left',
                                                    font_style='Body'))

                    self.root.ids['notes_list_search'].add_widget(md_list_item)

        self.root.ids['screen_manager'].current = 'search'

    def theme_active(self, theme_name):

        if theme_name == 'light':
            self.theme_cls.theme_style = 'Light'
            settings['theme'] = 'Light'
            update_settings_json()

        else:
            self.theme_cls.theme_style = 'Dark'
            settings['theme'] = 'Dark'
            update_settings_json()

    def color_theme_segment(self, color_name):

        if color_name == 'Red':

            self.theme_cls.primary_palette = 'Red'
            settings['theme_color'] = 'Red'
            update_settings_json()

        elif color_name == 'Green':

            self.theme_cls.primary_palette = 'Green'
            settings['theme_color'] = 'Green'
            update_settings_json()

        else:
            self.theme_cls.primary_palette = 'Blue'
            settings['theme_color'] = 'Blue'
            update_settings_json()

    def cols_segment(self, cols_num):
        self.root.ids['notes_list_search'].cols = cols_num
        self.root.ids['notes_md_list'].cols = cols_num
        settings['cols_number'] = cols_num
        update_settings_json()

LoffNotes().run()