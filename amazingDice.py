# ------ MODULES ------ #

import random  # imports random module for dice rolls
import time  # imports time module for delays and animations
import json  # imports json module for user data storage
import os  # imports os module for file operations
import hashlib  # imports hashlib module for password hashing
import amazingDiceGUI as adGUI  # imports GUI module

# ------ GLOBAL VARIABLES ------ #

width = 40  # width for text centering in console output

# ------ FILE STUFF ------ #

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # changes to scripts directory for file operations

# ------ USER DATA FUNCTIONS ------ #

def hashPassword(password):  # defines function to hash passwords using SHA256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()  # returns hashed password as hexadecimal string

def loadUsers():  # defines function to load user data from JSON file
    try:
        with open('userLoginInfo.json', 'r') as file:  # attempts to open user data file
            return json.load(file)  # returns user data as dictionary
    except FileNotFoundError:  # handles case where file doesnt exist
        print("Warning User data file not found Creating temporary user structure")  # prints warning message
        return {"users": {}}  # returns empty user structure
    except PermissionError:  # handles case where file cant be accessed
        print("Error Cannot access user data file Creating temporary user structure")  # prints error message
        return {"users": {}}  # returns empty user structure
    except json.JSONDecodeError:  # handles case where file is corrupted
        print("Error User data file is corrupted Creating temporary user structure")  # prints error message
        return {"users": {}}  # returns empty user structure

def saveUsers(data):  # defines function to save user data to JSON file
    try:
        with open('userLoginInfo.json', 'w') as file:  # opens file in write mode
            json.dump(data, file, indent=4)  # writes data to file with formatting
    except PermissionError:  # handles case where file cant be written
        print("Error Cannot save user data Check file permissions")  # prints error message

def addNewUser(username, password):  # defines function to add new user to system
    data = loadUsers()  # loads current user data
    
    if username in data['users']:  # checks if username already exists
        print("Username already exists")  # prints error message
        return False  # returns False if username exists
    
    data['users'][username] = {  # creates new user entry
        "hashedPassword": hashPassword(password),  # stores hashed password
        "joinDate": time.strftime("%d/%m/%Y"),  # stores join date in UK format
        "stats": {  # initializes user statistics
            "totalGames": 0,  # total games played
            "wins": 0,  # total wins
            "losses": 0,  # total losses
            "draws": 0,  # total draws
            "vsBot": {  # stats for bot matches
                "easy": {  # easy difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "medium": {  # medium difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "hard": {  # hard difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "expert": {  # expert difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                }
            },
            "vsPlayer": {  # stats for player vs player matches
                "wins": 0,
                "losses": 0,
                "draws": 0
            }
        }
    }
    
    saveUsers(data)  # saves updated user data
    print(f"\nUser {username} created successfully\n")  # prints success message
    return True  # returns True if user created successfully

def getStats(username):  # defines function to get user statistics
    data = loadUsers()  # loads user data
    stats = data['users'][username]['stats']  # gets users stats
    return stats  # returns stats dictionary

def login(username, password):  # defines function to handle user login
    userData = loadUsers()  # loads user data
    print('loaded user data')  # prints debug message
    
    if username in userData['users']:  # checks if username exists
        if userData['users'][username]['hashedPassword'] == hashPassword(password):  # checks if password is correct
            return username  # returns username if login successful
        else:
            print("Incorrect password")  # prints error for wrong password
            return False  # returns False for failed login
    else:
        print("Username not found")  # prints error for missing username
        return False  # returns False for failed login

def createAccount(username, password):  # defines function to create new account
    userData = loadUsers()  # loads user data
    if username in userData['users']:  # checks if username exists
        print('Username already exists\nTry a different username')  # prints error message
        createAccount(username, password)  # recursively tries again
    while not (len(password) >= 12 and  # checks password requirements
              any(c.isdigit() for c in password) and  # must have number
              any(c.isupper() for c in password) and  # must have uppercase
              any(c.islower() for c in password) and  # must have lowercase
              any(c in r'!#$%&()*+,-./:;<=>?@[]^_`{|}~\'"' for c in password)):  # must have special character
        print("Password must be at least 12 characters and contain uppercase lowercase numbers and special characters")  # prints requirements
    if addNewUser(username, password):  # attempts to add new user
        print(f"Account created successfully Welcome {username}")  # prints success message
        return username  # returns username if successful

# ------ GAME FUNCTIONS ------ #

def getDifficultyString(difficulty):  # defines function to convert difficulty number to string
    if difficulty == -2:  # easy difficulty
        return "easy"
    elif difficulty == -1:  # medium difficulty
        return "medium"
    elif difficulty == 0:  # hard difficulty
        return "hard"
    elif difficulty == 1:  # expert difficulty
        return "expert"
    return "hard"  # default fallback

def homeScreen():  # defines function to display home screen
    choice = menu('home', None, None)  # shows home menu
    if choice == 1:  # user chose login
        menuHandler(False, login())  # handles login process
    elif choice == 2:  # user chose create account
        menuHandler(False, createAccount())  # handles account creation
    elif choice == 3:  # user chose guest mode
        print(f'{"="*width}\n{"Guest mode enabled".center(width)}\n{"="*width}\n')  # prints guest mode message
        time.sleep(1)  # pauses for effect
        os.system('cls')  # clears screen
        menuHandler(True, None)  # starts guest mode

def playRound(difficulty, choice, scores, fastRoll):  # defines function to play one round
    rollTotal1, rollTotal2 = diceRoll(6, difficulty, choice, fastRoll)  # rolls dice for both players
    print(f"\nYour total roll {rollTotal2}")  # prints player 2s total
    print(f"{'Bot' if choice == 'bot' else 'Player 1'}s total roll {rollTotal1}")  # prints player 1s total
    
    if rollTotal1 > rollTotal2:  # player 1 wins
        scores['player1'] += 1  # increments player 1s score
        print(f"{'Bot' if choice == 'bot' else 'Player 1'} wins this round")  # prints winner
    elif rollTotal1 < rollTotal2:  # player 2 wins
        scores['player2'] += 1  # increments player 2s score
        print("You win this round")  # prints winner
    else:  # draw
        print("Draw Rolling again\n")  # prints draw message
        time.sleep(0.5)  # pauses before reroll
        playRound(difficulty, choice, scores, fastRoll)  # plays round again

def diceRoll(size, difficulty, choice, fastRoll):  # defines function to handle dice rolling
    rollTotal1, rollTotal2 = 0, 0  # initializes roll totals
    
    for i in range(3):  # rolls dice 3 times
        for x in range(4):  # animation loop
            print(f'Rolling{"." * x}', end='\r')  # prints rolling animation
            time.sleep(0.25) if fastRoll == 'n' else time.sleep(0.05)  # controls animation speed
            
        roll1 = random.randint(1, size)  # gets random roll for player 1
        roll2 = random.randint(1, size)  # gets random roll for player 2
        
        rollTotal1 += (roll1 + difficulty) if roll1 + difficulty > 0 else 0  # adds roll to total with difficulty modifier
        print(f"\nRoll {i + 1} \n{'Bot' if choice == 'bot' else 'Player 1'} rolled {roll1 + difficulty if roll1 + difficulty > 0 else 0} {'(' if difficulty != 0 else ''}{roll1 if difficulty != 0 else ''} {'-' if difficulty < 0 else '+' if difficulty > 0 else ''}{' ' if difficulty != 0 else ''}{abs(difficulty) if difficulty != 0 else ''} {'=' if difficulty != 0 else ''} {roll1 + difficulty if difficulty != 0 else ''}{')' if difficulty != 0 else ''}")  # prints roll details
        
        rollTotal2 += roll2  # adds roll to player 2s total
        time.sleep(0.25) if fastRoll == 'n' else time.sleep(0.05)  # controls display timing
        print(f"You rolled {roll2}")  # prints player 2s roll
        
        time.sleep(0.25) if fastRoll == 'n' else time.sleep(0.05)  # controls display timing
        print(f"\n{roll2} vs {rollTotal1}\n")  # shows current totals
        time.sleep(0.5) if fastRoll == 'n' else time.sleep(0.05)  # controls display timing
    
    time.sleep(0.75)  # pauses before showing final totals
    return rollTotal1, rollTotal2  # returns both totals

def menu(choice, guestMode, username):  # defines function to display menus
    if choice == 'menu':  # main menu
        choice = int(input(f'{"=" * width}            (Signed in as {username if not guestMode else "Guest"})\n{"MENU".center(width)}\n{"=" * width}\n1) View stats\n2) Start match \n3) Sign out\n\n'))  # shows menu options
        os.system('cls')  # clears screen
        return choice  # returns users choice
    elif choice == 'match':  # match menu
        choice = int(input(f'{"=" * width}\n{"START".center(width)}\n{"=" * width}\n1) Bot\n2) Person\n\n'))  # shows match options
        os.system('cls')  # clears screen
        return choice  # returns users choice
    elif choice == 'bot':  # bot difficulty menu
        choice = int(input(f'{"=" * width}\n{"DIFFICULTY".center(width)}\n{"=" * width}\n1) Easy\n2) Medium\n3) Hard\n4) Expert\n\n'))  # shows difficulty options
        os.system('cls')  # clears screen
        return choice  # returns users choice
    elif choice == 'home':  # home menu
        choice = int(input(f'\n{"=" * width}\n{"HOME".center(width)}\n{"=" * width}\n\n1) Login\n2) Create account\n3) Guest\n\n'))  # shows home options
        os.system('cls')  # clears screen
        return choice  # returns users choice

def match(choice, difficulty, username, guestMode):  # defines function to handle a match

    scores = {'player1': 0, 'player2': 0}  # initializes score dictionary

    fastRoll = input('Fast roll (y/n) ').lower()  # gets fast roll preference

    for i in range(5):  # plays 5 rounds
        time.sleep(0.25)  # pauses between rounds
        print(f"\nRound {i+1}\n".center(width))  # prints round number
        time.sleep(0.25)  # pauses for effect
        playRound(difficulty, choice, scores, fastRoll)  # plays one round
    
    time.sleep(0.75)  # pauses before showing final scores

    print("\n" + "Final Scores".center(width))  # prints final scores header
    time.sleep(0.25)  # pauses for effect
    print("="*width)  # prints separator
    time.sleep(0.25)  # pauses for effect
    print(f"You {scores['player2']} points".center(width))  # prints player 2s score
    time.sleep(0.25)  # pauses for effect
    print(f"{'Bot' if choice == 'bot' else 'Player 1'} {scores['player1']} points".center(width))  # prints player 1s score
    time.sleep(0.25)  # pauses for effect
    print("="*width)  # prints separator

    time.sleep(0.5)  # pauses before showing winner

    if scores['player1'] > scores['player2']:  # player 1 wins
        print(f"\n{'Bot' if choice == 'bot' else 'Player 1'} wins the game\n")  # prints winner
        if not guestMode:  # updates stats if not in guest mode
            userData = loadUsers()  # loads user data
            userData['users'][username]['stats']['totalGames'] += 1  # increments total games
            userData['users'][username]['stats']['losses'] += 1  # increments losses
            if choice == 'bot':  # updates bot stats
                difficultyString = getDifficultyString(difficulty)  # gets difficulty string
                userData['users'][username]['stats']['vsBot'][difficultyString]['losses'] += 1  # increments bot losses
            else:  # updates player stats
                userData['users'][username]['stats']['vsPlayer']['losses'] += 1  # increments player losses
            saveUsers(userData)  # saves updated stats
    elif scores['player1'] < scores['player2']:  # player 2 wins
        print("\nYou win the game\n".center(width))  # prints winner message
        print("              .-=========-")  # prints trophy ASCII art
        print("              \\'-=======-'/")
        print("              _|   .=.   |_")
        print("             ((|  {{1}}  |))")
        print("              \\|   /|\\   |/")
        print("               \\__ '`' __/")
        print("                 _`) (`_")
        print("               _/_______\\_")
        print("              /___________\\\n")
        
        if not guestMode:  # updates stats if not in guest mode
            userData = loadUsers()  # loads user data
            userData['users'][username]['stats']['totalGames'] += 1  # increments total games
            userData['users'][username]['stats']['wins'] += 1  # increments wins
            if choice == 'bot':  # updates bot stats
                difficultyString = getDifficultyString(difficulty)  # gets difficulty string
                userData['users'][username]['stats']['vsBot'][difficultyString]['wins'] += 1  # increments bot wins
            else:  # updates player stats
                userData['users'][username]['stats']['vsPlayer']['wins'] += 1  # increments player wins
            saveUsers(userData)  # saves updated stats
        input('Press Enter to return to menu ')  # waits for user input
        os.system('cls')  # clears screen
        menuHandler(guestMode, username)  # returns to menu
    else:  # draw shouldnt happen with 5 rounds
        print("\nIts a tie")  # prints tie message
        if not guestMode:  # updates stats if not in guest mode
            userData = loadUsers()  # loads user data
            userData['users'][username]['stats']['totalGames'] += 1  # increments total games
            userData['users'][username]['stats']['draws'] += 1  # increments draws
            saveUsers(userData)  # saves updated stats
        for x in range(4):  # restart animation
            print(f'Restarting match{"." * x}', end='\r')  # prints animation
            time.sleep(0.25)  # controls animation speed
        match(choice, difficulty, username, guestMode)  # restarts match

def menuHandler(guestMode, username):  # defines function to handle menu navigation
    choice = menu('menu', guestMode, username)  # shows main menu
    if choice == 2:  # user chose start match
        choice = menu('match', guestMode, username)  # shows match menu
        if choice == 1:  # user chose bot match
            choice = menu('bot', guestMode, username)  # shows bot menu
            if choice == 1:  # user chose easy difficulty
                match('bot', -2, username, guestMode)  # starts easy bot match
            elif choice == 2:  # user chose medium difficulty
                match('bot', -1, username, guestMode)  # starts medium bot match
            elif choice == 3:  # user chose hard difficulty
                match('bot', 0, username, guestMode)  # starts hard bot match
            elif choice == 4:  # user chose expert difficulty
                match('bot', 1, username, guestMode)  # starts expert bot match
        elif choice == 2:  # user chose player match
            match('person', 0, username, guestMode)  # starts player vs player match
    elif choice == 3:  # user chose sign out
        for i in range(4):  # sign out animation
            print(f'Signing out{"." * i}', end='\r')  # prints animation
            time.sleep(0.4)  # controls animation speed
        os.system('cls')  # clears screen
        print('Signed out\n')  # prints signed out message
        for i in range(4):  # return animation
            print(f'Returning to home screen{"." * i}', end='\r')  # prints animation
            time.sleep(0.4)  # controls animation speed
        time.sleep(0.6)  # pauses before clearing
        os.system('cls')  # clears screen
        homeScreen()  # returns to home screen

# ------ MAIN ------ #

if __name__ == "__main__":  # checks if file is being run directly
    adGUI.home()  # starts GUI application

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
        