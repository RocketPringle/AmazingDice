# ------ MODULES ------ #

import random
import time

# ------ FUNCTIONS ------ #

def diceRoll(size):
    for i in range(4):
        print(f'rolling{"." * i}', end='\r')
        time.sleep(0.5)
    return random.randint(1,size), random.randint(1,size)

def menu(choice): # prints menu and returns what u pick (tree style)
    if choice == 'menu':
        return int(input('--- MENU ---\n1) View stats\n2) Start match \n3) Sign out\n\n'))
    elif choice == 'match':
        return int(input('--- START ---\n1) Bot\n2) Person\n\n'))
    elif choice == 'bot':
        return int(input('--- DIFFICULTY ---\n1) Easy\n2) Medium\n3) Hard\n4) Expert\n\n'))

def match(choice, difficulty): # match function
    for i in range(3):
    roll1, roll2 = diceRoll(6) # rolls dice for both players
    if choice == 'bot': # if bot is chosen
        roll1 -= difficulty # reduces roll1 (bot roll) by difficulty
    

# ------ MAIN ------ #

# ONLINE:??????????????

# sign up:
    # make user + pass (pass can be random and has to be 12 chars, capital and lowercase, special char)
# log in:
    # get username + pass 
# guest
    # no acc

# show menu:
    # stats choice ✔
    # match with other (who signs in) or bot (difficulties make bot roll more times? or have buffed odds ig idk this ist skil based bro) ✔
    # logout ✔

def menuHandler():
    choice = menu('menu') # show main menu
    if choice == 1: # user chose to view stats
        # USE FILE MANAGEMENT TO SHOW STATS!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    elif choice == 2: # user chose to start match
        choice = menu('match') # show match menu
        if choice == 1: # user chose to play with bot
            choice = menu('bot') # show bot menu
            if choice == 1: # user chose easy
                match('bot', '-2') # use match function to start match with bot and difficulty (-2 is point reduction)
            elif choice == 2: # user chose medium
                match('bot', '-1') # use match function to start match with bot and difficulty (-1 is point reduction)
            elif choice == 3: # user chose hard
                match('bot', '0') # use match function to start match with bot and difficulty (0 is no point reduction)
            elif choice == 4: # user chose expert
                match('bot', '1') # use match function to start match with bot and difficulty (1 is point increase)
        elif choice == 2: # user chose to play with other player
            match('person') # use match function to start match with other player
    elif choice == 3: # user chose to sign out
        for i in range(4): # cool '...' animation (for loop)
            print(f'signing out{"." * i}', end='\r') # end='\r' is to overwrite the line to append the next '.' to signing out message
            time.sleep(0.5) # time.sleep(0.5) is to slow down the animation
        print('signed out') # prints signed out after the animation
        time.sleep(1) # waits 1 second before closing
        # SIGN OUT WHEN I MADE THE SIGN IN SYSTEM !!!!!!!!!!!!!!!!!!!!!!!!!!


# stats choice:
    # use file management to show stats

# match choice:
    # person:
        # other player sign in or guest (no acc)
        # do first roll to determine first ppl draws etc
        # roll 3 times and total for each person
        # if draw, roll again
        # whoever largest gets point stored in dict
        # find largest points
        # print ascii art trophy with score under
    # bot:
        # difficulties:
            # easy does score but -2 ✔
            # med does score but -1 ✔  
            # hard does score but -0 ✔
            # expert does score but +1 ✔
        # both roll 3 times and total for each person but bot -x based on difficulty
        # if draw, roll again
        # whoever largest gets point stored in dict
        # find largest points
        # print ascii art trophy with score under
        