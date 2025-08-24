# WRSR-MTL-Exporter
Tool to simplify the tedious task of making materials for Workers & Resources: Soviet Republic. Especially useful for complex models with multiple materials. Make mtl files with dozens of materials in just few clicks.

# How to use:
1. Install as normal addon.
2. In your viewport, go to sidebar, WRSR tab. Here you will find new menu called "MTL Editor" that looks like this:
<img width="332" height="206" alt="image" src="https://github.com/user-attachments/assets/01ec7f66-6db4-4226-979e-50e3ee4ab342" />

3. Set your preferences for export, such as rbga (a is not alpha for WRSR *sigh*) values for diffuse, specular and ambient; relative texture path you'd like to have in your material (useful if you have shared folders or subfolders) and export path for your mtl file.
4. Select all meshes you would like to generate mtl file for.
5. Click "Export W&R MTL". The resulted file will look like your normal mtl material file.
<img width="488" height="447" alt="image" src="https://github.com/user-attachments/assets/3e2c6a51-72da-4d9b-8037-c7b2ae55a71f" />


# Texture Slot Assignment (Blender - W&R MTL):
1. Diffuse - Base Color.
2. Roughness - Specular for vehicles or emissive for buildings.
3. Normal map - Bump texture.
