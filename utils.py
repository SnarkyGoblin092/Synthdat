import math
import bpy
import numpy as np
import mathutils as mu
import random
import os
from datetime import datetime

cam = None

cam_rot_x = 0.0
cam_rot_y = 0.0
cam_rot_z = 0.0
cam_dist = 0.0

light_pos_x = 0.0
light_pos_y = 0.0
light_pos_z = 0.0

light_rot_x = 0.0
light_rot_y = 0.0
light_rot_z = 0.0

light_intensity = 0.0

light_radius = 0.0

output_path = ''


def get_current_units():
    length_unit = bpy.context.scene.unit_settings.length_unit

    if length_unit == 'KILOMETERS':
        return 'km', 1000
    elif length_unit == 'METERS':
        return 'm', 1
    elif length_unit == 'CENTIMETERS':
        return 'cm', 1/100
    elif length_unit == 'MILLIMETERS':
        return 'mm', 1/1000
    elif length_unit == 'MICROMETERS':
        return 'mcm', 1/1000000
    elif length_unit == 'MILES':
        return 'mi', 1760
    elif length_unit == 'FEET':
        return 'ft', 1/3
    elif length_unit == 'INCHES':
        return 'in', 1/36
    elif length_unit == 'THOU':
        return 'thou', 1/36000
    else:
        return 'bu', 1


def bu_to_unit(value, scale):
    return value / scale


def unit_to_bu(value, scale):
    return value * scale


def get_scale(context):
    cust_props = context.scene.custom_properties

    if cust_props.depth_max_distance == 0:
        cust_props.depth_max_distance = 100.0

    value_range = cust_props.depth_max_distance

    if value_range < 0:
        value_range *= -1

    return bu_to_unit(value_range / 65536, get_current_units()[1])


def save_current_objects_in_scene():
    target_file = os.path.expanduser("~/Desktop/saved_objs.blend")
    bpy.ops.wm.save_as_mainfile(filepath=target_file)


def reset_saved_objects():
    target_file = os.path.expanduser("~/Desktop/saved_objs.blend")
    bpy.ops.wm.open_mainfile(filepath=target_file)

    os.remove(target_file)


# Get the eyedropped objects
def get_objects(context):
    cust_props = context.scene.custom_properties

    global cam

    if cust_props.camera is not None:
        cam = bpy.data.objects.get(cust_props.camera.name)

    if cam is None:
        return None
    else:
        return cam


# Get every setting from objects
def get_current_settings(context):
    cust_props = context.scene.custom_properties

    cust_props.camera_distance = np.linalg.norm(np.array(cam.location)-np.array([0, 0, 0]))

    cust_props.camera_min_rot_x = cam.rotation_euler[0]
    cust_props.camera_min_rot_y = cam.rotation_euler[1]
    cust_props.camera_min_rot_z = cam.rotation_euler[2]
    cust_props.camera_max_rot_x = cam.rotation_euler[0]
    cust_props.camera_max_rot_y = cam.rotation_euler[1]
    cust_props.camera_max_rot_z = cam.rotation_euler[2]

    # cust_props.light_min_intensity = light.energy
    # cust_props.light_max_intensity = light.energy

    # cust_props.light_min_rot_x = light_obj.rotation_euler[0]
    # cust_props.light_min_rot_y = light_obj.rotation_euler[1]
    # cust_props.light_min_rot_z = light_obj.rotation_euler[2]
    # cust_props.light_max_rot_x = light_obj.rotation_euler[0]
    # cust_props.light_max_rot_y = light_obj.rotation_euler[1]
    # cust_props.light_max_rot_z = light_obj.rotation_euler[2]
    #
    # cust_props.light_min_pos_x = light_obj.location[0]
    # cust_props.light_min_pos_y = light_obj.location[1]
    # cust_props.light_min_pos_z = light_obj.location[2]
    # cust_props.light_max_pos_x = light_obj.location[0]
    # cust_props.light_max_pos_y = light_obj.location[1]
    # cust_props.light_max_pos_z = light_obj.location[2]


# Set every value in the addon to 0
def zero_everything(context):
    cust_props = context.scene.custom_properties

    global cam
    cam = None

    cust_props.depth_min_distance = 0
    cust_props.depth_max_distance = 0

    cust_props.camera = None
    cust_props.camera_distance = 0.0

    cust_props.camera_min_rot_x = 0.0
    cust_props.camera_min_rot_y = 0.0
    cust_props.camera_min_rot_z = 0.0
    cust_props.camera_max_rot_x = 0.0
    cust_props.camera_max_rot_y = 0.0
    cust_props.camera_max_rot_z = 0.0

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


# Return to default values
def reset_default(context):
    cust_props = context.scene.custom_properties

    cust_props.camera = None
    cust_props.camera_distance = 10.0

    cust_props.camera_min_rot_x = -0.3490658504
    cust_props.camera_min_rot_y = 0.0
    cust_props.camera_min_rot_z = 0.0
    cust_props.camera_max_rot_x = -1.4835298642
    cust_props.camera_max_rot_y = 6.2831853072
    cust_props.camera_max_rot_z = 0.0

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


# Set settings to the set amounts or the object's original setting
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

    global light_pos_x
    if cust_props.light_min_pos_x == 0.0 and cust_props.light_max_pos_x == 0.0:
        light_pos_x = 0
    else:
        light_pos_x = random.uniform(cust_props.light_min_pos_x, cust_props.light_max_pos_x)

    global light_pos_y
    if cust_props.light_min_pos_y == 0.0 and cust_props.light_max_pos_y == 0.0:
        light_pos_y = 0
    else:
        light_pos_y = random.uniform(cust_props.light_min_pos_y, cust_props.light_max_pos_y)

    global light_pos_z
    if cust_props.light_min_pos_z == 0.0 and cust_props.light_max_pos_z == 0.0:
        light_pos_z = 10
    else:
        light_pos_z = random.uniform(cust_props.light_min_pos_z, cust_props.light_max_pos_z)

    global light_rot_x
    if cust_props.light_min_rot_x == 0.0 and cust_props.light_max_rot_x == 0.0:
        light_rot_x = 0
    else:
        light_rot_x = random.uniform(cust_props.light_min_rot_x, cust_props.light_max_rot_x)

    global light_rot_y
    if cust_props.light_min_rot_y == 0.0 and cust_props.light_max_rot_y == 0.0:
        light_rot_y = 0
    else:
        light_rot_y = random.uniform(cust_props.light_min_rot_y, cust_props.light_max_rot_y)

    global light_rot_z
    if cust_props.light_min_rot_z == 0.0 and cust_props.light_max_rot_z == 0.0:
        light_rot_z = 0
    else:
        light_rot_z = random.uniform(cust_props.light_min_rot_z, cust_props.light_max_rot_z)



# Show a message box
def show_message_box(message='', title='Message Box', icon='NONE'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


# Generate and arrange a node tree with the given settings
def create_node_tree(per_row=4):
    cust_props = bpy.context.scene.custom_properties

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
            if objects[i].name.find("Plane") == -1 and objects[i].name.find("plane") == -1:
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
        outputs[i].format.file_format = 'PNG'
        outputs[i].format.compression = 0
        cut_outputs[i].base_path = output_path + "mask_visib/{}/".format(outputs[i].name, outputs[i].name)
        cut_outputs[i].file_slots[0].path = "{}####".format(outputs[i].name)
        cut_outputs[i].format.color_mode = 'BW'
        cut_outputs[i].format.file_format = 'PNG'
        cut_outputs[i].format.compression = 0

    render_layers.append(bpy.context.scene.node_tree.nodes.new('CompositorNodeRLayers'))
    denoise = bpy.context.scene.node_tree.nodes.new('CompositorNodeDenoise')
    compositor = bpy.context.scene.node_tree.nodes.new('CompositorNodeComposite')
    depth_map_range = bpy.context.scene.node_tree.nodes.new('CompositorNodeMapRange')
    depth_map_output = bpy.context.scene.node_tree.nodes.new('CompositorNodeOutputFile')

    y = 0
    for i in range(0, len(objects.items())):
        if objects[i].type == 'MESH':
            if objects[i].name.find("Plane") == -1 and objects[i].name.find("plane") == -1:
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
    bpy.context.scene.node_tree.links.new(render_layers[len(render_layers)-1].outputs['Depth'], depth_map_range.inputs[0])
    bpy.context.scene.node_tree.links.new(depth_map_range.outputs[0], depth_map_output.inputs['Image'])

    render_layers[len(render_layers)-1].location = mu.Vector((-20, 0))
    denoise.location = mu.Vector((260, 160))
    compositor.location = mu.Vector((420, 160))

    depth_map_range.inputs[1].default_value = 0
    depth_map_range.inputs[2].default_value = cust_props.depth_max_distance
    depth_map_range.inputs[3].default_value = 0
    depth_map_range.inputs[4].default_value = 1
    depth_map_range.location = mu.Vector((580, 205))
    depth_map_output.format.color_mode = 'BW'
    depth_map_output.format.file_format = 'PNG'
    depth_map_output.format.color_depth = '16'
    depth_map_output.format.compression = 0
    depth_map_output.base_path = output_path + "depth_map/"
    depth_map_output.file_slots[0].path = "Image####"
    depth_map_output.location = mu.Vector((740, 205))

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


def generate_light(i, decider):
    cust_props = bpy.context.scene.custom_properties

    global light_intensity
    if cust_props.light_min_intensity == 0.0 and cust_props.light_max_intensity == 0.0:
        light_intensity = 3
    else:
        light_intensity = random.uniform(cust_props.light_min_intensity, cust_props.light_max_intensity)

    if decider < 0.5:
        light_data = bpy.data.lights.new(name="l{}".format(i + 1), type='POINT')
        light_data.energy = light_intensity * 10
        light_data.shadow_soft_size = 1
        light_object = bpy.data.objects.new(name=light_data.name, object_data=light_data)
        bpy.context.collection.objects.link(light_object)
        light_object.location = mu.Vector((
            random.uniform(cust_props.light_min_pos_x, cust_props.light_max_pos_x),
            random.uniform(cust_props.light_min_pos_y, cust_props.light_max_pos_y),
            random.uniform(cust_props.light_min_pos_z, cust_props.light_max_pos_z)
        ))
    else:
        light_data = bpy.data.lights.new(name="l{}".format(i + 1), type='SUN')
        shifted_energy = light_intensity
        while shifted_energy > 1:
            shifted_energy /= 10
        light_data.energy = 1.0 + shifted_energy
        light_object = bpy.data.objects.new(name=light_data.name, object_data=light_data)
        bpy.context.collection.objects.link(light_object)
        light_object.location = mu.Vector((
            random.uniform(cust_props.light_min_pos_x, cust_props.light_max_pos_x),
            random.uniform(cust_props.light_min_pos_y, cust_props.light_max_pos_y),
            random.uniform(cust_props.light_min_pos_z, cust_props.light_max_pos_z)
        ))
        light_object.rotation_euler = mu.Vector((
            random.uniform(cust_props.light_min_rot_x, cust_props.light_max_rot_x),
            random.uniform(cust_props.light_min_rot_y, cust_props.light_max_rot_y),
            random.uniform(cust_props.light_min_rot_z, cust_props.light_max_rot_z)
        ))


def create_lights():
    cust_props = bpy.context.scene.custom_properties

    for light in bpy.data.lights:
        bpy.data.lights.remove(light)

    if cust_props.point_lights is True and cust_props.sun_lights is True:
        for i in range(0, cust_props.lights_count):
            decider = random.uniform(0, 1)
            generate_light(i, decider)

    elif cust_props.point_lights is True and cust_props.sun_lights is not True:
        for i in range(0, cust_props.lights_count):
            generate_light(i, 0)

    elif cust_props.point_lights is not True and cust_props.sun_lights is True:
        for i in range(0, cust_props.lights_count):
            generate_light(i, 1)


# Separate every object to another collection and layer
def separate_objects_to_render_layers():
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
            if o.name.find("Plane") == -1 and o.name.find("plane") == -1:
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
            if o.name.find("Plane") == -1 and o.name.find("plane") == -1:
                if layers.find(o.name) == -1:
                    layers.new(o.name)

    for o in objects:
        if o.type == 'MESH':
            if o.name.find("Plane") == -1 and o.name.find("plane") == -1:
                for col in collections:
                    if o.name != col.name:
                        layers[o.name].layer_collection.children[o.name].exclude = True

    for o in objects:
        if o.type == 'MESH':
            if o.name.find("Plane") == -1 and o.name.find("plane") == -1:
                for col in collections:
                    if o.name != col.name:
                        layers[o.name].layer_collection.children[col.name].exclude = True
                    else:
                        layers[o.name].layer_collection.children[col.name].exclude = False


def save_positions():
    cam_pos = cam.location.copy()

    for i in range(0, len(bpy.data.objects)):
        print("{}. object relative camera pos: {}".format(i, cam_pos - bpy.data.objects[i].location))


# Handles the placement of all objects in the scene and renders images
def rotate_and_render(context):
    cust_props = context.scene.custom_properties

    if cust_props.return_to_original:
        save_current_objects_in_scene()

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    global output_path
    output_path = os.path.expanduser("~/Desktop/Renders/{}/".format(dt_string))

    for scene in bpy.data.scenes:
        scene.render.engine = 'CYCLES'

    bpy.context.scene.frame_set(1)

    separate_objects_to_render_layers()
    create_node_tree()

    for i in range(cust_props.render_count):

        set_variables(cust_props)
        create_lights()

        if cam_dist != 0.0:
            cam.location = mu.Vector((0, 0, 0))
            cam.rotation_euler = [math.radians(90) + cam_rot_x, cam_rot_z, cam_rot_y]

            bpy.ops.object.select_all(action='DESELECT')
            cam.select_set(True)
            bpy.ops.transform.translate(value=[0, 0, cam_dist], orient_type='LOCAL')

        if cust_props.render_checkbox:
            context.scene.render.filepath = os.path.expanduser(
                "~/Desktop/Renders/{}/images/image{}{}".format(dt_string, i+1, bpy.context.scene.render.file_extension)
            )

            print("Rendering image{}{}...".format(i+1, bpy.context.scene.render.file_extension))
            bpy.ops.render.render(write_still=True)

            for o in bpy.data.objects:
                if o.type == 'MESH':
                    if o.name.find("Plane") == -1 and o.name.find("plane") == -1:
                        os.rename(output_path + "id_masks/{}/{}0001.png".format(o.name, o.name),
                                  output_path + "id_masks/{}/{}_{}.png".format(o.name, o.name, i + 1))
                        os.rename(output_path + "mask_visib/{}/{}0001.png".format(o.name, o.name),
                                  output_path + "mask_visib/{}/{}_{}.png".format(o.name, o.name, i + 1))

            os.rename(output_path + "depth_map/Image0001.png",
                      output_path + "depth_map/depth_map{}.png".format(i+1))

    # scale = get_scale(context)

    if cust_props.return_to_original:
        reset_saved_objects()
