import pygame
import sys
import json
from math import sin, cos, pi, radians


def end():
    pygame.quit()
    sys.exit()

class Circle(pygame.Rect):
    def __init__(self, left: float, top: float, width: float, height: float, xratio, yratio) -> None:
        super().__init__(left, top, width, height)
        self.speed   = -pi/2
        self.yoffset = self.y + width /2
        self.xoffset = self.x + height/2
        self.x_ratio = xratio
        self.y_ratio = yratio


def main():
    pygame.init()
    screen_info = pygame.display.Info()
    
    SETTINGS = json.load(open("settings.json"))
    c_radius = SETTINGS["circle-radius"]

    WIDTH = SETTINGS["width"]
    if WIDTH == "default":
        WIDTH = screen_info.current_w

    HEIGHT = SETTINGS["height"]
    if HEIGHT == "default":
        HEIGHT = screen_info.current_h

    HW, HH = WIDTH//2, HEIGHT//2
    
    speed = SETTINGS["speed"]

    move_radius = SETTINGS["big-circle-radius"]
    if move_radius == "fit":
        move_radius = min(WIDTH, HEIGHT)
    elif move_radius == "fill":
        move_radius = max(WIDTH, HEIGHT)
    
    c_diameter = 2 * c_radius
    moving = move_radius/2 - c_radius
    center = (HW-c_radius, HH-c_radius)

    n_circles = SETTINGS["number-of-circles"]
    circles: list[Circle] = []
    angle_between_circles = SETTINGS["angle-between-circles"]
    if angle_between_circles == "default":
        angle_between_circles = pi/n_circles
    elif type(angle_between_circles) == str or type(angle_between_circles) == bool:
        raise ValueError(f"\"angle-between-circles\" must be set to \"default\" or a number not \"{angle_between_circles}\" of type {type(angle_between_circles)}")
    else:
        angle_between_circles = radians(angle_between_circles)
    
    
    for i in range(n_circles):
        angle = i*angle_between_circles
        xratio = sin(angle) * moving
        yratio = cos(angle) * moving
        circle = Circle(*center, c_diameter, c_diameter, xratio, yratio)
        circle.speed -= angle
        circles.append(circle)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        dt = clock.get_time() / 1000
        
        screen.fill("#161716")
        pygame.display.set_caption(f"fps: {clock.get_fps():.2f}")
        
        s = dt * speed
        
        for circle in circles:
            pygame.draw.ellipse(screen, "#ffffff", circle)
            circle.centerx = sin(circle.speed) * circle.x_ratio + circle.xoffset
            circle.centery = sin(circle.speed) * circle.y_ratio + circle.yoffset
            circle.speed += s
        
        print(f"\r{circle.speed}", end="")
        
        pygame.display.flip()
        clock.tick(360)


if __name__ == "__main__":
    main()
    end()