import pygame
import sys
import json
from math import sin, cos, radians, pi, tau


def is_number(x):
    if type(x) == bool:
        return False
    try:
        float(x)
        return True
    except ValueError:
        return False
        

def end():
    pygame.quit()
    sys.exit()

class Circle(pygame.Rect):
    def __init__(self, left: float, top: float, width: float, height: float, xratio, yratio) -> None:
        super().__init__(left, top, width, height)
        self.time    = -pi/2
        self.yoffset = self.y + width /2
        self.xoffset = self.x + height/2
        self.x_ratio = xratio
        self.y_ratio = yratio


def main():
    pygame.init()
    screen_info = pygame.display.Info()
    
    SETTINGS = json.load(open("settings.json"))
    
    TARGET_FPS = SETTINGS["fps"]
    if not is_number(TARGET_FPS):
        raise ValueError(f"\"fps\" must be a number not \"{TARGET_FPS}\" of type {type(TARGET_FPS)}")
    else:
        TARGET_FPS = float(TARGET_FPS)
    
    c_radius = SETTINGS["circle-radius"]

    WIDTH = SETTINGS["width"]
    if type(WIDTH) == str:
        if WIDTH.lower() == "height":
            HEIGHT = SETTINGS["height"]
            if type(HEIGHT) == str:
                if HEIGHT.lower() == "fill":
                    HEIGHT = screen_info.current_h
                elif HEIGHT.lower() == "width":
                    raise BaseException("No, you can't do that")
            elif is_number(HEIGHT):
                HEIGHT = float(HEIGHT)
            WIDTH = HEIGHT
        
        elif WIDTH.lower() == "fill":
            WIDTH = screen_info.current_w
    
    elif is_number(WIDTH):
        WIDTH = float(WIDTH)
    
    HEIGHT = SETTINGS["height"]
    if type(HEIGHT) == str:
        if HEIGHT.lower() == "fill":
            HEIGHT = screen_info.current_h
        elif HEIGHT.lower() == "width":
            HEIGHT = WIDTH
    
    elif is_number(HEIGHT):
        HEIGHT = float(HEIGHT)
    

    HW, HH = WIDTH//2, HEIGHT//2
    
    speed = SETTINGS["speed"]
    
    bg_color = SETTINGS["bg-color"]
    circle_color = SETTINGS["circle-color"]

    big_circle_width = SETTINGS["big-circle-width"]
    fmove_radius = SETTINGS["big-circle-radius"]
    if fmove_radius == "fit":
        fmove_radius = min(WIDTH, HEIGHT)
    elif fmove_radius == "fill":
        fmove_radius = max(WIDTH, HEIGHT)
    
    move_radius = fmove_radius - big_circle_width*2
    
    c_diameter = 2 * c_radius
    moving = move_radius/2 - c_radius
    center = (HW-c_radius, HH-c_radius)

    n_circles = SETTINGS["number-of-circles"]
    if not n_circles:
        raise BaseException("serieously, what's the point of not having any circles?")
    
    circles: list[Circle] = []
    angle_between_circles = SETTINGS["angle-between-circles"]
    if angle_between_circles == "default":
        angle_between_circles = pi/n_circles
    elif not is_number(angle_between_circles):
        raise ValueError(f"\"angle-between-circles\" must be set to \"default\" or a number not \"{angle_between_circles}\" of type {type(angle_between_circles)}")
    else:
        angle_between_circles = radians(float(angle_between_circles))
    
    
    for i in range(n_circles):
        angle = i*angle_between_circles
        xratio = sin(angle) * moving
        yratio = cos(angle) * moving
        circle = Circle(*center, c_diameter, c_diameter, xratio, yratio)
        circle.time -= angle
        circles.append(circle)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_icon(pygame.image.load("icon.jpg").convert())
    
    hfmr = fmove_radius/2
    hmr = move_radius/2
    big_c_pos = (HW - hmr, HH - hmr)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        dt = clock.get_time() / 1000
        
        screen.fill(bg_color)
        pygame.display.set_caption(f"fps: {clock.get_fps():.2f}")
        
        pygame.draw.ellipse(screen, (90, 24, 10), (*big_c_pos, move_radius, move_radius))
        if big_circle_width:
            pygame.draw.circle(screen, "#0b0d09", (HW, HH), hfmr, big_circle_width)
        
        time = dt * speed
        
        for circle in circles:
            pygame.draw.ellipse(screen, circle_color, circle)
            sin_time = sin(circle.time)
            circle.centerx = sin_time * circle.x_ratio + circle.xoffset
            circle.centery = sin_time * circle.y_ratio + circle.yoffset
            circle.time += time
            if circle.time >= tau:
                circle.time = circle.time % tau
        
        pygame.display.flip()
        clock.tick(TARGET_FPS)
        


if __name__ == "__main__":
    main()
    end()