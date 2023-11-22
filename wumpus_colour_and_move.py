import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
from collections import Counter
import threading

# To use the functions defined here, save this file in the same derectory as
# your main file and import this file

# Use these labled pins to connect GPIO pins
# For more reference see the pin diagram of L298n and Rpi
in1 = 24
in2 = 23
ena = 25
in3 = 17
in4 = 27
enb = 18
temp1=1


# GPIO initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)

# Set Low
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

# PWM with 100 duty cycle
q=GPIO.PWM(enb,10)
p=GPIO.PWM(ena,10)
p.start(100)
q.start(100)


# Time (in seconds) to Run the action
# Fine tune it according to your rover
t_forward = 0.95
t_turn = 0.61


# Handling individual pins
def start_pin(pin, time):
    GPIO.output(pin, GPIO.HIGH)
    t = threading.Timer(time, end)
    t.start()

def end():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)


# Call these functions to execute unit movements

def move_forword():
    start_pin(in1, t_forward)
    start_pin(in3, t_forward)
    sleep(t_forward)

def turn_left():
    start_pin(in3, t_turn)
    sleep(t_turn)

def turn_right():
    start_pin(in1, t_turn)
    sleep(t_turn)


# Calculate Mode
def calculate_mode(numbers):
    counter = Counter(numbers)
    mode = counter.most_common(1)[0][0]
    return mode



# Call these functions to measure colour of the current grid

def Detect_color():
    cap=cv2.VideoCapture(3)

    # Proportion of the colour
    percent_pink  = percent_green = percent_yellow = percent_sky_blue = percent_purple = percent_black= 0
    colour_index = [] # just for internal computation

    loop_count = 10
    while(loop_count>0):
        # Reading the video from the
        # webcam in image frames
        _, imageFrame = cap.read()
        #imageFrame=cv2.resize(imageFrame,(300,300))

        # Convert the imageFrame in
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)


        # Colour Filters
        # The test setup will have the following color mappings
        # Purple - Wumpus
	# Pink - Stench
	# Blue - Breeze
	# Green - Pit
	# Yellow - Gold
	#
	# The following values have been calibrated for the test setup in 105
	#
        pink_lower = np.array([148,43,34], np.uint8)
        pink_upper = np.array([179,255,255], np.uint8)
        pink_mask = cv2.inRange(hsvFrame, pink_lower, pink_upper)
        pink_count = np.sum(np.nonzero(pink_mask))

        #cv2.imshow("pink",pink_mask)

        # Set range for green color and
        # define mask
        green_lower = np.array([31,40,45], np.uint8)
        green_upper = np.array([80,255,190], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
        green_count = np.sum(np.nonzero(green_mask))

        # Set range for yellow color and
        # define mask
        yellow_lower = np.array([0,75,50], np.uint8)
        yellow_upper = np.array([44,255,168], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
        yellow_count = np.sum(np.nonzero(yellow_mask))

        # Set range for sky_blue color and
        # define mask
        sky_blue_lower = np.array([70,40,120], np.uint8)
        sky_blue_upper = np.array([137,255,255], np.uint8)
        sky_blue_mask = cv2.inRange(hsvFrame, sky_blue_lower, sky_blue_upper)
        sky_blue_count = np.sum(np.nonzero(sky_blue_mask))

        # Set range for purple color and
        # define mask
        purple_lower = np.array([68,10,2], np.uint8)
        purple_upper = np.array([152,154,229], np.uint8)
        purple_mask = cv2.inRange(hsvFrame, purple_lower, purple_upper)
        purple_count = np.sum(np.nonzero(purple_mask))

        # Set range for black color and
        # define mask
        black_lower = np.array([23,143,0], np.uint8)
        black_upper = np.array([179,255,40], np.uint8)
        black_mask = cv2.inRange(hsvFrame, black_lower, black_upper)
        black_count = np.sum(np.nonzero(black_mask))

        total_count = pink_count + green_count + yellow_count + sky_blue_count + purple_count + black_count

        # Individual Share
        percent_pink  = pink_count*100/total_count
        percent_green = green_count*100/total_count
        percent_yellow = yellow_count*100/total_count
        percent_sky_blue = sky_blue_count*100/total_count
        percent_purple = purple_count*100/total_count
        percent_black= black_count*100/total_count

        # each loop has a max detected colour
        frame_list = [percent_pink,percent_green,percent_yellow,percent_sky_blue,percent_purple,percent_black]
        colour_index.append(frame_list.index(max(frame_list)))

        loop_count-=1

    colour = calculate_mode(colour_index)
    print(colour)


    cap.release()
    cv2.destroyAllWindows()

    if colour == 0:
        print("stench: pink")
        return "pink"
    elif colour == 1:
        print("pit: green")
        return "green"
    elif colour == 2:
        print("gold: yellow")
        return "yellow"
    elif colour == 3:
        print("breeze: sky_blue")
        return "sky_blue"
    elif colour == 4:
        print("wumpus: purple")
        return "purple"
    elif colour == 5:
        print("stop: black")
        return "black"


# Generate percept sequance
#  Your code...

def get_real_tvec():
    """
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)
    """
    detected_color = Detect_color()
    if(detected_color == "pink"):
        tvec = [True, False, False, False, False]
    elif(detected_color == "green"):
        print("Agent reached in the pit.")
        tvec = [False, False, False, False, False]
    elif(detected_color == "yellow"):
        print("Agent reached on the block of gold.")
        tvec = [False, False, True, False, False]
    elif(detected_color == "sky_blue"):
        tvec = [False, True, False, False, False]
    elif(detected_color=="black"):
        tvec = [False, False, False, False, False]

    return tvec

def get_input_tvec():
    """
    tvec := a boolean (True/False) vector with entries corresponding to

            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)
    """
    detected_color = input("Enter current detected colour from [pink, green, yellow, sky_blue, black]: ").lower() # Detect_color()
    if(detected_color == "pink"):
        tvec = [True, False, False, False, False]
    elif(detected_color == "green"):
        print("Agent reached in the pit.")
        tvec = [False, False, False, False, False]
    elif(detected_color == "yellow"):
        print("Agent reached on the block of gold.")
        tvec = [False, False, True, False, False]
    elif(detected_color == "sky_blue"):
        tvec = [False, True, False, False, False]
    elif(detected_color=="black"):
        tvec = [False, False, False, False, False]

    return tvec
)

# Detect_color()



# To terminate the GPIO last state use:
print("bye!")
GPIO.cleanup()
