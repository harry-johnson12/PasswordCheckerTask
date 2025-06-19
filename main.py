import customtkinter as ctk
import hashlib
import requests
import math
import random
import pyperclip
import webbrowser

MAIN_WIDTH = 600
MAIN_HEIGHT = 400
MENU_WIDTH = 250
MENU_HEIGHT = 300
OTHER_WIDTH = 350
OTHER_HEIGHT = 300

FONT = "Avenir Next Medium"
CORNER_RADIUS = 4
PLACEHOLDER_TEXT_SIZE = 13

class Menu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.geometry(f"{MENU_WIDTH}x{MENU_HEIGHT}")
        self.resizable(False, False)
        self._set_appearance_mode("light")
        self.initialize_menu_widgets()
        self.place_menu_widgets()
    
    def show_menu(self):
        for widget in self.winfo_children():
            widget.place_forget()
        self.title("Menu")
        self.geometry(f"{MENU_WIDTH}x{MENU_HEIGHT}")
        self.place_menu_widgets()
    
    def show_help(self):
        for widget in self.winfo_children():
            widget.place_forget()
        self.title("Help")
        self.geometry(f"{OTHER_WIDTH}x{OTHER_HEIGHT}")
        self.help_text.place(relx=0.5, rely=0.06, anchor="n")
        self.back_button.place(relx=0.5, rely=0.85, anchor="n")
    
    def show_about(self):
        for widget in self.winfo_children():
            widget.place_forget()
        self.title("About PassPy")
        self.geometry(f"{OTHER_WIDTH}x{OTHER_HEIGHT}")
        self.about_text.place(relx=0.5, rely=0.06, anchor="n")
        self.back_button.place(relx=0.5, rely=0.85, anchor="n")
    
    def create_links(self, widget, url):
        widget.configure(state="normal")
        start = widget.search(url, "1.0", stopindex="end")
        end = f"{start}+{len(url)}c"
        widget.tag_add("link", start, end)
        widget.tag_config("link", foreground="blue", underline=True)
        widget.tag_bind("link", "<Button-1>", lambda e: webbrowser.open(url))
        widget.configure(state="disabled")

    def generate_password(self):
        self.characters = []
        self.generated_password = ""
        dispersion = random.randint(0, 3)  # Randomly decide the type of character to add
        # Define excluded special character ASCII codes not allowed in passwords
        excluded_codes = {32, 34, 38, 39, 42, 47, 58, 59, 60, 62, 63, 92, 96, 124}
        special_chars = [chr(i) for i in range(33, 127)
            if not chr(i).isalnum() and i not in excluded_codes]

        #decide the amount of each type of character to add based on the dispersion
        if dispersion == 0:
                self.lower_case = 4
                self.uppercase = 4
                self.digits = 4
                self.special_characters = 5
        elif dispersion == 1:
                self.lower_case = 4
                self.uppercase = 4
                self.digits = 5
                self.special_characters = 4
        elif dispersion == 2:
                self.lower_case = 4
                self.uppercase = 5
                self.digits = 4
                self.special_characters = 4
        elif dispersion == 3:
                self.lower_case = 5
                self.uppercase = 4
                self.digits = 4
                self.special_characters = 4
            #first decide the characters in the password, equal amount of each 

                self.generated_password += chr(random.randint(33, 126))  # Generate a random password with characters from ASCII range 33 to 126

        # Generate random characters for each type
        for i in range(self.lower_case):
            self.characters.append(chr(random.randint(97, 122)))
        for i in range(self.uppercase):
            self.characters.append(chr(random.randint(65, 90)))
        for i in range(self.digits):
            self.characters.append(chr(random.randint(48, 57)))
        for i in range(self.special_characters):
            self.characters.append(random.choice(special_chars))  # Randomly select a special character from the list
        
        # Shuffle the characters to create a random password
        random.shuffle(self.characters)
        self.generated_password = "".join(self.characters)  # Join the characters to form the password
        pyperclip.copy(self.generated_password)  # Copy the generated password to the clipboard
    
        self.password_generator_button.configure(text="Copied to clipboard!")
        self.after(2000, lambda: self.password_generator_button.configure(text="Generate Password"))

    def initialize_menu_widgets(self):
        self.menu_title_lbl = ctk.CTkLabel(self, text="Menu", font=(FONT, 25), text_color="black")
        self.help_button = ctk.CTkButton(self, text="Help", command=self.show_help, font=(FONT, 12), width=170, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.about_button = ctk.CTkButton(self, text="About", command=self.show_about, font=(FONT, 12), width=170, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.password_generator_button = ctk.CTkButton(self, text="Generate password", command=self.generate_password, font=(FONT, 12), width=170, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.back_to_menubutton = ctk.CTkButton(self, text="Back", command=self.destroy, font=(FONT, 12), width=170, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.back_button = ctk.CTkButton(self, text="Back", command=self.show_menu, font=(FONT, 12), width=170, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        
        self.help_text = ctk.CTkTextbox(self, width=295, height=220, corner_radius=CORNER_RADIUS, font=(FONT, 11), state="normal", fg_color="light grey", text_color="black", scrollbar_button_color="dark grey", wrap="word")
        self.help_text.insert("0.0", "To use PassPy, simply enter your password into the input field and click 'Enter'. The application will then analyze your password and provide feedback on its strength, including any issues that may make it weak or vulnerable to attacks.\n\nDepending on your internet connection there may be issues connecting to the pwned passwords API, in this case if your password is breached visit:\nhttps://haveibeenpwned.com/Passwords\n\nYou can also view the time it would take to crack your password based on its mathematical complexity, assuming a GPU guess rate of two hundred billion guesses per second however this is not the greatest measure to test security, hence why it is below the feedback feild.\n\nThere is also a button in the menu which will generate and copy a secure password to your clipboard which you can then test and use.\n\nFor more information, visit the GitHub repository (link in the about section) or open an issue if you have any questions or suggestions.")
        self.help_text.configure(state="disabled")
        
        self.about_text = ctk.CTkTextbox(self, width=295, height=220, corner_radius=CORNER_RADIUS, font=(FONT, 11), state="normal", fg_color="light grey", text_color="black", scrollbar_button_color="dark grey", wrap="word")
        self.about_text.insert("0.0", "PassPy is a password strength checker created by Harry Johnson for a year 11 software engineering task. It uses a range of tests including checking your password against common passwords, dictionary words, data breaches in combination with length and character tests to help you create a strong password. \n\nFor more information, visit the GitHub repository:\nhttps://github.com/harry-johnson12/Password-Checker-Task/tree/main\n\nIf you have any questions or suggestions, feel free to open an issue on the GitHub repository.\n\nThank you for using PassPy!")
        self.about_text.configure(state="disabled")

        link = "https://github.com/harry-johnson12/Password-Checker-Task/tree/main"
        self.create_links(self.about_text, link)

        link = "https://haveibeenpwned.com/Passwords"
        
        self.create_links(self.help_text, link)

    def place_menu_widgets(self):
        self.menu_title_lbl.place(relx=0.5, rely=0.10, anchor="n")
        self.help_button.place(relx=0.5, rely=0.28, anchor="n")
        self.about_button.place(relx=0.5, rely=0.44, anchor="n")
        self.password_generator_button.place(relx=0.5, rely=0.59, anchor="n")
        self.back_to_menubutton.place(relx=0.5, rely=0.74, anchor="n")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.password_checker = password_checker
        self.title("PassPy")
        self.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")
        self._set_appearance_mode("light") # Modes: "system" (default), "dark", "light"
        self.resizable(False, False) 
        #self.iconbitmap("assets/icon.ico")
        self.initialize_main_widgets()
        self.place_main_widgets()

    def show_text(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
            self.show_button.configure(text="Hide")
        else:
            self.password_entry.configure(show="*")
            self.show_button.configure(text="Show")
        
    def toggle_text(self):
        if password_checker.toggled_text == password_checker.astrixed_password:
            password_checker.toggled_text = password_checker.password
            self.previous_password_lbl.configure(text=f"Password entered (TAB to view):  {password_checker.toggled_text}")  # Update the previous password label

        else:
            password_checker.toggled_text = password_checker.astrixed_password
            self.previous_password_lbl.configure(text=f"Password entered (TAB to view):  {password_checker.toggled_text}")  # Update the previous password label
            
    def initialize_main_widgets(self):
        self.password_entry = ctk.CTkEntry(self, corner_radius=CORNER_RADIUS, placeholder_text="Password", width=200, show="*", font=(FONT, PLACEHOLDER_TEXT_SIZE))
        self.show_button = ctk.CTkButton(self, text="Show", command=self.show_text, font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.enter_button = ctk.CTkButton(self, text="Enter", command=password_checker.update_password, font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.menu_button = ctk.CTkButton(self, text="Menu", command=Menu, font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
        self.welcome_text = ctk.CTkTextbox(self, width=550, height=200, corner_radius=CORNER_RADIUS, font=(FONT, 12), state="normal", fg_color="transparent", text_color="dark grey", scrollbar_button_color="light grey", wrap="word")
        self.password_strength_bar = ctk.CTkProgressBar(self, width=492, height=10, corner_radius=CORNER_RADIUS, mode="determinate", fg_color="", progress_color="", orientation="horizontal")
        self.password_strength_label = ctk.CTkLabel(self, text="", font=(FONT, 14), text_color="black")
        self.password_feedback = ctk.CTkTextbox(self, width=550, height=120, corner_radius=CORNER_RADIUS, font=(FONT, 12), state="disabled", fg_color="transparent", text_color="black", scrollbar_button_color="light grey", wrap="word")
        self.time_to_crack_label = ctk.CTkLabel(self, text="", font=(FONT, 13), text_color="dark grey", fg_color="transparent")
        self.previous_password_lbl = ctk.CTkLabel(self, text="Password entered: ", font=(FONT, 13), text_color="dark grey")
        self.title_lbl = ctk.CTkLabel(self, text="PassPy", font=(FONT, 28), text_color="black")
        self.enter_pass_lbl = ctk.CTkLabel(self, text="Enter Password", font=(FONT, 20), text_color="black")
        self.credit_lbl = ctk.CTkLabel(self, text="A password strength checker by Harry Johnson.", font=(FONT, 12), text_color="dark grey")

        self.password_strength_bar.set(0/100)  # Initialize the progress bar to 0
        self.bind("<Return>", lambda event: password_checker.update_password())
        self.bind("<Tab>", lambda event: (self.toggle_text(), "break"))  # Toggle password visibility with Tab key
        self.welcome_text.insert("0.0", "PassPy is a password strength checker that will help you create a strong password. \n\nTo get started, enter your password in the input field and click 'Enter'. The application will analyze your password and provide feedback on its strength, including any issues that may make it weak or vulnerable to attacks.\n\nFor more information, visit the help or about sections via the menu or GitHub repository (link in the menu -> about) or open an issue if you have any questions or suggestions.")
        self.welcome_text.configure(state="disabled")
    
    def place_main_widgets(self):
        self.welcome_text.place(relx=0.03, rely=0.8, anchor="sw")
        self.password_entry.place(relx=0.295, rely=0.24, anchor="sw")
        self.enter_button.place(relx=0.65, rely=0.24, anchor="sw")
        self.show_button.place(relx=0.76, rely=0.24, anchor="sw")
        self.menu_button.place(relx=0.87, rely=0.24, anchor="sw")
        self.password_strength_bar.place(relx=0.03, rely=0.39, anchor="sw")
        self.password_strength_label.place(relx=0.03, rely=0.34, anchor="sw")
        self.password_feedback.place(relx=0.03, rely=0.43, anchor="nw") #nw so it dosent change position with the height if i have time will change them all to NW as this positioning makes more sense to me
        self.title_lbl.place(relx=0.03, rely=0.12, anchor="sw")
        self.enter_pass_lbl.place(relx=0.03, rely=0.24, anchor="sw")
        self.credit_lbl.place(relx=0.2, rely=0.14, anchor="sw")

        self.welcome_text.lift()

class PasswordChecker:
    def __init__(self):
        self.password = ""
        self.rock_you_issue = False
        self.common_passwords_issue = False
        self.saved_password = self.password
        self.password_length = len(self.password)
        self.password_strength = "Weak"
        self.breaches = 0
        self.common = False
        self.score = 100
        self.password_issues = []
        self.Seconds_to_crack = 0
        self.load_common_passwords()
        self.load_dictionary_words()

    def load_common_passwords(self, path="rockyou.txt"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as rockyou_file:
                self.common_passwords = set(line.strip() for line in rockyou_file)
        except FileNotFoundError:
            self.rock_you_issue = True

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
            self.common_passwords_issue = True

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
        password_a_word = False
        self.word_count = 0
        containing_words = []
        for word in self.dictionary_words: # Check if the password is a single dictionary word before checking for containing words to ensure no overlaps
            if word == self.password.lower():
                self.password_issues.append(f"Your password is the just the word '{word}', which is not secure.")
                self.score -= 80
                password_a_word = True
                break
        
        if not password_a_word:  # If the password is not a single dictionary word
            for word in self.dictionary_words:        
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
        try:
            self.seconds_to_crack = combinations / 200000000000  # Assuming 200 billion guesses per second (fast end GPU cracking)
        except:
            self.seconds_to_crack = 1 * 10**15

        if self.seconds_to_crack < 1:
            self.seconds_to_crack = "instantly"  # Round to 2 decimal places
        else:
            self.seconds_to_crack = round(self.seconds_to_crack, 2)
                    
    def update_gui(self):
        if self.password == "joshkenny":
            app.password_entry.configure(placeholder_text="You have found the easter egg password, well done!")
        bar_colour = "light green"
        if self.score >= 95:
            app.password_strength_label.configure(text="Your password is incredibly strong!")
        elif self.score >= 90:
            app.password_strength_label.configure(text="Your password section is very strong, view the below recomendations.")
        elif self.score >= 80:
            app.password_strength_label.configure(text="Your password is strong, to maximise security, view the issues below.")
        elif self.score >= 50: 
            bar_colour = "yellow"
            app.password_strength_label.configure(text="Your password is average strength, view the issues and reccomendations belows")
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
        if len(self.password_issues) == 0 and not self.rock_you_issue and not self.common_passwords_issue:
            app.password_feedback.configure(fg_color="transparent")
        app.password_feedback.delete("0.0", "end")  # Clear the textbox before inserting new issues

        if self.rock_you_issue:
            app.password_feedback.insert("end", "There was an error loading the common passwords file, the common password check will be disabled.\n")
        if self.common_passwords_issue:
            app.password_feedback.insert("end", "There was an error loading the dictionary words file, the dictionary password check will be disabled.\n")
        for issue in self.password_issues:
            app.password_feedback.insert("end", issue + "\n")
            app.password_feedback.insert("end", "\n")  # Add a newline after each issue for better readability
        for i in range(2): app.password_feedback.delete("end-1c", "end") # Remove the last newline character to avoid an extra blank line at the end
        app.password_feedback.configure(state="disabled")  # Disable the textbox after updating it

        #configure the time to crack label
        if not len(self.password_issues) == 0:
            calculated_y = 0.45 + (len(self.password_issues*30))/MAIN_HEIGHT # The initial height down of the feedback box + the decimal of the screen it covers after its hegiht is updated
        else: calculated_y = 0.41
        
        if not type(self.seconds_to_crack) == str: # if it takes time to crack, update the gui accordingly
            Seconds_to_crack = int(self.seconds_to_crack)
            
            Years = Seconds_to_crack // 31536000  # 365 Days

            remaining = Seconds_to_crack % 31536000
            Months = remaining // 2592000  # 30 Days
            remaining = remaining % 2592000
            Days = remaining // 86400
            remaining = remaining % 86400
            Hours = remaining // 3600
            remaining = remaining % 3600
            Minutes = remaining // 60
            Seconds = remaining % 60

            if Years > 0:
                app.time_to_crack_label.configure(text=f"Your password will take: {Years} Years, {Months} Months and {Days} Days to crack.")
            elif Months > 0:
                app.time_to_crack_label.configure(text=f"Your password will take: {Months} Months, {Days} Days and {Hours} Hours to crack.")
            elif Days > 0:
                app.time_to_crack_label.configure(text=f"Your password will take: {Days} Days, {Hours} Hours and {Minutes} Minutes to crack.")
            elif Hours > 0:
                app.time_to_crack_label.configure(text=f"Your password will take: {Hours} Hours, {Minutes} Minutes and {Seconds} Seconds to crack.")
            elif Minutes > 0:
                app.time_to_crack_label.configure(text=f"Your password will take: {Minutes} Minutes and {Seconds} Seconds to crack.")
            else:
                app.time_to_crack_label.configure(text=f"Your password will take: {Seconds} Seconds to crack.")
            
            if Years > 1 * 10**15:
                app.time_to_crack_label.configure(text="Your password will take over one quadrillion years to crack by brute force.")
            
        else:
            app.time_to_crack_label.configure(text=f"Your password will be cracked {self.seconds_to_crack}.") # instantly instance

        app.time_to_crack_label.place(relx=0.03, rely=calculated_y, anchor="nw")

        #configure the previous password label
        self.astrixed_password = ""
        for i in range(len(self.password)): 
            self.astrixed_password += "•"

        self.toggled_text = self.astrixed_password
        app.previous_password_lbl.configure(text=f"Password entered (TAB to view):  {password_checker.toggled_text}")  # Update the previous password label
        
        calculated_y += 0.07  # Increment the y position for the next label
        app.previous_password_lbl.place(relx=0.03, rely=calculated_y, anchor="nw")
        
        #hide the welcome text
        app.welcome_text.place_forget()  # Hide the welcome text after the first password is entered
   
    def check_password_strength(self):
        self.password_issues = []
        self.breaches = self.password_breaches()
        self.common = self.check_common_passwords()
        self.length_penalty()
        self.check_for_dictionary_words()
        self.check_password_character_diversity()
        self.calculate_time_to_crack()
        if self.score < 0: self.score = 0
        self.update_gui()  # Update the GUI with the new password strength and issues

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
            app.password_entry.configure(placeholder_text="Password")
            app.focus_set()
        else:
            app.password_entry.configure(placeholder_text="Please enter a password")  # Change the placeholder text to red if no password is entered
            app.focus_set()

password_checker = PasswordChecker()
app = App()
app.mainloop()