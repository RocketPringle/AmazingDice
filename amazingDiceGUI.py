# MARK: - IMPORTS

import customtkinter # imports customtkinter library for BEAUTIFL GUI
from CTkTable import * # ALL THE TABLE YES
import amazingDice as ad  # imports main game file WOOOOO
from PIL import Image, ImageTk # use this for gif later aAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHGgg
import time # FOR DELAY TO MAKE NOT BAD IG YEEEE
import random # FOR LOADING PROGRESS BAR
import keyring # for keyring integration

# MARK: - SHOP

def shop(username, guestMode, settings): # unfinished so mostly not tagged or accesible and does absolutely nothing lmao
    shopWindow = customtkinter.CTk()
    shopWindow.geometry('850x600')
    shopWindow.title('Amazing Dice - Shop')

    titleLabel = customtkinter.CTkLabel(shopWindow, text='Shop', font=('Arial Bold', 20)) # TITLE
    titleLabel.pack(pady=20)

    coins = ad.getCoins(username)
    itemList = ad.getItems()

    coinsLabel = customtkinter.CTkLabel(shopWindow, text=f"Coins: {coins}")
    coinsLabel.place(relx=0.95, rely=0.07, anchor='ne')  # positions account label in top right

    accountLabel = customtkinter.CTkLabel(shopWindow, text=f'Signed in as: {username if not guestMode else "Guest"}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right

    infoLabel = customtkinter.CTkLabel(shopWindow, text='go away aaaaa') # info label my beloved
    infoLabel.pack(pady=10)

    scrollFrame = customtkinter.CTkScrollableFrame(shopWindow, width=700, height=400)
    scrollFrame.pack(pady=10)

    errorCounters = {
        
    }
    
    def buyPressed(item):
        ad.buy(username, item, itemList['items'][item]['cost'])

    for item in itemList["items"]:
        itemFrame = customtkinter.CTkFrame(scrollFrame, fg_color=("gray85", "gray25"))
        itemFrame.pack(pady=10, padx=10, side='left', ipadx=50, ipady=5)

        itemNameLabel = customtkinter.CTkLabel(itemFrame, text=itemList['items'][item]["name"], font=('Arial Bold', 15))
        itemNameLabel.pack(pady=3)

        itemCostLabel = customtkinter.CTkLabel(itemFrame, text=f"Cost: {itemList['items'][item]['cost']}")
        itemCostLabel.pack(pady=3)

        itemDescLabel = customtkinter.CTkLabel(itemFrame, text=itemList['items'][item]["desc"])
        itemDescLabel.pack(pady=3)

        buyButton = customtkinter.CTkButton(itemFrame, text='Buy', fg_color='green', command=buyPressed(item))
        buyButton.pack(pady=3)


    def backPressed():
        shopWindow.destroy()
        menu(guestMode, username, settings)

    backButton = customtkinter.CTkButton(shopWindow, text='Back', command=backPressed)
    backButton.pack(pady=10)

    shopWindow.mainloop()

# MARK: - PASS CHANGE

def passwordChange(username, guestMode, settings): # CHANGE UR PASSWORD WITH THIS ONE SIMPLE TRICK 😮😮😮😮😮

    changeWindow = customtkinter.CTk() # makeeeeeing the iwndowuiew
    changeWindow.geometry('850x600')
    changeWindow.title('Amazing Dice - Password Change')

    titleLabel = customtkinter.CTkLabel(changeWindow, text='Change password', font=('Arial Bold', 20)) # title 
    titleLabel.pack(pady=20)

    accountLabel = customtkinter.CTkLabel(changeWindow, text=f'Signed in as: {username if not guestMode else "Guest"}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right

    coins = ad.getCoins(username) #GET COUJNTS FOR NO RESAON THE SHOP DOESNT EXIST :SOB:'

    coinsLabel = customtkinter.CTkLabel(changeWindow, text=f"Coins: {coins}")
    coinsLabel.place(relx=0.95, rely=0.07, anchor='ne')  # positions account label in top right

    infoLabel = customtkinter.CTkLabel(changeWindow, text='') # i love info label my beloved
    infoLabel.pack(pady=10)
    
    errorCounters = { # LOIKE A MILLION DIFERENBT ERROR DOUNBTERS
        "wrongPassword": 0,
        "passwordsMismatch": 0,
        "passwordRequirements": 0,
        "samePassword": 0
    }

    def changePressed(): # u press change
        userData = ad.loadUsers()
        if ad.hashPassword(currentPassField.get()) != userData['users'][username]['hashedPassword']:
            errorCounters["wrongPassword"] += 1
            infoLabel.configure(text=f'Wrong password, please enter the correct password! ({errorCounters["wrongPassword"]})', text_color='red') # INFO LABEL MY BELOVED
        elif newPassField1.get() != newPassField2.get():  
            errorCounters["passwordsMismatch"] += 1
            infoLabel.configure(text=f'Make sure passwords are the same in both boxes! ({errorCounters["passwordsMismatch"]})', text_color='red') # if not same do agaim (im a poet)
        else:
            password = newPassField1.get() # js so i didnt have to change all the var names i cant be bothered ( i copy pasted this from createAccountWindow)
            if not (len(password) >= 12 and  # checks password requirements
                any(c.isdigit() for c in password) and  # must have number
                any(c.isupper() for c in password) and  # must have uppercase
                any(c.islower() for c in password) and  # must have lowercase
                any(c in r'!#$%&()*+,-./:;<=>?@[]^_`{|}~\'"' for c in password)):  # must have special character
                errorCounters["passwordRequirements"] += 1
                infoLabel.configure(text=f'Password must be at least 12 characters and contain uppercase lowercase numbers and special characters! ({errorCounters["passwordRequirements"]})', text_color='red')
            else:
                saveText, saveBool = ad.editUser(username, password)
                if not saveBool:
                    errorCounters["samePassword"] += 1
                    infoLabel.configure(text=f'{saveText} ({errorCounters["samePassword"]})', text_color='red')
                else:
                    infoLabel.configure(text=saveText, text_color='green') # u got past the thing yay ill change now and make output the INFO LABEL MY BELOVED

    def backPressed(): # u press bakc
        changeWindow.destroy() # boom
        settingsWindow(username, guestMode, settings) # go to setitngs now yeee

    currentPassField = customtkinter.CTkEntry(changeWindow, placeholder_text='Verify current passsword', width=200, height=50, show='*') # copy pastd from createAccountWindow again but slighly edited it js a text field for ur passowrd with asterisks in place of characters so u secure or whatever idk nobody gonna steal ur account in this random dice game thing vro 😭😭😭😭😭
    currentPassField.pack(pady=10)  # pady sounds funny (pack to make exist)
    currentPassField.bind('<Return>', changePressed) # makes it run changePressed if you press enter

    newPassField1 = customtkinter.CTkEntry(changeWindow, placeholder_text='Enter new password', width=200, height=50, show='*')
    newPassField1.pack(pady=10)  # displays new psswrd field
    newPassField1.bind('<Return>', changePressed)  # binds enter key to change function

    newPassField2 = customtkinter.CTkEntry(changeWindow, placeholder_text='Enter again', width=200, height=50, show='*')
    newPassField2.pack(pady=10)  # displays another one ig so u do it right yk
    newPassField2.bind('<Return>', changePressed)  # binds enter key to change function

    changeButton = customtkinter.CTkButton(changeWindow, text='Update Password', command=changePressed) # CHANGE PASSWORD BUTTON
    changeButton.pack(pady=10)

    backButton = customtkinter.CTkButton(changeWindow, text='Back', command=backPressed) # BACK BUTTON
    backButton.pack(pady=10)

    changeWindow.mainloop()

# MARK: - SETTINGS

def settingsWindow(username, guestMode, settings):

    global fastRoll # mkaes fatst roll a globalt variab le so it doesnt make a new one upo and actualyl works yaya
    settingsWindow = customtkinter.CTk() # WINDOW STUFFFFF
    settingsWindow.geometry('850x600')
    settingsWindow.title('Amazing Dice - Settings')

    fastRoll = settings['fastRoll']

    titleLabel = customtkinter.CTkLabel(settingsWindow, text='Settings', font=('Arial Bold', 20)) # TITLE
    titleLabel.pack(pady=20)

    accountLabel = customtkinter.CTkLabel(settingsWindow, text=f'Signed in as: {username if not guestMode else "Guest"}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right

    infoLabel = customtkinter.CTkLabel(settingsWindow, text='')
    infoLabel.pack(pady=10)
    
    errorCounters = { # error counter
        "guestPasswordChange": 0
    }

    print(f"fastRoll on open: {fastRoll}") # DEBUG

    def fastRollPressed():

        global fastRoll # MORE GLOAOBL VARIABLE YAY I DONT ACTUALLY NEED THIS I THINK BC OF SAVING SETTINGS BUT IDK MB FAMALAM

        print(f"fastRoll on press: {fastRoll}") # DEBUG

        if  not fastRoll:  # if normal coloUr (I WANT THE U BACK)
            print('made green (on)') # debuggg
            fastRollButton.configure(fg_color=['#4CAF50', '#006400'], hover_color=['#388E3C', '#004200']) # MAKE COLOUR NICE GREEN LEFT IS LIGHT (I THINK) RIGHT IS DARJK
            fastRoll = True
            ad.saveUserSettings(username, {'fastRoll': True, 'theme': settings['theme']})
            settings['fastRoll'] = True
        else:
            print('made blue (off)') # more debug i dont even need this vro
            fastRollButton.configure(fg_color=['#3B8ED0', '#1F6AA5'], hover_color=['#36719F', '#144870']) # BLUIE
            fastRoll = False
            ad.saveUserSettings(username, {'fastRoll': False, 'theme': settings['theme']})
            settings['fastRoll'] = False
    def themeChanged():
        if themeCheckbox.get():  # hceckbox is checked (1 == True so doint need if .. == 1)
            customtkinter.set_appearance_mode("Dark") # MAKE DARK
            ad.saveUserSettings(username, {'theme': 'dark', 'fastRoll': settings['fastRoll']})
            settings['theme'] = 'dark'
        else:  # checkbox is unchecked
            customtkinter.set_appearance_mode("Light") # MAKE LITGHT
            ad.saveUserSettings(username, {'theme': 'light', 'fastRoll': settings['fastRoll']})
            settings['theme'] = 'light'

    def backPressed(): # back button preseed
        settingsWindow.destroy() # boom
        menu(guestMode, username, settings) # go tyo menu again yee

    def passChangePressed(): # MORE WINDOWS YAAAAAAA
        if guestMode:
            errorCounters["guestPasswordChange"] += 1
            infoLabel.configure(text=f'Guests do not have passwords! Login to change your password! ({errorCounters["guestPasswordChange"]})')
        else:
            settingsWindow.destroy()
            passwordChange(username, guestMode, settings) # (i should rlly make those global variables but im in too deep ive passed them so many times at this point idc)

    fastRollButton = customtkinter.CTkButton(settingsWindow, text='Fast Roll', command=fastRollPressed, width=140, fg_color=(['#4CAF50', '#006400'] if fastRoll else ['#3B8ED0', '#1F6AA5']), hover_color=(['#388E3C', '#004200'] if fastRoll else ['#36719F', '#144870'])) # MAKE ROLL FAST BC IT TAKES SO LONGGGGGG (ts js logic for color depending if fastRoll is on or not)
    fastRollButton.pack(pady=10)

    passChangeButton = customtkinter.CTkButton(settingsWindow, text='Change password', command=passChangePressed)
    passChangeButton.pack(pady=10)

    themeFrame = customtkinter.CTkFrame(settingsWindow, width=140, height=28) # FRAME AAAAA
    themeFrame.pack_propagate(False)  # STOP MOVING AND BEING WIDE AAAA
    themeFrame.pack(pady=10)

    themeLabel = customtkinter.CTkLabel(themeFrame, text="Dark Mode", font=('Arial', 14)) # LABEL
    themeLabel.pack(side="left", padx=10) # ON THE LEFT BIT

    themeCheckbox = customtkinter.CTkCheckBox(themeFrame, text="", command=themeChanged) # CHECKBOX
    if customtkinter.get_appearance_mode() == "Dark": # MAKE IT TICK IF UR DARK ALREADY
        themeCheckbox.select()
    themeCheckbox.pack(side="right") # PUT ON RIGHT

    backButton = customtkinter.CTkButton(settingsWindow, text='Back', command=backPressed) # M,AKE BACK BUTTON
    backButton.pack(pady=10) 

    settingsWindow.mainloop() 

# MARK: - MATCH

def match(botOrNot, difficulty, username, username2, guestMode, settings): # botOrNot is the best var name ever ( also i hate ts code vro fr )
    gameWindow = customtkinter.CTk() # WINDOW
    gameWindow.geometry('850x600')
    gameWindow.title('Amazing dice - Match')

    trophyImage = Image.open("images/trophy.png") # make treophy imaghe
    trophy = customtkinter.CTkImage(trophyImage, size=(150, 150))

    sobImage = Image.open("images/sob.png") # make sob image
    sob = customtkinter.CTkImage(sobImage, size=(150, 150)) # more

    fastRoll = settings['fastRoll'] # fast roll

    questionMarkImage = Image.open("images/questionMark.png") # make question mark image
    questionMark = customtkinter.CTkImage(questionMarkImage, size=(150, 150)) # more
    
    # Use "Guest" as username if playing as guest
    displayUsername = "Guest" if username == "Guest" else username
    displayUsername2 = "Guest" if username2 == "Guest" else username2

    rollsList = [['','Roll 1', 'Roll 2', 'Roll 3'], # NICE LIST TABLE THING FOR THE TABLE YE
                [displayUsername,'-','-','-'],
                [displayUsername2,'-','-','-']]
    
    titleLabel = customtkinter.CTkLabel(gameWindow, text='Match', font=('Arial Bold', 20)) # TITLE
    titleLabel.pack(pady=20)

    roundLabel = customtkinter.CTkLabel(gameWindow, text='Round 1', font=('Arial', 15)) # ROUJND
    roundLabel.pack(pady=5)

    rollTable = CTkTable(master=gameWindow, row=3, column=4, values=rollsList) # TABLE MAKE (idk why this is giving me an error without this comment) -> # type: ignore
    rollTable.pack(expand=True, padx=15, pady=15) 

    infoLabel = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15), text_color='green')     # TELLS U STUFF LATER WHEN U WIN
    infoLabel.pack(pady=5)

    rollingLabel = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15), text_color='gray') # TELL U U R ROLLING
    rollingLabel.pack(pady=5)

    startRoll1Label = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15)) # START ROLL 1 SHOW
    startRoll1Label.pack(pady=5)

    startRoll2Label = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15)) # START ROLL 2 SHOW
    startRoll2Label.pack(pady=5)

    player1TotalLabel = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15)) # TOTAL FOR PLAYER ONE READ THE VAR NAMES BRO OMG
    player1TotalLabel.pack(pady=2.5)

    player2TotalLabel = customtkinter.CTkLabel(gameWindow, text='', font=('Arial', 15)) # READ THE NAME
    player2TotalLabel.pack(pady=2.5)

    player1ScoreLabel = customtkinter.CTkLabel(gameWindow, text=f"{displayUsername}: 0", font=('Arial', 15)) # TOTAL FOR PLAYER ONE
    player1ScoreLabel.pack(pady=1)

    player2ScoreLabel = customtkinter.CTkLabel(gameWindow, text=f"{displayUsername2}: 0", font=('Arial', 15)) # TOTAL FOR PLAYER 2
    player2ScoreLabel.pack(pady=1)

    def startPressed(): # TERRIBLE CODE DONT LOOK AT THIS 

        startButton.configure(state='disabled', fg_color='gray') # so u cant break my code byu spoamnmming it

        playerScore1, playerScore2 = 0, 0 # SET DEFAULT SCORES
        delay = 100 if fastRoll else 1000  # store delay in ms based on fastroll var

        def wait(multiplier=1): #MAKE A WAIT THING SO I DONT HAVER TO RIGHT 2 LINES EVERY TIME I WANNA WAIT AND UPODATE ( A LOT ) ALSO TAKES INTO ACCOUNBT FASTROLL AND A MUKLTIPOLIERIIF WAITING IMPORTANT
            gameWindow.update() # UPDATE THE WINDOW
            gameWindow.after(delay*multiplier) # WAIT FOR THE DELAY

        for i in range(0, 5): # 5 rounds
            infoLabel.configure(text_color='gray') # RESET COLOR
            roundLabel.configure(text=f'Round {i+1}') # UPDATE ROUND LABEL TO SHOW CURRENT ROUND YAYAYA
            print(ad.getDifficultyInt(difficulty))
            print(ad.getDifficultyNumString(difficulty))
            rolls1, rolls2, rollTotal1, rollTotal2, player1Starts, startRoll1, startRoll2 = ad.playRound(6,ad.getDifficultyInt(difficulty) if botOrNot else 0)  # rolls 3 times and stores it in a list. gets the roll totals and gets who starts + their starting rolls
            print('rolled (playround)') # DEBUG THINK MEANT TO BE F STRING IDK ITS BEEN AGES SINCE I WROTE THIS (1 MONTH)
            # generate bracket texts AS I HAD AN ERROR BEFORE BUT TS WASNT THE ISSUE BUT IT MAKES IT NEATER SO IDC
            if botOrNot and difficulty != 'hard':
                print('passed if') # DEBUG
                difficultyInt = ad.getDifficultyInt(difficulty) # get the difficulty int
                bracketText = f"({(int(startRoll2)-difficultyInt)} {ad.getDifficultyNumString(difficulty)})" # make the bracket text with roll and then how got the roll 
                print(f"bracketText: {bracketText}")
                bracketText1 = f"({(int(rolls2[0])-difficultyInt)} {ad.getDifficultyNumString(difficulty)})"
                print(f"bracketText1: {bracketText1}")
                bracketText2 = f"({(int(rolls2[1])-difficultyInt)} {ad.getDifficultyNumString(difficulty)})"
                print(f"bracketText2: {bracketText2}")
                bracketText3 = f"({(int(rolls2[2])-difficultyInt)} {ad.getDifficultyNumString(difficulty)})"
                print(f"bracketText3: {bracketText3}")
            else:
                print('failed if') # DEBUG
                bracketText, bracketText1, bracketText2, bracketText3 = '', '', '', '' # make the bracket text empty
            if player1Starts: # DO A LONG ROLLING SEQUENCE THATS ACUTALLY FAKE AS I ROLL THEM AT START AND JUST PRETENT TO DO THAT NOW BECAUSE THE BRIEF IS WEIRD LIKE WHY DOES IT MATTER WHO GOES FIRST ITS JUST GAMBLING AAAAAAA

                # AAAAAAA YOU HAVE A 98% CHGANCE OIF LOSING TO THE HARD BOT A AAAAASGFDFSATYSDFY98P7STGF YIUSUF I HAVE TO CGANGE IT ALLLLLL THE EASY BOT LOSES 0.0001% OF THE TIME AAAAAA WHYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY I HATE MATHS NOWWW
                # ( I NERFED/BUFFED THEM )

                # ACTUAL EXPLANATION:
                # 1. ROLLING LABEL IS SET TO ROLLING
                # 2. WAIT FOR 100/1000 MS (depends on fastroll)
                # 3. START ROLL 1 LABEL IS SET TO THE START ROLL 1
                # 4. START ROLL 2 LABEL IS SET TO THE START ROLL 2
                # 5. INFO LABEL IS SET TO THE START ROLL 1
                # 6. ROLLING LABEL IS SET TO ""
                # 7. WAIT FOR 100/1000 MS (depends on fastroll)
                # 8. DO IT MORE SORRY I DIDNT TAG IT ALL ITS THE DAY BEFORE THE DUE DATE AND I HAVE NO TIMEEEE



                rollingLabel.configure(text='Rolling')
                wait()
                startRoll1Label.configure(text=f'{displayUsername} rolled a {startRoll1}!', text_color='green' if player1Starts else 'red')
                startRoll2Label.configure(text=f"{displayUsername2} rolled a {startRoll2} {bracketText}", text_color = 'green' if not player1Starts else 'red')

                startRoll1Label.configure(text='')
                startRoll2Label.configure(text='')
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], [displayUsername, rolls1[0], '-', '-'], [displayUsername2, '-', '-', '-']])
                rollingLabel.configure(text='')
                wait()

                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], [displayUsername, rolls1[0], rolls1[1], '-'], [displayUsername2, '-', '-', '-']])
                rollingLabel.configure(text='')
                wait()

                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], [displayUsername, rolls1[0], rolls1[1], rolls1[2]], [displayUsername2, '-', '-', '-']])
                rollingLabel.configure(text='')
                wait()
            else: # DO IT BUT SLIGHTLY DIFFEREENT THIS PROBABLY COULD HAVE BEEN MADE LIKE HALF THE LENGTH
                rollingLabel.configure(text='Rolling')
                wait()
                infoLabel.configure(text=f'{displayUsername2} starts!', text_color=('red' if botOrNot else 'yellow'))
                rollingLabel.configure(text='')
                wait()
                
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, '-', '-', '-'], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", '-', '-']])
                rollingLabel.configure(text='')
                wait()
                
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, '-', '-', '-'], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", f"{rolls2[1]} {bracketText2}", '-']])
                rollingLabel.configure(text='')
                wait()
                
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, '-', '-', '-'], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", f"{rolls2[1]} {bracketText2}", f"{rolls2[2]} {bracketText3}"]])
                rollingLabel.configure(text='')
                wait()

            if player1Starts:
                player1TotalLabel.configure(text=f'{displayUsername} rolled a total of {rollTotal1}!') # say total
            else:
                player2TotalLabel.configure(text=f'{displayUsername2} rolled a total of {rollTotal2}!') # say total
            wait(3)

            if player1Starts: # MOREEEE NEXT PERSONS ROLLS NOW THO
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, rolls1[0], rolls1[1], rolls1[2]], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", '-', '-']])
                rollingLabel.configure(text='')
                wait()
                
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, rolls1[0], rolls1[1], rolls1[2]], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", f"{rolls2[1]} {bracketText2}", '-']])
                rollingLabel.configure(text='')
                wait()
                
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, rolls1[0], rolls1[1], rolls1[2]], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", f"{rolls2[1]} {bracketText2}", f"{rolls2[2]} {bracketText3}"]])
                rollingLabel.configure(text='')
                wait()
            else: # OTHER PERSON INSTEAD
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, rolls1[0], '-', '-'], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", f"{rolls2[1]} {bracketText2}", f"{rolls2[2]} {bracketText3}"]])
                rollingLabel.configure(text='')
                wait()
                
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, rolls1[0], rolls1[1], '-'], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", f"{rolls2[1]} {bracketText2}", f"{rolls2[2]} {bracketText3}"]])
                rollingLabel.configure(text='')
                wait()
                
                rollingLabel.configure(text='Rolling')
                wait()
                rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], 
                    [displayUsername, rolls1[0], rolls1[1], rolls1[2]], 
                    [displayUsername2, f"{rolls2[0]} {bracketText1}", f"{rolls2[1]} {bracketText2}", f"{rolls2[2]} {bracketText3}"]])
                rollingLabel.configure(text='')
                wait()

            player1TotalLabel.configure(text=f'{displayUsername} rolled a total of {rollTotal1}!') # say total
            player2TotalLabel.configure(text=f'{displayUsername2} rolled a total of {rollTotal2}!') # say other total (both bc doesnt matter order at this point)
            wait(3) # slower it used to zoom bro 🥀

            if rollTotal1 > rollTotal2: # you win
                infoLabel.configure(text=f"{displayUsername if not botOrNot else 'You'} win{'s' if not botOrNot else ''} round {i+1}!", text_color='green') # TELL U U WON
                playerScore1 += 1 # SCORE
                if rollTotal1 == 18:
                    ad.checkAchievement(username, 'perfectScore')
            elif botOrNot: # if u lost and vs bot
                infoLabel.configure(text=f"You lost round {i+1}!", text_color='red') # HAHAHAHAAHHAHHA YOU LOSE
                playerScore2 += 1 # SCORE
            else: # U LOST IN P[VP SAY OTHER WON YEE]
                if rollTotal2 == 18:
                    ad.checkAchievement(username2, 'perfectScore')
                infoLabel.configure(text=f'{displayUsername2} wins round {i+1}!', text_color='green') # SAY OTHER DUDE WORNNN
                playerScore2 += 1 #' SCPOREW
            
            player1ScoreLabel.configure(text=f"{displayUsername}: {playerScore1}") # UPDATE SCORE LABELS
            player2ScoreLabel.configure(text=f"{displayUsername2}: {playerScore2}")
            rollingLabel.configure(text='') # CLEAR ROLLING TEXT
            wait() #WAIT
            infoLabel.configure(text='') # RESET
            player1TotalLabel.configure(text='') # THIS COULD PROBABLYT BE ONE LINE MB
            player2TotalLabel.configure(text='')
            rollTable.configure(values=[['','Roll 1', 'Roll 2', 'Roll3'], [displayUsername, '-', '-', '-'], [displayUsername2, '-', '-', '-']])
            wait(3)

# MARK: - WIN

        if playerScore2 < playerScore1: # IF YOU WON OVERALL
            if botOrNot: # YOU WON VS BOT
                ##if difficulty == 'Easy': tagged as shop not exist rn and ts didnt even work xd
                #    winReward = 500
                #elif difficulty == 'Medium':
                #    winReward = 750
                #elif difficulty == 'Hard':
                #    winReward = 1000
                #elif difficulty == 'Expert':
                #    winReward = 1500
                infoLabel.configure(text='YOU WIN!', text_color='green', font=('Arial Bold', 25)) # TERLL U
                trophyLabel = customtkinter.CTkLabel(gameWindow, text="", image=trophy) # create a trophy label
                trophyLabel.place(relx=0.5, rely=0.6, anchor="center")  # put below info label
                #rewardLabel = customtkinter.CTkLabel(gameWindow, text=f"Reward: {winReward}", font=('Arial Bold', 15))
                #ewardLabel.place(relx=0.5, rely=0.6, anchor="center")  # put below info label
            else: # YOU WON VS PLAYER
                #winReward = 500
                infoLabel.configure(text=f'{displayUsername} WON!', text_color='green', font=('Arial Bold', 25)) # TERLL U
                trophyLabel = customtkinter.CTkLabel(gameWindow, text="", image=trophy) # create a trophy label
                trophyLabel.place(relx=0.5, rely=0.6, anchor="center")  # put below info label
                userData['users'][username2]['achievementProgress']['losses'] += 1
                userData['users'][username2]['achievementProgress']['ConsecutiveLosses'] += 1
                userData['users'][username2]['achievementProgress']['ConsecutiveWins'] = 0
                #rewardLabel = customtkinter.CTkLabel(gameWindow, text=f"Reward: {winReward}", font=('Arial Bold', 15))
                #rewardLabel.place(relx=0.5, rely=0.8, anchor="center")  # put below info label # MOVE TJHE LAVBEL DOPWNNNNNNNNNNNNNNN
            if username != 'Guest':  # CHECK 4 TGUESS MODE SO NOT EDITING NON EXCISTENT STATS
                ad.checkAchievement(username, 'wins', 1)
                ad.checkAchievement(username, 'consecutiveWins', 1)
                userData = ad.loadUsers() # GET DATA
                userData['users'][username]['stats']['totalGames'] += 1 # EDIT IT
                userData['users'][username]['stats']['wins'] += 1 # MORE EDIT
                if username2 == 'Bot': # EDIT WINS FOR BOTS 
                    userData['users'][username]['stats']['vsBot'][difficulty]['wins'] += 1 # ACUTALLY EDIT
                    #userData['users'][username]['stats']['netWorth'] += winReward
                    #userData['users'][username]['coins'] += winReward
                else:
                    userData['users'][username]['stats']['vsPlayer']['wins'] += 1 # YOU WON AND SAVE IT YAYAYAYAYAYAYA
                    userData['users'][username2]['stats']['totalGames'] += 1 # OTHER LOST SAVE IT TOO
                    userData['users'][username2]['stats']['losses'] += 1   
                    #userData['users'][username2]['coins'] += winReward
                    #userData['users'][username]['stats']['netWorth'] += winReward
                    #userData['users'][username]['coins'] += winReward
                    #userData['users'][username2]['coins'] -= winReward
                ad.saveUsers(userData) # ACTUAKLY SAFE THE DATA

# MARK: - LOSE

        elif playerScore2 > playerScore1: #OTHER DUDE WON
            infoLabel.configure(text=f"{'YOU LOSE' if botOrNot else displayUsername2} {'WON' if not botOrNot else ''}!", text_color=('red' if botOrNot else 'green'), font=('Arial Bold', 25)) # IF VS BOT CALLS U A LOSER ELSE JS SAYS WHO WON
            if not botOrNot: # if a player won display a trophy
                trophyLabel = customtkinter.CTkLabel(gameWindow, text="", image=trophy) # create a trophy label
                trophyLabel.place(relx=0.5, rely=0.6, anchor="center")  # put below info label
            else: # if a bot won display :sob:
                sobLabel = customtkinter.CTkLabel(gameWindow, text="", image=sob) # create a trophy label
                sobLabel.place(relx=0.5, rely=0.6, anchor="center")  # put below info label
            if username != 'Guest':  # all the stat stuff i dont want to tag it all you read the last bit 
                ad.checkAchievement(username, 'losses')
                ad.checkAchievement(username, 'consecutiveLosses')
                userData = ad.loadUsers()
                userData['users'][username]['stats']['totalGames'] += 1
                userData['users'][username]['stats']['losses'] += 1
                if username2 == 'Bot':
                    userData['users'][username]['stats']['vsBot'][difficulty]['losses'] += 1
                else:
                    userData['users'][username]['stats']['vsPlayer']['losses'] += 1 # HAHA U LOSE ILL SAVE IT YEEEEE
                    userData['users'][username2]['stats']['totalGames'] += 1
                    userData['users'][username2]['stats']['wins'] += 1 # OTHER WON SAVE IT TOO YAYAYAYA
                ad.saveUsers(userData)

# MARK: - DRAW

        else: # if draw which legit ISNT POSSIBLE THERS 5 ROUNDS IM DUMB BUT I DONT CARE ENOUGH TO DELETE THIS ENJOY USELESS CODE RIPPPP
            infoLabel.configure(text='HOW DID YOU DRAW?!', text_color='red', font=('Arial Bold', 25)) # TELLSYU YOPU TDRAEW WITH TYELLOW BC DRAWK IS YELLLOW AAAA
            questionMarkLabel = customtkinter.CTkLabel(gameWindow, text="", image=questionMark) # create a question mark label
            questionMarkLabel.place(relx=0.5, rely=0.6, anchor="center")  # put below info label
            if username != 'Guest':  # OGUEST MODE CHECK
                userData = ad.loadUsers() # BLAH BLAHG
                userData['users'][username]['stats']['totalGames'] += 1
                userData['users'][username]['stats']['draws'] += 1
                userData['users'][username2]['achievementProgress']['draws'] += 1
                userData['users'][username2]['achievementProgress']['ConsecutiveLosses'] = 0
                userData['users'][username2]['achievementProgress']['ConsecutiveWins'] = 0
                if username2 == 'Bot':
                    userData['users'][username]['stats']['vsBot'][difficulty]['draws'] += 1
                else:
                    userData['users'][username]['stats']['vsPlayer']['draws'] += 1
                ad.saveUsers(userData) # DONE AND SAVED 

    def backPressed(): # BACK BUTTON
        gameWindow.destroy() # CLOSE THE GAME WINDOW
        matchWindow(username, guestMode, settings) # GO BACK TO THE MATCH WINDOW

    startButton = customtkinter.CTkButton(gameWindow, text='Start', font=('Arial', 15), command=startPressed, state='enabled') # START BUTTON
    startButton.pack(pady=10) # MAKE IT

    backButton = customtkinter.CTkButton(gameWindow, text='Back', font=('Arial', 15), command=backPressed) # BACK BUTTON
    backButton.pack(pady=10)

    gameWindow.mainloop()      

# MARK: - PVP

def pvp(username, settings):
    pvpWindow = customtkinter.CTk() # make the window
    pvpWindow.geometry('850x600') # set the size
    pvpWindow.title('Amazing dice - VS Person') # set the title

    titleLabel = customtkinter.CTkLabel(pvpWindow, text='Player vs Player', font=('Arial Bold', 30)) # make title label
    titleLabel.pack(pady=10)

    infoLabel = customtkinter.CTkLabel(pvpWindow, text='Enter username of person you want to play against:', font=('Arial Bold', 15)) # make info label (my beloved)
    infoLabel.pack(pady=10)

    progressFrame = customtkinter.CTkFrame(pvpWindow, fg_color="transparent", width=1, height=1) # make frame for progress bar to be in (js above buttons so it doesnt default to bottom)      fg color transparent so it doesnt show as its ugly and small so not move other stuff out of way
    progressFrame.pack(pady=10)

    accountLabel = customtkinter.CTkLabel(pvpWindow, text=f'Signed in as: {username}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right

    errorCounters = { # counts hgow many mistakjes stupoid player made lmao
        "emptyFields": 0,
        "selfPlay": 0,
        "invalidCredentials": 0
    }

    def backPressed(): # u press ack
        pvpWindow.destroy() # close the pvp window
        matchWindow(username, False, settings) # go back to de match window

    def startPressed(event=None): # u press start event is bc pressing enter need one ig so js makes it nothing 
        if usernameField.get() == '' or passwordField.get() == '': # if the username or password is empty
            errorCounters["emptyFields"] += 1 # add 1 to the empty fields counter
            infoLabel.configure(text=f'Please fill in all fields! ({errorCounters["emptyFields"]})', text_color='red') # tell the user to fill in all fields
        elif usernameField.get() == username: # if the username is the same as the current username ( dumbo )
            errorCounters["selfPlay"] += 1 # add 1 to the self play counter
            infoLabel.configure(text=f'You cannot play against yourself! ({errorCounters["selfPlay"]})', text_color='red') # tell the user they cant play against themselves ( dumbo )
        elif ad.checkPassword(usernameField.get(), passwordField.get()): # if the password is correct
            infoLabel.configure(text='Successfully logged in!', text_color='green') # tell the user they logged in successfully yayaaaaaa
            
            progressbar = customtkinter.CTkProgressBar(progressFrame, width=300) # make progress bar
            progressbar.pack(pady=10)
            
            infoLabel.configure(text='Loading into match...', text_color='green') # tell the user they are loading into the match
            
            loadTime = random.uniform(0.5, 3) # random load time as a float
            steps = 200 # steps for the progress bar (200 for decent detail)
            for i in range(steps + 1): # loops through the steps
                progressbar.set(i/steps) # sets the progress bar to the current step
                pvpWindow.update() # updates the window (progress bar needs to be updated to show bc ctkinter is dumb)
                time.sleep(loadTime/steps) # waits based on the steps to make equal amouint of time for each step
            
            opponentUsername = usernameField.get() # get the opponent username

            pvpWindow.destroy() # closes the pvp window
            match(False, 0, username, opponentUsername, False, settings) # starts the match with both users usernames, false bc not bot (duh)
        else:
            errorCounters["invalidCredentials"] += 1 # add 1 to the invalid credentials counter
            infoLabel.configure(text=f'Invalid username or password ({errorCounters["invalidCredentials"]})', text_color='red') # tell the user they have invalid credentials ( bozo )

    usernameField = customtkinter.CTkEntry(pvpWindow, placeholder_text='Username', width=200, height=30)
    usernameField.pack(pady=10) # make field for username
    usernameField.bind('<Return>', startPressed) # bind the enter key to the startPressed function

    passwordField = customtkinter.CTkEntry(pvpWindow, placeholder_text='Password', width=200, height=30)
    passwordField.pack(pady=10)
    passwordField.bind('<Return>', startPressed) # bind the enrtr key to the startPressed function

    startButton = customtkinter.CTkButton(pvpWindow, text='Start', command=startPressed)
    startButton.pack(pady=10) # make button for start

    backButton = customtkinter.CTkButton(pvpWindow, text='Back', command=backPressed)
    backButton.pack(pady=10) # make button for back

    pvpWindow.mainloop()

# MARK: - BOT

def bot(username, guestMode, settings):
    botWindow = customtkinter.CTk() # make the window
    botWindow.geometry('850x600') # set the size
    botWindow.title('Amazing Dice - VS Bot') # set the title

    titleLabel = customtkinter.CTkLabel(botWindow, text='Choose bot difficulty!', font=('Arial Bold', 30)) # nmake s titkle lavel
    titleLabel.pack(pady=10)

    accountLabel = customtkinter.CTkLabel(botWindow, text=f'Signed in as: {username if not guestMode else "Guest"}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne') 

    infoLabel = customtkinter.CTkLabel(botWindow, text='', font=('Arial Bold', 15))  # info label my beloved (ts so fire)
    infoLabel.pack(pady=10)

    def continuePressed(): # if u pressed continue
        difficulty = difficultyBox.get() # get the difficulty (before so the difficultyBox actually exists)
        botWindow.destroy() # close the bot window
        match(True, difficulty, username, 'Bot', guestMode, settings) # start the match

    def backPressed():
        botWindow.destroy()
        matchWindow(username, guestMode, settings) 

    difficultyBox = customtkinter.CTkComboBox(botWindow, values=['Easy', 'Medium', 'Hard', 'Expert']) # makes a dropdown for the difficulty I DIDS IT AYAYA
    difficultyBox.pack(pady=10)

    continueButton = customtkinter.CTkButton(botWindow, text='Continue', command=continuePressed) # copntinu so u can actually start it
    continueButton.pack(pady=10)

    backButton = customtkinter.CTkButton(botWindow, text='Back', command=backPressed) # back button 
    backButton.pack(pady=10)

    botWindow.mainloop()

# MARK: - MATCH WINDOW

def matchWindow(username, guestMode, settings):  # defines match window function that takes username and guest mode status
    matchWindow = customtkinter.CTk()  # creates new window
    matchWindow.geometry('850x600')  # sets window size to 600x500 pixels
    matchWindow.title('Amazing Dice - Match')  # sets window title

    titleLabel = customtkinter.CTkLabel(matchWindow, text="Match", font=('Arial Bold', 30))  # creates title label with large bold font
    titleLabel.pack(pady=10)  # adds padding and displays title

    accountLabel = customtkinter.CTkLabel(matchWindow, text=f'Signed in as: {username if not guestMode else "Guest"}', font=('Arial Bold', 15))  # creates account label showing current user
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right corner

    messageLabel = customtkinter.CTkLabel(matchWindow, text="", text_color="red")  # creates empty error message label in red
    messageLabel.pack(pady=10)  # adds padding and displays message label
    
    errorCounters = { # countrs how many rtimes the error happens to show the ppl so they get like feedba\CK ON their epresses
        "guestPvp": 0
    }

    def backPressed():  # defines function for back button
        matchWindow.destroy()  # closes match window
        menu(guestMode, username, settings)  # returns to menu

    def pvpPressed():
        if not guestMode: # IF NOPT IN GUEST MODE (READ THE CODEEEEE 😠😠😠😠😠)
            matchWindow.destroy() # 💥💥💥💥💥💥
            pvp(username, settings) # FIGHT YAYAYAYAYAYYYA
        else:
            errorCounters["guestPvp"] += 1
            messageLabel.configure(text=f'Guests can only play against bots, make an account for more features! ({errorCounters["guestPvp"]})') # HAHA BAD UR A GUEST GHAHAA

    def botPressed():
        matchWindow.destroy() # make dropdown later w/ difficulties <- REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS REMMEBR THIS  I DID IT UYAYAAAAYAYA
        bot(username, guestMode, settings)

    botButton = customtkinter.CTkButton(matchWindow, text='VS Bot', command=botPressed) # BUTTON 4 FBOT MODE
    botButton.pack(pady=10)

    pvpButton = customtkinter.CTkButton(matchWindow, text='Vs Person', command=pvpPressed) # PVP (PERSON VS PERSON) BUTTON
    pvpButton.pack(pady=10)   

    backButton = customtkinter.CTkButton(matchWindow, text='Back', command=backPressed)  # creates back button
    backButton.pack(pady=10) 

    matchWindow.mainloop()  # starts the window event loop

# MARK: - STAT WINDOW

def viewStatsWindow(stats, username, settings):  # defines stats window function that takes stats dictionary and username
    statsWindow = customtkinter.CTk()  # creates new window
    statsWindow.geometry('850x600')  # sets window size
    statsWindow.title('Amazing Dice - Stats')  # sets window title

    #coinImage = customtkinter.CTkImage(light_image=Image.open('images/icons/coinIcon.png'), dark_image=Image.open('images/icons/coinIcon.png'), size=(20, 20)) # make coin image

    titleLabel = customtkinter.CTkLabel(statsWindow, text=f"Stats for {username}", font=('Arial Bold', 30))  # creates title with username
    titleLabel.pack(pady=10) 

    accountLabel = customtkinter.CTkLabel(statsWindow, text=f'Signed in as: {username}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # put in corner

    scrollFrame = customtkinter.CTkScrollableFrame(statsWindow, width=500, height=400)  # creates scrollable frame for showinm g stats ( doesnt rlly need to be screollable as theres not enoguht but just incase ig)
    scrollFrame.pack(pady=10, padx=20, fill="both", expand=True)

    totalGamesLabel = customtkinter.CTkLabel(scrollFrame, text=f"Total Games: {stats['totalGames']}", font=('Arial Bold', 15))  # shows total games played
    totalGamesLabel.pack(pady=10)  # displays total games with padding

    overallLabel = customtkinter.CTkLabel(scrollFrame, text=f"Overall: {stats['wins']} Wins, {stats['losses']} Losses, {stats['draws']} Draws", font=('Arial Bold', 15))  # shows overall stats
    overallLabel.pack(pady=10)  # displays overall stats with padding

    #coinIconLabel = customtkinter.CTkLabel(scrollFrame, image=coinImage, text="") # make label for icon nuh uh ts gone now L
    #coinIconLabel.place(relx=0.572, rely=0.247) # put in rlly specific place as i didnt knkw how to put next to the label

    netWorthLabel = customtkinter.CTkLabel(scrollFrame, text=f"Net Worth: {stats['netWorth']}", font=('Arial Bold', 15))  # shows net worth from stats
    netWorthLabel.pack(pady=10)  

    vsBotLabel = customtkinter.CTkLabel(scrollFrame, text="Vs Bot", font=('Arial Bold', 20))  # creates bot section header
    vsBotLabel.pack(pady=10)  # displays bot header with padding

    for difficulty in ['Easy', 'Medium', 'Hard', 'Expert']:  # loops through each difficulty level
        botStats = stats['vsBot'][difficulty]  # gets stats for current difficulty
        botLabel = customtkinter.CTkLabel(scrollFrame, text=f"{difficulty.capitalize()}: {botStats['wins']} Wins, {botStats['losses']} Losses, {botStats['draws']} Draws", font=('Arial', 15))  # creates label for difficulty stats
        botLabel.pack(pady=5)  # displays difficulty stats with padding

    vsPlayerLabel = customtkinter.CTkLabel(scrollFrame, text="Vs Player", font=('Arial Bold', 20))  # creates player section header
    vsPlayerLabel.pack(pady=10)  # displays player header with padding

    vsPlayerStats = stats['vsPlayer']  # gets player vs player stats
    playerStatsLabel = customtkinter.CTkLabel(scrollFrame, text=f"Wins: {vsPlayerStats['wins']}, Losses: {vsPlayerStats['losses']}, Draws: {vsPlayerStats['draws']}", font=('Arial', 15))  # creates label for player stats
    playerStatsLabel.pack(pady=5)  # displays player stats with padding

    def achievementsPressed(): # if u pressed achievements button
        statsWindow.destroy() # close stats window
        achievementsWindow(username, settings) # open achievements window

    def backPressed():  # defines function for back button
        statsWindow.destroy()  # closes stats window
        menu(False, username, settings)  # returns to menu

    achievementsButton = customtkinter.CTkButton(statsWindow, text='Achievements', command=achievementsPressed) # make button for achievements
    achievementsButton.pack(pady=10)

    backButton = customtkinter.CTkButton(statsWindow, text='Back', command=backPressed)  # creates back button
    backButton.pack(pady=10)  # displays back button with padding

    statsWindow.mainloop()  # starts the window event loop

# MARK: - ACHIEVEMENTS WINDOW

def achievementsWindow(username, settings):
    achievementsWindow = customtkinter.CTk()  # creates new window
    achievementsWindow.geometry('850x600')  # sets window size
    achievementsWindow.title('Amazing Dice - Achievements')  # sets window title

    titleLabel = customtkinter.CTkLabel(achievementsWindow, text=f"Achievements for {username}", font=('Arial Bold', 30))  # creates title with username
    titleLabel.pack(pady=10)  # actuaklky display

    accountLabel = customtkinter.CTkLabel(achievementsWindow, text=f'Signed in as: {username}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # put in corner (top right)

    achievements = ad.getAchievements(username) # get achievements data
    allAchievements = ad.loadAchievements()['achievements'] # loads achievements bit of achievements file bit dumb that i need [achievements] imo
    totalAchievements = len(allAchievements) # get total achievements using len of list
    unlockedAchievements = len(achievements) # get unlocked achievements using same method

    progressFrame = customtkinter.CTkFrame(achievementsWindow) # make progress frame
    progressFrame.pack(pady=10, padx=20, fill="x") 

    achievementCountLabel = customtkinter.CTkLabel(progressFrame, text=f"Unlocked: {unlockedAchievements}/{totalAchievements}", font=('Arial Bold', 15)) # show unlocked vs total
    achievementCountLabel.pack(pady=10)

    progressBar = customtkinter.CTkProgressBar(progressFrame, width=400) # make progress bar
    progressBar.pack(pady=5)
    
    progressValue = unlockedAchievements / totalAchievements
    progressBar.set(progressValue) # set progress bar to the progress value

    scrollFrame = customtkinter.CTkScrollableFrame(achievementsWindow, width=600, height=350)
    scrollFrame.pack(pady=10, padx=20, fill="both", expand=True) # make scroillable frame for unlocked achievements

    achievementsLabel = customtkinter.CTkLabel(scrollFrame, text="Unlocked Achievements", font=('Arial Bold', 18))
    achievementsLabel.pack(pady=10) # make label to shgow unlocked achievements

    for achievement in achievements:
        achievementFrame = customtkinter.CTkFrame(scrollFrame, fg_color=("gray85", "gray25"))
        achievementFrame.pack(pady=5, padx=10, fill="x") # make frame for achievement

        achievementNameLabel = customtkinter.CTkLabel(achievementFrame, text=achievement['name'], font=('Arial Bold', 15))
        achievementNameLabel.pack(pady=5, padx=10, anchor="w") # make label for name

        achievementDescLabel = customtkinter.CTkLabel(achievementFrame, text=achievement['description'], font=('Arial', 12))
        achievementDescLabel.pack(pady=5, padx=10, anchor="w") # make label for description with user achievement data

        dateLabel = customtkinter.CTkLabel(achievementFrame, text=f"Unlocked: {achievement.get('date', 'Unknown date')}", font=('Arial', 10), text_color="gray") # say when they were unlocked
        dateLabel.pack(pady=5, padx=10, anchor="w")

    lockedLabel = customtkinter.CTkLabel(scrollFrame, text="Locked Achievements", font=('Arial Bold', 18)) # create label to show that achievements below havent been completed
    lockedLabel.pack(pady=10)

    unlockedIds = [achievement.get('id', '') for achievement in achievements] # gets the ids of the unlocked achievements

    userData = ad.loadUsers() # gets data from users file
    userProgress = userData['users'][username]['achievementProgress'] # gets the achievement progress for the user

    for achievementId, achievementData in allAchievements.items(): # loops through all achievements with the id and the data as the like variables
        if achievementId not in unlockedIds:
            achievementFrame = customtkinter.CTkFrame(scrollFrame, fg_color=("gray80", "gray20")) # create frame thats slightly darker than scroll frame for nice background
            achievementFrame.pack(pady=5, padx=10, fill="x")

            if achievementData['secret']: # if the achievement is a secret achievement
                nameText = "???" # show ??? for everything
                descText = "???"
            else:
                nameText = achievementData['name'] # else proper name and description from fetched data
                descText = achievementData['description']

            achievementNameLabel = customtkinter.CTkLabel(achievementFrame, text=nameText, font=('Arial Bold', 15), text_color="gray")
            achievementNameLabel.pack(pady=5, padx=10, anchor="w") # make lkabel for name

            achievementDescLabel = customtkinter.CTkLabel(achievementFrame, text=descText, font=('Arial', 12), text_color="gray")
            achievementDescLabel.pack(pady=5, padx=10, anchor="w") # make label for description
            
            achievementType = achievementData['type'] # get the achievement type
            currentProgress = userProgress.get(achievementType, 0) # gets the current progress for this achievement type with 0 as backup (int)
            requirement = achievementData['requirement'] # gets the requirement for this achievement type (int)
            
            progressDecimal = min(currentProgress / requirement, 1.0) # calculate progrss but maxes at 1.0 with min (tuple as not changed)
            
            achievementProgressBar = customtkinter.CTkProgressBar(achievementFrame, width=750, height=5) #  creates a progress bar
            achievementProgressBar.place(relx=0.5, rely=0.9, anchor="center") # places at bottom
            achievementProgressBar.set(progressDecimal)  # sets value
            
            progressLabelText = f"{currentProgress}/{requirement}" # makes a label showing progress in numbers
            achievementProgressLabel = customtkinter.CTkLabel(achievementFrame, text=progressLabelText, font=('Arial', 10), text_color="gray")
            achievementProgressLabel.place(relx=0.5, rely=0.9, anchor="center")

    def backPressed(): # function if pressed
        achievementsWindow.destroy() # destroys window
        viewStatsWindow(ad.getStats(username), username, settings) # opens the stats window by running its function

    backButton = customtkinter.CTkButton(achievementsWindow, text='Back', command=backPressed) # makes and packs back button
    backButton.pack(pady=10)

    achievementsWindow.mainloop()

# MARK: - MENU 

def menu(guestMode, username, settings):  # defines menu window function that takes guest mode status and username

    menuWindow = customtkinter.CTk()  # creates new window
    menuWindow.geometry('850x600')  # sets window size
    menuWindow.title('Amazing Dice - Menu')  # sets window title

    # settings config

    if settings['theme'] == 'dark': # get theme and set to it
        customtkinter.set_appearance_mode('dark')
    else:
        customtkinter.set_appearance_mode('light')

    titleLabel = customtkinter.CTkLabel(menuWindow, text="Menu", font=('Arial Bold', 30))  # creates menu title
    titleLabel.pack(pady=10)  # displays title with padding

    accountLabel = customtkinter.CTkLabel(menuWindow, text=f'Signed in as: {username if not guestMode else "Guest"}', font=('Arial Bold', 15))  # creates account label
    accountLabel.place(relx=0.95, rely=0.02, anchor='ne')  # positions account label in top right

    messageLabel = customtkinter.CTkLabel(menuWindow, text="", text_color="red")  # creates error message label
    messageLabel.pack(pady=10)  # displays message label with padding
    
    errorCounters = {  # stores how many times an error occured to display to user
        "guestStats": 0
    }

    def statsPressed():  # defines function for stats button
        if not guestMode:  # checks if user is not in guest mode                
            menuWindow.destroy()  # closes menu window
            viewStatsWindow(ad.getStats(username), username, settings)  # opens stats window
        else:
            errorCounters["guestStats"] += 1
            messageLabel.configure(text=f"Guest mode does not have stats ({errorCounters['guestStats']})")  # shows error for guest mode

    def matchPressed():  # defines function for match button
        menuWindow.destroy()  # closes menu window
        matchWindow(username, guestMode, settings)  # opens match window

    def shopPressed():
        menuWindow.destroy()
        shop(username, guestMode, settings)

    def signOutPressed():  # defines function for sign out button
        menuWindow.destroy()  # closes menu window
        home()  # returns to home screen

    def settingsPressed(): # U PREESED SETING
        menuWindow.destroy() # BOOM
        settingsWindow(username, guestMode, settings) #OPENM SUITIINGS WITH USERNAME AND GUESTOMODE SO I CAN KEEP IG IDK AA

    statsButton = customtkinter.CTkButton(menuWindow, text='View Stats', command=statsPressed)  # creates stats button
    statsButton.pack(pady=10)  # displays stats button with padding

    matchButton = customtkinter.CTkButton(menuWindow, text='Match', command=matchPressed)  # creates match button
    matchButton.pack(pady=10)  # displays match button with padding

    shopButton = customtkinter.CTkButton(menuWindow, text='Shop', command=shopPressed, fg_color='gray')  # creates shop button (disabled bc didnt finish shop in time)
    shopButton.pack(pady=10)  # displays shop button with padding

    comingSoonLabel = customtkinter.CTkLabel(menuWindow, text='Coming Soon...', font=('Arial Bold', 15), text_color='gray') # (ts a lie im not finishing ts xd)
    comingSoonLabel.place(relx=0.6, rely=0.35)

    settingsButton = customtkinter.CTkButton(menuWindow, text='Settings', command=settingsPressed)
    settingsButton.pack(pady=10)

    signOutButton = customtkinter.CTkButton(menuWindow, text='Sign Out', command=signOutPressed)  # creates sign out button
    signOutButton.pack(pady=10)  # displays sign out button with padding

    menuWindow.mainloop()  # starts the window event loop

# MARK: - LOGIN

def login(savedUsername, savedPassword):  # defines login window function
    loginWindow = customtkinter.CTk()  # creates new window
    loginWindow.geometry('850x600')  # sets window size
    loginWindow.title('Amazing Dice - Login')  # sets window title

    titleLabel = customtkinter.CTkLabel(loginWindow, text='Login to your account', font=('Arial Bold', 30))  # creates login title
    titleLabel.pack(pady=10)  # displays title with padding

    messageLabel = customtkinter.CTkLabel(loginWindow, text="", text_color="red")  # creates error message label
    messageLabel.pack(pady=10)  # displays message label with padding

    # Error counters for different types of errors
    error_counters = {
        "emptyFields": 0,
        "invalidCredentials": 0,
        "quickLogin": 0,
        "keyringFailure": 0
    }

    def backPressed():  # defines function for back button
        loginWindow.destroy()  # closes login window
        home()  # returns to home screen

    def onEnter(event):  # defines function for enter key press
        loginPress()  # triggers login button press

    def loginPress():  # defines function for login button
        username = usernameField.get()  # gets username from input field
        password = passwordField.get()  # gets password from input field

        if username == savedUsername and ad.hashPassword(password) == savedPassword: # if username is saved username and password is saved password
            loginWindow.destroy()
            settings = ad.getUserSettings(username) # gets user settings
            menu(False, username, settings) # logs in with saved settings
            return
        
        
        if username == savedUsername and not password: # if trying to use saved username but with empty password field will attempt to use keyring auto login
            try: # try to get the password from keyring
                storedPassword = keyring.get_password("AmazingDice", username)
                if storedPassword and ad.login(username, storedPassword): # if password is found and is valid
                    settings = ad.getUserSettings(username) # gets user settings and stores in variable called settings
                    loginWindow.destroy()
                    menu(False, username, settings) # opens menu with logged in user and saved settings
                    return
                else:
                    error_counters["keyringFailure"] += 1
                    messageLabel.configure(text=f"Please enter your password ({error_counters['keyringFailure']})", text_color="red") # shows error for failed login
            except:
                error_counters["keyringFailure"] += 1
                messageLabel.configure(text=f"Please enter your password ({error_counters['keyringFailure']})", text_color="red")
                pass  # js continue normal stuff if keyring fails
        
        if not username or not password:  # checks if fields are empty
            error_counters["emptyFields"] += 1
            messageLabel.configure(text=f"Please fill in all fields ({error_counters['emptyFields']})", text_color="red")  # shows error for empty fields
            return  # exits function so other if statements dont run
            
        if ad.login(username, password):  # attempts to log in with credentials normally
            settings = ad.getUserSettings(username) # gets user settings and stores in variable called settings
            loginWindow.destroy()  # closes login window if successful
            if rememberMe.get(): # if remember me is checked
                ad.saveLogin(username, password) # saves login if remember me is checked
            else: # if not checked
                ad.saveLogin(username, password, False) # runs savelogin with remember me false to trigger deletion of login ( if any stored )
            menu(False, username, settings)  # opens menu with logged in user and saved settings
        else:
            error_counters["invalidCredentials"] += 1
            messageLabel.configure(text=f"Login failed. Check username and password. ({error_counters['invalidCredentials']})", text_color="red")  # shows error for failed login


    usernameField = customtkinter.CTkEntry(loginWindow, placeholder_text='Enter username here', width=200, height=50)  # creates username input field
    usernameField.pack(pady=10)  # displays username field with padding
    usernameField.bind('<Return>', onEnter)  # binds enter key to login function
    
    # Pre-fill username if provided
    if savedUsername:
        usernameField.insert(0, savedUsername)
        messageLabel.configure(text="Username loaded from saved login. Enter your password to continue.", text_color="green")

    passwordField = customtkinter.CTkEntry(loginWindow, placeholder_text='Enter password here', width=200, height=50, show='*')  # creates password input field with hidden text
    passwordField.pack(pady=10)  # displays password field with padding
    passwordField.bind('<Return>', onEnter)  # binds enter key to login function

    rememberMe = customtkinter.CTkCheckBox(loginWindow, text='Remember me')
    rememberMe.pack(pady=10)

    if savedUsername:
        rememberMe.select()  # checks it bc we r loading saved stuff already

    # Add login button with autologin option if we have saved credentials
    if savedUsername:
        loginButtonFrame = customtkinter.CTkFrame(loginWindow)
        loginButtonFrame.pack(pady=5)
        
        loginButton = customtkinter.CTkButton(loginButtonFrame, text='Login', command=loginPress, width=120)
        loginButton.pack(side="left", padx=5)
        
        # Add one-click login button that will attempt to use keyring
        def autoLoginPressed():
            try:
                storedPassword = keyring.get_password("AmazingDice", savedUsername)
                
                if passwordField.get(): # if entered password
                    loginPress() # login normally
                elif storedPassword and ad.login(savedUsername, storedPassword) and savedUsername == usernameField.get(): # else if stored password is right and username is right
                    settings = ad.getUserSettings(savedUsername)
                    loginWindow.destroy()
                    menu(False, savedUsername, settings) # open menu with saved settings (logging in but skipping login process)
                else:
                    error_counters["quickLogin"] += 1
                    messageLabel.configure(text=f"Quick login failed. Please enter your password. ({error_counters['quickLogin']})", text_color="red")
            except:
                error_counters["quickLogin"] += 1
                messageLabel.configure(text=f"Quick login failed. Please enter your password. ({error_counters['quickLogin']})", text_color="red")
                
        autoLoginButton = customtkinter.CTkButton(loginButtonFrame, text='Quick Login', command=autoLoginPressed, width=120, fg_color="green")
        autoLoginButton.pack(side="left", padx=5)
    else:
        loginButton = customtkinter.CTkButton(loginWindow, text='Login', command=loginPress)
        loginButton.pack(pady=10)  # displays login button with padding

    backButton = customtkinter.CTkButton(loginWindow, text='Back', command=backPressed)  # creates back button
    backButton.pack(pady=10)  # displays back button with padding

    loginWindow.mainloop()  # starts the window event loop

# MARK: - CREATE ACCOUNT

def createAccountWindow():  # defines create account window function
    createAccountWindow = customtkinter.CTk()  # creates new window
    createAccountWindow.geometry('850x600')  # sets window size
    createAccountWindow.title('Amazing Dice - Create Account')  # sets window title

    titleLabel = customtkinter.CTkLabel(createAccountWindow, text='Create your account', font=('Arial Bold', 30))  # creates title
    titleLabel.pack(pady=10)  # displays title with padding

    messageLabel = customtkinter.CTkLabel(createAccountWindow, text="", text_color="red")  # creates error message label
    messageLabel.pack(pady=10)  # displays message label with padding

    # Error counters for different types of errors
    error_counters = {
        "emptyFields": 0,
        "passwordRequirements": 0,
        "usernameExists": 0
    }

    def backPressed():  # defines function for back button
        createAccountWindow.destroy()  # closes create account window
        home()  # returns to home screen

    def onEnter(event):  # defines function for enter key press
        createAccountPressed()  # triggers create account button press

    def createAccountPressed():  # defines function for create account button
        username = usernameField.get()  # gets username from input field
        password = passwordField.get()  # gets password from input field

        if not username or not password:  # checks if fields are empty
            error_counters["emptyFields"] += 1
            messageLabel.configure(text=f"Please fill in all fields ({error_counters['emptyFields']})")  # shows error for empty fields
            return  # exits function

        if not (len(password) >= 12 and  # checks password requirements
              any(c.isdigit() for c in password) and  # must contain a number
              any(c.isupper() for c in password) and  # must contain uppercase
              any(c.islower() for c in password) and  # must contain lowercase
              any(c in r'!#$%&()*+,-./:;<=>?@[]^_`{|}~\'"' for c in password)):  # must contain special character
            error_counters["passwordRequirements"] += 1
            messageLabel.configure(text=f"Password must be at least 12 characters and contain uppercase lowercase numbers and special characters ({error_counters['passwordRequirements']})")  # shows error for invalid password
            return  # exits function

        if ad.createAccount(username, password):  # attempts to create account
            createAccountWindow.destroy()  # closes window if successful
            if rememberMe.get(): # if remember me is checked
                ad.saveLogin(username, password) # saves login if remember me is checked
            else: # if not checked
                ad.saveLogin(username, password, False) # runs savelogin with remember me false to trigger deletion of login ( if any stored )
            menu(False, username, {'fastRoll': False, 'theme': 'light'})  # opens menu with new account
        else:
            error_counters["usernameExists"] += 1
            messageLabel.configure(text=f"Username already exists, please choose another ({error_counters['usernameExists']})")

    usernameField = customtkinter.CTkEntry(createAccountWindow, placeholder_text='Enter username here', width=200, height=50)  # creates username input field
    usernameField.pack(pady=10)  # displays username field with padding
    usernameField.bind('<Return>', onEnter)  # binds enter key to create account function

    passwordField = customtkinter.CTkEntry(createAccountWindow, placeholder_text='Enter password here', width=200, height=50, show='*')  # creates password input field with hidden text
    passwordField.pack(pady=10)  # displays password field with padding
    passwordField.bind('<Return>', onEnter)  # binds enter key to create account function

    rememberMe = customtkinter.CTkCheckBox(createAccountWindow, text='Remember me:')
    rememberMe.pack(pady=10)

    createAccountButton = customtkinter.CTkButton(createAccountWindow, text='Create Account', command=createAccountPressed)  # creates create account button
    createAccountButton.pack(pady=10)  # displays create account button with padding

    backButton = customtkinter.CTkButton(createAccountWindow, text='Back', command=backPressed)  # creates back button
    backButton.pack(pady=10)  # displays back button with padding

    createAccountWindow.mainloop()  # starts the window event loop

# MARK: - HOME

def home():  # defines home window function
    homeWindow = customtkinter.CTk()  # creates new window
    homeWindow.geometry('850x600')  # sets window size
    homeWindow.title('Amazing Dice')  # sets window title

    defaultSettings = {'fastRoll': False, 'theme': 'light'}

    customtkinter.set_appearance_mode(defaultSettings['theme'])

    titleLabel = customtkinter.CTkLabel(homeWindow, text='Welcome to Amazing Dice', font=('Arial Bold', 30))  # creates welcome title
    titleLabel.pack(pady=10)  # displays title with padding

    def loginPressed():  # defines function for login button
        homeWindow.destroy()  # closes home window
        savedLogin = ad.checkSavedLogin()
        if savedLogin[0]:
            login(savedLogin[1], savedLogin[2])  # opens login window
        else:
            login(None, None)  # opens login window

    def createAccountPressed():  # defines function for create account button
        homeWindow.destroy()  # closes home window
        createAccountWindow()  # opens create account window

    def guestPressed():  # defines function for guest mode button
        homeWindow.destroy()  # closes home window
        menu(True, 'Guest', defaultSettings)  # opens menu in guest mode

    loginButton = customtkinter.CTkButton(homeWindow, text="Login", command=loginPressed)  # creates login button
    loginButton.pack(pady=10)  # displays login button with padding

    createAccountButton = customtkinter.CTkButton(homeWindow, text="Create Account", command=createAccountPressed)  # creates create account button
    createAccountButton.pack(pady=10)  # displays create account button with padding

    guestButton = customtkinter.CTkButton(homeWindow, text="Guest Mode", command=guestPressed)  # creates guest mode button
    guestButton.pack(pady=10)  # displays guest mode button with padding

    homeWindow.mainloop()  # starts the window event loop

# MARK: - MAIN

if __name__ == "__main__":  # checks if file is being run directly( NOT IJMKPOROIT) AAA I  IFNALTY DID ALL THE TAGS YAYAYAAA
    ad.start()  # starts IT