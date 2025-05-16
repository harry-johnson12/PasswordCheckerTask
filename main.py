import customtkinter as ctk

WIDTH = 800
HEIGHT = 600



app = ctk.CTk()
app.title("PassPy")
app.geometry(f"{WIDTH}x{HEIGHT}")
app._set_appearance_mode("light") # Modes: "system" (default), "dark", "light"
#app.iconbitmap("assets/icon.ico")
# app.resizable(False, False) 

label = ctk.CTkLabel(app, text="PassPy", font=("Arial Rounded MT Bold", 30)) 
label.place(relx=0.5, rely=0.1, anchor="center")

app.mainloop()