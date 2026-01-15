from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.app import MDApp
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast

from .CircularRippleButton import CircularRippleRaisedButton
from .Constant import WHITE1

import re


class User_Input(FloatLayout):
    VARIABLES = {"A", "B", "C", "D"}
    VAR_BUTTONS = {"A", "B", "C", "D", "A'", "B'", "C'", "D'"}

    def __init__(self, parent_screen, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.primary_color = self.app.theme_cls.primary_color
        self.parent_screen = parent_screen

        self.button_text = [
            "A", "B", "C", "D",
            "A'", "B'", "C'", "D'",
            "'", "+", "(", ")",
            "DEL", "CLR", "COPY", "OK"
        ]

        self.btns = []
        self.build()


    def build(self):
        self.user_text_input_box = MDTextField(
            hint_text='Enter Expression',
            size_hint=(1, 0.2),
            pos_hint={'top': 0.95, 'center_x': 0.5},
            mode='round',
            readonly=True,
            disabled=True,
        )
        self.user_text_input_box.line_color_normal = self.primary_color
        self.add_widget(self.user_text_input_box)

        self.button_grid = MDGridLayout(
            rows=4,
            cols=4,
            spacing=(15, 10),
            size_hint=(1, 0.75),
            pos_hint={'top': 0.73, 'center_x': 0.5},
        )

        for txt in self.button_text:
            btn = CircularRippleRaisedButton(
                text=txt,
                size_hint=(0.9, 0.9),
                on_release=self.button_pressed,
            )
            btn.is_disabled = False
            self.button_grid.add_widget(btn)
            self.btns.append(btn)

        self.add_widget(self.button_grid)


    def button_pressed(self, btn, *args):
        if btn.is_disabled:
            self.set_error('This sub-term already exists in this term.')
            return

        txt = btn.text
        expr = self.user_text_input_box.text

        if txt in self.VAR_BUTTONS:
            self.user_text_input_box.text += txt
            self.reset_errors()
            self.update_button_states()
            return
        
        if txt == "'":
            if not expr:
                self.set_error('Invalid NOT placement')
                return
            if expr[-1] in self.VARIABLES or expr[-1] == ")":
                for button in self.btns:
                    if button.text == (expr[-1]) + "'" and expr[-1] in self.VARIABLES:
                        if button.is_disabled:
                            self.set_error('Invalid NOT placement')
                            return

                self.user_text_input_box.text += "'"
                self.reset_errors()
                self.update_button_states()
            else:
                self.set_error('Invalid NOT placement')
            return

        if txt == "+":
            if expr != None and expr != '':
                if expr[-1] == "+":
                    self.set_error('Two ORs cannot go togther without an expression in between.')
                else:
                    self.user_text_input_box.text += "+"
                    self.reset_errors()
                    self.enable_all_buttons()
                    return
            else:
                self.set_error('You need an expression to OR.')
                return

        if txt == "(":
            self.user_text_input_box.text += "("
            self.reset_errors()
            self.enable_all_buttons()
            return

        if txt == ")":
            if expr.count("(") <= expr.count(")"):
                self.set_error('No open bracket to close')
                return
            if expr.endswith("("):
                self.set_error('Cannot close empty bracket')
                return
            if expr.endswith('+)'):
                self.set_error('Enter an expression before closing the set of brackets.')
                return

            self.user_text_input_box.text += ")"
            self.reset_errors()
            self.update_button_states()
            return
        
        if txt == "DEL":
            if not expr or expr == '':
                self.set_error('There is nothing to delete!')
                return
            elif expr.endswith(")'"):
                self.user_text_input_box.text = expr[:-1]
            elif expr.endswith("'"):
                self.user_text_input_box.text = expr[:-2]
            else:
                self.user_text_input_box.text = expr[:-1]
            self.reset_errors()
            self.update_button_states()
            return
        
        if txt == 'CLR':
            self.user_text_input_box.text = ''
            self.reset_errors()
            self.enable_all_buttons()
            return
        
        if txt == 'COPY':
            Clipboard.copy(self.user_text_input_box.text)
            self.reset_errors()
            toast('Copied to Clipboard')
            return
        
        if txt == 'OK':
            if expr == None or expr == '':
                self.set_error('Cannot map an empty expression.')
                return
            elif not self.all_brackets_closed(expr):
                self.set_error('Not all brackets have been closed.')
                return
            elif expr.strip().endswith('+'):
                self.set_error('Expression cannot end with an OR operator.')
                return
            
            else:
                self.reset_errors()
                self.parent_screen.draw_expression(self.user_text_input_box.text)
                return



    def update_button_states(self):
        self.enable_all_buttons()

        term = self.get_current_term()
        used = set(re.findall(r"[ABCD]'?", term))

        for btn in self.btns:
            if btn.text in used:
                self.disable_button(btn)


    def enable_all_buttons(self):
        for btn in self.btns:
            self.re_enable_button(btn)

    def all_brackets_closed(self, expr):
        counter = 0
        for exp in expr:
            if exp == '(':
                counter +=1
            elif exp == ')':
                counter -= 1
        if counter == 0:
            return True
        else:
            return False

    def get_current_term(self):
        text = self.user_text_input_box.text
        depth = 0
        buf = []

        for ch in reversed(text):
            if ch == ")":
                depth += 1
                continue

            if ch == "(":
                if depth > 0:
                    depth -= 1
                    continue
                else:
                    break

            if depth > 0:
                continue

            if ch == "+":
                break

            buf.append(ch)

        return "".join(reversed(buf))

    def disable_button(self, btn):
        btn.md_bg_color = (0.6, 0.6, 0.6, 1)
        btn.text_color = (0.8, 0.8, 0.8, 1)
        btn.is_disabled = True

    def re_enable_button(self, btn):
        btn.md_bg_color = self.primary_color
        btn.text_color = WHITE1
        btn.is_disabled = False

    def reset_errors(self):
        self.user_text_input_box.error = False
        self.user_text_input_box.helper_text = ""
        self.user_text_input_box.line_color_normal = self.primary_color

    def set_error(self, msg):
        self.user_text_input_box.error = True
        self.user_text_input_box.helper_text = msg
        self.user_text_input_box.line_color_normal = (1, 0, 0, 1)