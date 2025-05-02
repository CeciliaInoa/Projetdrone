#Programme de suivi et reconnaissance
from djitellopy import Tello
import cv2
from pynput import keyboard
from time import strftime, sleep
import os

# Initialiser l'instance du drone Tello
tello = Tello()

# Initialiser le détecteur de visages d'OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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
            tello.move_up(30)
        elif key == keyboard.Key.down:
            tello.move_down(30)
        elif key == keyboard.Key.left:
            tello.move_left(30)
        elif key == keyboard.Key.right:
            tello.move_right(30)
        elif key.char == 'f':  # Avancer
            tello.move_forward(30)
        elif key.char == 'b':  # Reculer
            tello.move_back(30)
        elif key.char == 'm':
            tello.rotate_counter_clockwise(30)
        elif key.char == 'c':
            tello.rotate_clockwise(30)
        elif key.char == 'w' and tello.get_height() > 100:  # Flip avant, vérifier la hauteur
            tello.flip_forward()
        elif key.char == 'y' and tello.get_height() > 100:  # Flip gauche, vérifier la hauteur
            tello.flip_left()
        elif key.char == 'p':
            frame_read = tello.get_frame_read()
            img = frame_read.frame
            take_picture(img)
        elif key.char == 'o':
            tello.rotate_clockwise(180)  # Tourner à 180 degrés
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
    sleep(2)

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    frame_width = 640  # Réduire la résolution pour améliorer les performances
    frame_height = 480

    while True:
        try:
            frame_read = tello.get_frame_read()
            img = frame_read.frame

            # Vérifier si l'image est valide
            if img is None or img.size == 0:
                continue

            # Réduire la résolution de l'image pour alléger le traitement
            img = cv2.resize(img, (frame_width, frame_height))

            # Détection de visages
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Calcul du centre du visage
                face_center_x = x + w // 2
                face_center_y = y + h // 2

                # Calcul de l'erreur par rapport au centre de l'image
                error_x = face_center_x - frame_width // 2
                error_y = face_center_y - frame_height // 2

                # Définition d'une zone de tolérance pour éviter des mouvements trop fréquents
                tolerance = 30

                # Déplacement horizontal
                if abs(error_x) > tolerance:
                    if error_x > 0:
                        tello.move_right(20)
                    else:
                        tello.move_left(20)

                # Déplacement vertical
                if abs(error_y) > tolerance:
                    if error_y > 0:
                        tello.move_down(20)
                    else:
                        tello.move_up(20)

            cv2.imshow("Tello Camera", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Erreur : {e}")
            continue

    cv2.destroyAllWindows()
    listener.stop()
    tello.land()
    tello.end()

