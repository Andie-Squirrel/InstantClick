"""
Welcome to my simple auto-clicker code. Please enjoy!

Keep in mind, if this script is running, even if auto-clicking is disabled,
it may interefere with certain applications.

I plan to use listeners instead of keyboard and mouse button
detection within the main loop, which should hopefully reduce the lag.
"""

#<#####------------------Squirrelia.AUTOCLICKER.py------------------#####>#

MINIMUM_DELAY = 0.015 # The minimum wait time between clicks in seconds.
# BEWARE: as the delay approaches 0, the system may be overwhelmed and become unresponsive for a time
# modify this to your heart's content while accepting any and all responsibility for damage done

# Exit function for exception handling
def close():
	input("Press enter to exit\n")
	exit()

try: # Default preinstalled modules whose availability depends on your operating system
	import time # this module is great for cps monitoring, pausing the script for a certain duration, or just telling what time it is >w<
	import pythoncom # hack that gets win32api to function without dll errors. Taken from (https://stackoverflow.com/questions/24089133/win32api-no-dll-error-python)
	import tkinter # this module can display a window on screen
	import winsound # (cygwin module on windows) the only thing this module is here for is the BEEPS! (Coming soon to your computer... much annoyance)
except Exception as e:
	print(e)
	print("\nThis module should be preinstalled. Check which modules are compatible with your operating system.")
	close()

try: # modules that can be installed from install-requirements.bat
	from pynput.mouse import Button , Controller # can be used to control the mouse if needed, but in this stage it's only used to send clicks
	mouse = Controller() # create a little mouse object that we can mess with later
	import keyboard # detects keypresses or sends them out
	import win32api, win32con # detects mouse button presses or sends mouse clicks
except Exception as e:
	print(e)
	print("\nRun 'install-requirements.bat' to install all required modules")
	#print("pip install pynput")
	#print("pip install keyboard")
	#print("pip install pywin32")
	#print("pip install getch") # which is msvcrt and is not installable. Windows compatible
	close()


def switch(case):
	"""Switch operator instead of 'match' and 'case', which
	are not compatible with Python 3.9 and below"""
	entries = {
		'': True,
		'Y': True,
		'N': False,	
	}
	return entries.get(case,'False')

# Allow the user to control if the console should print the click rate time or not
# Exception handling
try:
	valid = False
	while not valid:
		inputCPS = input("Display delay between clicks? ([Y or press enter]/N)") # Ask the user if the delay should be printed

		valid = True

		# Only compatible with Python 3.10 and above:
		# # match str(inputCPS).upper():
		# # 	case "":
		# # 		inputCPS = True
		# # 	case 'Y':
		# # 		inputCPS = True
		# # 	case 'N':
		# # 		inputCPS = False
		# # 	case _:
		# # 		valid = False

		# backwards compatible method:
		inputCPS = switch(str(inputCPS.upper()))

		if inputCPS == 'False':
			valid = False

	enableCPSDisplay = inputCPS
	print("\tSelected:",enableCPSDisplay,"\n\n")

except Exception as e:
	print(e)


# This function creates beeps to alert the user when the clicks are enabled/disabled
# the usage is `beep(beep highness, beep amount, and beep quantity[back-to-back beeps])`
def beep(p,l,quan=1): # set the default amount of beeps to ONE, just in case it wasn't specified
	i = 0 # initialize the counting variable, much like a 'for' loop
	while i < quan: # keep running the code directly underneath until the new variable 'i' is equal to or greater than the 'quan', or specified amount of beeps
		winsound.Beep(p, l) # generate a tone based on the input given
		i += 1 # increase the counter variable for each iteration

# exit flag for main loop
exitFlag = False

# this function that will check if the key associated with exiting is pressed and will output either true or false
# Two methods of key input is employed instead of perhaps preferably hooking the keys.
def checkEsc():
	# get the key
	if keyboard.is_pressed('esc'): #the `keyboard` module is used to detect an `ESC` press
		print('esc by keyboard module')
		return True
	else:
		return False # In all other cases, forget it, you're not leaving

# function that alerts the user when the auto-clicking state has changed
def declareAutoClickFur():
	""" Module to display if auto-clicking is enabled
	"""
	if enableClicking:
		isEnabled = 'enabled'
		beep(1000,30) # one high beep to indicate it's been turned on
	else:
		isEnabled = 'disabled'
		beep(1000,30,2) # two high beeps to indicate it's now off
	print(f"\tPerma-click {isEnabled}") # print the click state
	time.sleep(0.1) # wait a tenth of a second to make sure this function doesn't get called immediately again, so the user has time to release the button


# pastTime variable to measure elapsed time between auto-clicks
pTime = 0

# These state variables keep track of the previous mouse state to ensure auto-clicking is only
# toggled when the clicks have been registered, and not while the mouse buttons are held down.

# past middle click
stateMiddle = win32api.GetKeyState(0x04) # checks if the middlemouse button is being pressed at this point of the code
# past right click
stateRight = win32api.GetKeyState(0x02) # same with the right mouse button.
# Left mouse button does not need to be checked, as it will be controlled by the script

# Instruct the user
print("Hold left click and middle-mouse click to\nenable auto-clicking. Right click or middle-mouse click \nto disable auto-clicking.\n\nPress ESC to exit\n")

# global flag to enable/ disable auto-clicking
global enableClicking
enableClicking = False # disable auto-clicking by default

# A function to register a mouse click
def sendClick():
	"""
	A module to send mouse press and release to the system
	"""

	time.sleep(MINIMUM_DELAY) # BEWARE, see line 7

	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) # register mouse-down
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0) # mouse-up release


	# ineffective old code

	# mouse.press(Button.left) #old click thing
	#print("pressedLeft") # and of course let the user know, if they bother to read the console
	#mouse.release(Button.left) 
    #print("releasedLeft") # yes, tell the user it's not being pressed anymore

def displayDelay():
	try: # I'm using 'try' just in case the following code doesn't work, especially because, if the code happens to be registered as instant, it will try to divide 1 by zero, and that would ordinarily result in a crash, so 'try' will ignore that and continue the code after printing that there was no detectable change in time.
		print("\tChange: ", 1/(time.time()-pTime)) # this just tells the user the amount of time that went by by calculating the difference between the Current time and the Past time we created a few lines ago. If you divide 1 with this value, you get the change in seconds
	except:
		print("No Detected Delay Between Clicks") # in the odd case that somehow, the current time and past time have not changed at all since the creation of the past time variable, we don't want the program to crash due to a mathematical error, so just tell the user that there is no time change and move on

#--------------------------MAIN LOOP--------------------------#

while not exitFlag: # main loop
	# What I hope to use instead of this to reduce lag: (https://nitratine.net/blog/post/how-to-use-pynputs-mouse-and-keyboard-listener-at-the-same-time/)
	exitFlag = checkEsc() # start each iteration by checking if the `ESC` key is pressed

	# these three variables check if the LEFT, RIGHT, and middle mouse buttons are immediately being pressed
	ml = win32api.GetKeyState(0x01)
	mr = win32api.GetKeyState(0x02)
	mm = win32api.GetKeyState(0x04) # these codes check which button is pressed. Win32Api checks action buttons, which includes detecting mouse buttons

	if enableClicking: # Auto-clicking heart and soul
		pTime = time.time() # this sets the past time to the current time, and as the code runs, the current time will increase while this variable stays the same, thus making the perfect method for cps-monitoring
		
		sendClick() # register a mouse-down and mouse-up
		
		# if enabled, displays the amount of time elapsed for each auto-click
		if enableCPSDisplay:
			displayDelay()
	
	# The keyStates check if the mouse buttons are immediately being pressed, but not if they have just been pressed since a previous iteration. In other words, we want to check if the
	# buttons have been clicked for one iteration, not keep toggling auto-clicking for every iteration while the mouse buttons have been held down. Therefore, the mouse has to be checked if it has just been pressed
	# or released and that the mouse state has changed. The state variable booleans accomplish this task.
	if mm != stateMiddle: # This check to see if the middlemouse button state is NOT the same as it was when we previously checked its state. If this is the case, then run the following code
		stateMiddle = mm # because the middle mouse state has changed, the state must be updated to prevent the line from being called multiple times. Basically, we can now say that the middle mouse button is being pressed, and this variable will be set to prove it, otherwise this line of code will keep being run by the while loop due to their inequality

		# This only checks if it had changed states. The following code will handle mouse-down and mouse-up events.

		# If the mouse has been pressed, win32api will yield a negative value
		# (usually -127), and a 0 or positive value if it is resting or released.
		# Thus, we may assume if the output is negative, the mouse button has been
		# pressed down. Otherwise, it is released.
		if mm < 0: # Mouse down
			if (not enableClicking and ml < 0) or (enableClicking): # now this is a bit more complicated, but all this does is (1) check that auto-clicking is right now NOT enabled, but also (2) that the LEFT mouse button is being pressed. Keep in mind, all we need to check was that the middle mouse button has changed its state and is being pressed, we don't need to check for the left click because it won't be used unless the middle-mouse is being pressed too and that autoclicking is enabled. The next indented lines of code will also run if (3) clicking has already been enabled (because the indented code after while loops) and then don't bother to check if the LEFT mouse button is pressed, just run the code to turn it back off again.
				enableClicking = not enableClicking # no matter how we got here, this line reverses the state of the auto-clicking boolean. If it's True, it will equal what is NOT True: False. And if False, it will be set to True. A nice little switch!
				declareAutoClickFur() # because of this, make sure that the user knows that auto-clicking has been changed. We run the function we made before at line 55. It's always good to find a way to communicate with the user if they maybe accidentally changed an important variable, like autoclicking. Keep 'em informed!

				print()
		else: # this else is for the RELEASE of the middle mouse button. If the middle mouse button has changed, and it is NOT less than zero, than we can be sure the user released the button, which can be used to tell them they let go. It's not super important, but I find it a nice feature
			if enableClicking: # of course, I would only want to tell the user if they had just turned clicking on and then released the middle mouse button. So not to bother them that they released the button while auto clicking is off. Floof!
				beep(540,60,1) # give them a slightly lower beep! I think it sounds nice, but if you want to change it, you can. [beep(beep frequency, beep duration, amount of beeps)]
	elif mr != stateRight: # We just defined how to change the autoclicking variable with the middlemouse button! Now, what if another button can to used to change it? Well, I would rather not use the RIGHT mouse button to turn it on, and can't use the LEFT button because it would turn itself on or off way too easily cause win32api would think that a simulated input is the same as one from the actual mouse, breaking itself. So instead, I'm just going to use the RIGHT mouse button as another way to turn autoclicking off. This is how:
		stateRight = mr # we just checked if the state of the RIGHT mouse button has changed, just like with the middle mouse button, so we have to make sure it updates for the RIGHT state as well.
		if mr < 0: # if it's being pressed down, we can run the following code
			if enableClicking: # if the autoclicker is enabled:
				enableClicking = False # disable
				declareAutoClickFur() # and, as always, inform the user

print('Exiting...')
beep(500,800,1) # Plays a much deeper, longer tone, perfect for a farewell
close() #FIN