import random

import numpy as np
import pymunk
from Creature import Creature


class Prey(Creature):

    def __init__(self, space, brain=None):
        super().__init__(brain)
        self.who_am_I = 'Prey'
        self.energy_renewal = 1
        self.max_split = 600
        self.angle_between_vision_lines = 30
        self.vision_range = 150
        self.start_position = (200, 200)
        self.color = (0, 255, 0, 100)
        self.shape_category = 0b01

        self.pymunk_object = self.create_pymunk_object(space, self.radius, self.mass)
        self.pymunk_object.filter = pymunk.ShapeFilter(categories=self.shape_category)
        self.vision_distances = np.full(self.vision_lines_count, self.vision_range)
        self.clicked = False
        self.split = random.randint(0, self.max_split // 2)

    def update(self, space):
        self.energy_update(False)
        self.split_update()
        self.movement_handle()
        self.vision_update(space)

    def split_update(self):
        self.brain.show_model(self.brain, self.vision_distances)
        input(r)
        if self.split < self.max_split:
            self.split += 1
        else:
            self.split = 0

    def energy_update(self, is_moving):
        if self.energy >= self.energy_cost and is_moving:
            self.energy -= self.energy_cost
        elif self.energy < self.max_energy and self.pymunk_object.body.velocity == (0, 0):
            self.energy += self.energy_renewal

    def print_stats(self):
        print('Energy ', self.energy)
        print('Split ', self.split)
        print('Vision ', self.vision_distances)

    def split_child(self, space):
        child = Prey(space, self.brain)
        child.generation = self.generation + 1
        child.pymunk_object.body.position = self.pymunk_object.body.position
        self.children += 1
        return child
