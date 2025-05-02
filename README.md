# 📡 Projet 1 Surveillance avec Drone Tello

Ce projet implémente un système de surveillance interactif en utilisant un drone **Tello**. Il permet de contrôler le drone en temps réel à l'aide du clavier, de visualiser le flux vidéo en direct et de capturer des photos.

---

## 🎮 Commandes Clavier

| Touche        | Action                         |
|---------------|--------------------------------|
| `a`           | Avancer                        |
| `r`           | Reculer                        |
| `←` (gauche)  | Déplacer à gauche              |
| `→` (droite)  | Déplacer à droite              |
| `m`           | Tourner dans le sens antihoraire |
| `c`           | Tourner dans le sens horaire   |
| `↑` (haut)    | Monter                         |
| `↓` (bas)     | Descendre                      |
| `w`           | Flip avant                     |
| `x`           | Flip arrière                   |
| `y`           | Flip à gauche                  |
| `z`           | Flip à droite                  |
| `o`           | Rotation à 360°                |
| `p`           | Prendre une photo              |
| `ESC` ou `q`  | Atterrir et quitter le programme |

---

## 🧩 Fonctionnalités Principales

### 1. Connexion au Drone
- Initialisation de l’objet `Tello` via la bibliothèque **djitellopy**
- Vérification du niveau de batterie
- Blocage du décollage si la batterie est < 20%

### 2. Contrôle Clavier
- Utilisation de **pynput.keyboard** pour capturer les touches
- Mouvement, flips, rotations, montées/descentes en temps réel

### 3. Capture de Photos
- Sauvegarde d’une image avec date/heure lors de l’appui sur `p`
- Création automatique d’un dossier `photos` si inexistant

### 4. Flux Vidéo en Direct
- Lecture en continu du flux via **OpenCV (cv2)**
- Affichage en temps réel dans une fenêtre

---

## 📦 Bibliothèques Utilisées

- `djitellopy` – Contrôle du drone Tello
- `opencv-python` (`cv2`) – Affichage vidéo et traitement d’image
- `pynput` – Écoute des événements clavier
- `time`, `os` – Gestion du temps et des fichiers

---

## 🚀 Exécution

```bash
python Surveillance1.py

