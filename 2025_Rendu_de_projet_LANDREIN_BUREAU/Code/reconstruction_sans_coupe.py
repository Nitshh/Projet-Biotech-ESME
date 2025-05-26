import nibabel as nib
import numpy as np
from skimage.measure import marching_cubes
from stl import mesh
from open3d import io, geometry
import sys
import json
import os

nii_path = sys.argv[1]
nii_img = nib.load(nii_path)
volume = nii_img.get_fdata()
espacement_voxel = nii_img.header.get_zooms()[:3]

seuil = 0.6
sommets, faces, _, _ = marching_cubes(volume, level=seuil, spacing=espacement_voxel)

stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
stl_mesh.vectors = sommets[faces]
stl_mesh.save("static/aorte_3d_reconstructed.stl")

maillage_o3d = io.read_triangle_mesh("static/aorte_3d_reconstructed.stl")
maillage_o3d.compute_vertex_normals()

pcd = maillage_o3d.sample_points_poisson_disk(30000)
mesh_poisson, _ = geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, 8)
mesh_poisson.compute_vertex_normals()

mesh_poisson.remove_duplicated_vertices()
mesh_poisson.remove_degenerate_triangles()
mesh_poisson.remove_unreferenced_vertices()
mesh_poisson.paint_uniform_color([0.8, 0.8, 0.8])

io.write_triangle_mesh("static/aorte_poisson_lisse.stl", mesh_poisson)

bounding_box = mesh_poisson.get_axis_aligned_bounding_box()
dimensions = bounding_box.get_extent()
try:
    volume_estime = mesh_poisson.get_volume()
except:
    volume_estime = 0

infos = {
    "fichier": os.path.basename(nii_path),
    "largeur_mm": round(dimensions[0], 2),
    "hauteur_mm": round(dimensions[1], 2),
    "profondeur_mm": round(dimensions[2], 2),
    "volume_estime_mm3": round(volume_estime, 2),
    "nb_faces": len(np.asarray(mesh_poisson.triangles)),
    "mode": "sans"
}

with open("static/aorte_infos.json", "w") as f:
    json.dump(infos, f)
