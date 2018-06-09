import utils
import loader
import pajson

import math
import copy
import random
import colorsys

false = False
true = True

def load_json(path):
	with open(path, 'r') as f:
		return pajson.load(f)

base_pointlight = load_json("base/pointlight.json")
base_orb = load_json("base/orb.json")
base_outer_orb = load_json("base/outer_orb.json")

initial_orb = load_json("base/initial_orb.json")

total_time = 7.0;

effects = []
# there are two orbs
# make the orb here
base_orb['emissionRate'] = 7
base_orb['delay'] = 0.7
# def rainbow(n, offset=0, scale=1, revs=1, time=1):
base_orb['red'], base_orb['green'], base_orb['blue'] = (0.1, 0.3, 16)
effects.append(base_orb)

base_orb = copy.deepcopy(base_orb)
base_orb['delay'] = 0.7 + 0.5 / base_orb['emissionRate']
# base_orb['emitterLifetime'] = 3
base_orb['red'], base_orb['green'], base_orb['blue'] = (0.5, 1.8, 5)
effects.append(base_orb)

base_orb = copy.deepcopy(base_orb)
base_orb['delay'] = 0.7 + 0.5 / base_orb['emissionRate']
# base_orb['emitterLifetime'] = 3
base_orb['red'], base_orb['green'], base_orb['blue'] = (0.6 , 0.5, 10)

light_flecks = load_json("base/light_flecks.json")

base_sparks = load_json("base/sparks.json")

effects.append(base_orb)
effects.append(base_outer_orb)
effects.append(light_flecks)
effects.append(base_sparks)

explosion = load_json("base/explosion.json")


for effect in explosion:
	effect["delay"] = 5
explosion[1]["delay"] = 5.1

effects = effects

effects += load_json("base/first_explosion_ring.json")


initial_smoke_wave = load_json("base/initial_smoke_wave.json")
effects.append(initial_smoke_wave)

initial_flare = load_json("base/initial_flare.json")
effects.append(initial_flare)

flare2 = copy.deepcopy(initial_flare)
flare2["rotationRange"] = 3.1415


# periodic point light

strobe_light = copy.deepcopy(base_pointlight)

def y(x):
	x = x * 3.0
	return (0.25 * x + 1) * math.fabs(math.sin(math.exp(x)))


# 5\operatorname{abs}\left(\frac{\sin \left(3e^x\right)}{4x+1}\right)
num_steps = 100

strobe_light["alpha"] = 10
strobe_light["offsetZ"] = 50
strobe_light["sizeX"] = 1
strobe_light["spec"]["sizeX"] = [[0, 100], [3, 20]]
strobe_light["spec"]["alpha"] = [[i / num_steps, y(i / num_steps)] for i in range(0, num_steps)]
strobe_light["lifetime"] = 3
strobe_light["delay"] = 2

effects.append(strobe_light)

landing_light = copy.deepcopy(base_pointlight)
landing_light["lifetime"] = 3
landing_light["sizeX"] = 150
landing_light["offsetZ"] = 50
landing_light["delay"] = 5
landing_light["spec"]["alpha"] = [[0, 0], [0.1, 10], [1, 0]]

effects.append(landing_light)

bright_flash_1 = copy.deepcopy(landing_light)

bright_flash_1["lifetime"] = 0.3
bright_flash_1["spec"]["size"] = [[0, 1], [1, 0]]
bright_flash_1["spec"]["red"] = 0.7
bright_flash_1["spec"]["green"] = 1
bright_flash_1["delay"] = 1.8

effects.append(bright_flash_1)

effects.append(flare2)

strobe_rings = load_json("base/explosion_ring.json")


strobe_rings["emissionRate"] = [[0, 0.1], [3, 5]]
strobe_rings["emitterLifetime"] = 2
strobe_rings["delay"] = 2

effects.append(strobe_rings)

super_bright_flash = copy.deepcopy(bright_flash_1)
super_bright_flash["lifetime"] = 0.5
super_bright_flash["delay"] = 5
super_bright_flash["spec"]["red"], super_bright_flash["spec"]["green"], super_bright_flash["spec"]["blue"] = 3, 3, 3
super_bright_flash["sizeX"] = 180
super_bright_flash["offsetZ"] = 50

effects.append(super_bright_flash)

def run():
	num_steps = 100;

	base_pointlight["spec"]["size"] = {"stepped" : True, "keys" : [[0.0125,1],[0.03,0.82],[0.04875,0.72],[0.0725,0.84],[0.10375,0.8],[0.13875,0.86],[0.16625,0.86],[0.21625,0.7],[0.23875,0.86],[0.35375,0.98],[0.685,1],[0.69375,0.88],[0.7075,0.92],[0.795,1.12],[0.91,1.14],[0.935,1.22],[0.96125,1.32],[0.985,1.32],[1,1.36]]}
	base_pointlight["spec"]["alpha"] = [[0,5],[0.015,4.8],[0.02875,4.05],[0.04375,2.2],[0.04875,0.2],[0.065,3.8],[0.07875,4.5],[0.08875,4.9],[0.09375,0.25],[0.10375,4.9],[0.11,1.15],[0.11625,3],[0.12375,2.1],[0.12875,4.8],[0.13625,4.45],[0.1375,4.7],[0.14125,4.9],[0.1525,4.5],[0.15625,4.8],[0.1625,4.5],[0.17,4.9],[0.1775,4.5],[0.20625,4.6],[0.205,5],[0.21375,4.95],[0.2175,4.7],[0.2225,3.6],[0.22375,4.55],[0.235,4.7],[0.24125,4.95],[0.2475,4.7],[0.2625,4.6],[0.2725,3.85],[0.27875,4.65],[0.28375,4.7],[0.28875,4.9],[0.29125,4.75],[1,0]]
	# [[0, 0], [0.1, 10], [0.2, 0], [0.5, 10], [1, 0]]
	# [[0.0025,4],[0.01,3.92],[0.015,3.84],[0.0225,3.64],[0.03,3.08],[0.0375,2.64],[0.0475,1.32],[0.0525,0.24],[0.0525,0.12],[0.06625,3.08],[0.07875,3.16],[0.08625,3.24],[0.09125,2.92],[0.1,2.4],[0.10875,0.52],[0.12,3.36],[0.1275,3.84],[0.14375,3.92],[0.15,3.68],[0.1525,3.24],[0.1725,3.2],[0.1725,3.92],[0.18375,3.96],[0.1875,3.32],[0.20125,3.32],[0.21125,1.88],[0.21625,3.2],[0.22375,3.32],[0.23375,3.88],[0.2475,3.32],[0.27,3.32],[0.28125,3.88],[0.29,3.48],[0.31875,3.44],[0.32125,3.92],[0.33875,3.96],[0.36,3.96],[0.36625,3.4],[0.375,3.48],[0.3825,3.88],[0.39375,3.48],[0.40125,2.36],[0.40125,3.48],[0.4175,3.52],[0.42125,2.72],[0.425,3.48],[0.4475,3.36],[0.45,3],[0.45625,3.44],[0.47,3.64],[0.49125,3.84],[0.715,3.88],[1.00125,4.04]]
	effect = {
	"emitters" : explosion + [
			base_pointlight,
			initial_orb
    	] + effects
	}
	# effect = {
	# "emitters" : explosion
	# }

	return pajson.loads("""[
		{
			"target" : "/pa/effects/specs/default_commander_landing_ent.json",
			"patch" : [
				{"op": "replace", "path" : "/spawn_response/effect_spec", "value" : "/mod/tele_commander_landing.pfx"}
			]
		},
		{
			"target": "/pa/effects/specs/ping_ent.json",
			"destination": "/mod/tele_commander_landing.pfx",
			"patch" : [
				{"op": "replace", "path" : "", "value" : """ + loader.dumps(effect) + """}
			]
		}
		]
		""");