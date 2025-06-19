from customtkinter import *
from icmplib import ping
import ipaddress, os


class ErrorWindow(CTkToplevel):
    def __init__(self, parent): 
        super().__init__()
        self.geometry("250x75")
        self.title("ERROR")
        self.resizable(False, False) # Disable resizing of the error window

        self.transient(parent)  # Make this window always on top of parent
        self.grab_set()         # Block interaction with parent window until closed

        self.label = CTkLabel(master=self, text="IPv4 address is not valid")
        self.label.pack(pady=3, padx=20)

        self.close_button = CTkButton(master=self, text="Close", corner_radius=32, fg_color="#029cff", hover_color="#0062b1", command=self.destroy)
        self.close_button.pack(padx=20, pady=10)


class ICMPing(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        self.geometry("300x200")
        self.title("ICMPing")
        self.resizable(False, False) # Disable resizing of the main window

        current_dir = os.path.dirname(os.path.abspath(__file__)) # Get the current directory of the script
        icon_path = os.path.join(current_dir, "LOGO.ico")
        self.iconbitmap(icon_path)

        self.label = CTkLabel(master=self, text="ICMPing", font=("Arial", 32)) # Title label
        self.label.place(relx=0.5, y=50, anchor="center")

        self.input = CTkEntry(master=self, placeholder_text="Input IP Address", width=150, text_color="#ffffff") # Input field for IP address
        self.input.place(relx=0.5, y=100, anchor="center")

        self.button = CTkButton(master=self, text="Ping", corner_radius=32, fg_color="#029cff", hover_color="#0062b1", command=self.ping) # Ping button
        self.button.place(relx=0.5, y=150, anchor="center")

        self.ErrorWindow = None


    def validIP(self):
        try:
            ipaddress.ip_address(self.input.get()) # Validate the IP address using ipaddress module
            return True
        except ValueError:
            return False


    def open_error_window(self):
        if self.ErrorWindow is None or not self.ErrorWindow.winfo_exists(): # Check if the window is not already open
            self.ErrorWindow = ErrorWindow(self)

        x = self.winfo_rootx() + 18
        y = self.winfo_rooty() + 70
        self.ErrorWindow.geometry(f"+{x}+{y}") # Position the error window relative to the main window
        self.ErrorWindow.focus() # Bring the existing error window to the front


    def ping(self):
        if self.validIP():
            ping(self.input.get(), timeout=5, count=1) # Ping the IP with a max wait time of 5 seconds and only one packet
        else:
            self.open_error_window()


if __name__ == "__main__":
    app = ICMPing()
    app.mainloop()
