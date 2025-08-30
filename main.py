from tkinter import PhotoImage
from datetime import datetime
from customtkinter import *
from icmplib import ping
from PIL import Image
import ipaddress
import os
import time
import threading
import sys

'''
ICMPing - A lightweight tool used for sending ICMP (ping) requests.

GitHub - https://github.com/Caleb-Greene/ICMPing

License - https://github.com/Caleb-Greene/ICMPing/tree/main?tab=License-1-ov-file
'''


class ErrorWindow(CTkToplevel):  # Errow Window class - Inherits from CTkToplevel
    def __init__(self, parent, message):
        super().__init__()
        self.geometry("250x75")
        self.title("ERROR")
        self.resizable(False, False)  # disables resizing of the window

        self.transient(parent)  # Make this window always on top of parent
        self.grab_set()         # Block interaction with parent window until closed

        self.label = CTkLabel(master=self, text=message, wraplength=225)
        self.label.pack(pady=3, padx=20)

        self.close_button = CTkButton(master=self, text="Close", corner_radius=32,
                                      fg_color="#029cff", hover_color="#0062b1", command=self.destroy)
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

    def get_current_time():
        current_time = datetime.now().time()
        return current_time.strftime("%H:%M:%S")

    def get_current_time_dot():  # returns current time seperated with . for file naming
        current_time = datetime.now().time()
        return current_time.strftime("%H.%M.%S")

    def get_current_date():
        current_date = datetime.now().date()
        return current_date.strftime("%Y-%m-%d")

    def no_reply(self):
        return f"[{self.sent}] {Data.get_current_time()} - No reply from {self.ip}\n"

    def add_rtt(self, rtt):
        self.rtts.append(rtt)
        return f"[{self.sent}] {Data.get_current_time()} - Reply from {self.ip} RTT = {rtt}ms\n"

    def summary(self, interval, timeout):
        message = (
            f"\n--- Summary ({Data.get_current_date()})---\n"
            f"Packets Sent: {self.sent}\n"
            f"Packets Received: {self.received}\n"
            f"Packet Loss: {((self.sent - self.received) / self.sent) * 100:.2f}%\n\n"
        )

        if interval == 1:
            message += f"Interval: {interval} second\n"
        else:
            message += f"Interval: {interval} seconds\n"

        if timeout == 1:
            message += f"Timeout: {timeout} second\n\n"
        else:
            message += f"Timeout: {timeout} seconds\n\n"

        if self.sent > 1 and self.received > 1:
            message += (
                f"RTT Min: {round(min(self.rtts), 3) if self.rtts else 'N/A'}ms\n"
                f"RTT Max: {round(max(self.rtts), 3) if self.rtts else 'N/A'}ms\n"
                f"RTT Avg: {round(sum(self.rtts) / len(self.rtts), 3) if self.rtts else 'N/A'}ms\n"
                f"Jitter: {round(max(self.rtts) - min(self.rtts), 3) if self.rtts else 'N/A'}ms\n\n"
            )
        return message


class ICMPing(CTk):  # Main class - Inherits from CTk
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        self.geometry("750x250")
        self.title("ICMPing")
        self.resizable(False, False)  # Disable resizing of the main window

        # Get the current path of the code
        current_dir = os.path.dirname(os.path.abspath(__file__))

        bg_path = os.path.join(current_dir, "BG.png")
        dbutton_path = os.path.join(current_dir, "dButton.png")

        operating_system = sys.platform

        if operating_system == "win32":
            icon_path = os.path.join(current_dir, "logo.ico")
            self.iconbitmap(icon_path)

        elif operating_system == "darwin":
            self.iconphoto(True, PhotoImage(
                file=os.path.join(current_dir, "logo.png")))

        # Images
        bg_image = Image.open(bg_path)
        background = CTkImage(light_image=bg_image,
                              dark_image=bg_image, size=(750, 250))
        image_label = CTkLabel(self, image=background, text="")
        image_label.place(x=0, y=0)

        download_image = Image.open(dbutton_path)
        download_button = CTkImage(
            light_image=download_image, dark_image=download_image, size=(25, 25))

        # Ping Count input
        self.Countinput = CTkEntry(master=self, width=125, text_color="#ffffff",
                                   bg_color="#2f2f2f", corner_radius=0, placeholder_text="Number")
        self.Countinput.place(x=180, y=73, anchor="center")

        # Interval input
        self.Intervalinput = CTkEntry(master=self, width=125, text_color="#ffffff",
                                      bg_color="#2f2f2f", corner_radius=0, placeholder_text="Seconds")
        self.Intervalinput.place(x=180, y=108, anchor="center")

        # Timeout input
        self.Timeoutinput = CTkEntry(master=self, width=125, text_color="#ffffff",
                                     bg_color="#2f2f2f", corner_radius=0, placeholder_text="Seconds")
        self.Timeoutinput.place(x=180, y=143, anchor="center")

        # IP address input
        self.IPinput = CTkEntry(master=self, width=125, text_color="#ffffff",
                                bg_color="#2f2f2f", corner_radius=0, placeholder_text="IPv4 or IPv6")
        self.IPinput.place(x=180, y=178, anchor="center")

        # Ping button
        self.button = CTkButton(master=self, width=125, height=25, text="Start Ping", corner_radius=16,
                                fg_color="#029cff", hover_color="#0062b1", command=self.ping, font=("", 16), bg_color="#2f2f2f")
        self.button.place(x=180, y=225, anchor="center")

        # Download button
        self.Downloadbutton = CTkButton(master=self, image=download_button, command=self.download,
                                        width=25, height=25, text="", bg_color="#2f2f2f", fg_color="#2f2f2f", hover=False)
        self.Downloadbutton.place(x=25, y=225, anchor="center")

        self.textbox = CTkTextbox(
            master=self, width=500, height=250, bg_color="#1c1c1c", text_color="#ffffff")

        self.ErrorWindow = None

    def validIP(self):
        try:
            # Validate the IP address using ipaddress
            ipaddress.ip_address(self.IPinput.get())
            return True
        except ValueError:
            return False

    def open_error_window(self, message):

        if self.ErrorWindow is None or not self.ErrorWindow.winfo_exists():  # Check if the window is not already open
            self.ErrorWindow = ErrorWindow(self, message)

        self.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()

        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        error_width = 250
        error_height = 75

        # Center calculation
        x = parent_x + (parent_width // 2) - (error_width // 2)
        y = parent_y + (parent_height // 2) - (error_height // 2)

        self.enable_button()
        self.ErrorWindow.geometry(f"{error_width}x{error_height}+{x}+{y}")
        self.ErrorWindow.focus()  # Bring window to the front

    def disable_button(self):
        self.button.configure(state="disabled")

    def enable_button(self):
        self.button.configure(state="normal")

    def ping_logic(self):
        # Validation
        if not self.validIP():
            self.open_error_window("Invalid IP address.")
            return

        try:  # Validates Count, Interval, and Timeout inputs
            count = int(self.Countinput.get()) if self.Countinput.get(
            ) != "" else 1  # default of 1 ping
            interval = int(self.Intervalinput.get()) if self.Intervalinput.get(
            ) != "" else 1  # default of 1 second interval
            timeout = int(self.Timeoutinput.get()) if self.Timeoutinput.get(
            ) != "" else 2  # default of 2 seconds timeout

        except ValueError:
            self.open_error_window(
                "Count, Interval, and Timeout must be integers.")
            return

        if count < 1:
            self.open_error_window("Count must be at least 1.")
            return

        if interval < 0 or timeout < 0:
            self.open_error_window(
                "Interval and Timeout must be non-negative integers.")
            return

        if count >= sys.maxsize or interval >= sys.maxsize or timeout >= sys.maxsize:
            self.open_error_window(
                "Count, Interval, and Timeout must be less than the maximum integer size.")
            return

        # Ping
        self.data = Data(self.IPinput.get())

        self.display_textbox()

        for i in range(count):
            try:
                # Send a ping request
                response = ping(self.IPinput.get(), count=1,
                                timeout=timeout, privileged=False)
            except Exception as e:
                print(f"Ping Failed on Attempt {i + 1} - {e}")
                continue

            if response.is_alive:
                self.data.increment_sent()
                self.data.increment_received()
                self.add(response.avg_rtt)
                self.data.add_rtt(response.avg_rtt)
            else:
                self.data.increment_sent()
                self.display(self.data.no_reply())

            if i != (count - 1):
                time.sleep(interval)

        self.display(self.data.summary(interval, timeout))
        self.enable_button()

    def ping(self):
        thread = threading.Thread(target=self.ping_logic)
        self.disable_button()
        thread.daemon = True
        thread.start()

    def display(self, text):
        self.textbox.after(0, lambda: self.textbox.insert("end", text))

    def add(self, rtt):
        self.textbox.after(0, lambda: self.textbox.insert(
            "end", self.data.add_rtt(rtt)))

    def display_textbox(self):
        self.textbox.place(relx=2/3, rely=1/2, anchor="center")

    def download(self):
        folder_path = filedialog.askdirectory()

        if not folder_path:
            return  # User clicked cancel

        file_name = f"ICMPing {Data.get_current_date()} {Data.get_current_time_dot()}.txt"
        file = os.path.join(folder_path, file_name)

        with open(file, "w") as f:
            f.write(self.textbox.get("0.0", "end"))


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
