import nibabel as nib
import numpy as np
from skimage.measure import marching_cubes
from stl import mesh
import open3d as o3d
import sys
import json
import os

def coupe_extremite(maillage, axe='y', quantile=97):
    indice_axe = {'x': 0, 'y': 1, 'z': 2}[axe]
    sommets = np.asarray(maillage.vertices)
    triangles = np.asarray(maillage.triangles)
    seuil = np.percentile(sommets[:, indice_axe], quantile)
    maillage_conserver = np.all(sommets[triangles][:, :, indice_axe] < seuil, axis=1)
    nouv_maillage = triangles[maillage_conserver]
    indices_sommets = np.unique(nouv_maillage)
    nouveaux_sommets = sommets[indices_sommets]
    correspondance_indices = {ancien: i for i, ancien in enumerate(indices_sommets)}
    nouveaux_triangles = np.array([[correspondance_indices[i] for i in triangle] for triangle in nouv_maillage])
    maillage_filtre = o3d.geometry.TriangleMesh()
    maillage_filtre.vertices = o3d.utility.Vector3dVector(nouveaux_sommets)
    maillage_filtre.triangles = o3d.utility.Vector3iVector(nouveaux_triangles)
    maillage_filtre.compute_vertex_normals()
    return maillage_filtre

nii_path = sys.argv[1]
nii_img = nib.load(nii_path)
volume = nii_img.get_fdata()
spacing = nii_img.header.get_zooms()[:3]

level = 0.6
verts, faces, _, _ = marching_cubes(volume, level=level, spacing=spacing)

stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
stl_mesh.vectors = verts[faces]
stl_mesh.save("static/aorte_3d_reconstructed.stl")

mesh_o3d = o3d.io.read_triangle_mesh("static/aorte_3d_reconstructed.stl")
mesh_o3d.compute_vertex_normals()

pcd = mesh_o3d.sample_points_poisson_disk(number_of_points=30000)
mesh_poisson, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)

mesh_poisson.remove_duplicated_vertices()
mesh_poisson.remove_degenerate_triangles()
mesh_poisson.remove_unreferenced_vertices()
mesh_poisson.compute_vertex_normals()
mesh_poisson.paint_uniform_color([0.8, 0.8, 0.8])

mesh_final = coupe_extremite(mesh_poisson, axe='y', quantile=97)
o3d.io.write_triangle_mesh("static/aorte_poisson_coupe.stl", mesh_final)

bounding_box = mesh_final.get_axis_aligned_bounding_box()
dimensions = bounding_box.get_extent()
try:
    volume_estime = mesh_final.get_volume()
except:
    volume_estime = 0

infos = {
    "fichier": os.path.basename(nii_path),
    "largeur_mm": round(dimensions[0], 2),
    "hauteur_mm": round(dimensions[1], 2),
    "profondeur_mm": round(dimensions[2], 2),
    "volume_estime_mm3": round(volume_estime, 2),
    "nb_faces": len(np.asarray(mesh_final.triangles)),
    "mode": "avec"
}

with open("static/aorte_infos.json", "w") as f:
    json.dump(infos, f)
