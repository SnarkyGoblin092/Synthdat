# Synthdat - Synthetic Data Generator addon for Blender
This addon is being made to make Blender able to generate synthetic data for neural networks and learning algorithms. There aren't many if any Blender addons for synthetic data generation. Most softwares developed for this reason work in the backround without even opening the Blender GUI. This makes configuration hard (.json, .yml, etc files), rendering slow (always opening blender and loading models all over again) and the models have to have a specific name.
<br><br>
Synthdat makes configuration much easier, you only have to load models once, they can have any name because the code doesn't work on an object name basis.

<p align="center">
  <b>The addon panel:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/addon.png" height="200" width="auto">
</p>

The final goal of the project is to make Blender able to:

 - render images, masks, depth maps
 - create annotations for each object
 - calculate the camera positions relative to all objects in the scene

with support for multiple cameras, procedurally create annotation for all objects in the scene, etc. 

Currently, it supports image and depth map rendering, creating masks for all objects having other objects covering them and the full mask for each object. It can render any amount of images with random camera and light positions. It can generate sun and point lights based on the given settings. The code also generates a compositor node tree (hence being able to render masks) and arranges the nodes for easier understanding.

<p align="center">
  <b>An example node tree:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/nodes.png" height="200" width="auto">
</p>

It creates separate collections and view layers for all objects to make it easier to render all masks and maps at once.

<p align="center">
  <b>Example for generated collections:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/collections.png" height="200" width="auto">
</p>

<p align="center">
  <b>Example for generated view layers:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/view_layers.png" height="200" width="auto">
</p>

The addon creates a folder with the current timestamp as a name and subfolders for each mask type and the images. All the folders where images multiple objects are saved, these images are separated into different folders with the objects' name.

<p align="center">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/timestamp.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/folders.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/folder_per_object.png" height="200" width="auto">
</p>

For the rendering process, you can specify the settings with the original settings of Blender, but you are restricted to only use Cycles as the rendering engine. Don't worry about setting it the active render engine, the code does that by itself. You can change everything: render resolution, sample size, every setting of Cycles, the lights and cameras.
If you wish, you can enable the "Return To Original" option, which saves the whole project as a .blend file before rendering and loads it back after it finished, so all the changes the code does will be reverted.

<p align="center">
  <b>Here are some examples created by the addon:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/image.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/depth_map.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/cone_full.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/main/img/cone_cut.png" height="200" width="auto">
</p>
