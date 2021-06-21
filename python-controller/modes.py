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

#Optional libraries you might want to remove if you do not require them.
#import pulsectl                                  # Get volume level in Linux, pip3 install pulsectl
#from obswebsocket import obsws, requests, events # Control OBS. This requires the websocket plugin in OBS (https://github.com/Palakis/obs-websocket) and the Python library obs-websocket-py (pip3 install obs-websocket-py, https://github.com/Elektordi/obs-websocket-py)


        ############# Simple example. For Blender we just set up a few key assignments with corresponding images.
        ## Blender ## To be honest: Blender is just the minimalistic example here. Blender is very keyboard centric
        ############# and you should get used to the real shortcuts as it is much more efficient to stay on the keyboard all the time.

# class ModeBlender:

#     def activate(self, device):
#         device.sendTextFor("title", "Blender", inverted=True) #Title

#         #Button1 (Jog dial press)
#         device.sendTextFor(1, "<   Play/Pause   >")
#         device.assignKey(KeyCode.SW1_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.PRESS)]) #Play/pause
#         device.assignKey(KeyCode.SW1_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.RELEASE)])

#         #Jog dial rotation
#         device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT)]) #CW = Clock-wise, one frame forward
#         device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT)]) #CCW = Counter clock-wise, one frame back

#         #Button2 (top left)
#         device.sendIconFor(2, "icons/camera-reels.png")
#         device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_0, ActionCode.PRESS)]) #Set view to camera
#         device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_0, ActionCode.RELEASE)])

#         #Button3 (left, second from top)
#         device.sendIconFor(3, "icons/person-bounding-box.png")
#         device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.PRESS)]) #Isolation view
#         device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.RELEASE)])

#         #Button4 (left, third from top)
#         device.sendIconFor(4, "icons/dot.png")
#         device.assignKey(KeyCode.SW4_PRESS, []) #Not used, set to nothing.
#         device.assignKey(KeyCode.SW4_RELEASE, [])

#         #Button5 (bottom left)
#         device.sendIconFor(5, "icons/dot.png")
#         device.assignKey(KeyCode.SW5_PRESS, []) #Not used, set to nothing.
#         device.assignKey(KeyCode.SW5_RELEASE, [])

#         #Button6 (top right)
#         device.sendIconFor(6, "icons/aspect-ratio.png")
#         device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.PRESS)]) #Center on selection
#         device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.RELEASE)])

#         #Button7 (right, second from top)
#         #Button4 (left, third from top)
#         device.sendIconFor(7, "icons/collection.png")
#         device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F12), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE)]) #Render sequence
#         device.assignKey(KeyCode.SW7_RELEASE, [])

#         #Button8 (right, third from top)
#         device.sendIconFor(8, "icons/dot.png")
#         device.assignKey(KeyCode.SW8_PRESS, []) #Not used, set to nothing.
#         device.assignKey(KeyCode.SW8_RELEASE, [])

#         #Button9 (bottom right)
#         device.sendIconFor(9, "icons/dot.png")
#         device.assignKey(KeyCode.SW9_PRESS, []) #Not used, set to nothing.
#         device.assignKey(KeyCode.SW9_RELEASE, [])

#         device.updateDisplay()

#     def poll(self, device):
#         return False    # No polling in this example

#     def animate(self, device):
#         device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

#     def deactivate(self, device):
#         pass            # Nothing to clean up in this example




        ##########
        ## Gimp ## The Gimp example is similar to Blender, but we add a callback to pressing the jog dial to switch functions
        ##########

# class ModeGimp:
#     jogFunction = ""    #Keeps track of the currently selected function of the jog dial

#     def activate(self, device):
#         device.sendTextFor("title", "Gimp", inverted=True)  #Title

#         #Button2 (top left)
#         device.sendIconFor(2, "icons/fullscreen.png")
#         device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_Z)]) #Cut to selection (this shortcut appears to be language dependent, so you will probably need to change it)
#         device.assignKey(KeyCode.SW2_RELEASE, [])

#         #Button3 (left, second from top)
#         device.sendIconFor(3, "icons/upc-scan.png")
#         device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_I)]) #Cut to content (this shortcut appears to be language dependent, so you will probably need to change it)
#         device.assignKey(KeyCode.SW3_RELEASE, [])

#         #Button4 (left, third from top)
#         device.sendIconFor(4, "icons/crop.png")
#         device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_L)]) #Canvas size (this shortcut appears to be language
#         device.assignKey(KeyCode.SW4_RELEASE, [])

#         #Button5 (bottom left)
#         device.sendIconFor(5, "icons/arrows-angle-expand.png")
#         device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S)]) #Resize (this shortcut appears to be language
#         device.assignKey(KeyCode.SW5_RELEASE, [])

#         #Button6 (top right)
#         device.sendIconFor(6, "icons/clipboard-plus.png")
#         device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #Paste as new image
#         device.assignKey(KeyCode.SW6_RELEASE, [])

#         #Button7 (right, second from top)
#         device.sendIconFor(7, "icons/layers-half.png")
#         device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #New layer
#         device.assignKey(KeyCode.SW7_RELEASE, [])

#         #Button8 (right, third from top)
#         device.sendIconFor(8, "icons/arrows-fullscreen.png")
#         device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #Zom to fill screen
#         device.assignKey(KeyCode.SW8_RELEASE, [])

#         #Button9 (bottom right)
#         device.sendIconFor(9, "icons/dot.png")
#         device.assignKey(KeyCode.SW9_PRESS, []) #Not used, set to nothing.
#         device.assignKey(KeyCode.SW9_RELEASE, [])


#         self.jogFunction = ""

#         #This toggles the jog function and sets up key assignments and the label for the jog dial. It calls "updateDiplay()" if update is not explicitly set to False (for example if you need to update more parts of the display before updating it.)
#         def toggleJogFunction(update=True):
#             if self.jogFunction == "size":  #Tool opacity in GIMP
#                 device.clearCallback(KeyCode.JOG)
#                 device.sendTextFor(1, "Tool opacity")
#                 device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_COMMA), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
#                 device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PERIOD), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
#                 self.jogFunction = "opacity"
#                 if update:
#                     device.updateDisplay()
#             else:                            #Tool size in GIMP
#                 device.clearCallback(KeyCode.JOG)
#                 device.sendTextFor(1, "Tool size")
#                 device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_BRACE)])
#                 device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT_BRACE)])
#                 self.jogFunction = "size"
#                 if update:
#                     device.updateDisplay()


#         #Button 1 / jog dial press
#         device.registerCallback(toggleJogFunction, KeyCode.JOG_PRESS) #Call "toggleJogFunction" if the dial is pressed
#         device.assignKey(KeyCode.SW1_PRESS, [])                       #We do not send a key stroke when the dial is pressed, instead we use the callback.
#         device.assignKey(KeyCode.SW1_RELEASE, [])                     #We still need to overwrite the assignment to clear previously set assignments.
#         toggleJogFunction(False)    #We call toggleJogFunction to initially set the label and assignment
#         device.updateDisplay()      #Everything has been sent to the display. Time to refresh it.

#     def poll(self, device):
#         return False #Nothing to poll

#     def animate(self, device):
#         device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

#     def deactivate(self, device):
#         device.clearCallbacks() #Remove our callbacks if we switch to a different mode




        ############## This mode is used as a fallback and a much more complex example than Gimp. It also uses a switchable Jog dial,
        ## Fallback ## but most of its functions give a feedback via LED. Also, we use MQTT (via a separately defined class) to get
        ############## data from a CO2 sensor and control a light (both including feedback)

class ModeFallback:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Default", inverted=True) #Title
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
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S, ActionCode.RELEASE)])
        device.sendIconFor(7, "icons/file-earmark-image.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.PRESS)]) 
        device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_T, ActionCode.RELEASE)])
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
        #Called periodically for animations.
        pass

    def deactivate(self, device):
        pass
        # device.clearCallbacks() #Clear our callbacks if we switch to a different mode


        ######### One of the most complex examples. This controls OBS scenes and gives feedback about the current state. For this we
        ## OBS ## use the websocket plugin and address scenes and sources by their names (so, you need to adapt these to your setup).
        ######### We subscribe to OBS events and show the status on the key and LEDs.

# class ModeOBS:
#     ws = None           #Websocket instance
#     currentScene = None #Keep track of current scene

#     #Scenes assigned to buttons with respective icons.
#     scenes = [\
#                 {"name": "Moderation", "icon": "icons/card-image.png", "button": 2}, \
#                 {"name": "Closeup", "icon": "icons/person-square.png", "button": 3}, \
#                 {"name": "Slides", "icon": "icons/easel.png", "button": 4}, \
#                 {"name": "Video-Mute", "icon": "icons/camera-video-off.png", "button": 5}, \
#              ]

#     #State of sources within scenes. "items" is an array of scene/item combinations to keep track of items that need to be switched on multiple scenes simultaneously, so you can mute all mics in all scenes and switch scenes without an unpleasant surprise. The current state is tracked in this object ("current")
#     states = [\
#                 {"items": [("Moderation", "Phone"), ("Closeup", "Phone"), ("Slides", "Phone")], "icon": "icons/phone.png", "button": 7, "current": True}, \
#                 {"items": [("Slides", "Cam: Closeup")], "icon": "icons/pip.png", "button": 8, "current": True}, \
#                 {"items": [("Moderation", "Mic: Moderation"), ("Closeup", "Mic: Closeup"), ("Slides", "Mic: Closeup")], "icon": "icons/mic.png", "button": 9, "current": True}, \
#              ]

#     #Switch to scene with name "name"
#     def setScene(self, name):
#         self.ws.call(requests.SetCurrentScene(name))

#     #Toggle source visibility as defined in a state (see states above)
#     def toggleState(self, state):
#         visible = not state["current"]
#         for item in state["items"]:
#             self.ws.call(requests.SetSceneItemProperties(item[1], scene_name=item[0], visible=visible))

#     #Generates a callback function which in turn calls "setScene" with the fixed scene "name" without requiring a parameter
#     def getSetSceneCallback(self, name):
#         return lambda: self.setScene(name)

#     #Generates a callback function which in turn calls "toggleState" with a fixed "state" object without requiting a parameter
#     def getToggleStateCallback(self, state):
#         return lambda: self.toggleState(state)

#     #Updates the buttons associated with scenes. Unless "init" is set to true, it only updates changed parts of the display and returns True if anything has changed so that the calling function should call updateDisplay()
#     def updateSceneButtons(self, device, newScene, init=False):
#         if self.currentScene == newScene:
#             return False
#         for scene in self.scenes:
#             if (init and newScene != scene["name"]) or self.currentScene == scene["name"]:
#                 device.sendIconFor(scene["button"], scene["icon"], centered=True)
#             elif newScene == scene["name"]:
#                 device.sendIconFor(scene["button"], scene["icon"], centered=True, marked=True)
#         self.currentScene = newScene
#         return True

#     #Updates the buttons associated with states. Unless "init" is set to true, it only updates changed parts of the display and returns True if anything has changed so that the calling function should call updateDisplay()
#     def updateStateButtons(self, device, scene, item, visible, init=False):
#         anyUpdate = False
#         for state in self.states:
#             if init or ((scene, item) in state["items"] and visible != state["current"]):
#                 device.sendIconFor(state["button"], state["icon"], centered=True, crossed=(not (state["current"] if init else visible)))
#                 anyUpdate = True
#                 if not init:
#                     state["current"] = visible
#         return anyUpdate

#     #Change LED colors if the microphones are muted
#     def updateLED(self, device):
#         if self.currentScene == "Video-Mute" or self.states[2]["current"] == False:
#             leds = [0xff0000 for i in range(device.nLeds)] #Either this is the empty "Video-Mute" scene or the mics are muted -> red
#         else:
#             leds = [0x00ff00 for i in range(device.nLeds)] #In any other case the mics are live -> green
#         device.setLeds(leds)

#     def activate(self, device):
#         self.ws = obsws("localhost", 4444) #Connect to websockets plugin in OBS

#         #Callback if OBS is shutting down
#         def on_exit(message):
#             self.ws.disconnect()

#         #Callback if the scene changes
#         def on_scene(message):
#             if self.updateSceneButtons(device, message.getSceneName()):
#                 device.updateDisplay() #Only update if parts of the display actually changed
#             self.updateLED(device)

#         #Callback if the visibility of a source changes
#         def on_visibility_changed(message):
#             if self.updateStateButtons(device, message.getSceneName(), message.getItemName(), message.getItemVisible()):
#                 device.updateDisplay() #Only update if parts of the display actually changed
#             self.updateLED(device)

#         #Register callbacks to OBS
#         self.ws.register(on_exit, events.Exiting)
#         self.ws.register(on_scene, events.SwitchScenes)
#         self.ws.register(on_visibility_changed, events.SceneItemVisibilityChanged)

#         self.ws.connect()

#         device.sendTextFor("title", "OBS", inverted=True) #Title



#         ### Buttons 2 to 5 set different scenes (Moderation, Closeup, Slides and Video Mute) ###

#         for scene in self.scenes:
#             device.assignKey(KeyCode["SW"+str(scene["button"])+"_PRESS"], [])
#             device.assignKey(KeyCode["SW"+str(scene["button"])+"_RELEASE"], [])
#             device.registerCallback(self.getSetSceneCallback(scene["name"]), KeyCode["SW"+str(scene["button"])+"_PRESS"])



#         ### Button 6: Order!

#         def stopOrder():
#             self.ws.call(requests.SetSceneItemProperties("Order", visible=False))

#         def playOrder():
#             self.ws.call(requests.SetSceneItemProperties("Order", visible=True))
#             Timer(3, stopOrder).start()


#         device.assignKey(KeyCode["SW6_PRESS"], [])
#         device.assignKey(KeyCode["SW6_RELEASE"], [])
#         device.registerCallback(playOrder, KeyCode["SW6_PRESS"])
#         device.sendIconFor(6, "icons/megaphone.png", centered=True)


#         ### Buttons 7 to 9 toogle the visibility of items, some of which are present in multiple scenes (Mics, Picture-In-Picture cam, Video stream from phone) ###

#         for state in self.states:
#             device.assignKey(KeyCode["SW"+str(state["button"])+"_PRESS"], [])
#             device.assignKey(KeyCode["SW"+str(state["button"])+"_RELEASE"], [])
#             device.registerCallback(self.getToggleStateCallback(state), KeyCode["SW"+str(state["button"])+"_PRESS"])



#         ### Get current state and initialize buttons accordingly ###
#         current = self.ws.call(requests.GetSceneList())
#         for scene in current.getScenes():
#             for item in scene["sources"]:
#                 for state in self.states:
#                     if (scene["name"], item["name"]) in state["items"]:
#                         state["current"] = item["render"]

#         #Call updateSceneButtons and updateStateButtons to initialize their images
#         self.currentScene = None
#         self.updateSceneButtons(device, current.getCurrentScene(), init=True)
#         self.updateStateButtons(device, None, None, True, init=True)
#         device.updateDisplay()
#         self.updateLED(device)

#     def poll(self, device):
#         return False    #No polling required

#     def animate(self, device):
#         pass    #In this mode we want permanent LED illumination. Do not fade or animate otherwise.

#     def deactivate(self, device):
#         device.clearCallbacks() #Clear our callbacks if we switch to a different mode

