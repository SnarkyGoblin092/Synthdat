import json
import random
import mathutils as mu
from .installer import install_modules

try:
    import bpy
    import numpy as np
    from . import utils
    from . import calc
except ImportError:
    install_modules()

    import bpy
    import numpy as np
    from . import utils
    from . import calc

object_ids_filepath = ''
id_dict = {}


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


def construct_scene_gt_json(last, file, it, objects, camera):
    data = {}
    data[f'{it}'] = []
    i = 0
    for obj in objects:
        if obj.type == 'MESH' and obj.name in id_dict.values():
            rot_matrix = calc.get_relative_rotation_matrix(obj.rotation_euler, camera.rotation_euler)
            rot_matrix = np.ravel(rot_matrix)
            loc_diff = np.array(obj.location - camera.location)

            data[f'{it}'].append({
                'cam_R_m2c': rot_matrix,
                'cam_t_m2c': loc_diff,
                'obj_id': utils.get_key(obj.name)
            })
            i += 1
    data_str = json.dumps(data, cls=NumpyArrayEncoder)[1:-1]
    if not last:
        data_str += ','
    file.write(f'{data_str}\n')


def construct_scene_camera_json(last, file, it, camera):
    data = {}
    rot_matrix = calc.get_relative_rotation_matrix(mu.Vector([0, 0, 0]), camera.rotation_euler)
    rot_matrix = np.ravel(rot_matrix)
    data[f'{it}'] = {
        'cam_K': np.ravel(calc.calc_cam_k()),
        'scale': utils.scale,
        'cam_R_w2c': rot_matrix,
        'cam_t_w2c': np.array(camera.location)
    }

    data_str = json.dumps(data, cls=NumpyArrayEncoder)[1:-1]
    if not last:
        data_str += ','
    file.write(f'{data_str}\n')


def construct_id_dictionary():
    global id_dict
    id_dict.clear()

    with open(bpy.path.abspath(object_ids_filepath), 'r') as file:

        lines = file.readlines()

        for line in lines:
            split_line = line.split()
            obj_id = split_line[0]
            name = split_line[1]
            id_dict[int(obj_id)] = name


def construct_light(i, decider):
    cust_props = bpy.context.scene.custom_properties

    if cust_props.light_min_intensity == 0.0 and cust_props.light_max_intensity == 0.0:
        utils.light_intensity = 3
    else:
        utils.light_intensity = random.uniform(cust_props.light_min_intensity, cust_props.light_max_intensity)

    if decider < 0.5:
        light_data = bpy.data.lights.new(name=f'light_{i + 1}', type='POINT')
        light_data.energy = utils.light_intensity * 10
        light_data.shadow_soft_size = 1
        light_object = bpy.data.objects.new(name=light_data.name, object_data=light_data)
        bpy.context.collection.objects.link(light_object)
        light_object.location = mu.Vector((
            random.uniform(cust_props.light_min_pos_x, cust_props.light_max_pos_x),
            random.uniform(cust_props.light_min_pos_y, cust_props.light_max_pos_y),
            random.uniform(cust_props.light_min_pos_z, cust_props.light_max_pos_z)
        ))
    else:
        light_data = bpy.data.lights.new(name=f'light_{i + 1}', type='SUN')
        shifted_energy = utils.light_intensity
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


def construct_lights():
    cust_props = bpy.context.scene.custom_properties

    for light in bpy.data.lights:
        bpy.data.lights.remove(light)

    if cust_props.point_lights is True and cust_props.sun_lights is True:
        for i in range(0, cust_props.lights_count):
            decider = random.uniform(0, 1)
            construct_light(i, decider)

    elif cust_props.point_lights is True and cust_props.sun_lights is not True:
        for i in range(0, cust_props.lights_count):
            construct_light(i, 0)

    elif cust_props.point_lights is not True and cust_props.sun_lights is True:
        for i in range(0, cust_props.lights_count):
            construct_light(i, 1)


# Separate every object to another collection and layer
def construct_object_layers():
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
            if o.name in id_dict.values():
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
            if o.name in id_dict.values():
                if layers.find(o.name) == -1:
                    layers.new(o.name)

    for o in objects:
        if o.type == 'MESH':
            if o.name in id_dict.values():
                for col in collections:
                    if o.name != col.name:
                        layers[o.name].layer_collection.children[o.name].exclude = True

    for o in objects:
        if o.type == 'MESH':
            if o.name in id_dict.values():
                for col in collections:
                    if o.name != col.name:
                        layers[o.name].layer_collection.children[col.name].exclude = True
                    else:
                        layers[o.name].layer_collection.children[col.name].exclude = False


# Generate and arrange a node tree with the given settings
def construct_node_tree(per_row=4):
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
            if objects[i].name in id_dict.values():
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
        outputs[i].base_path = utils.output_path + 'mask/'
        outputs[i].file_slots[0].path = f'{outputs[i].name}####'
        outputs[i].format.color_mode = 'BW'
        outputs[i].format.file_format = 'PNG'
        outputs[i].format.compression = 100
        cut_outputs[i].base_path = utils.output_path + 'mask_visib/'
        cut_outputs[i].file_slots[0].path = f'{outputs[i].name}####'
        cut_outputs[i].format.color_mode = 'BW'
        cut_outputs[i].format.file_format = 'PNG'
        cut_outputs[i].format.compression = 100

    render_layers.append(bpy.context.scene.node_tree.nodes.new('CompositorNodeRLayers'))
    denoise = bpy.context.scene.node_tree.nodes.new('CompositorNodeDenoise')
    compositor = bpy.context.scene.node_tree.nodes.new('CompositorNodeComposite')
    depth_map_range = bpy.context.scene.node_tree.nodes.new('CompositorNodeMapRange')
    depth_map_output = bpy.context.scene.node_tree.nodes.new('CompositorNodeOutputFile')

    y = 0
    for i in range(0, len(objects.items())):
        if objects[i].type == 'MESH':
            if objects[i].name in id_dict.values():
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
    depth_map_output.format.compression = 100
    depth_map_output.base_path = utils.output_path + 'depth/'
    depth_map_output.file_slots[0].path = 'Image####'
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

