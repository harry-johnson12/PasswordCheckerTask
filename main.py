import customtkinter as ctk

#IDEAS(GUI): about, settings, help, by harry j, customise for light/dark mode
#IDEAS(SECURITY): password strength/breach checker - common password list, api
#password generator, password manager
#size parameter could fix the cut off text issue, eventually make it resizable

WIDTH = 600
HEIGHT = 400
FONT = "Helvetica Neue Medium"
CORNER_RADIUS = 3

app = ctk.CTk()
app.title("PassPy")
app.geometry(f"{WIDTH}x{HEIGHT}")
app._set_appearance_mode("light") # Modes: "system" (default), "dark", "light"
#app.iconbitmap("assets/icon.ico")
# app.resizable(False, False) 

class Frame:
    pass

class Button:
    def __init__(self, window, text, x, y, font, font_size, width, height, text_color, bg_color="light grey", corner_radius=CORNER_RADIUS):
        self.x = x
        self.y = y
        self.button = ctk.CTkButton(window, text=text, font=(font, font_size), width=width, height=height, text_color=text_color, fg_color=bg_color, corner_radius=corner_radius)

    def place(self):
        self.button.place(relx=self.x, rely=self.y, anchor="sw")

class Label:
    def __init__(self, window, text, x, y, font, font_size, colour):
        self.x = x
        self.y = y
        self.label = ctk.CTkLabel(window, text=text, font=(font, font_size), text_color=colour)

    def place(self):
        self.label.place(relx=self.x, rely=self.y, anchor="sw")

titleLbl = Label(app, "PassPy", 0.03, 0.12, FONT, 28, "black")
enterPassLbl = Label(app, "Enter Password", 0.03, 0.24, FONT, 20, "black",)
creditLbl = Label(app, "A password strength checker by Harry Johnson.", 0.21, 0.14, FONT, 12, "dark grey")

enterButton = Button(app, "Enter", 0.64, 0.24, FONT, 15, 60, 30, "black")
showButton = Button(app, "Show", 0.75, 0.24, FONT, 15, 60, 30, "black")
passwordEntry = ctk.CTkEntry(app, corner_radius=CORNER_RADIUS, placeholder_text="Password", width=200, show="*", font=(FONT, 15))

titleLbl.place()
enterPassLbl.place()
creditLbl.place()
enterButton.place()
showButton.place()
passwordEntry.place(relx=0.29, rely=0.24, anchor="sw")

app.mainloop()