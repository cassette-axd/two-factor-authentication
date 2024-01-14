# This class will create the windows used for the front end of this application
from tkinter import *
from tkinter import messagebox
import re
import json
import time
import pyotp
import qrcode

#first page to open up where users can sign in to their account
class LoginWindow:
    def __init__(self, master):
        master.config(padx=50, pady=50)
        canvas = Canvas(master, width=200, height=200)
        canvas.grid(column=1, row=0) 

        username_text = Label(text="Username:")
        username_text.grid(column=0, row=1)

        password_text = Label(text="Password:")
        password_text.grid(column=0, row=2)

        self.username = StringVar()
        self.username_entry = Entry(textvariable=self.username, width=30)
        self.username_entry.grid(column=1, row=1)

        self.password = StringVar()
        self.password_entry = Entry(textvariable=self.password, width=30, show="*")
        self.password_entry.grid(column=1, row=2)

        login_button = Button(text="LOGIN", width=28, command=self.login)
        login_button.grid(column=1, row=3)

        create_account_button = Button(text="Create New Account", width=28, command=self.create_new_account)
        create_account_button.grid(column=1, row=4)

        forgot_password_button = Button(text="Forgot Password?", width=10, command=self.forgot_password)
        forgot_password_button.grid(column=2, row=2)

    def create_new_account(self):
        new_account_window = CreateAccountWindow()

    def forgot_password(self):
        enter_email_window = EnterEmailWindow()
        

    # try to log the user into their account
    def login(self):
        try:
            with open("data.json", "r") as data_file:
                # read data
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="Error""\nData File not Found")
        else:
            username = self.username_entry.get()
            password = self.password_entry.get()

            # check if website is stored in data
            if self.username_entry.get() == "" or self.password_entry == "":
                messagebox.showinfo(title="Error", message="Error""\nSome of your entries are blank")
            if username in data:
                # get the info for that website in the nested dictionary and display it in a popup
                if data[username]["Password"] == password:
                    messagebox.showinfo(title="Verification Code Sent", message="Scan the QR Code to recieve the verification code")
                    two_factor = TwoFactorWindow(username)
                    
                else:
                    messagebox.showinfo(title="Error", message="Invalid Password")
            else:
                messagebox.showinfo(title="Error", message="Invalid Username")
        

# Begin two-factor authentication here
class TwoFactorWindow:
    def __init__(self, username):

        key = "MySuperSecretKey"
        self.totp = pyotp.TOTP(key)
        code = self.totp.now()
        print(code)

        uri = pyotp.totp.TOTP(key).provisioning_uri(name=username, issuer_name="Two-Factor Authentication")
        qrcode.make(uri).save("totp.png")

        top = Toplevel()
        canvas = Canvas(top, width=200, height=200)
        canvas.grid(column=1, row=0)

        code_text = Label(top, text="Enter Code:")
        code_text.grid(column=0, row=2)

        self.code = StringVar()
        self.code_entry = Entry(top, textvariable=self.code, width=30)
        self.code_entry.grid(column=1, row=2)

        verify_button = Button(top, text="verify", width=6, command=self.verify_code)
        verify_button.grid(column=2,row=2)

    def verify_code(self):
        verified = self.totp.verify(self.code_entry.get())
        if verified:
            messagebox.showinfo(title="Success", message="Login Successful")
        elif verified == False:
            messagebox.showinfo(title="Error", message="Invalid Code Entered")


# open a new window to enter email
class EnterEmailWindow:
    def __init__(self):
        top = Toplevel()
        canvas = Canvas(top, width=200, height=200)
        canvas.grid(column=1, row=0) 
        
        email_text = Label(top, text="Enter Email:")
        email_text.grid(column=0, row=2)

        self.email = StringVar()
        self.email_entry = Entry(top, textvariable=self.email, width=30)
        self.email_entry.grid(column=1, row=2)

        submit_email_button = Button(top, text="submit", width=6, command=self.submit_email)
        submit_email_button.grid(column=2, row=2)

    def submit_email(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if str(re.match(regex, self.email.get())) == "None":
            messagebox.showinfo(title="Error", message="Error""\nEmail is invalid")

        try:
            with open("data.json", "r") as data_file:
                # read data
                data = json.load(data_file)
        except FileNotFoundError:
                messagebox.showinfo(title="Error", message="Error""\nNo accounts have been created")
        else:
            # check if input is stored in data
            found = FALSE
            for user, user_data in data.items():
                if user_data['Email'] == self.email.get():
                    # messagebox.showinfo(title="Success", message="sent email")
                    create_new_password_window = ResetPassword(user_data['Email'], user_data['Budget'], user_data['Money Spent'])
                    found = TRUE
                    self.email_entry.delete(0, END)
                    break
            if found == FALSE:
                messagebox.showinfo(title="Error", message="Error""\ncouldn't find email")

# Update password after confirming email
class ResetPassword:
    def __init__(self, email, budget, money_spent):
        self.email = email
        self.budget = budget
        self.money_spent = money_spent
        top = Toplevel()
        canvas = Canvas(top, width=200, height=200)
        canvas.grid(column=1, row=0)
        password_text = Label(top, text="Create new Password:")
        password_text.grid(column=0, row=2)

        password_text_2 = Label(top, text="Re-Enter New Password:")
        password_text_2.grid(column=0, row=3)

        self.password1 = StringVar()
        self.password_entry = Entry(top, textvariable=self.password1, width=30, show="*")
        self.password_entry.grid(column=1, row=2)

        self.password2 = StringVar()
        self.password_entry_2 = Entry(top, textvariable=self.password2, width=30, show="*")
        self.password_entry_2.grid(column=1, row=3)

        submit_passwords_button = Button(top, text="submit", width=28, command=self.reset_password)
        submit_passwords_button.grid(column=1, row=4)

    def reset_password(self):
        if self.password1.get() != self.password2.get():
            messagebox.showinfo(title="Error", message="Error""\nPasswords don't match")
        elif self.password1.get() == "" or self.password2.get() == "":
            messagebox.showinfo(title="Error", message="Error""\nSome of your entries are blank")
        else:
            # messagebox.showinfo(title="Reminder", message="Reminder""\nEdit the JSON file to rewrite the user's password")
            try:
                with open("data.json", "r") as data_file:
                    # read data
                    data = json.load(data_file)
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="Error""\nData File not Found")
            else:
                for user, user_data in data.items():
                    if user_data['Email'] == self.email:
                        updated_account = {
                            user: {
                                "Email": self.email,
                                "Password":  self.password1.get()
                            }
                        }
                try:
                    with open("data.json", "r") as data_file:
                        # read old data
                        data = json.load(data_file)
                # create a new json data file if it doesn't currently exist
                except FileNotFoundError:
                    with open("data.json", "w") as data_file:
                        json.dump(updated_account, data_file, indent=4)
                else:
                    # update old data with new data
                    data.update(updated_account)

                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                    messagebox.showinfo(title="Success", message="Success""\nPassword updated Successfully")

# Open a new window for user to create a new account
class CreateAccountWindow:
    def __init__(self):
        top = Toplevel()
        canvas = Canvas(top, width=200, height=200)
        canvas.grid(column=1, row=0) 

        username_text = Label(top, text="Enter Username:")
        username_text.grid(column=0, row=1)
        
        email_text = Label(top, text="Enter Email:")
        email_text.grid(column=0, row=2)

        password_text = Label(top, text="Enter Password:")
        password_text.grid(column=0, row=3)

        password_text_2 = Label(top, text="Re-Enter Password:")
        password_text_2.grid(column=0, row=4)

        self.username = StringVar()
        self.username_entry = Entry(top, textvariable=self.username, width=30)
        self.username_entry.grid(column=1, row=1)

        self.email = StringVar()
        self.email_entry = Entry(top, textvariable=self.email, width=30)
        self.email_entry.grid(column=1, row=2)

        self.password1 = StringVar()
        self.password_entry = Entry(top, textvariable=self.password1, width=30, show="*")
        self.password_entry.grid(column=1, row=3)

        self.password2 = StringVar()
        self.password_entry_2 = Entry(top, textvariable=self.password2, width=30, show="*")
        self.password_entry_2.grid(column=1, row=4)

        save_info_button = Button(top, text="Create Account", width=28, command=self.submit)
        save_info_button.grid(column=1, row=5)

    def save_info(self):
        stored_accounts = {
            self.username.get(): {
                "Email": self.email.get(),
                "Password":  self.password1.get()
            }
        }
        # store data as a json file
        try:
            with open("data.json", "r") as data_file:
                # read old data
                data = json.load(data_file)
        # create a new json data file if it doesn't currently exist
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(stored_accounts, data_file, indent=4)
        else:
            # update old data with new data
            data.update(stored_accounts)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        # clear text boxes regardless of what happens
        finally:
            messagebox.showinfo(title="success", message="Your New Account Has Been Created")
            self.username_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.password_entry.delete(0, END)
            self.password_entry_2.delete(0, END)

    def submit(self):
        # first check if account information already exists
        try:
            with open("data.json", "r") as data_file:
                # read data
                data = json.load(data_file)
        except FileNotFoundError:
                pass
        else:
            # check if input is stored in data
            if self.username.get() in data:
                messagebox.showinfo(title="Error", message="Error""\nUsername already exists")
            for user, user_data in data.items():
                if user_data['Email'] == self.email.get():
                    messagebox.showinfo(title="Error", message="Error""\nEmail already exists")
            
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        # then check if given ivalid input
        if self.password1.get() != self.password2.get():
            messagebox.showinfo(title="Error", message="Error""\nPasswords don't match")
        elif self.username.get() == "" or self.email.get() == "" or self.password1.get() == "" or self.password2.get() == "":
            messagebox.showinfo(title="Error", message="Error""\nSome of your entries are blank")
        elif str(re.match(regex, self.email.get())) == "None":
            messagebox.showinfo(title="Error", message="Error""\nEmail is invalid")
        else:
            # if all input is valid, store it in a dictionary
            self.save_info()