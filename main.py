#IDEAS(GUI): settings, help, customise for light/dark mode

#IDEAS(SECURITY): password strength/breach checker - length check, character diversity, overall score out of 100

#OTHER: also have a password generator, password manager, potentially AI password improver, size parameter could fix the cut off text issue, eventually make it resizable

import customtkinter as ctk
import hashlib
import requests

WIDTH = 600
HEIGHT = 400
FONT = "Helvetica Neue Medium"
CORNER_RADIUS = 3
PLACEHOLDER_TEXT_SIZE = 15

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.password_checker = password_checker
        self.title("PassPy")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self._set_appearance_mode("light") # Modes: "system" (default), "dark", "light"
        self.resizable(False, False) 
        #self.iconbitmap("assets/icon.ico")
            
        def show_text():
            if self.password_entry.cget("show") == "*":
                self.password_entry.configure(show="")
                self.show_button.configure(text="Hide")
            else:
                self.password_entry.configure(show="*")
                self.show_button.configure(text="Show")

        #instantiate the GUI elements
        self.password_entry = ctk.CTkEntry(self, corner_radius=CORNER_RADIUS, placeholder_text="Password", width=200, show="*", font=(FONT, PLACEHOLDER_TEXT_SIZE))
        self.show_button = ctk.CTkButton(self, text="Show", command=show_text, font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.enter_button = ctk.CTkButton(self, text="Enter", command=password_checker.update_password, font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.title_lbl = ctk.CTkLabel(self, text="PassPy", font=(FONT, 28), text_color="black")
        self.enter_pass_lbl = ctk.CTkLabel(self, text="Enter Password", font=(FONT, 20), text_color="black")
        self.credit_lbl = ctk.CTkLabel(self, text="A password strength checker by Harry Johnson.", font=(FONT, 12), text_color="dark grey")

        #place the GUI elements
        self.password_entry.place(relx=0.29, rely=0.24, anchor="sw")
        self.enter_button.place(relx=0.64, rely=0.24, anchor="sw")
        self.show_button.place(relx=0.75, rely=0.24, anchor="sw")
        self.title_lbl.place(relx=0.03, rely=0.12, anchor="sw")
        self.enter_pass_lbl.place(relx=0.03, rely=0.24, anchor="sw")
        self.credit_lbl.place(relx=0.2, rely=0.14, anchor="sw")
    
        self.password_entry.bind("<Return>", lambda event: password_checker.update_password())

class Password_checker:
    def __init__(self):
        self.password = ""
        self.password_length = len(self.password)
        self.breaches = 0
        self.common = False
        self.score = 100
        self.password_issues = []
        self.common_passwords = set()
        self.load_common_passwords()

    def load_common_passwords(self, path="rockyou.txt"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as rockyou_file:
                self.common_passwords = set(line.strip() for line in rockyou_file)
        except FileNotFoundError:
            print("rockyou.txt not found. Common password check will be disabled.")

    def password_breaches(self):
        hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest().upper() # Hash the password to the API's required format
        password_hash_prefix, password_hash_suffix = hash[:5], hash[5:] # Split the hash into prefix and suffix
        url = f"https://api.pwnedpasswords.com/range/{password_hash_prefix}" # API takes the first 5 characters of the SHA-1 hash
        response = requests.get(url)
        if response.status_code != 200:
            print("Network error")#raise RuntimeError(f"Error fetching data: {response.status_code}")
        for line in response.text.splitlines():
            current_hash_suffix, breach_count = line.split(":") # each line contains the hash suffix and the count of breaches
            if current_hash_suffix == password_hash_suffix: #if the suffix matches the password's suffix, return True and the amount of breaches
                return int(breach_count)
        return 0 # if the suffix of the passwords hash was not found, return 0 breaches

    def check_common_passwords(self):
        return self.password in self.common_passwords

    def regular_checks(self):
        if self.password_length < 16:
            #score = 100 - (16 - len(self.password)) * 5
            self.password_issues.append(f"Your password is just {self.password_length} characters long. To maximise complexity should be at least 16 characters.")
             
        if not any(char.isdigit() for char in self.password):
            "Password must contain at least one digit."

        if not any(char.isalpha() for char in self.password):
            "Password must contain at least one letter."

        if not any(char.isupper() for char in self.password):
            "Password must contain at least one uppercase letter."

        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in self.password):
            "Password must contain at least one special character."


    def check_password_strength(self):
        self.breaches = self.password_breaches()
        self.common = self.check_common_passwords()
        self.regular_checks()
        print(self.breaches, self.common)

    def update_password(self):
        if not app.password_entry.get() == "":
            self.password = app.password_entry.get()
            self.password_length = len(self.password)
            app.password_entry.delete(0, 'end')  # Clear the entry field after getting the password
            app.password_entry.configure(show="*")
            self.score = 100
            self.check_password_strength()
        else:
            print("Please enter a password. Add this to the UI later")


password_checker = Password_checker()
app = App()
app.mainloop()
