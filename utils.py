import math
import bpy
import numpy as np
import mathutils as mu
import random
import os
import copy
from datetime import datetime

obj = None
cam = None
light = None

cam_rot_x = 0.0
cam_rot_y = 0.0
cam_rot_z = 0.0
cam_dist = 0.0

obj_pos_x = 0.0
obj_pos_y = 0.0
obj_pos_z = 0.0

obj_rot_x = 0.0
obj_rot_y = 0.0
obj_rot_z = 0.0

light_obj = None

light_pos_x = 0.0
light_pos_y = 0.0
light_pos_z = 0.0

light_rot_x = 0.0
light_rot_y = 0.0
light_rot_z = 0.0

light_intensity = 0.0

output_path = ''


def get_objects(context):
    cust_props = context.scene.custom_properties

    global obj
    global cam
    global light

    if cust_props.object is not None:
        obj = bpy.data.objects.get(cust_props.object.name)
    if cust_props.camera is not None:
        cam = bpy.data.objects.get(cust_props.camera.name)
    if cust_props.light is not None:
        light = cust_props.light

    if obj is None or cam is None or light is None:
        return None, None, None
    else:
        return obj, cam, light


def get_current_settings(context):
    cust_props = context.scene.custom_properties

    global light_obj
    light_obj = bpy.data.objects.get(light.name)

    cust_props.object_min_rot_x = obj.rotation_euler[0]
    cust_props.object_min_rot_y = obj.rotation_euler[1]
    cust_props.object_min_rot_z = obj.rotation_euler[2]
    cust_props.object_max_rot_x = obj.rotation_euler[0]
    cust_props.object_max_rot_y = obj.rotation_euler[1]
    cust_props.object_max_rot_z = obj.rotation_euler[2]

    cust_props.object_min_pos_x = obj.location[0]
    cust_props.object_min_pos_y = obj.location[1]
    cust_props.object_min_pos_z = obj.location[2]
    cust_props.object_max_pos_x = obj.location[0]
    cust_props.object_max_pos_y = obj.location[1]
    cust_props.object_max_pos_z = obj.location[2]

    cust_props.camera_distance = np.linalg.norm(np.array(cam.location)-np.array(obj.location))

    cust_props.camera_min_rot_x = cam.rotation_euler[0]
    cust_props.camera_min_rot_y = cam.rotation_euler[1]
    cust_props.camera_min_rot_z = cam.rotation_euler[2]
    cust_props.camera_max_rot_x = cam.rotation_euler[0]
    cust_props.camera_max_rot_y = cam.rotation_euler[1]
    cust_props.camera_max_rot_z = cam.rotation_euler[2]

    cust_props.light_min_intensity = light.energy
    cust_props.light_max_intensity = light.energy

    cust_props.light_min_rot_x = light_obj.rotation_euler[0]
    cust_props.light_min_rot_y = light_obj.rotation_euler[1]
    cust_props.light_min_rot_z = light_obj.rotation_euler[2]
    cust_props.light_max_rot_x = light_obj.rotation_euler[0]
    cust_props.light_max_rot_y = light_obj.rotation_euler[1]
    cust_props.light_max_rot_z = light_obj.rotation_euler[2]

    cust_props.light_min_pos_x = light_obj.location[0]
    cust_props.light_min_pos_y = light_obj.location[1]
    cust_props.light_min_pos_z = light_obj.location[2]
    cust_props.light_max_pos_x = light_obj.location[0]
    cust_props.light_max_pos_y = light_obj.location[1]
    cust_props.light_max_pos_z = light_obj.location[2]


def zero_everything(context):
    cust_props = context.scene.custom_properties

    cust_props.object = None
    cust_props.object_min_rot_x = 0.0
    cust_props.object_min_rot_y = 0.0
    cust_props.object_min_rot_z = 0.0
    cust_props.object_max_rot_x = 0.0
    cust_props.object_max_rot_y = 0.0
    cust_props.object_max_rot_z = 0.0

    cust_props.object_min_pos_x = 0.0
    cust_props.object_min_pos_y = 0.0
    cust_props.object_min_pos_z = 0.0
    cust_props.object_max_pos_x = 0.0
    cust_props.object_max_pos_y = 0.0
    cust_props.object_max_pos_z = 0.0

    cust_props.camera = None
    cust_props.camera_distance = 0.0

    cust_props.camera_min_rot_x = 0.0
    cust_props.camera_min_rot_y = 0.0
    cust_props.camera_min_rot_z = 0.0
    cust_props.camera_max_rot_x = 0.0
    cust_props.camera_max_rot_y = 0.0
    cust_props.camera_max_rot_z = 0.0

    cust_props.light = None
    cust_props.light_min_intensity = 0.0
    cust_props.light_max_intensity = 0.0

    cust_props.light_min_rot_x = 0.0
    cust_props.light_min_rot_y = 0.0
    cust_props.light_min_rot_z = 0.0
    cust_props.light_max_rot_x = 0.0
    cust_props.light_max_rot_y = 0.0
    cust_props.light_max_rot_z = 0.0

    cust_props.light_min_pos_x = 0.0
    cust_props.light_min_pos_y = 0.0
    cust_props.light_min_pos_z = 0.0
    cust_props.light_max_pos_x = 0.0
    cust_props.light_max_pos_y = 0.0
    cust_props.light_max_pos_z = 0.0


def reset_default(context):
    cust_props = context.scene.custom_properties

    cust_props.object = None
    cust_props.object_min_rot_x = 0.0
    cust_props.object_min_rot_y = 0.0
    cust_props.object_min_rot_z = 0.0
    cust_props.object_max_rot_x = 0.0
    cust_props.object_max_rot_y = 0.0
    cust_props.object_max_rot_z = 6.2831853072

    cust_props.object_min_pos_x = -1.5
    cust_props.object_min_pos_y = -1.5
    cust_props.object_min_pos_z = 0.0
    cust_props.object_max_pos_x = 1.5
    cust_props.object_max_pos_y = 1.5
    cust_props.object_max_pos_z = 0.0

    cust_props.camera = None
    cust_props.camera_distance = 10.0

    cust_props.camera_min_rot_x = -0.3490658504
    cust_props.camera_min_rot_y = 0.0
    cust_props.camera_min_rot_z = 0.0
    cust_props.camera_max_rot_x = -1.4835298642
    cust_props.camera_max_rot_y = 6.2831853072
    cust_props.camera_max_rot_z = 0.0

    cust_props.light = None
    cust_props.light_min_intensity = 1.0
    cust_props.light_max_intensity = 2.0

    cust_props.light_min_rot_x = -1.308996939
    cust_props.light_min_rot_y = -1.308996939
    cust_props.light_min_rot_z = 0.0
    cust_props.light_max_rot_x = 1.308996939
    cust_props.light_max_rot_y = 1.308996939
    cust_props.light_max_rot_z = 0.0

    cust_props.light_min_pos_x = -5.0
    cust_props.light_min_pos_y = -5.0
    cust_props.light_min_pos_z = 5.0
    cust_props.light_max_pos_x = 5.0
    cust_props.light_max_pos_y = 5.0
    cust_props.light_max_pos_z = 5.0


def set_variables(cust_props):

    global cam_dist
    cam_dist = cust_props.camera_distance

    global cam_rot_x
    if cust_props.camera_min_rot_x == 0.0 and cust_props.camera_max_rot_x == 0.0:
        if cam_dist == 0.0:
            cam_rot_x = cam.rotation_euler[0]
        else:
            cam_rot_x = 0.0
    else:
        cam_rot_x = random.uniform(cust_props.camera_min_rot_x, cust_props.camera_max_rot_x)

    global cam_rot_y
    if cust_props.camera_min_rot_y == 0.0 and cust_props.camera_max_rot_y == 0.0:
        if cam_dist == 0.0:
            cam_rot_y = cam.rotation_euler[1]
        else:
            cam_rot_y = 0.0
    else:
        cam_rot_y = random.uniform(cust_props.camera_min_rot_y, cust_props.camera_max_rot_y)

    global cam_rot_z
    if cust_props.camera_min_rot_z == 0.0 and cust_props.camera_max_rot_z == 0.0:
        if cam_dist == 0.0:
            cam_rot_z = cam.rotation_euler[2]
        else:
            cam_rot_z = 0.0
    else:
        cam_rot_z = random.uniform(cust_props.camera_min_rot_z, cust_props.camera_max_rot_z)

    global obj_pos_x
    if cust_props.object_min_pos_x == 0.0 and cust_props.object_max_pos_x == 0.0:
        obj_pos_x = obj.location[0]
    else:
        obj_pos_x = random.uniform(cust_props.object_min_pos_x, cust_props.object_max_pos_x)

    global obj_pos_y
    if cust_props.object_min_pos_y == 0.0 and cust_props.object_max_pos_y == 0.0:
        obj_pos_y = obj.location[1]
    else:
        obj_pos_y = random.uniform(cust_props.object_min_pos_y, cust_props.object_max_pos_y)

    global obj_pos_z
    if cust_props.object_min_pos_z == 0.0 and cust_props.object_max_pos_z == 0.0:
        obj_pos_z = obj.location[2]
    else:
        obj_pos_z = random.uniform(cust_props.object_min_pos_z, cust_props.object_max_pos_z)

    global obj_rot_x
    if cust_props.object_min_rot_x == 0.0 and cust_props.object_min_rot_x == 0.0:
        obj_rot_x = obj.rotation_euler[0]
    else:
        obj_rot_x = random.uniform(cust_props.object_min_rot_x, cust_props.object_max_rot_x)

    global obj_rot_y
    if cust_props.object_min_rot_y == 0.0 and cust_props.object_min_rot_y == 0.0:
        obj_rot_y = obj.rotation_euler[1]
    else:
        obj_rot_y = random.uniform(cust_props.object_min_rot_y, cust_props.object_max_rot_y)

    global obj_rot_z
    if cust_props.object_min_rot_z == 0.0 and cust_props.object_min_rot_z == 0.0:
        obj_rot_z = obj.rotation_euler[2]
    else:
        obj_rot_z = random.uniform(cust_props.object_min_rot_z, cust_props.object_max_rot_z)

    global light_obj
    light_obj = bpy.data.objects.get(light.name)

    global light_pos_x
    if cust_props.light_min_pos_x == 0.0 and cust_props.light_max_pos_x == 0.0:
        light_pos_x = light_obj.location[0]
    else:
        light_pos_x = random.uniform(cust_props.light_min_pos_x, cust_props.light_max_pos_x)

    global light_pos_y
    if cust_props.light_min_pos_y == 0.0 and cust_props.light_max_pos_y == 0.0:
        light_pos_y = light_obj.location[1]
    else:
        light_pos_y = random.uniform(cust_props.light_min_pos_y, cust_props.light_max_pos_y)

    global light_pos_z
    if cust_props.light_min_pos_z == 0.0 and cust_props.light_max_pos_z == 0.0:
        light_pos_z = light_obj.location[2]
    else:
        light_pos_z = random.uniform(cust_props.light_min_pos_z, cust_props.light_max_pos_z)

    global light_rot_x
    if cust_props.light_min_rot_x == 0.0 and cust_props.light_max_rot_x == 0.0:
        light_rot_x = light_obj.rotation_euler[0]
    else:
        light_rot_x = random.uniform(cust_props.light_min_rot_x, cust_props.light_max_rot_x)

    global light_rot_y
    if cust_props.light_min_rot_y == 0.0 and cust_props.light_max_rot_y == 0.0:
        light_rot_y = light_obj.rotation_euler[1]
    else:
        light_rot_y = random.uniform(cust_props.light_min_rot_y, cust_props.light_max_rot_y)

    global light_rot_z
    if cust_props.light_min_rot_z == 0.0 and cust_props.light_max_rot_z == 0.0:
        light_rot_z = light_obj.rotation_euler[2]
    else:
        light_rot_z = random.uniform(cust_props.light_min_rot_z, cust_props.light_max_rot_z)

    global light_intensity
    if cust_props.light_min_intensity == 0.0 and cust_props.light_max_intensity == 0.0:
        light_intensity = light.energy
    else:
        light_intensity = random.uniform(cust_props.light_min_intensity, cust_props.light_max_intensity)


def show_message_box(message='', title='Message Box', icon='NONE'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def create_node_tree(per_row=4):
    # Create nodes and links
    bpy.context.scene.use_nodes = True
    for lay in bpy.context.scene.view_layers:
        lay.use_pass_object_index = True
        lay.cycles.denoising_store_passes = True

    bpy.context.scene.node_tree.nodes.clear()
    bpy.context.scene.node_tree.links.clear()

    render_layers = []
    id_masks = []
    cut_id_masks = []
    outputs = []
    cut_outputs = []

    objects = bpy.data.objects

    y = 0
    for i in range(0, len(objects.items())):
        if objects[i].type == 'MESH':
            objects[i].pass_index = y + 1
            render_layers.append(bpy.context.scene.node_tree.nodes.new('CompositorNodeRLayers'))
            id_masks.append(bpy.context.scene.node_tree.nodes.new('CompositorNodeIDMask'))
            cut_id_masks.append(bpy.context.scene.node_tree.nodes.new('CompositorNodeIDMask'))
            outputs.append(bpy.context.scene.node_tree.nodes.new('CompositorNodeOutputFile'))
            cut_outputs.append(bpy.context.scene.node_tree.nodes.new('CompositorNodeOutputFile'))
            outputs[y].name = objects[i].name
            y += 1

    for i in range(0, len(id_masks)):
        id_masks[i].index = i + 1
        cut_id_masks[i].index = i + 1

    for i in range(0, len(outputs)):
        outputs[i].base_path = output_path + "id_masks/{}/".format(outputs[i].name)
        outputs[i].file_slots[0].path = "{}####".format(outputs[i].name)
        outputs[i].format.color_mode = 'BW'
        cut_outputs[i].base_path = output_path + "mask_visib/{}/".format(outputs[i].name, outputs[i].name)
        cut_outputs[i].file_slots[0].path = "{}####".format(outputs[i].name)
        cut_outputs[i].format.color_mode = 'BW'

    render_layers.append(bpy.context.scene.node_tree.nodes.new('CompositorNodeRLayers'))
    denoise = bpy.context.scene.node_tree.nodes.new('CompositorNodeDenoise')
    compositor = bpy.context.scene.node_tree.nodes.new('CompositorNodeComposite')

    y = 0
    for i in range(0, len(objects.items())):
        if objects[i].type == 'MESH':
            render_layers[y].layer = objects[i].name
            bpy.context.scene.node_tree.links.new(render_layers[y].outputs['IndexOB'], id_masks[y].inputs[0])
            bpy.context.scene.node_tree.links.new(id_masks[y].outputs[0], outputs[y].inputs['Image'])
            bpy.context.scene.node_tree.links.new(render_layers[len(render_layers)-1].outputs['IndexOB'], cut_id_masks[y].inputs[0])
            bpy.context.scene.node_tree.links.new(cut_id_masks[y].outputs[0], cut_outputs[y].inputs['Image'])
            y += 1

    bpy.context.scene.node_tree.links.new(render_layers[len(render_layers)-1].outputs['Image'], denoise.inputs['Image'])
    bpy.context.scene.node_tree.links.new(render_layers[len(render_layers)-1].outputs['Denoising Normal'], denoise.inputs['Normal'])
    bpy.context.scene.node_tree.links.new(render_layers[len(render_layers)-1].outputs['Denoising Albedo'], denoise.inputs['Albedo'])
    bpy.context.scene.node_tree.links.new(denoise.outputs['Image'], compositor.inputs['Image'])

    render_layers[len(render_layers)-1].location = mu.Vector((-20, 0))
    denoise.location = mu.Vector((260, 160))
    compositor.location = mu.Vector((420, 160))

    # Arrange nodes
    y = 580
    o = 0
    it = 0
    for i in range(0, len(cut_id_masks)):
        if i == 0:
            cut_id_masks[i].location = mu.Vector((260, 0))
        elif i % per_row == 0:
            it += 1
            o -= o
        else:
            o += 1

        if i != 0:
            cut_id_masks[i].location = mu.Vector((260, -(y * it) - (140 * o)))

    y = 580
    o = 0
    it = 0
    for i in range(len(cut_outputs)):
        if i == 0:
            cut_outputs[i].location = mu.Vector((420, 0))
        elif i % per_row == 0:
            it += 1
            o -= o
        else:
            o += 1

        if i != 0:
            cut_outputs[i].location = mu.Vector((420, -(y * it) - (140 * o)))

    y = 0
    it = 0
    for i in range(0, len(render_layers)-1):
        if i == 0:
            render_layers[i].location = mu.Vector((580, 0))
        elif i % per_row == 0:
            y += 580
            it -= it
            render_layers[i].location = mu.Vector((580 + it * 420, 0 - y))
        else:
            render_layers[i].location = mu.Vector((580 + it * 420, 0 - y))

        it += 1

    y = 0
    it = 0
    for i in range(0, len(id_masks)):
        if i == 0:
            id_masks[i].location = mu.Vector((840, 0))
        elif i % per_row == 0:
            y += 580
            it -= it
            id_masks[i].location = mu.Vector((840 + it * 420, 0 - y))
        else:
            id_masks[i].location = mu.Vector((840 + it * 420, 0 - y))

        it += 1

    y = 150
    it = 0
    for i in range(0, len(outputs)):
        if i == 0:
            outputs[i].location = mu.Vector((840, -150))
        elif i % per_row == 0:
            y += 580
            it -= it
            outputs[i].location = mu.Vector((840 + it * 420, 0 - y))
        else:
            outputs[i].location = mu.Vector((840 + it * 420, 0 - y))

        it += 1


def seperate_objects_to_render_layers():
    objects = bpy.data.objects
    layers = bpy.context.scene.view_layers
    collections = bpy.data.collections

    for col in collections:
        if col.name != 'Collection':
            collections.remove(col)

    for lay in layers:
        if lay.name != 'View Layer':
            layers.remove(lay)

    for o in objects:
        if o.type == 'MESH':
            if collections.find(o.name) == -1:
                col = collections.new(o.name)
                bpy.context.scene.collection.children.link(col)

    for col in collections:
        for o in objects:
            if o.name == col.name:
                if col.objects.find(o.name) == -1:
                    col.objects.link(o)
            else:
                if o in col.objects.items():
                    col.objects.unlink(o)

    for o in objects:
        if o.type == 'MESH':
            if layers.find(o.name) == -1:
                layers.new(o.name)

    for o in objects:
        if o.type == 'MESH':
            for col in collections:
                if o.name != col.name:
                    layers[o.name].layer_collection.children[o.name].exclude = True

    for o in objects:
        if o.type == 'MESH':
            for col in collections:
                if o.name != col.name:
                    layers[o.name].layer_collection.children[col.name].exclude = True
                else:
                    layers[o.name].layer_collection.children[col.name].exclude = False


def rotate_and_render(context):
    cust_props = context.scene.custom_properties

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    global output_path
    output_path = os.path.expanduser("~/Desktop/Renders/{}/".format(dt_string))

    for scene in bpy.data.scenes:
        scene.render.engine = 'CYCLES'

    global light_obj
    light_obj = bpy.data.objects.get(light.name)

    obj_loc = copy.deepcopy(obj.location)
    cam_loc = copy.deepcopy(cam.location)
    light_loc = copy.deepcopy(light_obj.location)
    obj_rot = copy.deepcopy(obj.rotation_euler)
    cam_rot = copy.deepcopy(cam.rotation_euler)
    light_rot = copy.deepcopy(light_obj.rotation_euler)

    light_int = copy.deepcopy(light.energy)

    seperate_objects_to_render_layers()
    create_node_tree()

    for i in range(cust_props.render_count):

        set_variables(cust_props)

        if cam_dist != 0.0:
            cam.location = obj.location
            cam.rotation_euler = [math.radians(90) + cam_rot_x, cam_rot_z, cam_rot_y]

            bpy.ops.object.select_all(action='DESELECT')
            cam.select_set(True)
            bpy.ops.transform.translate(value=[0, 0, cam_dist], orient_type='LOCAL')

        light.energy = light_intensity

        if obj_pos_x != obj.location[0] or obj_pos_y != obj.location[1] or obj_pos_z != obj.location[2]:
            obj.location = np.add(obj_loc, [obj_pos_x, obj_pos_y, obj_pos_z])

        obj.rotation_euler = (obj_rot_x, obj_rot_y, obj_rot_z)

        if light_obj.location[0] != light_pos_x or light_obj.location[1] != light_pos_y or light_obj.location[2] != light_pos_z:
            light_obj.location = np.add(obj_loc, [light_pos_x, light_pos_y, light_pos_z])

        if light_obj.rotation_euler[0] != light_rot_x or light_obj.rotation_euler[1] != light_rot_y or light_obj.rotation_euler[2] != light_rot_z:
            light_obj.rotation_euler = (light_rot_x, light_rot_y, light_rot_z)

        if cust_props.render_checkbox:
            context.scene.render.filepath = os.path.expanduser(
                "~/Desktop/Renders/{}/images/image{}{}".format(dt_string, i+1, bpy.context.scene.render.file_extension)
            )

            print("Rendering image{}{}...".format(i+1, bpy.context.scene.render.file_extension))
            bpy.ops.render.render(write_still=True)

            for o in bpy.data.objects:
                if o.type == 'MESH':
                    os.rename(output_path + "id_masks/{}/{}0001.png".format(o.name, o.name),
                              output_path + "id_masks/{}/{}{}.png".format(o.name, o.name, i + 1))
                    os.rename(output_path + "mask_visib/{}/{}0001.png".format(o.name, o.name),
                              output_path + "mask_visib/{}/{}{}.png".format(o.name, o.name, i + 1))

        obj.location = obj_loc

    if cust_props.return_to_original:
        cam.location = cam_loc
        light_obj.location = light_loc
        obj.rotation_euler = obj_rot
        cam.rotation_euler = cam_rot
        light_obj.rotation_euler = light_rot
        light.energy = light_int
