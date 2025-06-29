from datetime import datetime
from customtkinter import *
from icmplib import ping
from PIL import Image
import ipaddress, os, time, threading, sys

'''
ICMPing - A lightweight tool used for sending ICMP (ping) requests.

GitHub - https://github.com/Caleb-Greene/ICMPing

License - https://github.com/Caleb-Greene/ICMPing/tree/main?tab=License-1-ov-file
'''


class ErrorWindow(CTkToplevel): # Errow Window class - Inherits from CTkToplevel
    def __init__(self, parent, message): 
        super().__init__()
        self.geometry("250x75")
        self.title("ERROR")
        self.resizable(False, False) 

        self.transient(parent)  # Make this window always on top of parent
        self.grab_set()         # Block interaction with parent window until closed

        self.label = CTkLabel(master=self, text=message, wraplength=225)
        self.label.pack(pady=3, padx=20)

        self.close_button = CTkButton(master=self, text="Close", corner_radius=32, fg_color="#029cff", hover_color="#0062b1", command=self.destroy)
        self.close_button.pack(padx=20, pady=10)


class Data():
    def __init__(self, ip):
        self.ip = ip
        self.sent = 0
        self.received = 0
        self.rtts = []
    

    def increment_sent(self):
        self.sent += 1


    def increment_received(self):
        self.received += 1


    def get_current_time(self):
        current_time = datetime.now().time()
        return current_time.strftime("%H:%M:%S")
    

    def get_current_date(self):
        current_date = datetime.now().date()
        return current_date.strftime("%Y-%m-%d")
    

    def no_reply(self):
        return f"[{self.sent}] {self.get_current_time()} - No reply from {self.ip}\n"
    

    def add_rtt(self, rtt):
        self.rtts.append(rtt)  
        return f"[{self.sent}] {self.get_current_time()} - Reply from {self.ip} RTT = {rtt}ms\n"


    def summary(self):
        message = (
            f"\n--- Summary ({self.get_current_date()})---\n"
            f"Packets Sent: {self.sent}\n"
            f"Packets Received: {self.received}\n"
            f"Packet Loss: {((self.sent - self.received) / self.sent) * 100:.2f}%\n\n"
            )
        
        if self.sent > 1 and self.received > 1:
            message += (
            f"RTT Min: {round(min(self.rtts), 3) if self.rtts else 'N/A'}ms\n"
            f"RTT Max: {round(max(self.rtts), 3) if self.rtts else 'N/A'}ms\n"
            f"RTT Avg: {round(sum(self.rtts) / len(self.rtts), 3) if self.rtts else 'N/A'}ms\n"
            f"Jitter: {round(max(self.rtts) - min(self.rtts), 3) if self.rtts else 'N/A'}ms\n\n"
            )
        return message


class ICMPing(CTk): # Main class - Inherits from CTk
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        self.geometry("750x250")
        self.title("ICMPing")
        self.resizable(False, False) # Disable resizing of the main window

        current_dir = os.path.dirname(os.path.abspath(__file__)) # Get the current path of the code
        icon_path = os.path.join(current_dir, "LOGO.ico")
        font_path = os.path.join(current_dir, "Lekton-Regular.ttf")
        image_path = os.path.join(current_dir, "BG.png")
        self.iconbitmap(icon_path)

        # Background image
        my_image = Image.open(image_path)
        ctk_image = CTkImage(light_image=my_image, dark_image=my_image, size=(750, 250))  # Adjust size as needed
        image_label = CTkLabel(self, image=ctk_image, text="")
        image_label.place(x=0, y=0)

        # Ping Count input
        self.Countinput = CTkEntry(master=self, width=125, text_color="#ffffff", bg_color="#2f2f2f", corner_radius=0, placeholder_text="Count (int)")
        self.Countinput.place(relx=1/6, y=80, anchor="center")

        # Interval input
        self.Intervalinput = CTkEntry(master=self, width=125, text_color="#ffffff", bg_color="#2f2f2f", corner_radius=0, placeholder_text="Interval (sec)")
        self.Intervalinput.place(relx=1/6, y=115, anchor="center")

        # Timeout input
        self.Timeoutinput = CTkEntry(master=self, width=125, text_color="#ffffff", bg_color="#2f2f2f", corner_radius=0, placeholder_text="Timeout (sec)")
        self.Timeoutinput.place(relx=1/6, y=150, anchor="center")

        # IP address input
        self.IPinput = CTkEntry(master=self, width=125, text_color="#ffffff", bg_color="#2f2f2f", corner_radius=0, placeholder_text="IPv4 or IPv6")
        self.IPinput.place(relx=1/6, y=185, anchor="center")

        # Ping button
        self.button = CTkButton(master=self, text="ping", corner_radius=16, fg_color="#029cff", hover_color="#0062b1", command=self.ping, font=(font_path, 16), bg_color="#2f2f2f")
        self.button.place(relx=1/6, y=225, anchor="center")

        self.textbox = CTkTextbox(master=self, width=500, height=250, bg_color="#1c1c1c", text_color="#ffffff")

        self.ErrorWindow = None


    def validIP(self):
        try:
            ipaddress.ip_address(self.IPinput.get()) # Validate the IP address using ipaddress
            return True
        except ValueError:
            return False


    def open_error_window(self, message):
        if self.ErrorWindow is None or not self.ErrorWindow.winfo_exists(): # Check if the window is not already open
            self.ErrorWindow = ErrorWindow(self, message)

        x = self.winfo_rootx() + 18
        y = self.winfo_rooty() + 70
        self.enable_button()
        self.ErrorWindow.geometry(f"+{x}+{y}") # Position the error window relative to the main window
        self.ErrorWindow.focus() # Bring the existing error window to the front
    

    def disable_button(self):
        self.button.configure(state="disabled")
    

    def enable_button(self):
        self.button.configure(state="normal")


    def ping_logic(self):
        # Validation
        if not self.validIP():
            self.open_error_window("Invalid IP address.")
            return
        
        try: # Validates Count, Interval, and Timeout inputs
            count = int(self.Countinput.get()) if self.Countinput.get() != "" else 1 # default of 1 ping
            interval = int(self.Intervalinput.get()) if self.Intervalinput.get() != "" else 1 # default of 1 second interval
            timeout = int(self.Timeoutinput.get()) if self.Timeoutinput.get() != "" else 2 # default of 2 seconds timeout
            
        except ValueError:
            self.open_error_window("Count, Interval, and Timeout must be integers.")
            return
        
        if count < 1:
            self.open_error_window("Count must be at least 1.")
            return
        
        if interval < 0 or timeout < 0:
            self.open_error_window("Interval and Timeout must be non-negative integers.")
            return
        
        if count >= sys.maxsize or interval >= sys.maxsize or timeout >= sys.maxsize:
            self.open_error_window("Count, Interval, and Timeout must be less than the maximum integer size.")
            return

        
        # Ping
        self.data = Data(self.IPinput.get())

        self.display_textbox()
        for i in range(count):
            try:
                response = ping(self.IPinput.get(), count=1, timeout=timeout) # Send a ping request
            except Exception as e:
                return

            if response.is_alive:
                self.data.increment_sent();self.data.increment_received()
                self.add(response.avg_rtt)
                self.data.add_rtt(response.avg_rtt)
            else:
                self.data.increment_sent()
                self.display(self.data.no_reply())
                

            time.sleep(interval)

        self.display(self.data.summary())
        self.enable_button()


    def ping(self):
        thread = threading.Thread(target=self.ping_logic)
        self.disable_button()
        thread.daemon = True 
        thread.start()
        

    def display(self, text):
        self.textbox.after(0, lambda: self.textbox.insert("end", text))


    def add(self, rtt):
        self.textbox.after(0, lambda: self.textbox.insert("end", self.data.add_rtt(rtt)))
    

    def display_textbox(self):
        self.textbox.place(relx=2/3, rely=1/2, anchor="center")


if __name__ == "__main__":
    app = ICMPing()
    app.mainloop()


'''
COLORS
#029cff - Light blue
#0062b1 - Dark blue
#ffffff - White
#000000 - Black
#2f2f2f - Light gray
#1c1c1c - Dark gray
'''
