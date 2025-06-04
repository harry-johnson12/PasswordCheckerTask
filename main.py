#IDEAS(GUI): settings, help, about, customise for light/dark mode

#IDEAS(SECURITY): patterns such as aaaaa 1234 ect

#OTHER: also have a password generator, password manager, potentially AI password improver, size parameter could fix the cut off text issue, eventually make the window resizable

import customtkinter as ctk
import hashlib
import requests
import math

WIDTH = 600
HEIGHT = 400
FONT = "Helvetica Neue Medium"
CORNER_RADIUS = 3
PLACEHOLDER_TEXT_SIZE = 13

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
        self.password_strength_bar = ctk.CTkProgressBar(self, width=492, height=10, corner_radius=CORNER_RADIUS, mode="determinate", fg_color="", progress_color="", orientation="horizontal")
        self.password_strength_label = ctk.CTkLabel(self, text="", font=(FONT, 14), text_color="black")
        self.password_feedback = ctk.CTkTextbox(self, width=550, height=120, corner_radius=CORNER_RADIUS, font=(FONT, 12), state="disabled", fg_color="transparent", text_color="dark grey", scrollbar_button_color="light grey", wrap="word")
        self.time_to_crack_label = ctk.CTkLabel(self, text="", font=(FONT, 13), text_color="black")
        self.title_lbl = ctk.CTkLabel(self, text="PassPy", font=(FONT, 28), text_color="black")
        self.enter_pass_lbl = ctk.CTkLabel(self, text="Enter Password", font=(FONT, 20), text_color="black")
        self.credit_lbl = ctk.CTkLabel(self, text="A password strength checker by Harry Johnson.", font=(FONT, 12), text_color="dark grey")

        self.password_strength_bar.set(0/100)  # Initialize the progress bar to 0

        #place the GUI elements
        self.password_entry.place(relx=0.29, rely=0.24, anchor="sw")
        self.enter_button.place(relx=0.64, rely=0.24, anchor="sw")
        self.show_button.place(relx=0.75, rely=0.24, anchor="sw")
        self.password_strength_bar.place(relx=0.03, rely=0.39, anchor="sw")
        self.password_strength_label.place(relx=0.03, rely=0.34, anchor="sw")
        self.password_feedback.place(relx=0.03, rely=0.43, anchor="nw") #nw so it dosent change position with the height
        self.title_lbl.place(relx=0.03, rely=0.12, anchor="sw")
        self.enter_pass_lbl.place(relx=0.03, rely=0.24, anchor="sw")
        self.credit_lbl.place(relx=0.2, rely=0.14, anchor="sw")
    
        self.password_entry.bind("<Return>", lambda event: password_checker.update_password())

class Password_checker:
    def __init__(self):
        self.password = ""
        self.saved_password = self.password
        self.password_length = len(self.password)
        self.password_strength = "Weak"
        self.breaches = 0
        self.common = False
        self.score = 100
        self.password_issues = []
        self.time_to_crack_seconds = 0
        self.load_common_passwords()
        self.load_dictionary_words()

    def load_common_passwords(self, path="rockyou.txt"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as rockyou_file:
                self.common_passwords = set(line.strip() for line in rockyou_file)
        except FileNotFoundError:
            print("rockyou.txt not found. Common password check will be disabled.")

    def load_dictionary_words(self, path="10,000_common_words.txt"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as dictionary_file:
                clean_words = set()

                for word in dictionary_file:
                    stripped = word.strip()
                    if len(stripped) >= 4:
                        clean_words.add(stripped.lower())

                self.dictionary_words = clean_words            
        except FileNotFoundError:
            print("words_alpha.txt not found. dictionary password check will be disabled.")
        
    def password_breaches(self):
        hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest().upper() # Hash the password to the API's required format
        password_hash_prefix, password_hash_suffix = hash[:5], hash[5:] # Split the hash into prefix and suffix
        url = f"https://api.pwnedpasswords.com/range/{password_hash_prefix}" # API takes the first 5 characters of the SHA-1 hash
        try:
            response = requests.get(url)
            for line in response.text.splitlines():
                current_hash_suffix, breach_count = line.split(":") # each line contains the hash suffix and the count of breaches
                if current_hash_suffix == password_hash_suffix: #if the suffix matches the password's suffix, return True and the amount of breaches
                    if int(breach_count) > 0:
                        self.password_issues.append(f"Your password has been found in {breach_count} data breaches.")
                        self.score -= 100
                    return int(breach_count)
            return 0 # if the suffix of the passwords hash was not found, return 0 breaches
        except:
                self.password_issues.append("There was an error connecting to the API, your passsword may or may not be compromised.")

    def check_common_passwords(self):
        if self.password in self.common_passwords:
            self.password_issues.append("Your password is commonly used in brute force attacks.")
            self.score -= 100
        return self.password in self.common_passwords

    def check_for_dictionary_words(self):
        self.word_count = 0
        containing_words = []
        for word in self.dictionary_words:
            if word in self.password.lower():
                if word == self.password.lower():
                    self.password_issues.append(f"Your password is the just the word '{word}', which is not secure.")
                    self.score -= 80
                else: 
                    self.word_count += 1
                    containing_words.append(word)
                    self.score -= 10
        if self.word_count > 0:
            appending_feedback = "Your password contains: "
            for word in containing_words:
                appending_feedback += f"'{word}', "
            appending_feedback = appending_feedback[:-2] + "."
            appending_feedback += " This makes it easier to guess."
            self.password_issues.append(appending_feedback)

    def length_penalty(self):
        if self.password_length >= 16:
            return 0
        k = 0.25
        penalty = 50 * math.exp(-k * (self.password_length - 8))
        self.password_issues.append(f"Your password is just {self.password_length} characters long. To improve complexity should be at least 16 characters.")
        self.score -= round(min(penalty, 100), 2)

    def check_password_character_diversity(self):
        appending_issue = "Your password should contain a diverse range of characters. It is missing "
        if not any(char.isdigit() for char in self.password):
            appending_issue += "digits, "
            self.score -= 15
        if not any(char.isalpha() for char in self.password):
            appending_issue += "lowercase letters, "
            self.score -= 5
        if not any(char.isupper() for char in self.password):
            appending_issue += "uppercase letters, "
            self.score -= 10
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in self.password):
            appending_issue += "special characters, "
            self.score -= 20
        if appending_issue != "Your password should contain a diverse range of characters. It is missing ":
            appending_issue = appending_issue[:-2] + "."
            self.password_issues.append(appending_issue)

    def calculate_time_to_crack(self):
        charset = 0
        if any(character.islower() for character in self.password): 
            charset += 26 # how many possible characters are in the password
        if any(character.isupper() for character in self.password): 
            charset += 26
        if any(character.isdigit() for character in self.password): 
            charset += 10
        if any(not character.isalnum() for character in self.password): 
            charset += 32 # special characters
        
        combinations = charset ** len(self.password)  # Calculate the total number of combinations
        self.time_to_crack_seconds = combinations / 200000000000  # Assuming 200 billion guesses per second (fast end GPU cracking)
        kfactor = 1.0  # Adjust this factor based on the attacker's capabilities
        if self.time_to_crack_seconds < 0.0001:
            self.time_to_crack_seconds = "instantly"  # Round to 2 decimal places
        else:
            self.time_to_crack_seconds = round(self.time_to_crack_seconds, 2)
                    


    def check_password_strength(self):
        self.password_issues = []
        self.breaches = self.password_breaches()
        self.common = self.check_common_passwords()
        self.length_penalty()
        self.check_for_dictionary_words()
        self.check_password_character_diversity()
        self.calculate_time_to_crack()
        print(f"Time to crack: {(self.time_to_crack_seconds)} seconds")
        if self.score < 0:
            self.score = 0
        
        if self.score == 100:
            bar_colour = "green"
            app.password_strength_label.configure(text="Your password is incredibly strong.")
        if self.score >= 90:
            app.password_strength_label.configure(text="Your password section is very strong, to maximise security, view the below recomendations.")
        if self.score >= 80:
            bar_colour = "light green"
            app.password_strength_label.configure(text="Your password is strong, to maximise security, view the below recomendations.")
        elif self.score >= 50: 
            bar_colour = "yellow"
            app.password_strength_label.configure(text="Your password is average strength, view the issues below to improve your password.")
        elif self.score >= 30:
            bar_colour = "orange"
            app.password_strength_label.configure(text="Your password is weak, change your password.")
        elif self.score > 0:
            bar_colour = "red"
            app.password_strength_label.configure(text="Your password is incredibly weak, change your password.")
        else:
            bar_colour = "light grey"
            app.password_strength_label.configure(text="Your password is incredibly weak, change your password.")

        #configure the password strength bar
        app.password_strength_bar.configure(fg_color="light grey")  # Set the background color of the progress bar
        app.password_strength_bar.configure(progress_color=bar_colour)  # Change color based on score
        app.password_strength_bar.set(self.score / 100)  # Update the progress bar with the score as a percentage

        #configure the feedback text box
        app.password_feedback.configure(state="normal")  # Enable the textbox to update it
        app.password_feedback.configure(fg_color="light grey")  # Set the background color of the feedback textbox
        app.password_feedback.configure(height=len(self.password_issues) * 30)  # Adjust height based on number of issues
        if len(self.password_issues) == 0:
            app.password_feedback.configure(fg_color="transparent")
        app.password_feedback.delete("0.0", "end")  # Clear the textbox before inserting new issues

        for issue in self.password_issues:
            app.password_feedback.insert("end", issue + "\n")
            app.password_feedback.insert("end", "\n")  # Add a newline after each issue for better readability
        app.password_feedback.configure(state="disabled")  # Disable the textbox after updating it

        #configure the time to crack label
        if not len(self.password_issues) == 0:
            calculated_y = 0.44 + (len(self.password_issues*30))/HEIGHT # The initial height down of the feedback box + the decimal of the screen it covers after its hegiht is updated
        else: calculated_y = 0
        if not type(self.time_to_crack_seconds) == str:
            app.time_to_crack_label.configure(text=f"Your password will take: {self.time_to_crack_seconds} seconds to crack.")
        else: app.time_to_crack_label.configure(text=f"Your password will be cracked {self.time_to_crack_seconds}.")
        app.time_to_crack_label.place(relx=0.03, rely=calculated_y, anchor="nw")
   
    def update_password(self):
        if not app.password_entry.get() == "":
            self.saved_password = self.password  # Save the previous password
            self.password = app.password_entry.get()
            self.password_length = len(self.password)
            self.score = 100
            app.password_entry.delete(0, 'end')  # Clear the entry field after getting the password
            app.password_entry.configure(show="*")
            app.show_button.configure(text="Show")
            self.check_password_strength()
        else:
            print("Please enter a password. Add this to the UI later")

password_checker = Password_checker()
app = App()
app.mainloop()
