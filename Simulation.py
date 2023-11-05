import pymunk

from CollisionCollbacks import coll_begin
from Prey import Prey
from Predator import Predator


class Simulation:

    def __init__(self, space, border_position):
        self.space = space
        self.max_prey_count = 100
        self.max_predator_count = 100
        self.prey_init_count = 2
        self.predator_init_count = 1
        self.predators = []
        self.preys = []
        self.preys_history_count = []
        self.predators_history_count = []
        self.clicked = None
        self.border_position = border_position

        self.handler = self.space.add_default_collision_handler()
        self.handler.begin = coll_begin
        self.handler.data['Preys'] = self.preys
        self.scale = 1

        self.init_creatures()

    def update(self):
        for prey in self.preys:
            self.split_handle(prey)
            prey.update(self.space)
            self.overflow_handle(prey)
        for predator in self.predators:
            if predator.energy <= 0:
                predator.remove(self.space)
                self.predators.remove(predator)
            else:
                self.split_handle(predator)
                predator.update(self.space)
                self.overflow_handle(predator)

    def scaling(self, scale):
        self.scale = scale
        self.border_position = [i / scale for i in self.border_position]

    def update_history_count(self):
        self.preys_history_count.append(len(self.preys))
        self.predators_history_count.append(len(self.predators))
        if len(self.preys_history_count) > 500 and len(self.predators_history_count) > 500:
            self.predators_history_count.pop(0)
            self.preys_history_count.pop(0)

    def click_creature(self, creature):
        if self.clicked:
            self.clicked.clicked = False
            self.clicked.controlled = False
        if creature:
            self.clicked = creature
            creature.clicked = True
        else:
            self.clicked = None

    def split_handle(self, creature):
        if creature.split == creature.max_split:
            if creature.who_am_I == 'Prey' and len(self.preys) < self.max_prey_count:
                child_prey = creature.split_child(self.space)
                self.preys.append(child_prey)
            elif creature.who_am_I == 'Predator' and len(self.predators) < self.max_predator_count:
                child_predator = creature.split_child(self.space)
                self.predators.append(child_predator)

    def init_creatures(self):
        for i in range(self.prey_init_count):
            prey = Prey(self.space)
            self.preys.append(prey)

        for i in range(self.predator_init_count):
            predator = Predator(self.space)
            self.predators.append(predator)

    def overflow_handle(self, creature):
        if creature.pymunk_object.body.position[0] * self.scale > self.border_position[2]:
            creature.pymunk_object.body.position = (self.border_position[0], creature.pymunk_object.body.position[1])
        elif creature.pymunk_object.body.position[0] * self.scale < self.border_position[0]:
            creature.pymunk_object.body.position = (self.border_position[2] / self.scale, creature.pymunk_object.body.position[1])
        if creature.pymunk_object.body.position[1] * self.scale > self.border_position[3]:
            creature.pymunk_object.body.position = (creature.pymunk_object.body.position[0], self.border_position[1])
        elif creature.pymunk_object.body.position[1] * self.scale < self.border_position[1]:
            creature.pymunk_object.body.position = (creature.pymunk_object.body.position[0], self.border_position[3] / self.scale)

    def move(self, x, y):
        if not self.clicked or (self.clicked and not self.clicked.controlled):
            self.border_position[0] += x
            self.border_position[2] += x
            self.border_position[1] += y
            self.border_position[3] += y
            for prey in self.preys:
                prey.pymunk_object.body.position = prey.pymunk_object.body.position.__add__(pymunk.Vec2d(x, y))
            for predator in self.predators:
                predator.pymunk_object.body.position = predator.pymunk_object.body.position.__add__(pymunk.Vec2d(x, y))
