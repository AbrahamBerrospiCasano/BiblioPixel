from bibliopixel.drivers.SimPixel import SimPixel
from bibliopixel.layout.circle import Circle
from bibliopixel.layout import geometry
from bibliopixel.animation.sequence import Sequence
from bibliopixel.util import class_name
from BiblioPixelAnimations.circle.bloom import CircleBloom
from BiblioPixelAnimations.circle.swirl import Swirl
from BiblioPixelAnimations.circle.hyperspace import HyperspaceRainbow
from BiblioPixelAnimations.strip.Wave import Wave
import math


BLOOM = {
    'driver': {
        'typename': 'simpixel',
        'num': 0
    },

    'layout': {
        'typename': 'matrix',
        'width': 0,
        'height': 0,
    },

    'animation': {
        'typename': 'BiblioPixelAnimations.matrix.bloom.Bloom'
    },

    'run': {
        'amt': 6,
        'fps': 30
    }
}


MATRIX_PROJECT = {
    'driver': {
        'typename': 'simpixel',
        'num': 0
    },

    'layout': {
        'typename': 'matrix',
        'width': 0,
        'height': 0,
    },

    'animation': {
        'typename': 'sequence',
        'animations': [
            {
                'animation':
                'BiblioPixelAnimations.matrix.MatrixRain.MatrixRainBow',
                'run': {
                    'amt': 1,
                    'fps': 20,
                    'seconds': 8,
                },
            },
            {
                'animation': {
                    'typename': 'BiblioPixelAnimations.matrix.Text.ScrollText',
                    'xPos': 16,
                    'font_scale': 2,
                    'text': 'BiblioPixel Demo'
                },
                'run': {
                    'amt': 1,
                    'fps': 20,
                    'seconds': 8,
                    'until_complete': True,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.matrix.bloom.Bloom',
                'run': {
                    'amt': 3,
                    'fps': 60,
                    'seconds': 8,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.matrix.circlepop.CirclePop',
                'run': {
                    'amt': 1,
                    'fps': 15,
                    'seconds': 8,
                },
            },
        ],
    },
}

CUBE_PROJECT = {
    'driver': {
        'typename': 'simpixel',
        'num': 0
    },

    'layout': {
        'typename': 'cube',
        'x': 0,
        'y': 0,
        'z': 0
    },

    'animation': {
        'typename': 'sequence',
        'animations': [
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.cube.wave_spiral.WaveSpiral',
                    'dir': False,
                    'offset': 6
                },
                'run': {
                    'amt': 1,
                    'fps': 15,
                    'seconds': 8
                },
            },
            {
                'animation': 'BiblioPixelAnimations.cube.Rain.RainBow',
                'run': {
                    'amt': 1,
                    'fps': 10,
                    'seconds': 8
                },
            },
            {
                'animation': 'BiblioPixelAnimations.cube.bloom.CubeBloom',
                'run': {
                    'amt': 6,
                    'fps': 20,
                    'seconds': 8,
                },
            }
        ],
    },
}

_PIXELS_PER = [1, 4, 8, 12, 18, 24, 32, 40, 52, 64]
_RINGS, _STEPS = geometry.make_circle_coord_map(pixels_per=_PIXELS_PER)
_POINTS = geometry.make_circle_coord_map_positions(
    _RINGS, origin=(200, 200, 0), z_diff=16)

CIRCLE_PROJECT = {
    'driver': {
        'typename': 'simpixel',
        'num': sum(_PIXELS_PER),
        'pixel_positions': _POINTS,
    },

    'layout': {
        'typename': 'circle',
        'rings': _RINGS,
        'maxAngleDiff': 0,
    },

    'animation': {
        'typename': 'sequence',
        'length': 8,
        'animations': [
            class_name.class_name(CircleBloom),
            class_name.class_name(Swirl),
            class_name.class_name(HyperspaceRainbow)]
    }
}


def circle(args):
    pixels_per = [1, 4, 8, 12, 18, 24, 32, 40, 52, 64]
    rings, steps = geometry.make_circle_coord_map(pixels_per=pixels_per)
    points = geometry.make_circle_coord_map_positions(
        rings, origin=(200, 200, 0), z_diff=16)
    driver = SimPixel(sum(pixels_per), pixel_positions=points)
    layout = Circle(driver, rings=rings, maxAngleDiff=0)
    anim = Sequence(layout)

    anim.add_animation(CircleBloom(layout), amt=3, fps=30, seconds=8)
    anim.add_animation(Swirl(layout, angle=4), amt=6, fps=15, seconds=8)
    anim.add_animation(HyperspaceRainbow(layout), fps=15, seconds=8)

    return anim

####################
# adding fluidicData as demo since loading of python modules via bp CLI seems broken

num_rings = []
num_points = []

num_pods = 8
num_flowers = 6
pod_leds = 8
flower_leds = 12
pod_ring = [0, 1, 2, 3, 4, 5, 6, 7] #    rings, steps = geometry.make_circle_coord_map(pixels_per=[pods_leds])
flower_ring = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
x_off = 200
y_off = 200

for ring in range(0,num_pods*2,2):
    # 2x 8 LED rings per pod
    points = geometry.make_circle_coord_map_positions(
        [pod_ring], origin=(x_off, y_off, ring*10), radii=[1 * math.pi]*pod_leds)
    num_rings += [[r+pod_leds*ring for r in pod_ring]] # add with offset
    num_points += points
    # second pod ring
    points = geometry.make_circle_coord_map_positions(
        [pod_ring], origin=(x_off, y_off, ring*10+4), radii=[1 * math.pi]*pod_leds)
    num_rings += [[r+pod_leds*(ring+1) for r in pod_ring]] # add with offset
    num_points += points


for ring in range(num_flowers):
    # distribute as spiral
    theta = ring / 3 * math.pi * 2
    x = int(x_off + math.sin(theta) * 4)
    y = int(y_off + math.cos(theta) * 4)
    # 1x 12 LED ring per flower
    points = geometry.make_circle_coord_map_positions(
        [flower_ring], origin=(x, y, (num_pods-1)*23 + ring*7), radii=[3 * math.pi]*flower_leds)
    num_rings += [[r+flower_leds*ring for r in flower_ring]] # add with offset
    num_points += points



FD_PROJECT = {
    'driver': {
        'typename': 'simpixel',
        'num': len(num_points),
        'pixel_positions': num_points,
    },
    'controls': {
    'typename': '.rest',
    'verbose': 'true',
    },
    'layout': {
        'typename': 'circle',
        'rings': num_rings,
        'maxAngleDiff': 0,
    },

    'animation': {
        'typename': 'split',
        'size': [16,16,16,16,16,16,16,16,12,12,12,12,12,12],
        'animations': [
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.strip.Wave.Wave',
                },
                'run': {
                    'amt': 1,
                    'fps': 30,
                },
            },
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.strip.WhiteTwinkle.WhiteTwinkle',
                        'speed': 20
                },
                'run': {
                    'amt': 1,
                    'fps': 30,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.strip.Searchlights.Searchlights',
                'run': {
                    'amt': 1,
                    'fps': 30,
                },
            },
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.strip.LarsonScanners.LarsonScanner',
                        'color': 'white'
                },
                'run': {
                    'amt': 3,
                    'fps': 30,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.strip.Rainbows.Rainbow',
                'run': {
                    'amt': 5,
                    'fps': 30,
                },
            },
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.strip.LarsonScanners.LarsonScanner',
                        'color': 'red'
                },
                'run': {
                    'amt': 4,
                    'fps': 30,
                },
            },
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.strip.LarsonScanners.LarsonScanner',
                        'color': 'green'
                },
                'run': {
                    'amt': 7,
                    'fps': 30,
                },
            },
            {
                'animation': {
                    'typename': 'BiblioPixelAnimations.strip.Rainbows.RainbowCycle', 
                 },
                'run': {
                    'amt': 9,
                    'fps': 30,
                },
            },
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.strip.LarsonScanners.LarsonScanner',
                        'color': 'blue'
                },
                'run': {
                    'amt': 2,
                    'fps': 15,
                },
            },
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.strip.Wave.Wave',
                        'color': 'green'
                },
                'run': {
                    'amt': 1,
                    'fps': 30,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.strip.Rainbows.Rainbow',
                'run': {
                    'amt': 12,
                    'fps': 30,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.strip.ColorFade.ColorFade',
                'run': {
                    'amt': 1,
                    'fps': 30,
                },
            },
            {
                'animation': {
                    'typename':
                        'BiblioPixelAnimations.strip.Wave.Wave',
                        'color': 'blue'
                },
                'run': {
                    'amt': 1,
                    'fps': 30,
                },
            },
            {
                'animation': 'BiblioPixelAnimations.strip.Rainbows.Rainbow',
                'run': {
                    'amt': 15,
                    'fps': 30,
                },
            }
        ]
    }
}

DEMO_TABLE = {
    'bloom': BLOOM,
    'circle': CIRCLE_PROJECT,
    'cube': CUBE_PROJECT,
    'matrix': MATRIX_PROJECT,
    'fluidicData': FD_PROJECT
}