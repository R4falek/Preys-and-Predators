import numpy as np
import pymunk
from Creature import Creature


class Predator(Creature):

    def __init__(self, space):
        super().__init__()
        self.who_am_I = 'Predator'
        self.energy_renewal = 400
        self.max_split = 2
        self.max_digestion = 120
        self.angle_between_vision_lines = 5
        self.vision_range = 150
        self.start_position = (300, 300)
        self.color = (255, 0, 0, 100)
        self.digestion = 0
        self.shape_category = 0b10

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
        self.energy += self.energy_renewal
        self.eaten += 1
        if self.energy > self.max_energy:
            self.energy = self.max_energy

        if self.digestion == 0:
            if self.split < self.max_split:
                self.split += 1
            else:
                self.split = 0

        self.digestion = self.max_digestion

    def energy_update(self, is_moving):
        if self.energy >= self.energy_cost and is_moving:
            self.energy -= self.energy_cost

    def print_stats(self):
        print('Energy ', self.energy)
        print('Split ', self.split)
        print('digestion ', self.digestion)
        print('Vision ', self.vision_distances)

    def split_child(self, space):
        child = Predator(space)
        child.generation = self.generation + 1
        child.pymunk_object.body.position = self.pymunk_object.body.position
        self.split = 0
        self.children += 1
        return child
