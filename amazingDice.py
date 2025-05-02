# ------ MODULES ------ #

import random  # imports random module for dice rolls
import time  # imports time module for delays and animations
import json  # imports json module for user data storage
import os  # imports os module for file operations
import hashlib  # imports hashlib module for password hashing
import amazingDiceGUI as adGUI  # imports GUI module
import keyring

# MARK: - FILE STUFF

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # changes to scripts directory for file operations (FUTURE ME DOESNT UNDERSTAND WHAT)

# MARK: - USER DATA FUNCTIONS

def checkLogin(username, hashedPassword):
    data = loadUsers()
    if username in data['users']:
        if data['users'][username]['hashedPassword'] == hashedPassword:
            return True
    return False

# MARK: - LOAD LAST LOGGED

def loadLastLogged():
    try:
        with open('lastedLogged.json', 'r') as file:
            return json.load(file)
    except:
        return {"savedLogins": {}}

# MARK: - SAVE LOGIN

def saveLogin(username, password, remember=True):
    # If remember is False, delete any saved credentials
    if not remember:
        try:
            # Delete the saved password for this username
            keyring.delete_password("AmazingDice", username)
            
            # Delete the record of who was the last logged in user
            keyring.delete_password("AmazingDice", "lastUser")

        except:
            # Print error if deletion fails (but don't disrupt program flow)
            print('Error removing saved login')
        return
    
    try:
        # Store the actual password (not hashed) securely in Windows Credential Manager
        # "AmazingDice" is the service name (identifies our application)
        # username is the key under which we store the password
        keyring.set_password("AmazingDice", username, password)
        
        # Also store which user was last logged in
        # This helps us know whose credentials to retrieve on startup
        keyring.set_password("AmazingDice", "lastUser", username)
        
    except:
        print("error saving login")

# MARK: - CHECK SAVED LOGIN

def checkSavedLogin():
    try:
        # First retrieve the username of the last logged in user
        username = keyring.get_password("AmazingDice", "lastUser")
        
        # If we found a last logged in user
        if username:
            try:
                # Get their saved password from the credential manager
                password = keyring.get_password("AmazingDice", username)
                
                # If we found a password
                if password:
                    # Return success along with the username and the hashed version of the password
                    # (hashing here because other functions expect the hashed version)
                    return True, username, hashPassword(password)
            except Exception as e:
                print(f"Error retrieving password: {e}")
    except Exception as e:
        # Print error if retrieval fails
        print(f"Error checking saved login: {e}")
    
    # Return default values if no saved login was found or an error occurred
    return False, None, None

# MARK: - CHECK PASSWORD

def checkPassword(username, password):
    data = loadUsers()
    if username in data['users']:
        if data['users'][username]['hashedPassword'] == hashPassword(password):
            return True
    return False

# MARK: - HASH PASSWORD

def hashPassword(password):  # defines function to hash passwords using SHA256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()  # returns password as hashed version ig idk

# MARK: - LOAD USERS

def loadUsers():  # defines function to load user data from JSON file
    try:
        with open('userInfo.json', 'r') as file:
            return json.load(file)
    except:
        print("error loading users")
        return {"users": {}}

# MARK: - SAVE USERS

def saveUsers(data):  # defines function to save user data to JSON file
    try:
        with open('userInfo.json', 'w') as file:
            json.dump(data, file, indent=4)
    except:
        print("error saving users")

# MARK: - ADD NEW USER

def addNewUser(username, password):  # defines function to add new user to system
    data = loadUsers()  # loads current user data
    
    if username in data['users']:  # checks if username already exists
        print("Username already exists")  # prints error message
        return False  # returns False if username exists
    
    data['users'][username] = {  # creates new user entry
        "hashedPassword": hashPassword(password),  # stores hashed password
        "joinDate": time.strftime("%d/%m/%Y"),  # stores join date in basic format
        "coins": 0,
        "stats": {  # initializes user statistics
            "netWorth": 0,
            "totalGames": 0,  # total games played
            "wins": 0,  # total wins
            "losses": 0,  # total losses
            "draws": 0,  # total draws
            "vsBot": {  # stats for bot matches
                "Easy": {  # easy difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "Medium": {  # medium difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "Hard": {  # hard difficulty stats
                    "wins": 0, 
                    "losses": 0, 
                    "draws": 0
                },
                "Expert": {  # expert difficulty stats
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
        },
        "achievements": [],  # initializes empty achievements list
        "achievementProgress": {  # initializes achievement progress
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "totalGames": 0,
            "consecutiveWins": 0,
            "consecutiveLosses": 0,
            "perfectScore": 0,
            "sweepGame": 0,
            "loseByOne": 0,
            "gamesPlayed": 0
        }
    }
    
    saveUsers(data)  # saves updated user data
    print(f"\nUser {username} created successfully\n")  # prints success message
    return True  # returns True if user created successfully

# MARK: - CREATE ACCOUNT

def createAccount(username, password):  # defines function to create new account
    if addNewUser(username, password):  # attempts to create account
        return True  # returns gud
    else:
        return False  # returns bad

# MARK: - GET COINS

def getCoins(username):
    data = loadUsers()
    return data['users'][username]['coins']

# MARK: - GET STATS

def getStats(username):  # defines function to get user statistics
    data = loadUsers()  # loads user data
    stats = data['users'][username]['stats']  # gets users stats
    return stats  # returns stats dictionary

# MARK: - EDIT USER FUNCTION

def editUser(username, newPassword):
    userData = loadUsers()
    if userData['users'][username]['hashedPassword'] == hashPassword(newPassword): # ITS THE SAMEE AAA
        return 'You must use a different password to your current password!', False
    else: # different
        userData['users'][username]['hashedPassword'] = hashPassword(newPassword) # change
        saveUsers(userData)
        return 'Success! Password changed.', True

# MARK: - LOGIN FUNCTION

def login(username, password):  # defines function to verify login credentials
    data = loadUsers()  # loads user data
    if username in data['users']:  # checks if username exists
        if data['users'][username]['hashedPassword'] == hashPassword(password):  # checks if password matches
            return True  # returns True if credentials are valid
    return False  # returns False if either username doesn't exist or password is wrong

# MARK: - LOAD USER SETTINGS

def loadUserSettings(): # create function to load user settings from userSettings.json and return it as dictionary
    try:
        with open('userSettings.json', 'r') as file: # try to open userSettings.json
            return json.load(file) # return settings
    except:
        print("error loading settings")
        return {"users": {}} # return empty dictionary if error

# MARK: - SAVE ALL SETTINGS

def saveAllUserSettings(userData):
    try:
        with open('userSettings.json', 'w') as file:
            json.dump(userData, file, indent=4)
    except:
        print("error saving settings")

# MARK: - GET USER SETTINGS

def getUserSettings(username):
    userData = loadUserSettings() # loads all settings
    if username in userData['users']: # if username is stored in settings
        return userData['users'][username] # return settings
    # Return default settings if user has no settings saved
    return {'fastRoll': False, 'theme': 'light'} # return default settings if user has no settings saved

# MARK: - SAVE USER SETTINGS

# ts is complex so ima explain:i
# saveUserSettings is called when the user changes a setting with settings var being the changed setting, eg fastRoll = True
# when it needs to be saved it gets all the settings then edits the one that was changed
# saveAllUserSettings is called when this ^^^ is done
# all that does is dump the userData into the file

def saveUserSettings(username, settings): # create function to save user settings to username
    userData = loadUserSettings() # gets all settings
    userData['users'][username] = settings # saves settings to username
    saveAllUserSettings(userData) # saves all settings to file

# MARK: - DICE ROLL

def diceRoll(size, difficulty):
    return random.randint(1,size) + difficulty # THIS FUNCTUIOIN DOESNT MATTER ITS SO SHORT AND DUMB

# MARK: - PLAY ROUND

def playRound(size, difficulty):
    startRoll1, startRoll2 = 0,0 # set to same defaul ig idk INITIALISE THATS THE WORKD
    while startRoll1 == startRoll2: # IF EQUAL SO DRAWS (IKTS NOT WHILE TRUE YAAAAYAYAYA) <- EXTRA POINTS FOR THAT PLS 🙏🙏🙏🙏
        startRoll1, startRoll2 = diceRoll(size, 0), diceRoll(size, difficulty) # ROLS FOR IRSTR THIS IS DUMB WHO CARES WHO;S FIRST AAA
    rolls1, rolls2 = [], [] # INITISALKISE
    for i in range(0, 3): # 3 rolls each
        rolls1.append(diceRoll(size, 0)) # roll for player 1
        rolls2.append(diceRoll(size, difficulty)) # roll for player 2, difficulty included as bots can only be player 2
    return rolls1, rolls2, sum(rolls1), sum(rolls2), startRoll1 > startRoll2, startRoll1, startRoll2

# MARK: - DIFFICULTY INT

def getDifficultyInt(difficulty):  # defines function to convert difficulty int to string
    # ok hi i changed the difficulty yay but i dont care that its not an int ima keep the name haahahahahahha get bozod mr scott
    if difficulty == 'Easy':
        return -1
    elif difficulty == 'Medium':
        return -0.5
    elif difficulty == 'Hard':
        return 0
    else:
        return 0.5

# MARK: - START FUNCTION

def start():
    hasSavedLogin, username, hashedPassword = checkSavedLogin() # get username and hashed password from saved login or returns False, None, None if no saved login
    if hasSavedLogin:  # if there is a saved login
        if checkLogin(username, hashedPassword): # checks if saved login is valid, eg pasword changed but not saved 
            adGUI.login(username, hashedPassword) # open login with saved login and settings
    else:
        adGUI.home() # open home if no saved login for default behaviour

# MARK: - GET ACHIEVEMENTS

def getAchievements(username):
    data = loadUsers()
    if 'achievements' in data['users'][username]:
        return data['users'][username]['achievements']
    return []

def getDifficultyNumString(difficulty):
    if difficulty == 'Easy':
        return '- 1'
    elif difficulty == 'Medium':
        return '- 0.5'
    elif difficulty == 'Hard':
        return ''
    else:
        return '+ 0.5'

# MARK: - LOAD ACHIEVEMENTS

def loadAchievements():
    try:
        with open('achievements.json', 'r') as file:
            return json.load(file)
    except:
        print("error loading achievements")
        return {"achievements": {}}

# MARK: - CHECK ACHIEVEMENT

def checkAchievement(username, achievementType, value=1):
    userData = loadUsers()
    allAchievements = loadAchievements()
    
    # Initialize achievements array if not exists
    if 'achievements' not in userData['users'][username]:
        userData['users'][username]['achievements'] = []
    
    # Initialize achievement progress if not exists
    if 'achievementProgress' not in userData['users'][username]:
        userData['users'][username]['achievementProgress'] = {}
    
    # Get current achievements and progress
    userAchievements = userData['users'][username]['achievements']
    userProgress = userData['users'][username]['achievementProgress']
    
    # Initialize progress for this type if not exists
    if achievementType not in userProgress:
        userProgress[achievementType] = 0
    
    # Update progress for the achievement type
    if achievementType in ['consecutiveWins', 'consecutiveLosses']:
        # These are special cases that need to be reset sometimes
        if achievementType == 'consecutiveWins' and value > 0:
            userProgress[achievementType] += 1
            userProgress['consecutiveLosses'] = 0  # Reset lose streak
        elif achievementType == 'consecutiveLosses' and value > 0:
            userProgress[achievementType] += 1
            userProgress['consecutiveWins'] = 0  # Reset win streak
        else:
            userProgress[achievementType] = 0  # Reset if not incrementing
    else:
        # For most achievement types, just add the value
        userProgress[achievementType] += value
    
    # Check all achievements against progress
    newAchievements = []
    for achievementId, achievement in allAchievements['achievements'].items():
        # Skip already achieved ones
        alreadyAchieved = False
        for userAchievement in userAchievements:
            if userAchievement.get('id') == achievementId:
                alreadyAchieved = True
                break
        
        if alreadyAchieved:
            continue
        
        # Check if achievement is of the right type and requirement is met
        if achievement['type'] == achievementType and userProgress.get(achievementType, 0) >= achievement['requirement']:
            # Create new achievement object
            newAchievement = {
                'id': achievementId,
                'name': achievement['secretName'] if achievement['secret'] else achievement['name'],
                'description': achievement['secretDescription'] if achievement['secret'] else achievement['description'],
                'achieved': True,
                'date': time.strftime("%d/%m/%Y"),
                'progress': userProgress.get(achievementType, 0),
                'requirement': achievement['requirement']
            }
            userAchievements.append(newAchievement)
            newAchievements.append(newAchievement)
    
    # Save updated user data
    if newAchievements:
        userData['users'][username]['achievementProgress'] = userProgress
        userData['users'][username]['achievements'] = userAchievements
        saveUsers(userData)
    
    return newAchievements

# MARK: - MAIN

if __name__ == "__main__":  # checks if file is being run directly (not from import)
    start()  # starts it

# MAKE SAVED LOGIN SHOW UP AS LIKE AUTOCOMPLETE ON LOGIN SCREEN

# ONLINE:?????????????? NO I RAN OUT OF TIME I PROCRASTINATED THIS TILL THE LAST WEEK OOOPS

# self reminder: 'a' account is special testing account with password 'e' to save time logging in during MANY tests
# incase of password change during test, the hash of 'e' is , 3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea, to be directly added in userLoginInfo.json