# Synthdat - Synthetic Data Generator addon for Blender
This addon is being made to make Blender able to generate synthetic data for neural networks and learning algorithms. There aren't many if any Blender addons for synthetic data generation. Most softwares developed for this reason work in the backround without even opening the Blender GUI. This makes configuration hard (.json, .yml, etc files), rendering slow (always opening blender and loading models all over again) and the models have to have a specific name.
<br><br>
Synthdat makes configuration much easier, you only have to load models once, they can have any name because the code doesn't work on an object name basis.

<p align="center">
  <b>The addon panel:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/addon.png" height="200" width="auto">
</p>

The scope of the project is to make Blender able to:

 - render images, masks, depth masks
 - create annotations for each object
 - calculate the positions from the camera to all objects in the scene

with support for multiple cameras, procedurally create annotation for all objects in the scene, etc. 

Currently, it supports image rendering, creating masks for all objects having other objects covering them and the full mask for each object. It can render any amount of images with random camera and light positions. The code also generates a compositor node tree (hence being able to render masks) and arranges the nodes for easier understanding.

<p align="center">
  <b>An example node tree:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/nodes.png" height="200" width="auto">
</p>

It creates separate collections and view layers for all objects to make it easier to render all masks and maps at once.

<p align="center">
  <b>Example for generated collections:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/collections.png" height="200" width="auto">
</p>

<p align="center">
  <b>Example for generated view layers:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/view_layers.png" height="200" width="auto">
</p>

The addon creates a folder with the current timestamp as a name and subfolders for each mask type and the images. All the folders where images multiple objects are saved, these images are separated into different folders with the objects' name.

<p align="center">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/timestamp.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/folders.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/folder_per_object.png" height="200" width="auto">
</p>

For the rendering process, you can specify the settings with the original settings of Blender, but you are restricted to only use Cycles as the rendering engine. Don't worry about setting it the active render engine, the code does that by itself. You can change everything: render resolution, sample size, every setting of Cycles, the lights and cameras.

<p align="center">
  <b>Here are some examples created by the addon:</b>
  <br><br>
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/image.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/cube_full.png" height="200" width="auto">
  <img src="https://github.com/SnarkyGoblin092/Synthdat/blob/dev/img/cube_cut.png" height="200" width="auto">
</p>
