from abc import abstractmethod
import pygame
import pymunk
import torch

from Brain import Brain
from Utils import calculate_coordinates, calculate_distance


class Creature:

    def __init__(self):
        self.VEL_FORCE = 500
        self.ANGLE_FORCE = 0.1
        self.BRAKE_RATIO = 0.85
        self.who_am_I = None
        self.max_energy = 10000
        self.energy_cost = 10
        self.energy_renewal = None
        self.max_split = None
        self.radius = 25
        self.mass = 10
        self.shape_elasticity = 0.4
        self.start_position = None
        self.color = None
        self.vision_lines_count = 10
        self.angle_between_vision_lines = None
        self.vision_range = None
        self.shape_category = None

        self.energy = self.max_energy
        self.children = 0
        self.generation = 0
        self.split = 0
        self.pymunk_object = None
        self.clicked = False
        self.controlled = False
        self.vision_lines = []
        self.vision_distances = []
        self.brain = None
        self.create_brain()

    @abstractmethod
    def update(self, screen):
        ...

    @abstractmethod
    def energy_update(self, is_moving):
        ...

    @abstractmethod
    def split_child(self, space):
        ...

    @abstractmethod
    def print_stats(self):
        ...

    def create_brain(self):
        self.brain = Brain()

    def movement_handle(self):
        self.brake_movement_handle()

        if not self.controlled:
            pass
            # input_tensor = torch.tensor(self.vision_distances, dtype=torch.float32).unsqueeze(0)
            # with torch.no_grad():
            #     output_tensor = self.brain(input_tensor)
            #
            # output_list = output_tensor.squeeze().tolist()
            #
            # if output_list[0] > 0.5:
            #     self.pymunk_object.body.angle -= self.ANGLE_FORCE
            # if output_list[1] > 0.5 and self.energy >= self.energy_cost:
            #     self.pymunk_object.body.apply_impulse_at_local_point((self.VEL_FORCE, 0))
            #     self.energy_update(True)
            # if output_list[2] > 0.5:
            #     self.pymunk_object.body.angle += self.ANGLE_FORCE
        else:
            keys_pressed = pygame.key.get_pressed()
            self.movement_handle_keyboard(keys_pressed)

    def create_pymunk_object(self, space, radius, mass):
        body = pymunk.Body()
        body.position = self.start_position
        shape = pymunk.Circle(body, radius)
        shape.creature = self
        shape.mass = mass
        shape.elasticity = self.shape_elasticity
        shape.color = self.color
        space.add(body, shape)

        return shape

    def vision_update(self, space):
        for line in self.vision_lines:
            space.remove(line)
        self.vision_lines.clear()

        for i in range(self.vision_lines_count):
            angle = (-self.vision_lines_count/2 + i) * self.angle_between_vision_lines + self.angle_between_vision_lines/2
            dest_cords = calculate_coordinates(self.pymunk_object.body, self.vision_range, angle)
            contact_info = space.segment_query_first(self.pymunk_object.body.position, dest_cords, 1, pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS() ^ self.shape_category))

            if self.clicked:
                if contact_info:
                    line = pymunk.Segment(space.static_body, self.pymunk_object.body.position, contact_info.point, 0.5)
                    self.vision_distances[i] = calculate_distance(self.pymunk_object.body.position, contact_info.point) - 25
                else:
                    line = pymunk.Segment(space.static_body, self.pymunk_object.body.position, dest_cords, 1)
                    self.vision_distances[i] = self.vision_range

                line.sensor = True
                line.color = (128, 128, 128, 1)
                self.vision_lines.append(line)
                space.add(line)

    def brake_movement_handle(self):
        self.pymunk_object.body.angular_velocity = 0
        self.pymunk_object.body.velocity *= self.BRAKE_RATIO
        if abs(self.pymunk_object.body.velocity[0]) <= 1 and abs(self.pymunk_object.body.velocity[1]) <= 1:
            self.pymunk_object.body.velocity = (0, 0)

    def movement_handle_keyboard(self, keys_pressed):
        if keys_pressed[pygame.K_UP] and self.energy >= self.energy_cost:
            self.pymunk_object.body.apply_impulse_at_local_point((self.VEL_FORCE, 0))
            self.energy_update(True)
        if keys_pressed[pygame.K_LEFT]:
            self.pymunk_object.body.angle -= self.ANGLE_FORCE
        if keys_pressed[pygame.K_RIGHT]:
            self.pymunk_object.body.angle += self.ANGLE_FORCE

    def remove(self, space):
        for line in self.vision_lines:
            space.remove(line)
        space.remove(self.pymunk_object.body, self.pymunk_object)
