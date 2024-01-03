import math
import pymunk


def calculate_distance(p1, p2):
    distance = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    return distance


def calculate_coordinates(body, length, angle):
    angle = angle * (math.pi / 180)
    x = abs(length * math.cos(angle))
    y = abs(length * math.sin(angle))

    if -180 * (math.pi / 180) <= angle < -90 * (math.pi / 180):
        x = -x
        y = -y
    elif -90 * (math.pi / 180) <= angle < 0 * (math.pi / 180):
        y = -y
    elif 0 * (math.pi / 180) <= angle < 90 * (math.pi / 180):
        pass
    elif 90 * (math.pi / 180) <= angle < 180 * (math.pi / 180):
        x = -x

    vector = pymunk.Vec2d(x, y).rotated(body.angle)

    return vector.__add__(body.position)


def append_row_to_file(filename, number1, number2):
    with open(filename, 'a') as file:
        file.write(f"{number1},{number2}\n")
