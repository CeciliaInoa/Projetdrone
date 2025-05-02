#Programme de surveillance
from djitellopy import Tello
import cv2
from pynput import keyboard
from time import strftime, sleep
import os

# Initialiser l'instance du drone Tello
tello = Tello()

# Fonction pour connecter et vérifier la batterie du drone
def connect_drone():
    tello.connect()

    battery = tello.get_battery()
    print(f"Niveau de batterie : {battery}%")
    if battery < 20:
        print("Le niveau de batterie est trop bas pour le vol.")
        return False
    return True

# Fonction pour prendre une photo
def take_picture(img):
    timestr = strftime("%Y%m%d-%H%M%S")
    dossier_images = 'Ressource/Images'
    if not os.path.exists(dossier_images):
        os.makedirs(dossier_images)
    fichier_image = f"{dossier_images}/image_{timestr}.jpg"
    cv2.imwrite(fichier_image, img)
    print(f"Photo capturée: {fichier_image}")


# Fonction pour gérer les pressions de touches
def on_press(key):
    try:
        if key == keyboard.Key.up:
            tello.move_up(25)
            sleep(0.1)  # Pause de 0,5 seconde
        elif key == keyboard.Key.down:
            tello.move_down(25)
            sleep(0.1)
        elif key == keyboard.Key.left:
            tello.move_left(25)
            sleep(0.1)
        elif key == keyboard.Key.right:
            tello.move_right(25)
            sleep(0.1)
        elif key.char == 'a':
            tello.move_forward(25)
            sleep(0.1)
        elif key.char == 'r':
            tello.move_back(25)
            sleep(0.1)
        elif key.char == 'g':
            tello.move_left(25)
            sleep(0.1)
        elif key.char == 'd':
            tello.move_right(25)
            sleep(0.1)
        elif key.char == 'm':
            tello.rotate_counter_clockwise(25)
            sleep(0.1)
        elif key.char == 'c':
            tello.rotate_clockwise(25)
            sleep(0.1)
        elif key.char == 'w':
            tello.flip_forward()
            sleep(0.1)
        elif key.char == 'x':
            tello.flip_back()
            sleep(0.1)
        elif key.char == 'y':
            tello.flip_left()
            sleep(0.1)
        elif key.char == 'z':
            tello.flip_right()
            sleep(0.1)
        elif key.char == 'p':
            frame_read = tello.get_frame_read()
            img = frame_read.frame
            take_picture(img)
            sleep(0.1)
        elif key.char == 'o':
            tello.rotate_clockwise(180)  # Tourner à 180 degrés
            sleep(0.1)
    except AttributeError:
        pass

# Fonction pour gérer les relâchements de touches
def on_release(key):
    if key == keyboard.Key.esc:
        # Arrête le drone et termine le programme en appuyant sur 'ESC'
        tello.land()
        tello.end()
        return False

# Initialiser la connexion
if connect_drone():
    tello.takeoff()
    sleep(5)
    tello.streamon()
    sleep(3)  # Ajout d'un délai pour s'assurer que le flux vidéo est activé

    # Configuration du listener de clavier
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Afficher le flux vidéo en temps réel
    while True:
        frame_read = tello.get_frame_read()
        img = frame_read.frame

        cv2.imshow("Tello Camera", img)

        # Appuyer sur 'q' pour quitter
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    listener.stop()
    tello.land()
    tello.end()