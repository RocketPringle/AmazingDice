# ------ MODULES ------ #

import random
import time
import json
import os
import hashlib

# ------ GLOBAL VARIABLES ------ #

width = 40  # width for cool centering
# ------ FILE STUFF ------ #

os.chdir(os.path.dirname(os.path.abspath(__file__))) # Change to the script's directory when starting
# ^^^^ so much stupid things i dont like file management

# ------ USER DATA FUNCTIONS ------ #

# note: this is so complicated bro 

def hashPassword(password): # hashes password using SHA-256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def loadUsers(): #loads user data from json file
    try:
        with open('userLoginInfo.json', 'r') as file: # opens userLoginInfo.json file
            #print('User data loaded successfully!') # prints user data loaded successfully message for debugging
            return json.load(file) # returns user data as a dictionary
    except FileNotFoundError: # handles case where file doesn't exist
        print("Warning: User data file not found! Creating temporary user structure...")
        return {"users": {}} # returns empty user structure
    except PermissionError: # handles case where file can't be accessed
        print("Error: Cannot access user data file! Creating temporary user structure...")
        return {"users": {}}
    except json.JSONDecodeError: # handles case where file is corrupted
        print("Error: User data file is corrupted! Creating temporary user structure... ")
        return {"users": {}}

def saveUsers(data): # saves user data to json file
    try:
        with open('userLoginInfo.json', 'w') as file:  # try to open file in write mode
            json.dump(data, file, indent=4)  # try to write the data to the file
            #print("User data saved successfully!")  # only prints if both operations succeed (for debugging)
    except PermissionError:  # if we can't write to the file (no permissions)
        print("Error: Cannot save user data! Check file permissions.")

def addNewUser(username, password): # adds a new user to the system
    data = loadUsers() # load current users
    
    if username in data['users']: # check if username already exists
        print("Username already exists!")
        return False
    
    # create new user with default stats
    data['users'][username] = {
        "hashedPassword": hashPassword(password),  # store the hashed password
        "joinDate": time.strftime("%d/%m/%Y"),  # store today's date in UK format
        "stats": {
            "totalGames": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "vsBot": {
                "easy": {
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "medium": {
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "hard": {
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "expert": {
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                }
            },
            "vsPlayer": {
                "wins": 0,
                "losses": 0,
                "draws": 0
            }
        }
    }
    
    saveUsers(data)  # save the updated data
    print(f"\nUser {username} created successfully!\n")
    return True

def viewUserStats(username): # displays user statistics
    data = loadUsers() # load user data
    
    if username not in data['users']: # check if user exists
        print("User not found!".center(width)) # prints error if user doesn't exist
        return False
    
    stats = data['users'][username]['stats'] # get user's stats
    
    # Display stats in a nice format with .center
    print(f"{'='*width}\n{'{username}\'s Stats'.center(width)}\n{'='*width}\n")
    print(f"Total Games: {stats['totalGames']}".center(width))
    print(f"Overall: {stats['wins']} Wins, {stats['losses']} Losses, {stats['draws']} Draws".center(width))
    
    # Bot stats with each difficulty
    print("\n" + "Bot Games".center(width))
    print("="*width)
    for difficulty in ['easy', 'medium', 'hard', 'expert']: # for each difficulty
        botStats = stats['vsBot'][difficulty] # gets bot stats for each difficulty
        print(f"{difficulty.capitalize()}: {botStats['wins']} Wins, {botStats['losses']} Losses, {botStats['draws']} Draws".center(width))
    
    # Player vs Player stats
    print("\n" + "Vs Player".center(width))
    print("="*width)
    playerStats = stats['vsPlayer'] # gets player stats
    print(f"Wins: {playerStats['wins']}, Losses: {playerStats['losses']}, Draws: {playerStats['draws']}".center(width))
    print("="*width + "\n")
    return True

def login(): # login function where u enter username and password and it checks if it exists and if it does it checks if the password is correct then returns username 
    os.system('cls')
    print(f"\n{'='*width}\n{'LOGIN'.center(width)}\n{'='*width}\n")
    username = input("Username: ") # gets username
    password = input("Password: ") # gets password
    userData = loadUsers() # loads user data
    
    if username in userData['users']: # checks if username exists
        if userData['users'][username]['hashedPassword'] == hashPassword(password): # checks if password is correct
            os.system('cls') # clears terminal
            print(f"Welcome back, {username}!") # prints welcome back message
            time.sleep(1)
            os.system('cls')
            return username # returns username
        else: # if password is incorrect
            print("Incorrect password!") # prints incorrect password message
            login()  # Try again by calling login again
    else: # if username does not exist
        print("Username not found!") # prints username not found message
        login()  # Try again by calling login again

def createAccount(): # creates an account
    userData = loadUsers() # loads user data
    username = input('Username: ') # gets username
    if username in userData['users']: # checks if username already exists
        print('Username already exists!\nTry a different username.') 
        createAccount() # recursively calls createAccount function to try again
    password = input('Password: ') # gets initial password
    while not (len(password) >= 12 and 
              any(c.isdigit() for c in password) and 
              any(c.isupper() for c in password) and 
              any(c.islower() for c in password) and 
              any(c in r'!#$%&()*+,-./:;<=>?@[]^_`{|}~\'"' for c in password)): # checks if password matches requirements
        print("Password must be at least 12 characters and contain uppercase, lowercase, numbers, and special characters.")
        password = input('Password: ') # gets password
    if addNewUser(username, password): # adds new user to userData (if checks if successful)
        print(f"Account created successfully! Welcome, {username}!") # prints success message
        return username # returns username

# ------ GAME FUNCTIONS ------ #

def getDifficultyString(difficulty): # needed to convert difficulty to string for stat storage as its stored as int not string
    if difficulty == -2:
        return "easy"
    elif difficulty == -1:
        return "medium"
    elif difficulty == 0:
        return "hard"
    elif difficulty == 1:
        return "expert"
    return "hard"  # default fallback

def homeScreen(): # defines homeScreen function that prints home screen for loging in or creating an account
    print(f"\n{'='*width}")
    print("Welcome to".center(width))
    print("Amazing Dice!".center(width))
    print(f"{'='*width}\n")
    print("         ________")
    print("        /\\   o   \\")
    print("       /o \\       \\")
    print("      /    \\   o   \\")
    print("      \\    /       /")
    print("       \\o /   o   /")
    print("        \\/___o___/")
    print("\nRoll the dice and test your luck!\n".center(width))
    time.sleep(2) # show welcome message for 2 seconds
    os.system('cls') # clear screen in prep for home screen
    choice = menu('home', None, None) # calls menu function with home as choice variable
    if choice == 1: # if u pick login
        menuHandler(False, login()) # calls menuHandler function with False as guestMode variable and username as username variable returned by login function
    elif choice == 2: # if u pick create account
        menuHandler(False, createAccount()) # calls menuHandler function with False as guestMode variable and username as username variable returned by createAccount function
    elif choice == 3: # if u pick guest
        print(f'{"="*width}\n{"Guest mode enabled!".center(width)}\n{"="*width}\n') # prints guest mode enabled message
        time.sleep(1)
        os.system('cls')
        menuHandler(True, None) # calls menuHandler function with True as guestMode variable and None as username variable

def playRound(difficulty, choice, scores, fastRoll): # defines playRound function that handles a single round
    rollTotal1, rollTotal2 = diceRoll(6, difficulty, choice, fastRoll) # rolls dice for both players
    print(f"\nYour total roll: {rollTotal2}") # prints your total roll
    print(f"{'Bot' if choice == 'bot' else 'Player 1'}'s total roll: {rollTotal1}") # prints bot's total roll
    if rollTotal1 > rollTotal2: # checks if first player has largest roll total
        scores['player1'] += 1 # adds 1 to player1's score
        print(f"{'Bot' if choice == 'bot' else 'Player 1'} wins this round!") # prints who wins this round
    elif rollTotal1 < rollTotal2: # checks if second player has largest roll
        scores['player2'] += 1 # adds 1 to player2's score
        print("You win this round!") # prints you win this round
    else: # if draw
        print("Draw! Rolling again...\n") # prints draw
        time.sleep(0.5) # wait before reroll
        playRound(difficulty, choice, scores, fastRoll) # recursively play the round again

def diceRoll(size, difficulty, choice, fastRoll): # defines diceRoll function using the size of the dice, bot difficulty, and choice of player (bot or person)
    rollTotal1, rollTotal2 = 0, 0 # initialize rolls to 0
    for i in range(3): # rolls dice 3 times
        for x in range(4): # cool '...' animation
            print(f'Rolling{"." * x}', end='\r') # prints rolling with \r to overwrite the line
            time.sleep(0.25) if fastRoll == 'n' else time.sleep(0.05) # slow down animation if fastRoll is not 'y' else faster animation
        roll1 = random.randint(1, size) # get current roll for player 1/bot
        roll2 = random.randint(1, size) # get current roll for player 2
        rollTotal1 += (roll1 + difficulty) if roll1 + difficulty > 0 else 0 # adds random roll to roll1 total for player 1/bot and take into account difficulty and will ignore negative rolls
        print(f"\nRoll {i + 1}: \n{'Bot' if choice == 'bot' else 'Player 1'} rolled: {roll1 + difficulty if roll1 + difficulty > 0 else 0} {'(' if difficulty != 0 else ''}{roll1 if difficulty != 0 else ''} {'-' if difficulty < 0 else '+' if difficulty > 0 else ''}{' ' if difficulty != 0 else ''}{abs(difficulty) if difficulty != 0 else ''} {'=' if difficulty != 0 else ''} {roll1 + difficulty if difficulty != 0 else ''}{')' if difficulty != 0 else ''}") # prints player 2s score and change from difficulty if necessary
        rollTotal2 += roll2 # adds random roll to roll total for player 2
        time.sleep(0.25) if fastRoll == 'n' else time.sleep(0.05) # slow down animation if fastRoll is not 'y' else faster animation
        print(f"You rolled: {roll2}")
        time.sleep(0.25) if fastRoll == 'n' else time.sleep(0.05) # slow down animation if fastRoll is not 'y' else faster animation
        print(f"\n{roll2} vs {rollTotal1}\n") # show individual rolls
        time.sleep(0.5) if fastRoll == 'n' else time.sleep(0.05) # slow down animation if fastRoll is not 'y' else faster animation
    
    time.sleep(0.75) # pause before showing totals
    return rollTotal1, rollTotal2 # returns total of 3 rolls for each player

def menu(choice, guestMode, username): # prints menu and returns what u pick (tree style)
    if choice == 'menu': # prints menu if u pick menu
        choice = int(input(f'{"=" * width}            (Signed in as: {username if not guestMode else "Guest"})\n{"MENU".center(width)}\n{"=" * width}\n1) View stats\n2) Start match \n3) Sign out\n\n')) # returns what u pick
        os.system('cls') # clears terminal
        return choice
    elif choice == 'match': # prints match menu if u pick match
        choice = int(input(f'{"=" * width}\n{"START".center(width)}\n{"=" * width}\n1) Bot\n2) Person\n\n')) # returns what u pick
        os.system('cls') # clears terminal
        return choice
    elif choice == 'bot': # prints bot menu if u pick bot
        choice = int(input(f'{"=" * width}\n{"DIFFICULTY".center(width)}\n{"=" * width}\n1) Easy\n2) Medium\n3) Hard\n4) Expert\n\n')) # returns what u pick
        os.system('cls') # clears terminal
        return choice
    elif choice == 'home': # prints home menu if u pick home
        choice = int(input(f'\n{"=" * width}\n{"HOME".center(width)}\n{"=" * width}\n\n1) Login\n2) Create account\n3) Guest\n\n')) # returns what u pick
        os.system('cls') # clears terminal
        return choice

def match(choice, difficulty, username, guestMode):  # add username parameter

    scores = {'player1': 0, 'player2': 0} # creates scores dict

    fastRoll = input('Fast roll? (y/n): ').lower()

    for i in range(5): # runs 5 rounds
        time.sleep(0.25)
        print(f"\nRound {i+1}\n".center(width)) # prints round number
        time.sleep(0.25)
        playRound(difficulty, choice, scores, fastRoll) # plays a round
    
    time.sleep(0.75) # pause before showing final scores

    print("\n" + "Final Scores:".center(width))
    time.sleep(0.25)
    print("="*width)
    time.sleep(0.25)
    print(f"You: {scores['player2']} points!".center(width))
    time.sleep(0.25)
    print(f"{'Bot' if choice == 'bot' else 'Player 1'}: {scores['player1']} points!".center(width))
    time.sleep(0.25)
    print("="*width)

    time.sleep(0.5) # pause before showing winner

    if scores['player1'] > scores['player2']:
        print(f"\n{'Bot' if choice == 'bot' else 'Player 1'} wins the game!\n")
        if not guestMode:  # Only update stats if not in guest mode
            userData = loadUsers()
            userData['users'][username]['stats']['totalGames'] += 1
            userData['users'][username]['stats']['losses'] += 1
            if choice == 'bot':
                difficultyString = getDifficultyString(difficulty)
                userData['users'][username]['stats']['vsBot'][difficultyString]['losses'] += 1
            else:
                userData['users'][username]['stats']['vsPlayer']['losses'] += 1
            saveUsers(userData)
    elif scores['player1'] < scores['player2']:
        print("\nYou win the game!\n".center(width))
        print("              .-=========-.")  # trophy ascii art
        print("              \\'-=======-'/")
        print("              _|   .=.   |_")
        print("             ((|  {{1}}  |))")
        print("              \\|   /|\\   |/")
        print("               \\__ '`' __/")
        print("                 _`) (`_")
        print("               _/_______\\_")
        print("              /___________\\\n")
        
        if not guestMode:  # Only update stats if not in guest mode
            userData = loadUsers()
            userData['users'][username]['stats']['totalGames'] += 1
            userData['users'][username]['stats']['wins'] += 1
            if choice == 'bot':
                difficultyString = getDifficultyString(difficulty)
                userData['users'][username]['stats']['vsBot'][difficultyString]['wins'] += 1
            else:
                userData['users'][username]['stats']['vsPlayer']['wins'] += 1
            saveUsers(userData)
        input('Press Enter to return to menu... ')
        os.system('cls')
        menuHandler(guestMode, username)
    else:
        print("\nIt's a tie!") # wont happen bc 5 rounds and tie is impossible
        if not guestMode:  # Only update stats if not in guest mode
            userData = loadUsers()
            userData['users'][username]['stats']['totalGames'] += 1 # adds 1 to total games (maybe shouldnt be here but idk bc it will add 1 to total games for every tie but its the same match just rerolled)
            userData['users'][username]['stats']['draws'] += 1 # adds 1 to draws
            saveUsers(userData)
        for x in range(4): # cool '...' animation
            print(f'Restarting match{"." * x}', end='\r') # prints rolling with \r to overwrite the line
            time.sleep(0.25) # slow down animation
        match(choice, difficulty, username, guestMode) # recursive call to match function to play again if tie

def menuHandler(guestMode, username): # defines menuHandler function that deals with the menu
    choice = menu('menu', guestMode, username) # show main menu
    if choice == 1 and not guestMode: # user chose to view stats and is not guest
        if viewUserStats(username): # use viewUserStats function to view stats
            input('Press Enter to return to menu... ')
            os.system('cls') # clears screen
            menuHandler(guestMode, username) # recursive call to menuHandler function to return to menu
    elif choice == 1 and guestMode: # user chose to view stats and is guest
        print('Guest mode does not have stats!\nSign in for more features!'.center(width)) # prints guest mode does not have stats message
        time.sleep(2)
        os.system('cls')
        menuHandler(guestMode, username)
    elif choice == 2: # user chose to start match
        choice = menu('match', guestMode, username) # show match menu
        if choice == 1: # user chose to play with bot
            choice = menu('bot', guestMode, username) # show bot menu
            if choice == 1: # user chose easy
                match('bot', -2, username, guestMode) # use match function to start match with bot and difficulty (-2 is point reduction)
            elif choice == 2: # user chose medium
                match('bot', -1, username, guestMode) # use match function to start match with bot and difficulty (-1 is point reduction)
            elif choice == 3: # user chose hard
                match('bot', 0, username, guestMode) # use match function to start match with bot and difficulty (0 is no point reduction)
            elif choice == 4: # user chose expert
                match('bot', 1, username, guestMode) # use match function to start match with bot and difficulty (1 is point increase)
        elif choice == 2: # user chose to play with other player
            match('person', 0, username, guestMode) # use match function to start match with other player with no point reduction
    elif choice == 3: # user chose to sign out
        for i in range(4): # cool '...' animation (for loop)
            print(f'Signing out{"." * i}', end='\r') # end='\r' is to overwrite the line to append the next '.' to signing out message
            time.sleep(0.4) # time.sleep(0.4) is to slow down the animation
        os.system('cls')
        print('Signed out!\n') # prints signed out after the animation
        for i in range(4): # cool '...' animation (for loop)
            print(f'Returning to home screen{"." * i}', end='\r') 
            time.sleep(0.4) # time.sleep(0.4) is to slow down the animation
        time.sleep(0.6) # waits 1 second before closing
        os.system('cls') # clear screen before returning to home screen
        homeScreen() # calls homeScreen function to return to home screen, only choices are to login, create account, or guest which will overwrite current login session



# ------ MAIN ------ #

os.system('cls')
homeScreen() # runs homeScreen function for first time users

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
        