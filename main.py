import customtkinter as ctk

#IDEAS(GUI): about, settings, help, show password, by harry j, customise for light/dark mode
#IDEAS(SECURITY): password strength/breach checker, password generator, password manager
#size parameter could fix the cut off text issue

WIDTH = 600
HEIGHT = 400
FONT = "Helvetica Neue Medium"

app = ctk.CTk()
app.title("PassPy")
app.geometry(f"{WIDTH}x{HEIGHT}")
app._set_appearance_mode("light") # Modes: "system" (default), "dark", "light"
#app.iconbitmap("assets/icon.ico")
# app.resizable(False, False) 

class Frame:
    pass

class Button:
    pass

class Label:
    def __init__(self, window, text, x, y, font, size, color):
        self.window = window
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.size = size
        self.color = color
        self.label = ctk.CTkLabel(self.window, text=self.text, font=(self.font, self.size), text_color=self.color)

    def place(self):
        self.label.place(relx=self.x, rely=self.y, anchor="sw")
    
titleLbl = Label(app, "PassPy", 0.03, 0.12, FONT, 28, "black")
enterPassLbl = Label(app, "Enter Password", 0.03, 0.24, FONT, 20, "black",)
passwordEntry = ctk.CTkEntry(app, corner_radius=3, placeholder_text="Password", width=200, show="*", font=(FONT, 15))

titleLbl.place()
enterPassLbl.place()
passwordEntry.place(relx=0.3, rely=0.24, anchor="sw")

app.mainloop()