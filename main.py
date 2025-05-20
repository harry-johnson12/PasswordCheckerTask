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

class Password:
    def __init__(self, password):
        pass
    
# Create the main window
passwordEntry = ctk.CTkEntry(app, corner_radius=CORNER_RADIUS, placeholder_text="Password", width=200, show="*", font=(FONT, 15))
titleLbl = ctk.CTkLabel(app, text="PassPy", font=(FONT, 28), text_color="black")
enterPassLbl = ctk.CTkLabel(app, text="Enter Password", font=(FONT, 20), text_color="black")
creditLbl = ctk.CTkLabel(app, text="A password strength checker by Harry Johnson.", font=(FONT, 12), text_color="dark grey")
enterButton = ctk.CTkButton(app, text="Enter", font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)
showButton = ctk.CTkButton(app, text="Show", font=(FONT, 12), width=60, height=30, text_color="black", fg_color="light grey", hover_color="dark grey", corner_radius=CORNER_RADIUS)

titleLbl.place(relx=0.03, rely=0.12, anchor="sw")
enterPassLbl.place(relx=0.03, rely=0.24, anchor="sw")
creditLbl.place(relx=0.2, rely=0.14, anchor="sw")
enterButton.place(relx=0.64, rely=0.24, anchor="sw")
showButton.place(relx=0.75, rely=0.24, anchor="sw")
passwordEntry.place(relx=0.29, rely=0.24, anchor="sw")

app.mainloop()