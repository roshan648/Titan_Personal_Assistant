import os
import wmi
import psutil
import tkinter as tk
from tkinter import simpledialog, messagebox
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

# Audio functions
def dB_to_linear(dB):
    return 10 ** (dB / 20.0)

def linear_to_dB(linear):
    return 20 * math.log10(linear)

def set_system_volume(level):
    level = max(0, min(100, level))
    linear_volume = level / 100.0
    volume_dB = linear_to_dB(linear_volume)
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_control.SetMasterVolumeLevel(volume_dB, None)
        print(f"Volume set to {level}% ({volume_dB:.2f} dB)")
    except Exception as e:
        print(f"Error setting volume: {e}")

def get_current_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume_dB = volume_control.GetMasterVolumeLevel()
        current_volume_linear = dB_to_linear(current_volume_dB)
        return int(current_volume_linear * 100)
    except Exception as e:
        print(f"Error getting current volume: {e}")
        return 50

def mute_system_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_control.SetMute(True, None)
        print("Volume muted.")
    except Exception as e:
        print(f"Error muting volume: {e}")

def unmute_system_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_control.SetMute(False, None)
        print("Volume unmuted.")
    except Exception as e:
        print(f"Error unmuting volume: {e}")

def increase_volume(amount):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume = get_current_volume()
        new_volume = max(0, min(100, current_volume + amount))
        volume_control.SetMasterVolumeLevelScalar(new_volume / 100.0, None)

        print(f"Volume increased to {new_volume}%")
    except Exception as e:
        print(f"Error increasing volume: {e}")

def decrease_volume(amount):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume = get_current_volume()
        new_volume = max(0, min(100, current_volume - amount))
        volume_control.SetMasterVolumeLevelScalar(new_volume / 100.0, None)

        print(f"Volume decreased to {new_volume}%")
    except Exception as e:
        print(f"Error decreasing volume: {e}")

# Brightness functions
def set_brightness(level):
    level = max(0, min(100, level))
    try:
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(level, 0)
        print(f"Brightness set to {level}%")
    except Exception as e:
        print(f"Error setting brightness: {e}")

def get_current_brightness():
    try:
        c = wmi.WMI(namespace='wmi')
        brightness = c.WmiMonitorBrightness()[0].CurrentBrightness
        print(f"Current brightness level: {brightness}%")
        return brightness
    except Exception as e:
        print(f"Error getting current brightness: {e}")
        return 50

# System functions
def connect_to_wifi(ssid, password):
    command = f'netsh wlan connect name="{ssid}"'
    os.system(command)

def shutdown_system():
    os.system("shutdown /s /t 1")

def reboot_system():
    os.system("shutdown /r /t 1")

def show_battery_percentage():
    battery = psutil.sensors_battery()
    if battery is not None:
        percent = battery.percent
        plugged_in = "Plugged in" if battery.power_plugged else "Not plugged in"
        return f"The battery is at {percent}% ({plugged_in})"
    else:
        return "Battery information not available."

# GUI Functions
def get_wifi_credentials():
    """
    Show a GUI dialog to get Wi-Fi credentials from the user.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    ssid = simpledialog.askstring("Wi-Fi Name", "Please provide the Wi-Fi name:")
    if not ssid:
        return None, None  # No SSID provided

    password = simpledialog.askstring("Wi-Fi Password", "Please provide the password:", show='*')
    return ssid, password

def open_wifi_gui():
    def connect():
        ssid, password = get_wifi_credentials()
        if ssid and password:
            connect_to_wifi(ssid, password)
            messagebox.showinfo("Success", f"Connecting to Wi-Fi network {ssid}.")
        else:
            messagebox.showwarning("Input Error", "Please enter both SSID and Password.")
    
    root = tk.Tk()
    root.title("Connect to Wi-Fi")
    
    tk.Label(root, text="Click to enter Wi-Fi credentials").pack(padx=20, pady=5)
    
    tk.Button(root, text="Get Credentials and Connect", command=connect).pack(pady=10)
    root.mainloop()

# Main function
def main():
    # Example usage of GUI
    open_wifi_gui()
    
    # Example usage of other functions
    print(show_battery_percentage())

if __name__ == "__main__":
    main()
