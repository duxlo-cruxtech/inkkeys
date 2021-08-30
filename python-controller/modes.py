#In here, the logic of the different modes are defined.
#Each mode has to implement four functions (use "pass" if not needed):
#
#- activate
#Called when the mode becomes active. Usually used to set up static key assignment and icons
#- poll
#Called periodically and typically used to poll a state which you need to monitor. At the end you have to return an interval in seconds before the function is to be called again - otherwise it is not called a second time
#- animate
#Called up to 30 times per second, used for LED animation
#- deactivate
#Called when the mode becomes inactive. Used to clean up callback functions and images on the screen that are outside commonly overwritten areas.

#To avoid multiple screen refreshs, the modules usually do not clean-up the display when being deactivvated. Instead, each module is supposed to set at least the area corresponding to each button (even if it needs to be set to white if unused).

from inkkeys import *
import time
from threading import Timer
from math import ceil, floor
from PIL import Image, ImageDraw, ImageFont
from colorsys import hsv_to_rgb

class ModeAltium:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Altium", inverted=True)  #Title

        #Button2 (top left) WIRE
        device.sendIconFor(2, "icons/slash.png")    
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_W, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_W, ActionCode.RELEASE)])

        #Button3 (left, second from top) MOVE
        device.sendIconFor(3, "icons/arrows-move.png")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_M, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_M, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_M, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_M, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW3_RELEASE, [])

        #Button4 (left, third from top) DELETE
        device.sendIconFor(4, "icons/trash.png")
        device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_E, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_E, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_D, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_D, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW4_RELEASE, [])

        #Button5 (bottom left) PLACE NET
        device.sendIconFor(5, "icons/place_net.png")
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW5_RELEASE, [])

        #Button6 (top right) PLACE TEXT or INTERACTIVE ROUTING
        device.sendIconFor(6, "icons/textarea-t.png")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW6_RELEASE, [])

        #Button7 (right, second from top) CREATE POLYGON FROM SELECTED PRIMITIVES
        device.sendIconFor(7, "icons/create_polygon_from_selected.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_G, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_G, ActionCode.RELEASE)])

        #Button8 (right, third from top) REPOUR ALL POLYGONS 
        device.sendIconFor(8, "icons/repour_polygon.png")
        device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_G, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_G, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW8_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_A, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_A, ActionCode.RELEASE)])

        #Button9 (bottom right) PLACE POLYGON
        device.sendIconFor(9, "icons/bounding-box-circles.png")
        device.assignKey(KeyCode.SW9_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_G, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_G, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW9_RELEASE, [])

        device.updateDisplay()

    def poll(self, device):
        return False #Nothing to poll

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        device.clearCallbacks() #Remove our callbacks if we switch to a different mode

class ModeZoom:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Zoom", inverted=True)  #Title

        #Button2 (top left) END MEETING
        device.sendIconFor(2, "icons/arrow-up-left-circle.png")    
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_Q, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_Q, ActionCode.RELEASE)])

        #Button3 (left, second from top) 
        device.sendIconFor(3, "icons/camera-video.png")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V, ActionCode.RELEASE)])

        #Button4 (left, third from top) 
        device.sendIconFor(4, "icons/white.png")
        device.assignKey(KeyCode.SW4_PRESS, [])
        device.assignKey(KeyCode.SW4_RELEASE, [])

        #Button5 (bottom left) 
        device.sendIconFor(5, "icons/white.png")
        device.assignKey(KeyCode.SW5_PRESS, [])
        device.assignKey(KeyCode.SW5_RELEASE, [])

        #Button6 (top right) MUTE
        device.sendIconFor(6, "icons/mic.png")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_A, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_A, ActionCode.RELEASE)])

        #Button7 (right, second from top) SHARE
        device.sendIconFor(7, "icons/aspect-ratio.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S, ActionCode.RELEASE)])

        #Button8 (right, third from top) CHAT
        device.sendIconFor(8, "icons/chat-dots.png")
        device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_H, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW8_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_H, ActionCode.RELEASE)])

        #Button9 (bottom right) PAUSE SHARE
        device.sendIconFor(9, "icons/aspect-ratio-fill.png")
        device.assignKey(KeyCode.SW9_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW9_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE)])

        device.updateDisplay()

    def poll(self, device):
        return False #Nothing to poll

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        device.clearCallbacks() #Remove our callbacks if we switch to a different mode

class ModeMicrosoftTeams:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Teams", inverted=True)  #Title

        #Button2 (top left) END MEETING
        device.sendIconFor(2, "icons/arrow-up-left-circle.png")    
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B, ActionCode.RELEASE)])

        #Button3 (left, second from top) 
        device.sendIconFor(3, "icons/camera-video.png")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_O, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_O, ActionCode.RELEASE)])

        #Button4 (left, third from top) 
        device.sendIconFor(4, "icons/white.png")
        device.assignKey(KeyCode.SW4_PRESS, [])
        device.assignKey(KeyCode.SW4_RELEASE, [])

        #Button5 (bottom left) 
        device.sendIconFor(5, "icons/white.png")
        device.assignKey(KeyCode.SW5_PRESS, [])
        device.assignKey(KeyCode.SW5_RELEASE, [])

        #Button6 (top right) MUTE
        device.sendIconFor(6, "icons/mic.png")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_M, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_M, ActionCode.RELEASE)])

        #Button7 (right, second from top) SHARE
        device.sendIconFor(7, "icons/aspect-ratio.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_E, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_E, ActionCode.RELEASE)])

        #Button8 (right, third from top) CHAT
        device.sendIconFor(8, "icons/chat-dots.png")
        device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_C, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW8_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_C, ActionCode.RELEASE)])

        #Button9 (bottom right) 
        device.sendIconFor(9, "icons/white.png")
        device.assignKey(KeyCode.SW9_PRESS, [])
        device.assignKey(KeyCode.SW9_RELEASE, [])

        device.updateDisplay()

    def poll(self, device):
        return False #Nothing to poll

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        device.clearCallbacks() #Remove our callbacks if we switch to a different mode

class ModeTest:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Test", inverted=True)  #Title
        device.sendTextFor(1, "1", inverted=False)
        device.sendTextFor(2, " SW2\n SW2-2", inverted=False)
        device.sendTextFor(3, " SW3", inverted=False)
        device.sendTextFor(4, " SW4", inverted=False)
        device.sendTextFor(5, " SW5", inverted=False)
        device.sendTextFor(6, "SW6 ", inverted=False)
        device.sendTextFor(7, "SW7 ", inverted=False)
        device.sendTextFor(8, "SW8 ", inverted=False)
        device.sendTextFor(9, "SW9 ", inverted=False)

        device.updateDisplay()

    def poll(self, device):
        return False #Nothing to poll

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        device.clearCallbacks() #Remove our callbacks if we switch to a different mode

        ############## 
        ## Fallback ## This mode is used as a fallback and a more complex example. It also uses a switchable Jog dial.
        ############## 

class ModeFallback:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        self.jogFunction = "Menu1"

        #This toggles the jog function and sets up key assignments and the label for the jog dial. It calls "updateDiplay()" if update is not explicitly set to False (for example if you need to update more parts of the display before updating it.)
        def toggleJogFunction(update=True):
            if self.jogFunction == "Menu1":  
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Next Menu")
                device.sendTextFor("title", "Menu 1", inverted=True) #Title
                device.sendIconFor(2, "icons/globe.png") #Firefox
                device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.RELEASE)])
                device.sendIconFor(3, "icons/file-earmark-smartsnippets.png") #SmartSnippets
                device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_1, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_1, ActionCode.RELEASE)])
                device.sendIconFor(4, "icons/terminal.png") #PowerShell
                device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_2, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW4_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_2, ActionCode.RELEASE)])
                device.sendIconFor(5, "icons/envelope.png") #Outlook
                device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_EMAIL_READER, ActionCode.PRESS)])
                device.assignKey(KeyCode.SW5_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_EMAIL_READER, ActionCode.RELEASE)])
                device.sendIconFor(6, "icons/file-earmark-code-fill.png") #Notepad++
                device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N, ActionCode.RELEASE)])
                device.sendIconFor(7, "icons/file-earmark_altium.png") #Altium
                device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_A, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_A, ActionCode.RELEASE)])
                device.sendIconFor(8, "icons/chat-dots.png") #Telegram
                device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW8_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE)])
                device.sendIconFor(9, "icons/calculator.png") #Calculator
                device.assignKey(KeyCode.SW9_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_CALCULATOR, ActionCode.PRESS)])
                device.assignKey(KeyCode.SW9_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_CALCULATOR, ActionCode.RELEASE)])
                self.jogFunction = "Menu2"
                if update:
                    device.updateDisplay()
            else:                            #Tool size in GIMP
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Next Menu")
                device.sendTextFor("title", "Menu 2", inverted=True) #Title
                device.sendIconFor(2, "icons/power.png") #Power Off
                device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F4, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F4, ActionCode.RELEASE)])
                device.sendTextFor(3, " Sublime", inverted=False) #Sublime
                device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S, ActionCode.RELEASE)])
                device.sendTextFor(4, " Joulescope", inverted=False) #JS
                device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW4_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J, ActionCode.RELEASE)])
                device.sendTextFor(5, " Tera Term", inverted=False) #Tera Term
                device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_3, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW5_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_3, ActionCode.RELEASE)])
                device.sendTextFor(6, " Allegro", inverted=False) #Allegro
                device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_4, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_4, ActionCode.RELEASE)])
                device.sendTextFor(7, " FreeCAD", inverted=False) #FreeCAD
                device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_5, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_5, ActionCode.RELEASE)])
                device.sendTextFor(8, " nRF Connect", inverted=False) #nRF Connect
                device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_6, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW8_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_6, ActionCode.RELEASE)])
                device.sendTextFor(9, " Photoshop", inverted=False) #Photoshop
                device.assignKey(KeyCode.SW9_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_7, ActionCode.PRESS)]) 
                device.assignKey(KeyCode.SW9_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_7, ActionCode.RELEASE)])
                self.jogFunction = "Menu1"
                if update:
                    device.updateDisplay()

        #Button 1 / jog dial press
        device.registerCallback(toggleJogFunction, KeyCode.JOG_PRESS)   #Call "toggleJogFunction" if the dial is pressed
        device.assignKey(KeyCode.SW1_PRESS, [])                         #We do not send a key stroke when the dial is pressed, instead we use the callback.
        device.assignKey(KeyCode.SW1_RELEASE, [])                       #We still need to overwrite the assignment to clear previously set assignments.
        toggleJogFunction(False)                                        #We call toggleJogFunction to initially set the label and assignment
        device.updateDisplay()                                          #Everything has been sent to the display. Time to refresh it.

    def poll(self, device):
        return False #No polling required

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching
        #Called periodically for animations.
#        pass

    def deactivate(self, device):
        #pass
        device.clearCallbacks() #Clear our callbacks if we switch to a different mode