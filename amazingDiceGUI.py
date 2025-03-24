# ------ IMPORTS ------ #
import customtkinter  # type: ignore # imports customtkinter library for modern GUI elements
from CTkTable import *
import amazingDice as ad  # imports main game logic file
from PIL import Image, ImageTk # use this for gif later aAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHGgg
import time

# ------ MATCH WINDOW FUNCTIONS ------ #

# ctk.set_appearance_mode('dark')

def settings():
    pass

def match(botOrNot, difficulty, username, username2):

    gameWindow = customtkinter.CTk()
    gameWindow.geometry('850x600')
    gameWindow.title('Amazing dice - Match')

    rollsList = [['Roll 1', 'Roll 2', 'Roll 3'],
                ['Player 1',0,0,0],
                ['Player 2',0,0,0]]

    rollTable = CTkTable(master=gameWindow, row=3, column=4, values=rollsList)
    rollTable.pack(expand=True, padx=15, pady=15) 

    infoLabel = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15), text_color='green')    
    infoLabel.pack(pady=10)

    player1TotalLabel = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15))
    player1TotalLabel.pack(pady=10)

    player2TotalLabel = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15))
    player2TotalLabel.pack(pady=10)

    def startPressed():
        for i in range(0, 5): # 5 rounds
            rolls1, rolls2, rollTotal1, rollTotal2, player1Starts = ad.playRound(6,ad.getDifficultyInt(difficulty) if botOrNot else 0)  # rolls 3 times and stores it in a list. gets the roll totals and gets who starts
            if player1Starts:
                infoLabel.configure(text='Rolling')
                time.sleep(1)
                infoLabel.configure(text='')
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', rolls1[0], '-', '-'], ['Player 2', '-', '-', '-']])
                infoLabel.configure(text='Rolling')
                time.sleep(1)
                infoLabel.configure(text='')
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', rolls1[0], rolls1[1]], ['Player 2', '-', '-', '-']])
                infoLabel.configure(text='Rolling')
                time.sleep(1)
                infoLabel.configure(text='')
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', rolls1[0], rolls1[1], rolls1[2]], ['Player 2', '-', '-', '-']])
            else:
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', '-', '-', '-'], ['Player 2', rolls1[0], '-', '-']])
                infoLabel.configure(text='Rolling')
                time.sleep(1)
                infoLabel.configure(text='')
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', '-', '-', '-'], ['Player 2', rolls1[0], rolls1[1]]])
                infoLabel.configure(text='Rolling')
                time.sleep(1)
                infoLabel.configure(text='')
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', '-', '-', '-'], ['Player 2  ', rolls1[0], rolls1[1], rolls1[2]]])
            player1TotalLabel.configure(text=f'{username if player1Starts else username2} rolled a total of {rollTotal1}!')
            if player1Starts:
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', rolls1[0], rolls1[1], rolls1[2]], ['Player 2', rolls1[0], '-', '-']])
                infoLabel.configure(text='Rolling')
                time.sleep(1)
                infoLabel.configure(text='')
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', rolls1[0], rolls1[1], rolls1[2]], ['Player 2', rolls1[0], rolls1[1], '-']])
                infoLabel.configure(text='Rolling')
                time.sleep(1)
                infoLabel.configure(text='')
                rollTable.configure(values=[['Roll 1', 'Roll 2', 'Roll3'], ['Player 1', rolls1[0], rolls1[1], rolls1[2]], ['Player 2  ', rolls1[0], rolls1[1], rolls1[2]]])
            player2TotalLabel.configure(text=f'{username2 if player1Starts else username} rolled a total of {rollTotal2}!')

            if (rollTotal1 > rollTotal2 and player1Starts) or (rollTotal1 < rollTotal2 and not player1Starts): # you win
                infoLabel.configure(text=f"{username if not botOrNot else 'You'} win{'s' if not botOrNot else ''}!")
            elif botOrNot: # if u lost and vs bot
                infoLabel.configure(text=f"You lost!", text_color='red')
            else:
                infoLabel.configure(text=f'{username2} wins!')


    startButton = customtkinter.CTkButton(gameWindow, text='Start', font=('Arial', 15), command=startPressed)
    startButton.pack(pady=10)

    gameWindow.mainloop()      

def pvp(username):
    print('hi')

def bot(username):
    botWindow = customtkinter.CTk()
    botWindow.geometry('850x600')
    botWindow.title('Amazing Dice - VS Bot')

    titleLabel = customtkinter.CTkLabel(botWindow, text='Choose bot difficulty!', font=('Arial Bold', 30))
    titleLabel.pack(pady=10)

    def easyPressed():
        botWindow.destroy()
        match(True, 'easy', username, 'bot')

    def mediumPressed():
        botWindow.destroy()
        match(True, 'medium', username, 'bot')

    def hardPressed():
        botWindow.destroy()
        match(True, 'hard', username, 'bot')

    def expertPressed():
        botWindow.destroy()
        match(True, 'expert', username, 'bot')    

    easyButton = customtkinter.CTkButton(botWindow, text='Easy', command=easyPressed)
    easyButton.pack(pady=10)

    mediumButton = customtkinter.CTkButton(botWindow, text='Medium', command=mediumPressed)
    mediumButton.pack(pady=10)

    hardButton = customtkinter.CTkButton(botWindow, text='Hard', command=hardPressed)
    hardButton.pack(pady=10)

    expertButton = customtkinter.CTkButton(botWindow, text='Expert', command=expertPressed)
    expertButton.pack(pady=10)

    botWindow.mainloop()

    
def matchWindow(username, guestMode):  # defines match window function that takes username and guest mode status
    matchWindow = customtkinter.CTk()  # creates new window
    matchWindow.geometry('850x600')  # sets window size to 600x500 pixels
    matchWindow.title('Amazing Dice - Match')  # sets window title

    titleLabel = customtkinter.CTkLabel(matchWindow, text="Match", font=('Arial Bold', 30))  # creates title label with large bold font
    titleLabel.pack(pady=10)  # adds padding and displays title

    accountLabel = customtkinter.CTkLabel(matchWindow, text=f'Signed in as: {username if not guestMode else "Guest"}', font=('Arial Bold', 15))  # creates account label showing current user
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right corner

    messageLabel = customtkinter.CTkLabel(matchWindow, text="", text_color="red")  # creates empty error message label in red
    messageLabel.pack(pady=10)  # adds padding and displays message label

    def backPressed():  # defines function for back button
        matchWindow.destroy()  # closes match window
        menu(guestMode, username)  # returns to menu

    def pvpPressed():
        if not guestMode:
            matchWindow.destroy()
            pvp(username)
        else:
            messageLabel.configure(text='Guests can only play against bots!')

    def botPressed():
        matchWindow.destroy() # make dropdown later w/ difficulties
        bot(username)

    botButton = customtkinter.CTkButton(matchWindow, text='VS Bot', command=botPressed)
    botButton.pack(pady=10)

    pvpButton = customtkinter.CTkButton(matchWindow, text='Vs Person', command=pvpPressed)
    pvpButton.pack(pady=10)   

    backButton = customtkinter.CTkButton(matchWindow, text='Back', command=backPressed)  # creates back button
    backButton.pack(pady=10)  # adds padding and displays back button



    matchWindow.mainloop()  # starts the window event loop

# ------ STATS WINDOW FUNCTIONS ------ #

def statsWindow(stats, username):  # defines stats window function that takes stats dictionary and username
    statsWindow = customtkinter.CTk()  # creates new window
    statsWindow.geometry('850x600')  # sets window size
    statsWindow.title('Amazing Dice - Stats')  # sets window title

    titleLabel = customtkinter.CTkLabel(statsWindow, text=f"Stats for {username}", font=('Arial Bold', 30))  # creates title with username
    titleLabel.pack(pady=10)  # displays title with padding

    accountLabel = customtkinter.CTkLabel(statsWindow, text=f'Signed in as: {username}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right

    scrollFrame = customtkinter.CTkScrollableFrame(statsWindow, width=500, height=400)  # creates scrollable frame for stats
    scrollFrame.pack(pady=10, padx=20, fill="both", expand=True)  # positions scrollable frame

    totalGamesLabel = customtkinter.CTkLabel(scrollFrame, text=f"Total Games: {stats['totalGames']}", font=('Arial Bold', 15))  # shows total games played
    totalGamesLabel.pack(pady=10)  # displays total games with padding

    overallLabel = customtkinter.CTkLabel(scrollFrame, text=f"Overall: {stats['wins']} Wins, {stats['losses']} Losses, {stats['draws']} Draws", font=('Arial Bold', 15))  # shows overall stats
    overallLabel.pack(pady=10)  # displays overall stats with padding

    vsBotLabel = customtkinter.CTkLabel(scrollFrame, text="Vs Bot", font=('Arial Bold', 20))  # creates bot section header
    vsBotLabel.pack(pady=10)  # displays bot header with padding

    for difficulty in ['easy', 'medium', 'hard', 'expert']:  # loops through each difficulty level
        botStats = stats['vsBot'][difficulty]  # gets stats for current difficulty
        botLabel = customtkinter.CTkLabel(scrollFrame, text=f"{difficulty.capitalize()}: {botStats['wins']} Wins, {botStats['losses']} Losses, {botStats['draws']} Draws", font=('Arial', 15))  # creates label for difficulty stats
        botLabel.pack(pady=5)  # displays difficulty stats with padding

    vsPlayerLabel = customtkinter.CTkLabel(scrollFrame, text="Vs Player", font=('Arial Bold', 20))  # creates player section header
    vsPlayerLabel.pack(pady=10)  # displays player header with padding

    vsPlayerStats = stats['vsPlayer']  # gets player vs player stats
    playerStatsLabel = customtkinter.CTkLabel(scrollFrame, text=f"Wins: {vsPlayerStats['wins']}, Losses: {vsPlayerStats['losses']}, Draws: {vsPlayerStats['draws']}", font=('Arial', 15))  # creates label for player stats
    playerStatsLabel.pack(pady=5)  # displays player stats with padding

    def backPressed():  # defines function for back button
        statsWindow.destroy()  # closes stats window
        menu(False, username)  # returns to menu

    backButton = customtkinter.CTkButton(statsWindow, text='Back', command=backPressed)  # creates back button
    backButton.pack(pady=10)  # displays back button with padding

    statsWindow.mainloop()  # starts the window event loop

# ------ MENU SCREEN FUNCTIONS ------ #

def menu(guestMode, username):  # defines menu window function that takes guest mode status and username
    menuWindow = customtkinter.CTk()  # creates new window
    menuWindow.geometry('850x600')  # sets window size
    menuWindow.title('Amazing Dice - Menu')  # sets window title

    titleLabel = customtkinter.CTkLabel(menuWindow, text="Menu", font=('Arial Bold', 30))  # creates menu title
    titleLabel.pack(pady=10)  # displays title with padding

    accountLabel = customtkinter.CTkLabel(menuWindow, text=f'Signed in as: {username if not guestMode else "Guest"}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right

    messageLabel = customtkinter.CTkLabel(menuWindow, text="", text_color="red")  # creates error message label
    messageLabel.pack(pady=10)  # displays message label with padding

    def statsPressed():  # defines function for stats button
        if not guestMode:  # checks if user is not in guest mode
            menuWindow.destroy()  # closes menu window
            statsWindow(ad.getStats(username), username)  # opens stats window
        else:
            messageLabel.configure(text="Guest mode does not have stats")  # shows error for guest mode

    def matchPressed():  # defines function for match button
        menuWindow.destroy()  # closes menu window
        matchWindow(username, guestMode)  # opens match window

    def signOutPressed():  # defines function for sign out button
        menuWindow.destroy()  # closes menu window
        home()  # returns to home screen

    def settingsPressed():
        menuWindow.destroy
        settings()

    statsButton = customtkinter.CTkButton(menuWindow, text='View Stats', command=statsPressed)  # creates stats button
    statsButton.pack(pady=10)  # displays stats button with padding

    matchButton = customtkinter.CTkButton(menuWindow, text='Match', command=matchPressed)  # creates match button
    matchButton.pack(pady=10)  # displays match button with padding

    settingsButton = customtkinter.CTkButton(menuWindow, text='Settings', command=settingsPressed)

    signOutButton = customtkinter.CTkButton(menuWindow, text='Sign Out', command=signOutPressed)  # creates sign out button
    signOutButton.pack(pady=10)  # displays sign out button with padding

    menuWindow.mainloop()  # starts the window event loop

# ------ LOGIN SCREEN FUNCTIONS ------ #

def login(loop):  # defines login window function that takes loop parameter
    if loop:  # checks if window should be destroyed for reloading
        loginWindow.destroy()  # destroys existing window

    loginWindow = customtkinter.CTk()  # creates new window
    loginWindow.geometry('850x600')  # sets window size
    loginWindow.title('Amazing Dice - Login')  # sets window title

    titleLabel = customtkinter.CTkLabel(loginWindow, text='Login to your account', font=('Arial Bold', 30))  # creates login title
    titleLabel.pack(pady=10)  # displays title with padding

    messageLabel = customtkinter.CTkLabel(loginWindow, text="", text_color="red")  # creates error message label
    messageLabel.pack(pady=10)  # displays message label with padding

    def backPressed():  # defines function for back button
        loginWindow.destroy()  # closes login window
        home()  # returns to home screen

    def onEnter(event):  # defines function for enter key press
        loginPress()  # triggers login button press

    def loginPress():  # defines function for login button
        username = usernameField.get()  # gets username from input field
        password = passwordField.get()  # gets password from input field
        
        if not username or not password:  # checks if fields are empty
            messageLabel.configure(text="Please fill in all fields")  # shows error for empty fields
            return  # exits function
            
        if ad.login(username, password):  # attempts to log in with credentials
            loginWindow.destroy()  # closes login window if successful
            menu(False, username)  # opens menu with logged in user
        else:
            messageLabel.configure(text="Login failed Check username and password")  # shows error for failed login

    usernameField = customtkinter.CTkEntry(loginWindow, placeholder_text='Enter username here', width=200, height=50)  # creates username input field
    usernameField.pack(pady=10)  # displays username field with padding
    usernameField.bind('<Return>', onEnter)  # binds enter key to login function

    passwordField = customtkinter.CTkEntry(loginWindow, placeholder_text='Enter password here', width=200, height=50, show='*')  # creates password input field with hidden text
    passwordField.pack(pady=10)  # displays password field with padding
    passwordField.bind('<Return>', onEnter)  # binds enter key to login function

    loginButton = customtkinter.CTkButton(loginWindow, text='Login', command=loginPress)  # creates login button
    loginButton.pack(pady=10)  # displays login button with padding

    backButton = customtkinter.CTkButton(loginWindow, text='Back', command=backPressed)  # creates back button
    backButton.pack(pady=10)  # displays back button with padding

    loginWindow.mainloop()  # starts the window event loop

# ------ CREATE ACCOUNT FUNCTIONS ------ #

def createAccountWindow(loop):  # defines create account window function that takes loop parameter
    if loop:  # checks if window should be destroyed for reloading
        createAccountWindow.destroy()  # destroys existing window

    createAccountWindow = customtkinter.CTk()  # creates new window
    createAccountWindow.geometry('850x600')  # sets window size
    createAccountWindow.title('Amazing Dice - Create Account')  # sets window title

    titleLabel = customtkinter.CTkLabel(createAccountWindow, text='Create your account', font=('Arial Bold', 30))  # creates title
    titleLabel.pack(pady=10)  # displays title with padding

    messageLabel = customtkinter.CTkLabel(createAccountWindow, text="", text_color="red")  # creates error message label
    messageLabel.pack(pady=10)  # displays message label with padding

    def backPressed():  # defines function for back button
        createAccountWindow.destroy()  # closes create account window
        home()  # returns to home screen

    def onEnter(event):  # defines function for enter key press
        createAccountPressed()  # triggers create account button press

    def createAccountPressed():  # defines function for create account button
        username = usernameField.get()  # gets username from input field
        password = passwordField.get()  # gets password from input field

        if not username or not password:  # checks if fields are empty
            messageLabel.configure(text="Please fill in all fields")  # shows error for empty fields
            return  # exits function

        if not (len(password) >= 12 and  # checks password requirements
              any(c.isdigit() for c in password) and  # must contain a number
              any(c.isupper() for c in password) and  # must contain uppercase
              any(c.islower() for c in password) and  # must contain lowercase
              any(c in r'!#$%&()*+,-./:;<=>?@[]^_`{|}~\'"' for c in password)):  # must contain special character
            messageLabel.configure(text="Password must be at least 12 characters and contain uppercase lowercase numbers and special characters")  # shows error for invalid password
            return  # exits function

        if ad.createAccount(username, password):  # attempts to create account
            createAccountWindow.destroy()  # closes window if successful
            menu(False, username)  # opens menu with new account

    usernameField = customtkinter.CTkEntry(createAccountWindow, placeholder_text='Enter username here', width=200, height=50)  # creates username input field
    usernameField.pack(pady=10)  # displays username field with padding
    usernameField.bind('<Return>', onEnter)  # binds enter key to create account function

    passwordField = customtkinter.CTkEntry(createAccountWindow, placeholder_text='Enter password here', width=200, height=50, show='*')  # creates password input field with hidden text
    passwordField.pack(pady=10)  # displays password field with padding
    passwordField.bind('<Return>', onEnter)  # binds enter key to create account function

    createAccountButton = customtkinter.CTkButton(createAccountWindow, text='Create Account', command=createAccountPressed)  # creates create account button
    createAccountButton.pack(pady=10)  # displays create account button with padding

    backButton = customtkinter.CTkButton(createAccountWindow, text='Back', command=backPressed)  # creates back button
    backButton.pack(pady=10)  # displays back button with padding

    createAccountWindow.mainloop()  # starts the window event loop

# ------ HOME SCREEN FUNCTIONS ------ #

def home():  # defines home window function
    homeWindow = customtkinter.CTk()  # creates new window
    homeWindow.geometry('850x600')  # sets window size
    homeWindow.title('Amazing Dice')  # sets window title

    titleLabel = customtkinter.CTkLabel(homeWindow, text='Welcome to Amazing Dice', font=('Arial Bold', 30))  # creates welcome title
    titleLabel.pack(pady=10)  # displays title with padding

    def loginPressed():  # defines function for login button
        homeWindow.destroy()  # closes home window
        login(False)  # opens login window

    def createAccountPressed():  # defines function for create account button
        homeWindow.destroy()  # closes home window
        createAccountWindow(False)  # opens create account window

    def guestPressed():  # defines function for guest mode button
        homeWindow.destroy()  # closes home window
        menu(True, 'Guest')  # opens menu in guest mode

    loginButton = customtkinter.CTkButton(homeWindow, text="Login", command=loginPressed)  # creates login button
    loginButton.pack(pady=10)  # displays login button with padding

    createAccountButton = customtkinter.CTkButton(homeWindow, text="Create Account", command=createAccountPressed)  # creates create account button
    createAccountButton.pack(pady=10)  # displays create account button with padding

    guestButton = customtkinter.CTkButton(homeWindow, text="Guest Mode", command=guestPressed)  # creates guest mode button
    guestButton.pack(pady=10)  # displays guest mode button with padding

    homeWindow.mainloop()  # starts the window event loop