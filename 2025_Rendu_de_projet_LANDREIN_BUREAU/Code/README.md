# 🎓 Projet ESME — Reconstruction 3D de l’Arc Aortique

Bienvenue dans ce projet développé dans le cadre d’un enseignement à l’**ESME Sudria**, dédié à la **reconstruction tridimensionnelle de l’arc aortique** à partir d’IRM médicales.  
Il combine : traitement d’images, visualisation 3D, interface web, et modélisation médicale.

---

## 📁 Structure du projet

```
projet_esme_final/
├── app.py
├── reconstruction_avec_coupe.py
├── reconstruction_sans_coupe.py
├── requirements.txt
├── README.md
├── static/
│   ├── style.css
│   ├── uploads/
│   └── aorte_*.stl
├── templates/
│   └── index2.html
```

---

## ⚙️ Installation manuelle (recommandée)

### 1. Pré-requis
- Python 3.10 ou 3.11 recommandé
- pip à jour : `python -m pip install --upgrade pip`

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
```

#### ✅ Activer :

- **Windows (PowerShell)** :
  ```bash
  venv\Scripts\Activate.ps1
  ```

- **Windows (CMD)** :
  ```bash
  venv\Scripts\activate.bat
  ```

- **Linux/macOS** :
  ```bash
  source venv/bin/activate
  ```

---

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

### 4. Lancer l’application Flask

```bash
python app.py
```

Puis ouvrir votre navigateur à :
```
http://127.0.0.1:5000
```

---

## 🖥️ Fonctionnalités de l’IHM

### 🎛️ Menu d’importation
- Importer un fichier `.nii` ou `.nii.gz`
- Choisir le **mode de reconstruction** :
  - Sans coupe : reconstruction complète
  - Avec coupe : suppression automatique de l’extrémité supérieure

### 🧠 Reconstruction
- L’algorithme traite le fichier IRM
- Génère un fichier `.stl` affiché en 3D

### 🌀 Visualisation interactive
- Tourner, zoomer, déplacer le modèle
- Bouton de **recentrage**
- Activer/désactiver les axes ou l’éclairage
- Zoom dynamique via slider

### 📊 Panneau d'informations à droite
- Nom du fichier
- Dimensions du modèle
- Volume estimé
- Nombre de faces
- Mode utilisé

### 📦 Export
- Télécharger le modèle généré au format `.stl`

---

## ❗ Dépannage

| Problème                            | Cause fréquente                      | Solution                            |
|-------------------------------------|--------------------------------------|-------------------------------------|
| `ModuleNotFoundError`              | Environnement non activé             | Activez `venv`                      |
| `404 .stl`                          | Fichier pas généré                   | Vérifiez que le fichier est valide |
| `get_volume()` échoue              | Maillage non fermé                   | Essayez le **mode avec coupe**      |

---

## 👨‍🎓 Réalisé par

**Alexandre LANDREIN**  
**Wandrille BUREAU**  
Encadré par **Mounir LAHLOUH** – ESME SUDRIA

---

## ❤️ Technologies utilisées

- [Python](https://www.python.org)
- [Flask](https://flask.palletsprojects.com/)
- [Open3D](http://www.open3d.org/)
- [Three.js](https://threejs.org/)
- [NIfTI format](https://nifti.nimh.nih.gov/)

---

> Ce projet illustre les liens entre l’ingénierie biomédicale, la géométrie algorithmique, et les interfaces web modernes.