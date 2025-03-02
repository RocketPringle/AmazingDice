# This imports the library and gives it a shorter name 'ctk' to use
import customtkinter as ctk  # type: ignore # A modern-looking GUI library based on tkinter
import amazingDice as ad

# ------ MENU SCREEN FUNCTIONS ------ #

def menu(guestMode, username):
    menuWindow = ctk.CTk()
    menuWindow.geometry('600x500')
    menuWindow.title('Amazing Dice - Menu :3')

    menuWindow.mainloop()

# ------ LOGIN SCREEN FUNCTIONS ------ #

def login(loop):
    if loop:
        loginWindow.destroy()

    loginWindow = ctk.CTk()
    loginWindow.geometry('600x500')
    loginWindow.title('Amazing Dice - Login')

    messageLabel = ctk.CTkLabel(loginWindow, text="", text_color="red")
    messageLabel.pack(pady=10)

    def backPressed():
        loginWindow.destroy()
        home()

    def loginPress():
        username = usernameField.get()
        password = passwordField.get()
        
        if not username or not password:
            messageLabel.configure(text="Please fill in all fields!")
            return
            
        if ad.login(username, password):
            loginWindow.destroy()
            menu(False, username)
        else:
            messageLabel.configure(text="Login failed! Check username and password.")

    loginLabel = ctk.CTkLabel(loginWindow, text='Login to your account!', font=('Arial Bold', 40))
    loginLabel.pack(pady=20)

    usernameField = ctk.CTkEntry(loginWindow, placeholder_text='Enter username here...', width=200, height=50)
    usernameField.pack(pady=10)

    passwordField = ctk.CTkEntry(loginWindow, placeholder_text='Enter password here...', width=200, height=50, show='*')
    passwordField.pack(pady=10)

    loginButton = ctk.CTkButton(loginWindow, text='Login', command=loginPress)
    loginButton.pack(pady=20)

    backButton = ctk.CTkButton(loginWindow, text='Back', command=backPressed)
    backButton.pack(pady=20)

    loginWindow.mainloop()

# ------ CREATE ACCOUNT FUNCTIONS ------ #

def createAccountWindow(loop):
    if loop:
        createAccountWindow.destroy()

    createAccountWindow = ctk.CTk()
    createAccountWindow.geometry('600x500')
    createAccountWindow.title('Amazing Dice - Create Account')

    titleLabel = ctk.CTkLabel(createAccountWindow, text='Create your account!', font=('Arial Bold', 40))
    titleLabel.pack(pady=20)

    messageLabel = ctk.CTkLabel(createAccountWindow, text="", text_color="red")
    messageLabel.pack(pady=10)

    def backPressed():
        createAccountWindow.destroy()
        home()

    def createAccountPressed():

        username = usernameField.get()
        password = passwordField.get()

        if not username or not password:
            messageLabel.configure(text="Please fill in all fields!")
            return

        if ad.createAccount(username, password):
            createAccountWindow.destroy()
            menu(False, username)

    usernameField = ctk.CTkEntry(createAccountWindow, placeholder_text='Enter username here...', width=200, height=50)
    usernameField.pack(pady=10)

    passwordField = ctk.CTkEntry(createAccountWindow, placeholder_text='Enter password here...', width=200, height=50, show='*')
    passwordField.pack(pady=10)

    createAccountButton = ctk.CTkButton(createAccountWindow, text='Create Account', command=createAccountPressed)
    createAccountButton.pack(pady=20)

    backButton = ctk.CTkButton(createAccountWindow, text='Back', command=backPressed)
    backButton.pack(pady=20)

    createAccountWindow.mainloop()
    
    


# ------ HOME SCREEN FUNCTIONS ------ #

def home():

    homeWindow = ctk.CTk()
    homeWindow.geometry('600x500')
    homeWindow.title('Amazing Dice!')

    titleLabel = ctk.CTkLabel(homeWindow, text='Welcome to Amazing Dice!', font=('Arial Bold', 40))
    titleLabel.pack(pady=20)

    def loginPressed():
        print('login clicked')
        homeWindow.destroy()
        login(False)

    def createAccountPressed():
        print('create account clicked')
        homeWindow.destroy()
        createAccountWindow(False)

    def guestPressed():
        print('guest clicked')
        homeWindow.destroy()
        menu(True, 'Guest')
        



    loginButton = ctk.CTkButton(homeWindow, text="Login", command=loginPressed)
    loginButton.pack(pady=20)

    createAccountButton = ctk.CTkButton(homeWindow, text="Create Account", command=createAccountPressed)
    createAccountButton.pack(pady=20)

    guestButton = ctk.CTkButton(homeWindow, text="Guest Mode", command=guestPressed)
    guestButton.pack(pady=20)

    homeWindow.mainloop()


