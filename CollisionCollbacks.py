import pymunk


def coll_begin(arbiter, space, data):
    shape_0 = arbiter.shapes[0]
    shape_1 = arbiter.shapes[1]

    # Prey and Predator collides - eating handle
    if not isinstance(shape_0, pymunk.Segment) and not isinstance(shape_1, pymunk.Segment):
        if shape_0.creature.who_am_I != shape_1.creature.who_am_I:
            if shape_0.creature.who_am_I == 'Prey':
                shape_0.creature.remove(space)
                data['Preys'].remove(shape_0.creature)
                shape_1.creature.eat()
            else:
                shape_1.creature.remove(space)
                if shape_1.creature:
                    data['Preys'].remove(shape_1.creature)
                shape_0.creature.eat()
    return True
