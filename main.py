
#IDEAS(GUI): settings, help, customise for light/dark mode

#IDEAS(SECURITY): password strength/breach checker - length check, character diversity, common password list, api breaches, overall score out of 100

#OTHER: also have a password generator, password manager, potentially AI password improver, size parameter could fix the cut off text issue, eventually make it resizable

import customtkinter as ctk

WIDTH = 600
HEIGHT = 400
FONT = "Helvetica Neue Medium"
CORNER_RADIUS = 3

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
        self.password_entry = ctk.CTkEntry(self, corner_radius=CORNER_RADIUS, placeholder_text="Password", width=200, show="*", font=(FONT, 15))
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
        self.password = None
    
    def update_password(self):
        self.password = app.password_entry.get()
        app.password_entry.delete(0, ctk.END)

password_checker = Password_checker()
app = App()
app.mainloop()
