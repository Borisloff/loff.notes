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
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Green'
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


        for key, value in notes.items():

            md_list_item = MDCard(on_release=lambda x, k=key: self.open_notes(k),
                                  orientation = 'vertical',
                                  size_hint=(1, None),
                                  radius=[dp(40)],
                                  style='outlined',
                                  padding=dp(20))
            
            md_list_item.note_id = key

            md_list_item.add_widget(MDLabel(text=str(value[0]),
                                            role = 'large',
                                            font_style = 'Title'))

            md_list_item.add_widget(MDLabel(text = str(value[1]),
                                            role = 'medium',
                                            shorten = True,
                                            halign = 'left',
                                            font_style = 'Body'))


            self.root.ids['notes_md_list'].add_widget(md_list_item)


        self.root.ids['screen_manager'].current = 'notes_list'
        self.root.transition = SlideTransition(direction='left')


    def open_notes(self, key):

        self.new_status = False
        self.key_note = key
        self.root.ids['title_field'].text = notes[key][0]
        self.root.ids['text_field'].text = notes[key][1]
        self.root.ids['screen_manager'].current = 'note'
        self.root.transition = SlideTransition(direction='right')
        self.save_status = False


    def back_to_notes_list(self):

        if self.new_status == False and self.save_status == False:

            loading(self.root.ids['title_field'].text,
                    self.root.ids['text_field'].text,
                    self.key_note)

        elif self.new_status == True and self.save_status == False:

            loading(self.root.ids['title_field'].text,
                    self.root.ids['text_field'].text)


        self.new_status = False


        self.update_notes_list()


        self.root.ids['plus_button'].active = False
        self.root.ids['search_button'].active = False
        self.root.ids['settings_button'].active = False
        self.root.ids['home_button'].active = True


    def save_note(self):

        if self.new_status == False:

            loading(self.root.ids['title_field'].text,
                    self.root.ids['text_field'].text,
                    self.key_note)

        else:

            loading(self.root.ids['title_field'].text,
                    self.root.ids['text_field'].text)


        self.save_status = True
        self.update_notes_list()


    def new_note_button(self):

        self.root.ids['title_field'].text = ''
        self.root.ids['text_field'].text = ''
        self.new_status = True
        self.root.ids['screen_manager'].current = 'note'
        self.root.transition = SlideTransition(direction = 'right')


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


    def back_delete_note(self):

        self.md_dialog_question_delete.dismiss()
        self.root.ids['screen_manager'].current = 'note'

    
    def settings_open(self):

        self.root.transition = SlideTransition(direction='left')
        self.root.ids['screen_manager'].current = 'settings'


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
            caller=self.root.ids['sort_button'], items=menu_items
        ).open()



    def on_switch_tabs(self, bar, item, *args):

        screen_manager = self.root.ids['screen_manager']

        if item.text == 'Главная':

            screen_manager.current = 'notes_list'

        elif item.text == 'Настройки':

            screen_manager.current = 'settings'

        elif item.text == 'Создать':

            self.root.ids['title_field'].text = ''
            self.root.ids['text_field'].text = ''
            self.new_status = True
            self.root.ids['screen_manager'].current = 'note'
            self.root.transition = SlideTransition(direction = 'right')
            screen_manager.current = 'note'


    def sort_alphabet(self):

        global settings, notes
        settings['sort'] = 'alphabet'
        notes_sorted = sorted(notes.items(), key = lambda x: x[1][0])
        notes = dict(notes_sorted)

        with open(os.path.join(path, 'settings.json'), 'w', encoding='utf-8') as f:

            json.dump(settings, f, ensure_ascii=False, indent=4)

        self.update_notes_list()
    
    def sort_date(self):

        global settings, notes
        settings['sort'] = 'date'
        notes_sorted = sorted(notes.items(), key = lambda x: int(x[0]))
        notes_sorted.reverse()
        notes = dict(notes_sorted)

        with open(os.path.join(path, 'settings.json'), 'w', encoding='utf-8') as f:

            json.dump(settings, f, ensure_ascii=False, indent=4)

        self.update_notes_list()

    def update_hint(self, instance):

        if instance.text.strip():

            instance.hint_text = ""

        else:

            instance.hint_text = "Содержание"
    


LoffNotes().run()