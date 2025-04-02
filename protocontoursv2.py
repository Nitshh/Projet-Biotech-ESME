import nibabel as nib
import numpy as np
from skimage.measure import marching_cubes
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 1. Charger le volume NIfTI
nii_path = "C:/Users/User/Documents/ESME/Ingé 2/Semestre 2/PROJET/Data/Labels/05 AORTE.nii.gz"
volume = nib.load(nii_path).get_fdata()

# 2. Paramètres
threshold = 0.5  # Seuil de segmentation (ajuster selon le contraste)
spacing = (1, 1, 1)  # Résolution spatiale (mm) - vérifier dans le header NIfTI !

# 3. Reconstruction 3D avec Marching Cubes
vertices, faces, _, _ = marching_cubes(volume, level=threshold, spacing=spacing)

# 4. Création du fichier STL
stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
stl_mesh.vectors = vertices[faces]
stl_mesh.save('aorte_3d_reconstructed.stl')

# 5. Visualisation
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
mesh = Poly3DCollection(vertices[faces], alpha=0.7, edgecolor='k')
ax.add_collection3d(mesh)
ax.set_xlim(0, volume.shape[0])
ax.set_ylim(0, volume.shape[1])
ax.set_zlim(0, volume.shape[2])
plt.title('Modèle 3D de l\'aorte (Marching Cubes)')
plt.tight_layout()
plt.show()