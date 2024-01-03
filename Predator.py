import numpy as np
import pymunk
import random

from Creature import Creature


class Predator(Creature):

    def __init__(self, space, brain=None, spawn_range=800):
        super().__init__(brain)
        self.who_am_I = 'Predator'
        self.energy_renewal = 2000
        self.max_split = 3
        self.max_digestion = 100
        self.angle_between_vision_lines = 2
        self.vision_range = 550
        self.start_position = (random.randint(0, spawn_range), random.randint(0, spawn_range))
        self.color = (255, 0, 0, 100)
        self.digestion = 0
        self.shape_category = 0b10
        self.VEL_FORCE = 600
        self.ANGLE_FORCE = 0.2
        self.BRAKE_RATIO = 0.9

        self.eaten = 0
        self.pymunk_object = self.create_pymunk_object(space, self.radius, self.mass)
        self.pymunk_object.filter = pymunk.ShapeFilter(categories=self.shape_category)
        self.vision_distances = np.full(self.vision_lines_count, self.vision_range)
        self.clicked = False

    def update(self, space):
        self.energy_update(False)
        self.digestion_update()
        self.movement_handle()
        self.vision_update(space)

    def digestion_update(self):
        if self.digestion > 0:
            self.digestion -= 1

    def eat(self):
        self.eaten += 1

        if self.digestion == 0:
            self.energy += self.energy_renewal
        if self.energy > self.max_energy:
            self.energy = self.max_energy

        if self.split < self.max_split:
            self.split += 1
        else:
            self.split = 0

        self.digestion = self.max_digestion

    def energy_update(self, is_moving):
        if self.energy >= self.energy_cost and is_moving:
            self.energy -= self.energy_cost
        else:
            self.energy -= self.energy_cost // 2

    def print_stats(self):
        print('Energy ', self.energy)
        print('Split ', self.split)
        print('digestion ', self.digestion)
        print('Vision ', self.vision_distances)

    def split_child(self, space):
        child = Predator(space, self.brain.modify_weights(1))
        child.generation = self.generation + 1
        child.pymunk_object.body.position = self.pymunk_object.body.position
        self.split = 0
        self.children += 1
        return child
