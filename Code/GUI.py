#import Modules

#imports partial this splits the function(atribute1) into partial(function, atribute1) so that the function doesn't initialise immediately
from functools import partial

#Kivy KivyMD GUI components
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivymd.uix.button import MDIconButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex

#Gets the Ripple Button Class
from .CircularRippleButton import CircularRippleFlatButton

#Local Logic and Constants
from .Constant import *
from .Cell import Cell
from .Loops import Loop
from .Logic import MapLogic
from .Expression_IMG import Expression
from .User_Input import User_Input
from .Parse import Parse

#Display Class
class GUI(MDApp):
    #init GUI
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #sets the app title
        self.title = 'Karnaugh Map'
        #Sets the default theme
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        #Ensures the screen size is above the min
        Window.minimum_width = MIN_WINDOW_WIDTH
        Window.minimum_height = MIN_WINDOW_HEIGHT
        #resets object related vars
        self.grid = None
        self.inps = 0
        self.cells = []
        self.loops_widget = []
        self.grid_labels = []
        self.expression_img = None
        self.input_mode = None
        self.submit_button = None

        #sets up menus as dicts
        self.kmap_to_exp_menu_itmes = [
            {'text' : '2 Inputs', 'on_release' : self.draw2inp},
            {'text' : '3 Inputs', 'on_release' : self.draw3inp},
            {'text' : '4 Inputs', 'on_release' : self.draw4inp}
        ]

        self.exp_to_kmap_menu_itmes = [
            {'text' : 'Input Expression', 'on_release' : self.input_expression}
        ]
    
    #main build class redirects to main class
    def build(self):
        return self.main()
    
    #Draws and positions toolbar
    def draw_toolbar(self):
        #Toolbar layout at the top of the screen
        self.toolbar_box = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            padding=(dp(8), 0, dp(8), 0),
            spacing=dp(10),
            pos_hint={'top': 1},
            md_bg_color=self.theme_cls.primary_color
        )

        #sets up button to open menu
        self.file_button = MDRaisedButton(
            text="K Map simplifier", 
            size_hint_x=None, 
            width=dp(80),
            text_color=(1, 1, 1, 1),
            pos_hint={'center_y': 0.5}
        )
        self.file_button.bind(on_release=self.open_menu)
        self.toolbar_box.add_widget(self.file_button)
        self.toolbar_box.add_widget(Widget(size_hint_x=0.35))

        #Adds a centered label to toolbar
        self.app_title_label = MDLabel(
            text= 'Karnaugh Map Solver',
            size_hint_x=None,
            width=dp(250),
            max_lines = 1,
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={'center_y': 0.5},
            font_style="H6"
        )
        self.toolbar_box.add_widget(self.app_title_label)

        self.toolbar_box.add_widget(Widget(size_hint_x=0.35))

        #Menu for Expression simplifier
        self.help_button = MDRaisedButton(
            text='Expression simplifier', 
            size_hint_x=None, 
            width=dp(80),
            text_color=(1, 1, 1, 1),
            pos_hint={'center_y': 0.5}
        )
        self.help_button.bind(on_release=self.open_menu)
        self.toolbar_box.add_widget(self.help_button)
        
        self.fields_layout.add_widget(self.toolbar_box)

        self.kmap_to_exp_menu = MDDropdownMenu(items=self.kmap_to_exp_menu_itmes, width_mult=1)
        self.exp_to_kmap_menu = MDDropdownMenu(items=self.exp_to_kmap_menu_itmes, width_mult=1, hor_growth='left')
        
        #At init draws the 4 loop start
        Clock.schedule_once(self.draw4inp)

    #opens menus in toolbar
    def open_menu(self, button):
        #chooses which toolbar has been pressed
        if button.text == "K Map simplifier":
            self.kmap_to_exp_menu.caller = button
            self.kmap_to_exp_menu.open()
        elif button.text == 'Expression simplifier':
            self.exp_to_kmap_menu.caller = button
            self.exp_to_kmap_menu.open()

    #creates a toggle widget with icons
    def colour_mode(self):
        #grid for toggle and icons
        row = GridLayout(
            cols=3,
            row_force_default=True,
            row_default_height=70,
            col_force_default=True,
            col_default_width=90,  
            spacing=25,            
            size_hint=(None, None),
            width=220,             
            pos_hint={'left_x': 0.5, 'center_y' : 0.125}
        )

        #sun icon
        sun = MDIconButton(
            icon="weather-sunny",
            theme_text_color="Custom",
            text_color=(1, 0.85, 0, 1),
            disabled=True,
            icon_size="32dp"
        )
        
        #moon icon
        moon = MDIconButton(
            icon="weather-night",
            theme_text_color="Custom",
            text_color=(0.6, 0.65, 1, 1),
            disabled=True,
            icon_size="32dp"
        )
        #layout for toggle / switch
        anchor = AnchorLayout()
        switch = MDSwitch(
            size_hint=(None, None),
            width="60dp",
            height="40dp"
        )
        anchor.add_widget(switch)
        switch.bind(active=self.toggle_theme)
        row.add_widget(moon)
        row.add_widget(anchor)
        row.add_widget(sun)
        self.fields_layout.add_widget(row)

    #function which toggles theme between light and dark mode and the relative image
    def toggle_theme(self, instance, value):
        #sets to dark by default
        if not value:
            self.theme_cls.theme_style = "Dark"
            image_path = IMAGE_PATH[1]

        #sets to light mode if required
        else:
            self.theme_cls.theme_style = "Light"
            #paper white as opposed to plain white
            Window.clearcolor = get_color_from_hex("#FAF9F6")
            image_path = IMAGE_PATH[0]
        
        #sets image to the correct mode so that the text can be viewed. High contrast.
        if self.expression_img:
            self.fields_layout.remove_widget(self.expression_img)

            self.expression_img = Image(
                source = image_path,
                size_hint = (0.8, 0.05),
                keep_ratio = True,
                pos_hint={"center_x": 0.5, "center_y": 0.05}
            )
            self.expression_img.reload()

            self.fields_layout.add_widget(self.expression_img)

    #2 input map draw and resets vars
    def draw2inp(self):
        self.general_draw_inp()
        #grid for map
        self.grid = GridLayout(
            cols = 2,
            rows = 2,
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}
        )
        #number of cells / inputs
        self.inps = 4

        self.draw_grid()
    

    #draws a 3 input map grid and resets vars
    def draw3inp(self):
        self.general_draw_inp()
        #grid for map
        self.grid = GridLayout(
            cols = 4,
            rows = 2,
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}
        )
        #number of cells / inputs
        self.inps = 8
        self.draw_grid()
    
    #draws a 4 input map grid and resets vars
    def draw4inp(self, *kwargs):
        self.general_draw_inp()
        self.grid = GridLayout(
            cols = 4,
            rows = 4,
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}
        )
        #number of cells / inputs
        self.inps = 16
        self.draw_grid()
    
    #resets all vars and clears screen from old widgets
    def general_draw_inp(self):
        if self.submit_button == None:
            self.draw_submit_button()
        self.clear_expression_float()
        self.reset_submit_button()
        self.clear_loops()
        self.dismiss_menu()
        self.submit_button.disabled = False
        self.clear_existing_grid()

    #dismisses menu in toolbar
    def dismiss_menu(self):
        if hasattr(self, 'kmap_to_exp_menu') and self.kmap_to_exp_menu.open:
            self.kmap_to_exp_menu.dismiss()
        if hasattr(self, 'exp_to_kmap_menu') and self.exp_to_kmap_menu.open:
            self.exp_to_kmap_menu.dismiss()

    #draws a grid with cell objects and also draws labels about boolean identities
    def draw_grid(self):
        #makes sure grid doesnt already exist
        if self.grid != None:
            self.cells = []
            self.cell_widgets = []
            #grays code
            col_labels = ["0", "1"] if self.grid.cols == 2 else ["00", "01", "11", "10"]
            row_labels = ["0", "1"] if self.grid.rows == 2 else ["00", "01", "11", "10"]

            #draws row and col labels.
            self.row_label_layout = MDBoxLayout(
                orientation='vertical',
                size_hint=(0.05, 0.5),
                pos_hint={'center_x': 0.22, 'center_y': 0.5}
            )
            for label_text in row_labels:
                lbl = MDLabel(
                    text=label_text,
                    halign='center',
                    theme_text_color='Secondary'
                )
                self.row_label_layout.add_widget(lbl)
            self.fields_layout.add_widget(self.row_label_layout)

            self.col_label_layout = GridLayout(
                cols=self.grid.cols,
                size_hint=(0.5, 0.05),
                pos_hint={'center_x': 0.5, 'center_y': 0.77}
            )

            for label_text in col_labels:
                lbl = MDLabel(
                    text=label_text,
                    halign='center',
                    theme_text_color='Secondary'
                )
                self.col_label_layout.add_widget(lbl)
            
            self.fields_layout.add_widget(self.col_label_layout)

            #for each cell in the grid it creates an object of cell which contains boolean identites.
            for i in range(self.inps):
                self.cells.append(Cell())
                cell = MDCard(
                    orientation = 'vertical',
                    size_hint = (1, 1),
                    line_color = (0, 0, 0, 1)
                )
                
                handler = partial(self.cell_clicked, i)

                cell_inp_btn = CircularRippleFlatButton(
                    text = str(self.cells[i].get_num()),
                    size_hint=(1, 1),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    on_release = handler,
                )
                
                #binds each cell to a function which switches the value of the cell's boolean identity
                cell_inp_btn.bind(height=self.update_cell_font_size)

                cell.add_widget(cell_inp_btn)
                self.grid.add_widget(cell)
                self.cell_widgets.append(cell)

            self.fields_layout.add_widget(self.grid)
    
    #clears old grids and their related col row labels
    def clear_existing_grid(self):
        if self.grid:
            self.fields_layout.remove_widget(self.grid)
        if hasattr(self, 'col_label_layout') and self.col_label_layout:
            self.fields_layout.remove_widget(self.row_label_layout)
            self.fields_layout.remove_widget(self.col_label_layout)
        if hasattr(self, 'row_label_layout') and self.row_label_layout:
            self.fields_layout.remove_widget(self.col_label_layout)
            self.fields_layout.remove_widget(self.row_label_layout)

    #automatically updates the cell's font size
    def update_cell_font_size(self, instance, value):
        instance.font_size = value * 0.5
    
    #if the cell is clicked it changes the Boolean value in the grid and the cell object
    def cell_clicked(self, i, instance):
        self.cells[i].clicked()
        instance.text = str(int(self.cells[i].get_num()))

    #draws the simplified expression to the screen
    def draw_simplified_expression(self):
        #gets the values of the objects in the loops
        self.expression = []
        for loop in self.loops_widget:
            self.expression.append(str(loop.expression))
        
        if len(self.expression) == 1:
            self.expression = self.expression[0]
        elif len(self.expression) == 0:
            self.expression = '0'
        else:
            self.expression = '+'.join(self.expression)
        expression = Expression(self.expression)

        #checks if the theme is light or dark and sets to relevant image type
        if self.theme_cls.theme_style == "Dark":
            image_path = expression.file_name[1]
        elif self.theme_cls.theme_style == 'Light':
            image_path = expression.file_name[0]

        #appends the image to the screen
        self.expression_img = Image(
            source = image_path,
            size_hint = (0.8, 0.05),
            keep_ratio = True,
            pos_hint={"center_x": 0.5, "center_y": 0.05}
        )
        self.expression_img.reload()

        self.fields_layout.add_widget(self.expression_img)

        
    #if the submit button is clicked the old loops are cleared and the new loop is drawn
    def submit(self, *kwargs):
        self.clear_loops()
        #disables all cells from being clicked
        for card in self.grid.children:
            for widget in card.walk():
                if isinstance(widget, CircularRippleFlatButton):
                    widget.disabled = True
        
        #changes the submit button to the retry button and the binding of it
        self.submit_button.text = 'Retry'
        self.submit_button.unbind(on_release = self.submit)
        self.submit_button.bind(on_release  = self.retry)
        
        array_of_vals = []
        for cell in self.cells:
            array_of_vals.append(int(cell.get_num()))
        
        array_of_vals = self.split_list(array_of_vals)
        self.loops = self.get_loops(array_of_vals)

        #draws the simplified expression
        self.draw_simplified_expression()

    #if the retry button is pressed a blank map appears.
    def retry(self, *args):
        if self.inps == 4:
            self.draw2inp()
        elif self.inps == 8:
            self.draw3inp()
        elif self.inps == 16:
            self.draw4inp()
        
        self.reset_submit_button()
    
    #resets the reset button to the original submit button.
    def reset_submit_button(self, *args):
        self.submit_button.text = 'Submit'
        self.submit_button.unbind(on_release  = self.retry)
        self.submit_button.bind(on_release = self.submit)
        if self.expression_img:
            self.fields_layout.remove_widget(self.expression_img)
            self.expression_img = None
            
    #splits into arrays of 4 or 2 depending on the size of the map
    def split_list(self, array):
        array_of_vals = []
        if self.inps == 4:
            for i in range(int(self.inps/2)):
                array_of_vals.append([array[(i*2)], array[(i*2)+1]])
        else:
            for i in range(int(self.inps / 4)):
                array_of_vals.append([array[(i*4)], array[(i*4)+1], array[(i*4) + 2], array[(i*4) + 3]])
        
        print(array_of_vals)
        return array_of_vals

    #adds the submit button to the screen
    def draw_submit_button(self):
        self.submit_button = MDRaisedButton(
            text = 'Submit',
            pos_hint = {'center_x' : 0.5, 'center_y' : 0.15},
            on_release = self.submit
        )
        self.fields_layout.add_widget(self.submit_button)

    #uses the MapLogic class to get the locations of the class
    def get_loops(self, array):
        k = MapLogic()
        #requests the class to get the loops as a list
        self.list_of_loops = k.get_loops(array)

        #for each list in the loop it draws the loop.
        for loop_coords in self.list_of_loops:
            loop = Loop(
                coords = loop_coords,
                grid = self.grid,
                padding = 5
            )
            self.fields_layout.add_widget(loop)
            self.loops_widget.append(loop)

    #clears the loops from the screen
    def clear_loops(self):
        for loop in self.loops_widget:
            self.fields_layout.remove_widget(loop)
        self.loops_widget = []

    #Sets the mode to input expression from the user
    def input_expression(self):
        #removes the submit button
        if self.submit_button != None:
            self.reset_submit_button()
            self.submit_button.disabled = False
            self.fields_layout.remove_widget(self.submit_button)
            self.submit_button = None

        #removes old loops
        self.clear_existing_grid()
        self.clear_loops()
        self.dismiss_menu()
        
        self.input_mode = User_Input(
            parent_screen = self,
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}
        )
        self.fields_layout.add_widget(self.input_mode)
    
    #Clears the get expression window 
    def clear_expression_float(self):
        if self.input_mode != None:
            self.fields_layout.remove_widget(self.input_mode)
            self.input_mode = None

    #draws the expression on the kmap after checking the expression variable num
    def draw_expression(self, expr):
        #parses the expression by finding values of each cell
        parser = Parse(expr)
        logical_ls = parser.return_logical_list()
        if parser.set_map_size() == 2:
            self.draw2inp()
        elif parser.set_map_size() == 3:
            self.draw3inp()
        elif parser.set_map_size() == 4:
            self.draw4inp()
        
        #sets each cell to the associated value
        for i in range (len(self.cells)):
            if logical_ls[i]:
                self.cell_clicked(i, self.cell_widgets[i].children[0])
        
        #presses the submit button to draw the loops
        self.submit()

    #main loop. Initialises the code and preps the buttons.
    def main(self):
        self.fields_layout = FloatLayout()
        self.draw_toolbar()
        self.draw_submit_button()
        self.colour_mode()

        return self.fields_layout