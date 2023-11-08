import pymunk
import pymunk.pygame_util
import pygame
import torch
import time
from Simulation import Simulation

WIDTH, HEIGHT = 1920, 1020
# WIDTH, HEIGHT = 1500, 800
background_colour = (134, 212, 252)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (60, 60, 60)
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
ORANGE = (225, 145, 45)

FPS = 60
dt = 1 / FPS
ticks = 0
start_time = time.time()
elapsed_time = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.WINDOWMAXIMIZED)
pygame.display.set_caption('Prey and Predator')

tile = pygame.image.load("assets/tile.jpg")
tile_position = (0, 0)
TILES_SIZE = (2, 2)
border_position = [tile_position[0], tile_position[1], TILES_SIZE[0] * tile.get_width(),
                   TILES_SIZE[1] * tile.get_height()]

MOVE_SPEED = 20
SCALE = 1

space = pymunk.Space()
space.gravity = (0, 0)
simulation = Simulation(space, border_position)
take_control_but = pygame.Rect(2 * tile.get_width() + 50, 600, 150, 40)

if torch.cuda.is_available():
    print("CUDA is available! You can use GPU acceleration.")
else:
    print("CUDA is not available. Running on CPU.")


def timer_update():
    global elapsed_time
    current_time = time.time()
    new_elapsed_time = current_time - start_time
    if round(new_elapsed_time) != round(elapsed_time):
        simulation.update_history_count()
    elapsed_time = new_elapsed_time


def draw_tiles(tile, size, screen):
    global tile_position
    tile = pygame.transform.scale(tile, (tile.get_width() * SCALE, tile.get_height() * SCALE))
    simulation.border_position = [tile_position[0], tile_position[1], TILES_SIZE[0] * tile.get_width(),
                                  TILES_SIZE[1] * tile.get_height()]
    for x in range(size[0]):
        for y in range(size[1]):
            tile_x = tile_position[0] + x * (tile.get_width() + 0)
            tile_y = tile_position[1] + y * (tile.get_height() + 0)
            screen.blit(tile, (tile_x, tile_y))

    border_height = tile.get_height() * TILES_SIZE[1]
    border_width = tile.get_width() * TILES_SIZE[0]
    pygame.draw.rect(screen, RED, (tile_position[0], tile_position[1], border_width, border_height), 10)


def text_draw(text, color, position, size):
    pygame.font.init()
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, False, color)
    screen.blit(text_surface, position)


def draw_dashboard():
    vertices = [(WIDTH, 0), (2 * tile.get_width(), 0), (2 * tile.get_width(), HEIGHT), (WIDTH, HEIGHT)]
    pygame.draw.polygon(screen, GRAY, vertices)
    pygame.draw.rect(screen, (50, 50, 90), (2 * tile.get_width(), 0, WIDTH - 2 * tile.get_width(), HEIGHT), 10)

    # Default stats
    text_draw('Ticks: ' + str(ticks), WHITE, (2 * tile.get_width() + 50, 50), 30)
    text_draw('Time: ' + str(round(elapsed_time)), WHITE, (2 * tile.get_width() + 50, 100), 30)
    text_draw('Preys: ' + str(len(simulation.preys)), WHITE, (2 * tile.get_width() + 50, 150), 30)
    text_draw('Predators: ' + str(len(simulation.predators)), WHITE, (2 * tile.get_width() + 50, 200), 30)

    # Clicked creature stats
    if simulation.clicked:
        text_draw('Generation: ' + str(simulation.clicked.generation), WHITE, (2 * tile.get_width() + 50, 300), 30)
        text_draw('Children: ' + str(simulation.clicked.children), WHITE, (2 * tile.get_width() + 50, 350), 30)
        if simulation.clicked.who_am_I == 'Predator':
            text_draw('Eaten: ' + str(simulation.clicked.eaten), WHITE, (2 * tile.get_width() + 50, 400), 30)
        text_draw('Energy', WHITE, (2 * tile.get_width() + 50, 450), 30)
        pygame.draw.rect(screen, WHITE, (2 * tile.get_width() + 50 + 150, 450, 102, 20), 1)
        pygame.draw.rect(screen, GREEN, (2 * tile.get_width() + 50 + 150 + 1, 450 + 1, simulation.clicked.energy
                                         / simulation.clicked.max_energy * 100, 18))
        text_draw('Split', WHITE, (2 * tile.get_width() + 50, 500), 30)
        pygame.draw.rect(screen, WHITE, (2 * tile.get_width() + 50 + 150, 500, 102, 20), 1)
        pygame.draw.rect(screen, BLUE, (2 * tile.get_width() + 50 + 150 + 1, 500 + 1, simulation.clicked.split
                                        / simulation.clicked.max_split * 100, 18))
        if simulation.clicked.who_am_I == 'Predator':
            text_draw('Digestion', WHITE, (2 * tile.get_width() + 50, 550), 30)
            pygame.draw.rect(screen, WHITE, (2 * tile.get_width() + 50 + 150, 550, 102, 20), 1)
            pygame.draw.rect(screen, ORANGE, (2 * tile.get_width() + 50 + 150 + 1, 550 + 1, simulation.clicked.digestion
                                              / simulation.clicked.max_digestion * 100, 18))

        if not simulation.clicked.controlled:
            pygame.draw.rect(screen, WHITE, take_control_but)
            text_draw('Take control', GRAY, (2 * tile.get_width() + 65, 610), 30)
            if take_control_but.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, BLUE, (2 * tile.get_width() + 50, 600, 150, 40), 5)

    # Preys and predators count plots
    text_draw('Preys', WHITE, (2 * tile.get_width() + 50, 725), 30)
    for index, item in enumerate(simulation.preys_history_count):
        end_position = (2 * tile.get_width() + 51 + index, 849 - item / simulation.max_prey_count * 98)
        pygame.draw.line(screen, GREEN, (2 * tile.get_width() + 51 + index, 849), end_position)
    pygame.draw.rect(screen, WHITE, (2 * tile.get_width() + 50, 750, 540, 100), 1)
    text_draw('Predators', WHITE, (2 * tile.get_width() + 50, 875), 30)
    for index, item in enumerate(simulation.predators_history_count):
        end_position = (2 * tile.get_width() + 51 + index, 999 - item / simulation.max_predator_count * 98)
        pygame.draw.line(screen, RED, (2 * tile.get_width() + 51 + index, 999), end_position)
    pygame.draw.rect(screen, WHITE, (2 * tile.get_width() + 50, 900, 540, 100), 1)


def draw_window(draw_options):
    screen.fill(background_colour)
    draw_tiles(tile, TILES_SIZE, screen)
    draw_options.transform = pymunk.Transform.scaling(SCALE)
    simulation.scaling(SCALE)
    space.debug_draw(draw_options)
    draw_dashboard()

    pygame.display.update()


def camera_movement():
    global tile_position, MOVE_SPEED
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_DOWN]:
        if tile_position[1] + (TILES_SIZE[1] - 1) * tile.get_height() >= 400:
            simulation.move(0, -MOVE_SPEED / SCALE)
            if not simulation.clicked or (simulation.clicked and not simulation.clicked.controlled):
                tile_position = (tile_position[0], tile_position[1] - MOVE_SPEED)
    if keys_pressed[pygame.K_UP]:
        if tile_position[1] < 0:
            simulation.move(0, MOVE_SPEED / SCALE)
            if not simulation.clicked or (simulation.clicked and not simulation.clicked.controlled):
                tile_position = (tile_position[0], tile_position[1] + MOVE_SPEED)
    if keys_pressed[pygame.K_RIGHT]:
        if tile_position[0] > -tile.get_width():
            simulation.move(-MOVE_SPEED / SCALE, 0)
            if not simulation.clicked or (simulation.clicked and not simulation.clicked.controlled):
                tile_position = (tile_position[0] - MOVE_SPEED, tile_position[1])
    if keys_pressed[pygame.K_LEFT]:
        if tile_position[0] < 0:
            simulation.move(MOVE_SPEED / SCALE, 0)
            if not simulation.clicked or (simulation.clicked and not simulation.clicked.controlled):
                tile_position = (tile_position[0] + MOVE_SPEED, tile_position[1])


def main():
    global screen, WIDTH, HEIGHT, ticks, SCALE
    creature_hover = None
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    draw_options.flags = pymunk.pygame_util.DrawOptions.DRAW_SHAPES

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        ticks += 1

        camera_movement()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_scaled = (pygame.mouse.get_pos()[0] / SCALE, pygame.mouse.get_pos()[1] / SCALE)
                query_info = space.point_query_nearest(mouse_scaled, 0, pymunk.ShapeFilter())
                if take_control_but.collidepoint(event.pos):
                    simulation.clicked.controlled = True
                elif query_info and isinstance(query_info.shape, pymunk.Circle):
                    simulation.click_creature(query_info.shape.creature)
                else:
                    simulation.click_creature(None)
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and SCALE < 2:
                    SCALE += 0.1
                elif event.y < 0 and SCALE > 0.4:
                    SCALE -= 0.1

            mouse_scaled = (pygame.mouse.get_pos()[0] / SCALE, pygame.mouse.get_pos()[1] / SCALE)
            query_info_hover = space.point_query_nearest(mouse_scaled, 0, pymunk.ShapeFilter())
            if creature_hover:
                creature_hover.color = creature_hover.creature.color
            if query_info_hover:
                query_info_hover.shape.color = (100, 20, 100, 0)
                creature_hover = query_info_hover.shape

        draw_window(draw_options)
        space.step(dt)
        timer_update()
        simulation.update()

    pygame.quit()


if __name__ == "__main__":
    main()
