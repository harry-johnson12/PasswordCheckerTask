import customtkinter as ctk

#IDEAS(GUI): about, settings, help, by harry j, customise for light/dark mode
#IDEAS(SECURITY): password strength/breach checker - length check, character diversity, common password list, api breaches, overall score out of 100
#could also have a password generator, password manager, potentially AI password improver
#size parameter could fix the cut off text issue, eventually make it resizable

WIDTH = 600
HEIGHT = 400
FONT = "Helvetica Neue Medium"
CORNER_RADIUS = 3

app = ctk.CTk()
app.title("PassPy")
app.geometry(f"{WIDTH}x{HEIGHT}")
app._set_appearance_mode("light") # Modes: "system" (default), "dark", "light"
app.resizable(False, False) 
#app.iconbitmap("assets/icon.ico")


password_entry = ctk.CTkEntry(app, corner_radius=CORNER_RADIUS, placeholder_text="Password", width=200, show="*", font=(FONT, 15))

class Password_checker:
    def __init__(self):
        self.password = ""
    
    def update_password(self):
        self.password = password_entry.get()
        print(self.password)

password_checker = Password_checker()

enter_button = ctk.CTkButton(app, text="Enter", command=password_checker.update_password, font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
show_button = ctk.CTkButton(app, text="Show", font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)

title_lbl = ctk.CTkLabel(app, text="PassPy", font=(FONT, 28), text_color="black")
enter_pass_lbl = ctk.CTkLabel(app, text="Enter Password", font=(FONT, 20), text_color="black")
credit_lbl = ctk.CTkLabel(app, text="A password strength checker by Harry Johnson.", font=(FONT, 12), text_color="dark grey")

password_entry.place(relx=0.29, rely=0.24, anchor="sw")
enter_button.place(relx=0.64, rely=0.24, anchor="sw")
show_button.place(relx=0.75, rely=0.24, anchor="sw")
title_lbl.place(relx=0.03, rely=0.12, anchor="sw")
enter_pass_lbl.place(relx=0.03, rely=0.24, anchor="sw")
credit_lbl.place(relx=0.2, rely=0.14, anchor="sw")

app.mainloop()
