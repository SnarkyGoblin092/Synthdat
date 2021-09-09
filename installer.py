import bpy
import sys
import subprocess

from bpy.app.handlers import persistent


@persistent
def install_modules():
    subprocess.check_call([sys.executable, '-m', 'ensurepip'])
    path = bpy.utils.resource_path(type='USER') + '/scripts/addons/synthetic_data_gen/requirements.txt'
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', path])