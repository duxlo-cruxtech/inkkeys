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
        device.sendIconFor(5, "icons/three-dots.png")
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW5_RELEASE, [])

        #Button6 (top right) PLACE TRACK
        device.sendIconFor(6, "icons/option.png")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_P, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW6_RELEASE, [])

        #Button7 (right, second from top) CREATE POLYGON FROM SELECTED PRIMITIVES
        device.sendIconFor(7, "icons/bounding-box-circles.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_G, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_G, ActionCode.RELEASE)])
        device.assignKey(KeyCode.SW7_RELEASE, [])

        #Button8 (right, third from top)
        device.sendIconFor(8, "icons/dot.png")
        device.assignKey(KeyCode.SW8_PRESS, [])
        device.assignKey(KeyCode.SW8_RELEASE, [])

        #Button9 (bottom right)
        device.sendIconFor(9, "icons/dot.png")
        device.assignKey(KeyCode.SW9_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW9_RELEASE, [])

        device.updateDisplay()
        # self.jogFunction = ""

        # #This toggles the jog function and sets up key assignments and the label for the jog dial. It calls "updateDiplay()" if update is not explicitly set to False (for example if you need to update more parts of the display before updating it.)
        # def toggleJogFunction(update=True):
        #     if self.jogFunction == "size":  #Tool opacity in GIMP
        #         device.clearCallback(KeyCode.JOG)
        #         device.sendTextFor(1, "Tool opacity")
        #         device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_COMMA), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
        #         device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PERIOD), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
        #         self.jogFunction = "opacity"
        #         if update:
        #             device.updateDisplay()
        #     else:                            #Tool size in GIMP
        #         device.clearCallback(KeyCode.JOG)
        #         device.sendTextFor(1, "Tool size")
        #         device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_BRACE)])
        #         device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT_BRACE)])
        #         self.jogFunction = "size"
        #         if update:
        #             device.updateDisplay()


        # #Button 1 / jog dial press
        # device.registerCallback(toggleJogFunction, KeyCode.JOG_PRESS) #Call "toggleJogFunction" if the dial is pressed
        # device.assignKey(KeyCode.SW1_PRESS, [])                       #We do not send a key stroke when the dial is pressed, instead we use the callback.
        # device.assignKey(KeyCode.SW1_RELEASE, [])                     #We still need to overwrite the assignment to clear previously set assignments.
        # toggleJogFunction(False)    #We call toggleJogFunction to initially set the label and assignment
        # device.updateDisplay()      #Everything has been sent to the display. Time to refresh it.

    def poll(self, device):
        return False #Nothing to poll

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        device.clearCallbacks() #Remove our callbacks if we switch to a different mode


        ############## This mode is used as a fallback and a much more complex example than Gimp. It also uses a switchable Jog dial,
        ## Fallback ## but most of its functions give a feedback via LED. Also, we use MQTT (via a separately defined class) to get
        ############## data from a CO2 sensor and control a light (both including feedback)

class ModeFallback:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Main", inverted=True) #Title
        device.sendIconFor(2, "icons/globe.png")
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.RELEASE)])
        device.sendIconFor(3, "icons/file-earmark-word.png")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_W, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_W, ActionCode.RELEASE)])
        device.sendIconFor(4, "icons/file-earmark-spreadsheet.png")
        device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_E, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW4_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_E, ActionCode.RELEASE)])
        device.sendIconFor(5, "icons/envelope.png")
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_EMAIL_READER, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW5_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_EMAIL_READER, ActionCode.RELEASE)])
        device.sendIconFor(6, "icons/file-earmark-code-fill.png")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N, ActionCode.RELEASE)])
        device.sendIconFor(7, "icons/file-earmark_altium.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_A, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_A, ActionCode.RELEASE)])
        device.sendIconFor(8, "icons/chat-dots.png")
        device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW8_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE)])
        device.sendIconFor(9, "icons/calculator.png")
        device.assignKey(KeyCode.SW9_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_CALCULATOR, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW9_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_CALCULATOR, ActionCode.RELEASE)])

        ### All set, let's update the display ###

        device.updateDisplay()

    def poll(self, device):
        return False #No polling required

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching
        #Called periodically for animations.
#        pass

    def deactivate(self, device):
        #pass
        device.clearCallbacks() #Clear our callbacks if we switch to a different mode