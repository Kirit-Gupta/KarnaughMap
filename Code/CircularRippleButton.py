
#Imports kivymd behaviour and button
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.button import MDFlatButton, MDRaisedButton

#merges kivyMD behaviour to button to create a flat button
class CircularRippleFlatButton(MDFlatButton, CircularRippleBehavior):
    pass
#merges kivyMD behaviour to button to create a Rasied button
class CircularRippleRaisedButton(MDRaisedButton, CircularRippleBehavior):
    pass