import customtkinter as ctk

WIDTH = 800
HEIGHT = 600

app = ctk.CTk()
app.title("PassPy")
app.geometry(f"{WIDTH}x{HEIGHT}")
app.resizable(False, False) 
#app.iconbitmap("assets/icon.ico")
#app.set_appearance_mode("dark")

app.mainloop()