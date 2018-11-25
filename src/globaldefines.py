import pygame

#defines
WIDTH = 600
HEIGHT = 800
FPS = 60

CENTERX = WIDTH*0.5
CENTERY = HEIGHT*0.5

NULLVEC = pygame.math.Vector2(0, 0)

#strange aliases
try:
    xrange
except NameError:
    xrange = range

font = pygame.font.Font("./res/Fonts/kenvector_future_thin.ttf", 30)
font_min = pygame.font.Font("./res/Fonts/kenvector_future_thin.ttf", 14)
font_med = pygame.font.Font("./res/Fonts/kenvector_future_thin.ttf", 24)

run_start = 0
segments = []
last_segment = 0

# methode securise pour lerp un point
def target_point(start, target, speed) :
    d = (target - start) * speed
    if d.length() < 2 :
        if dist_to_point(start, target) < 2 :
            return target
        else :
            d.scale_to_length(2)
    return start + d


def dist_to_point(start, target) :
    return (target-start).length()

def display_text(window, text, x, y, col) :
    img = font.render(text, True, col)
    drect = img.get_rect()
    drect.left = x
    drect.top = y
    if not window == None :
      window.blit(img, drect)
    return img

def display_text_med(window, text, x, y, col) :
    img = font_med.render(text, True, col)
    drect = img.get_rect()
    drect.left = x
    drect.top = y
    if not window == None :
      window.blit(img, drect)
    return img

def display_text_min(window, text, x, y, col) :
    img = font_min.render(text, True, col)
    drect = img.get_rect()
    drect.left = x
    drect.top = y
    if not window == None :
      window.blit(img, drect)
    return img


def start_timer() :
    global run_start
    run_start = pygame.time.get_ticks() * 0.001
    last_segment = run_start

def rc(val) :
  return round(val, 2)
def get_time() :
    return rc(pygame.time.get_ticks() * 0.001 - run_start)

def add_segment(name) :
    global last_segment
    time = rc(get_time())
    segments.insert(0, name + " : " + str(time))
    last_segment = time
    return time

def clear_segments() :
    global segments
    del segments[:]