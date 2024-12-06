import concurrent.futures
import random
import keyboard
import pydirectinput
import pyautogui
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *

##################### MESSAGE QUEUE VARIABLES #####################

# MESSAGE_RATE controls how fast we process incoming Twitch Chat messages. It's the number of seconds it will take to handle all messages in the queue.
# This is used because Twitch delivers messages in "batches", rather than one at a time. So we process the messages over MESSAGE_RATE duration, rather than processing the entire batch at once.
# A smaller number means we go through the message queue faster, but we will run out of messages faster and activity might "stagnate" while waiting for a new batch. 
# A higher number means we go through the queue slower, and messages are more evenly spread out, but delay from the viewers' perspective is higher.
# You can set this to 0 to disable the queue and handle all messages immediately. However, then the wait before another "batch" of messages is more noticeable.
MESSAGE_RATE = 0.5
# MAX_QUEUE_LENGTH limits the number of commands that will be processed in a given "batch" of messages. 
# e.g. if you get a batch of 50 messages, you can choose to only process the first 10 of them and ignore the others.
# This is helpful for games where too many inputs at once can actually hinder the gameplay.
# Setting to ~50 is good for total chaos, ~5-10 is good for 2D platformers
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 
"""
Game input variable, put game to play in game variable
MUST BE ALL LOWERCASE
"""

GAME=""

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False

##########################################################

# Count down before starting, so you have time to load up the game
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

#Replace this logic later with discord webhooks
if STREAMING_ON_TWITCH:
    t = TwitchPlays_Connection.Twitch()
    t.twitch_connect(TWITCH_CHANNEL)
else:
    t = TwitchPlays_Connection.YouTube()
    t.youtube_connect(YOUTUBE_CHANNEL_ID, YOUTUBE_STREAM_URL)

def handle_message(message):
    try:
        msg = message['message'].lower()
        username = message['username'].lower()

        print("Got this message from " + username + ": " + msg)

        # Now that you have a chat message, this is where you add your game logic.
        # Use the "HoldKey(KEYCODE)" function to permanently press and hold down a key.
        # Use the "ReleaseKey(KEYCODE)" function to release a specific keyboard key.
        # Use the "HoldAndReleaseKey(KEYCODE, SECONDS)" function press down a key for X seconds, then release it.
        # Use the pydirectinput library to press or move the mouse

        #Input logic for all games
        
        if msg== "screenshot":
            if random.randint(1, 8)==1:
                HoldAndReleaseKey(F12, .1)
        elif GAME=="trackmania":
            if msg == "left": 
                HoldAndReleaseKey(LEFT_ARROW, .8)
            elif msg == "right":
                HoldAndReleaseKey(RIGHT_ARROW, .8)
            elif msg == "gas" or "forward":
                ReleaseKey(DOWN_ARROW)
                HoldKey(UP_ARROW)
            elif msg == "stop" or "reverse" or "brake":
                ReleaseKey(UP_ARROW)
                HoldKey(DOWN_ARROW)
            elif msg=="release":
                ReleaseKey(UP_ARROW)
                ReleaseKey(DOWN_ARROW)
            elif msg=="respawn":
                if random.randint(1, 5) == 1:
                    HoldAndReleaseKey(ENTER, .1)
            elif msg=="still respawn" or "standstill respawn":
                if random.randint(1, 6) == 1:
                    HoldAndReleaseKey(ENTER, .1)
                    HoldAndReleaseKey(ENTER, .1)
            elif msg=="honk" or "horn":
                HoldAndReleaseKey(NUMPAD_0, .1)

        elif GAME=="peggle":
            if msg=="up":
                pydirectinput.moveRel(0, -15)
            elif msg=="down":
                pydirectinput.moveRel(0, 15)
            elif msg=="left":
                pydirectinput.moveRel(-15, 0)
            elif msg=="right":
                pydirectinput.moveRel(15, 0)    
            elif msg=="slight left" or "small left":
                HoldAndReleaseKey(MOUSE_WHEEL_DOWN, 2)
            elif msg=="slight right" or "small right":
                HoldAndReleaseKey(MOUSE_WHEEL_UP, 2)
            elif msg=="shoot":
                if random.randint(1, 7) == 1:
                    HoldAndReleaseKey(LEFT_MOUSE, .5)
        
        elif GAME=="american truck simulator":
            if msg=="gas" or "forward":
                HoldKey(W)
            elif msg=="brake" or "reverse" or "stop":
                HoldKey(S)
            elif msg=="left":
                HoldAndReleaseKey(A, 2.5)
            elif msg=="right":
                HoldAndReleaseKey(D, 2.5)
            elif msg=="start engine" or "stop engine" or "engine":
                HoldAndReleaseKey(E, .2)
            elif msg=="ebrake" or "emergency brake":
                if random.randint(1, 18)==1:
                    HoldAndReleaseKey(SPACE, .2)
            elif msg=="left signal" or "left turn signal":
                HoldAndReleaseKey(LEFT_BRACKET, .2)
            elif msg=="right signal" or "right turn signal":
                HoldAndReleaseKey(RIGHT_BRACKET, .2)
            elif msg=="lights" or "headlights":
                HoldAndReleaseKey(L, .2)
            elif msg=="hazards" or "hazard lights":
                HoldAndReleaseKey(F, .2)
            elif msg=="horn" or "honk":
                HoldAndReleaseKey(H, .7)
            elif msg=="wipers" or "windshield wipers":
                HoldAndReleaseKey(P, .2)
            elif msg=="confirm":
                HoldAndReleaseKey(ENTER, .2)
            elif msg=="mouse up":
                pydirectinput.moveRel(0, -15)
            elif msg=="mouse down":
                pydirectinput.moveRel(0, 15)
            elif msg=="mouse left":
                pydirectinput.moveRel(-15, 0)
            elif msg=="mouse right":
                pydirectinput.moveRel(15, 0) 
            elif msg =="trailer" or "connect trailer" or "disconnect trailer":
                if random.randint(1, 30) == 1:
                    HoldAndReleaseKey(T, .2)  
            elif msg=="skip" or "next track" or "radio next":
                HoldAndReleaseKey(PAGE_UP, .2)
            elif msg=="release":
                ReleaseKey(UP_ARROW)
                ReleaseKey(DOWN_ARROW)
        
        elif GAME=="beamng":
            if msg=="gas" or "forward":
                HoldKey(UP_ARROW)
            elif msg=="brake" or "reverse" or "stop":
                HoldKey(DOWN_ARROW)
            elif msg=="left":
                HoldAndReleaseKey(LEFT_ARROW, 2.5)
            elif msg=="right":
                HoldAndReleaseKey(RIGHT_ARROW, 2.5)
            elif msg=="mouse up":
                pydirectinput.moveRel(0, -15)
            elif msg=="mouse down":
                pydirectinput.moveRel(0, 15)
            elif msg=="mouse left":
                pydirectinput.moveRel(-15, 0)
            elif msg=="mouse right":
                pydirectinput.moveRel(15, 0)
            elif msg=="pause" or "esc" or "escape":
                if random.randint(1, 7)==1:
                    HoldAndReleaseKey(ESC, .2)
            elif msg=="lights" or "headlights":
                HoldAndReleaseKey(N, .2)
            elif msg=="respawn" or "recover" or "recover vehicle":
                if random.randint(1, 8)==1:
                    HoldAndReleaseKey(R, .2)
            elif msg=="release":
                ReleaseKey(UP_ARROW)
                ReleaseKey(DOWN_ARROW)
        
        elif GAME=="rocket league":
            if msg=="gas" or "forward":
                HoldKey(W)
            elif msg=="brake" or "reverse" or "stop":
                HoldKey(S)
            elif msg=="left":
                HoldAndReleaseKey(A, 1.7)
            elif msg=="right":
                HoldAndReleaseKey(D, 1.7)
            elif msg=="jump":
                HoldAndReleaseKey(RIGHT_MOUSE, .2)
            elif msg =="boost small" or "skip replay":
                HoldAndReleaseKey(LEFT_MOUSE, .5)
            elif msg=="boost medium":
                if random.randint(1,2)==1:
                    HoldAndReleaseKey(LEFT_MOUSE, 1)
            elif msg=="boost large":
                if random.randint(1, 3)==1:
                    HoldAndReleaseKey(LEFT_MOUSE, 1.75)
            elif msg=="powerslide" or "air roll":
                HoldAndReleaseKey(LEFT_SHIFT, 1.75)
            elif msg=="powerslide right" or "sharp right" or "air roll right":
                HoldKey(D)
                HoldAndReleaseKey(LEFT_SHIFT, .8)
                ReleaseKey(D)
            elif msg=="powerslide left" or "sharp left" or "air roll left":
                HoldKey(A)
                HoldAndReleaseKey(LEFT_SHIFT, .8)
                ReleaseKey(A)
            elif msg=="air roll forward" or "air roll forwards":
                HoldAndReleaseKey(W, .8)
            elif msg=="air roll backward" or "air roll backwards" or "airroll backward" or "airroll backwards":
                HoldAndReleaseKey(S, .8)
            elif msg=="ball cam" or "focus ball":
                HoldAndReleaseKey(SPACE, .2)
            elif msg=="behind" or "look backwards":
                HoldAndReleaseKey(MIDDLE_MOUSE, 1)
            elif msg=="scoreboard":
                HoldAndReleaseKey(TAB, 1)
        
        elif GAME=="geometry dash":
            if msg=="jump":
                HoldAndReleaseKey(SPACE, .35)
        
        elif GAME=="nothing":
            if msg=="click":
                if random.randint(1, 100):
                    HoldAndReleaseKey(LEFT_MOUSE, .1)
        

        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))


while True:

    active_tasks = [t for t in active_tasks if not t.done()]

    #Check for new messages
    new_messages = t.twitch_receive_messages()
    if new_messages:
        message_queue += new_messages; # New messages are added to the back of the queue
        message_queue = message_queue[-MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

    messages_to_handle = []
    if not message_queue:
        # No messages in the queue
        last_time = time.time()
    else:
        # Determine how many messages we should handle now
        r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            # Pop the messages we want off the front of the queue
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time()

    # If user presses Shift+Backspace, automatically end the program
    if keyboard.is_pressed('shift+backspace'):
        exit()

    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')
 