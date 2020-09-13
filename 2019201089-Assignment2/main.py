import glm
from tqdm import tqdm
import math
from ray import ray
from util import random_double, clamp

from sphere import sphere
from hittable import *
from hittable_list import hittable_list
from camera import camera


def write_color(file, color: glm.vec3, samples_per_pixel: int = 1):
    if file:
        r, b, g = color.x, color.y, color.z
        scale = 1 / samples_per_pixel

        r *= scale
        g *= scale
        b *= scale

        file.write('%d %d %d\n' % (256 * clamp(r, 0, .999),
                                   256 * clamp(g, 0, .999),
                                   256 * clamp(b, 0, .999)))


def ray_color(r: ray, world: hittable) -> glm.vec3:
    rec = hit_record()

    if world.hit(r, 0, math.inf, rec):
        return .5 * (rec.normal + glm.vec3(1., 1., 1.))

    unit_direction = glm.normalize(r.direction())
    t = .5 * (unit_direction.y + 1.)
    # both glms vectors are color vectors
    return (1. - t) * glm.vec3(1., 1., 1.) + t * glm.vec3(.5, .7, 1.)


# Image
aspect_ratio = 16 / 9
width = 512
height = int(width / aspect_ratio)
samples_per_pixel = 4

# Camera
cam = camera()

# World
world = hittable_list(sphere(glm.vec3(0, -100.5, -1), 100))
world.add(sphere(glm.vec3(0, 0, -1), .5))

with open('aliased_sphere.ppm', 'w') as f:
    f.write('P3\n%d %d\n255\n' % (width, height))
    for j in tqdm(range(height - 1, -1, -1), desc='loading:'):
        for i in range(width):
            pixel_color = glm.vec3(0, 0, 0)
            for s in range(samples_per_pixel):
                u, v = (i + random_double()) / (width - 1), (j + random_double()) / (height - 1)
                r = cam.get_ray(u, v)
                pixel_color += ray_color(r, world)

            write_color(f, pixel_color, samples_per_pixel)
