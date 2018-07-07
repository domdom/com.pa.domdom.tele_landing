#!/usr/bin/env python3
import os
import shutil

from pa_tools.pa import pafs
from pa_tools.pa import paths
from pa_tools.pa import pajson
from pa_tools.pa import spec

from pa_tools.mod.generator import update_modinfo, process_changes

print ('-------------------------------')
print ('PA MEDIA DIR:', paths.PA_MEDIA_DIR)
print ('-------------------------------')
print ('')

from tele_landing import run as generate_tele_landing

debug_mode = False

def create_source_fs():
    # setting up source file system
    src = pafs(paths.PA_MEDIA_DIR)

    src.mount('/pa', '/pa_ex1')
    src.mount('/src', '.')

    return src

def load_json(loader, path):
    resolved = loader.resolveFile(path)
    json, warnings = pajson.loadf(resolved)
    for w in warnings:
        print (w)
    return json


def generate_mod():
    out_dir = '../'
    global debug_mode

    # create the base file system
    src = create_source_fs()
    modinfo = load_json(src, '/src/modinfo.json')
    modinfo = update_modinfo(modinfo)

    destination_path = os.path.join(out_dir, 'modinfo.json')
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, 'w', newline='\n') as dest:
        pajson.dump(modinfo, dest, indent=2)

    # remove destination files
    shutil.rmtree(os.path.join(out_dir, 'pa'), ignore_errors=True)

    effect_path = 'pa/effects/specs'
    src_effect_file = os.path.join(effect_path, 'default_commander_landing.pfx')
    dst_effect_file = os.path.join(effect_path, 'ping.pfx')

    process_changes([generate_tele_landing()], src, out_dir)
    if debug_mode:
        print('copying ping.pfx')
        shutil.copy(os.path.join(out_dir, src_effect_file), os.path.join(paths.PA_MEDIA_DIR, dst_effect_file))

    ################# copy mod to pa mod directory
    mod_path = os.path.join(paths.PA_DATA_DIR, modinfo['context'] + '_mods', modinfo['identifier'])
    shutil.rmtree(mod_path + '/pa', ignore_errors=True)
    shutil.copytree(out_dir + '/pa', os.path.join(mod_path, 'pa'))
    shutil.copyfile(out_dir + '/modinfo.json', os.path.join(mod_path, 'modinfo.json'))


generate_mod()

