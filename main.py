import pygame, sys
import math
import sys
import json
import time
import pygame
from button import Button
from utils import blit_rotate_center, blit_text_center, scale_image

pygame.init()


TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BGMM = scale_image(pygame.image.load("assets/Background-MM.png"), 1.2)
BGO = scale_image(pygame.image.load("assets/Background-O.JPG"), 1.2)
BGP = scale_image(pygame.image.load("assets/Background-P.JPG"), 1.2)
BGS = scale_image(pygame.image.load("assets/Background-S.JPG"), 0.9)
BGC = scale_image(pygame.image.load("imgs/mechanics.JPG"), 2.5)
BGcontrols = scale_image(pygame.image.load("imgs/arcade.JPG"), 1)
MAIN_FONT = pygame.font.SysFont("comicsans", 44)


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play(background, car_colour):
  pygame.font.init()
  BACKGROUND = background

  TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

  TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
  TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

  FINISH = pygame.image.load("imgs/finish.png")
  FINISH_MASK = pygame.mask.from_surface(FINISH)
  FINISH_POSITION = (130, 250)

  
  CAR_COLOUR = car_colour
  GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

  WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
  WIN = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Speed Demon")

  MAIN_FONT = pygame.font.SysFont("comicsans", 44)

  FPS = 60
  PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713), (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]


  class GameInfo:
      LEVELS = 10
      
      def __init__(self, level=1):
          self.level = level
          self.score = 0
          self.started = False
          self.level_start_time = 0
          self.level_pause_time = 0

          

         

      def game_paused(self):
          self.level_pause_time = time.time()
          #not working :(
          
      def next_level(self):
          self.level += 1
          self.score += 10
          self.started = False

      def reset(self):
          self.level = 1
          self.score = 0
          self.started = False
          self.level_start_time = 0
          

      def game_finished(self):
          return self.level > self.LEVELS
          

      def start_level(self):
          self.started = True
          self.level_start_time = time.time()
          
          

      def get_level_time(self):
          if not self.started:
              return 0
          A =  time.time() - self.level_start_time
          return round(A)
        


  class AbstractCar:
      def __init__(self, max_vel, rotation_vel):
          self.img = self.IMG
          self.max_vel = max_vel
          self.vel = 0
          self.rotation_vel = rotation_vel
          self.angle = 0
          self.x, self.y = self.START_POS
          self.acceleration = 0.1

      def rotate(self, left=False, right=False):
          if left:
              self.angle += self.rotation_vel
          elif right:
              self.angle -= self.rotation_vel

      def draw(self, win):
          blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

      def move_forward(self):
          self.vel = min(self.vel + self.acceleration, self.max_vel)
          self.move()

      def move_backward(self):
          self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
          self.move()

      def move(self):
          radians = math.radians(self.angle)
          vertical = math.cos(radians) * self.vel
          horizontal = math.sin(radians) * self.vel

          self.y -= vertical
          self.x -= horizontal

      def collide(self, mask, x=0, y=0):
          car_mask = pygame.mask.from_surface(self.img)
          offset = (int(self.x - x), int(self.y - y))
          poi = mask.overlap(car_mask, offset)
          return poi

      def reset(self):
          self.x, self.y = self.START_POS
          self.angle = 0
          self.vel = 0


  class PlayerCar(AbstractCar):
      IMG = CAR_COLOUR
      START_POS = (180, 200)

      def reduce_speed(self):
          self.vel = max(self.vel - self.acceleration / 2, 0)
          self.move()

      def bounce(self):
          self.vel = -self.vel
          self.move()


  class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0


  def draw(win, images, player_car, computer_car, game_info):
      for img, pos in images:
          win.blit(img, pos)

      level_text = MAIN_FONT.render(f"Level {game_info.level}", 1, (255, 255, 255))
      win.blit(level_text, (10, HEIGHT - level_text.get_height() - 100))
                     
      time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
      win.blit(time_text, (10, HEIGHT - time_text.get_height() - 70))

      vel_text = MAIN_FONT.render(f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
      win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 40))
   
      score_text = MAIN_FONT.render(f"Score {game_info.score}", 1, (255, 255, 255))
      win.blit(score_text, (10, HEIGHT - score_text.get_height() - 10))

      player_car.draw(win)
      computer_car.draw(win)
      pygame.display.update()


  def move_player(player_car):
      keys = pygame.key.get_pressed()
      moved = False

      if keys[pygame.K_a]:
          player_car.rotate(left=True)
      if keys[pygame.K_d]:
          player_car.rotate(right=True)
      if keys[pygame.K_w]:
          moved = True
          player_car.move_forward()
      if keys[pygame.K_s]:
          moved = True
          player_car.move_backward()

      if not moved:
          player_car.reduce_speed()


  def handle_collision(player_car, computer_car, game_info):
      if player_car.collide(TRACK_BORDER_MASK) != None:
          player_car.bounce()

      computer_finish_poi_collide = computer_car.collide(
          FINISH_MASK, *FINISH_POSITION)
      if computer_finish_poi_collide != None:
          blit_text_center(WIN, MAIN_FONT, f"You lost. Score: {game_info.score}")
          pygame.display.update()
          pygame.time.wait(5000)
          game_info.reset()
          player_car.reset()
          computer_car.reset()

      player_finish_poi_collide = player_car.collide(
          FINISH_MASK, *FINISH_POSITION)
      if player_finish_poi_collide != None:
          if player_finish_poi_collide[1] == 0:
              player_car.bounce()
          else:
              game_info.next_level()
              player_car.reset()
              computer_car.next_level(game_info.level)




  run = True
  clock = pygame.time.Clock()
  images = [(BACKGROUND, (0, 0)), (TRACK, (0, 0)),
            (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
  player_car = PlayerCar(4, 4)
  computer_car = ComputerCar(2, 4, PATH)
  game_info = GameInfo()

  while run:
      clock.tick(FPS)

      draw(WIN, images, player_car, computer_car, game_info)

      while not game_info.started:
          blit_text_center(
              WIN, MAIN_FONT, f"Press any key to start level {game_info.level}")
          pygame.display.update()
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  break

              if event.type == pygame.KEYDOWN:
                  game_info.start_level()

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              run = False
              break

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          game_info.game_paused()
          paused = True
          while paused: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                    if event.key == pygame.K_m:
                        main_menu()
            blit_text_center(WIN, MAIN_FONT, "Paused")
            pygame.display.update()                       
                


        
      move_player(player_car)
      computer_car.move()

      handle_collision(player_car, computer_car, game_info)

      if game_info.game_finished():
          blit_text_center(WIN, MAIN_FONT, f"You Won. Score: {game_info.score}")
          pygame.time.wait(5000)
          game_info.reset()
          player_car.reset()
          computer_car.reset()


  pygame.quit()

def customize():

    while True:
        SCREEN.blit(BGC, (-500, -50))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("CUSTOMIZE", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        RED_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 250), 
                            text_input="RED CAR", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        PURPLE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 350), 
                            text_input="PURPLE CAR", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        GREY_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 450), 
                            text_input="GREY CAR", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        WHITE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 550), 
                            text_input="WHITE CAR", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 650), 
                            text_input="BACK", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [RED_BUTTON, PURPLE_BUTTON, GREY_BUTTON, WHITE_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RED_BUTTON.checkForInput(MENU_MOUSE_POS):
                   car_colour = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
                   circuit_menu(car_colour)
                    
                if PURPLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    car_colour = scale_image(pygame.image.load("imgs/purple-car.png"), 0.55)
                    circuit_menu(car_colour)
                    
                if GREY_BUTTON.checkForInput(MENU_MOUSE_POS):
                   car_colour = scale_image(pygame.image.load("imgs/grey-car.png"), 0.55)
                   circuit_menu(car_colour)
                if WHITE_BUTTON.checkForInput(MENU_MOUSE_POS):
                   car_colour = scale_image(pygame.image.load("imgs/white-car.png"), 0.55)
                   circuit_menu(car_colour)
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                    

        pygame.display.update()


def scoreboard():
    while True:
        SCREEN.blit(BGS, (-700, -50))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("SCOREBOARD", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
  
        BACK_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 650), 
                            text_input="BACK", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:          
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BGMM, (-500, -50))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        SCOREBOARD_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400), 
                            text_input="SCOREBOARD", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 550), 
                            text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, SCOREBOARD_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    customize()
                if SCOREBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    scoreboard()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def ingame_menu(background, car_colour):

    while True:
        SCREEN.blit(BGP, (-500, -50))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Pause Menu", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        RESUME_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 250), 
                            text_input="Resume", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        CONTROLS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400), 
                            text_input="Controls", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 550), 
                            text_input="Main Menu", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [RESUME_BUTTON, CONTROLS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(background, car_colour)

                if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    controls(background, car_colour)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def circuit_menu(car_colour):
    while True:
        SCREEN.blit(BGO, (-500, -50))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("CHOOSE CIRCUIT", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        SANDY_SEASHORE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 250), 
                            text_input="SANDY SEASHORE", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        FREAKY_FOREST_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 350), 
                            text_input="FREAKY FOREST", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        WINTER_WONDERLAND_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 450), 
                            text_input="WINTER WONDERLAND", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        MOUNTAIN_MANIA_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 550), 
                            text_input=" MOUNTAIN MANIA", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 650), 
                            text_input="BACK", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [SANDY_SEASHORE_BUTTON, FREAKY_FOREST_BUTTON, WINTER_WONDERLAND_BUTTON, MOUNTAIN_MANIA_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SANDY_SEASHORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    background = scale_image(pygame.image.load("imgs/sand.jpg"), 2.5)
                    play(background, car_colour)
                    
                if FREAKY_FOREST_BUTTON.checkForInput(MENU_MOUSE_POS):
                    background = scale_image(pygame.image.load("imgs/forest.jpg"), 2.5)
                    play(background, car_colour)
                    
                if WINTER_WONDERLAND_BUTTON.checkForInput(MENU_MOUSE_POS):
                    background = scale_image(pygame.image.load("imgs/winter.jpg"), 2.5)
                    play(background, car_colour)
                    
                if MOUNTAIN_MANIA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    background = scale_image(pygame.image.load("imgs/mountain.jpg"), 2.5)
                    play(background, car_colour)
                    
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def controls(background, car_colour):
    while True:
        SCREEN.blit(BGcontrols, (-700,-50))
        CONTROLS_MOUSE_POS = pygame.mouse.get_pos()

        
        CONTROLS_TEXT = get_font(50).render("CONTROLS", True, "#000000")
        CONTROLS_RECT = CONTROLS_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(CONTROLS_TEXT, CONTROLS_RECT)



        CONTROLS_BACK = Button(image=None, pos=(400, 650), 
                            text_input="BACK", font=get_font(40), base_color="Black", hovering_color="Green")

        CONTROLS_BACK.changeColor(CONTROLS_MOUSE_POS)
        CONTROLS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTROLS_BACK.checkForInput(CONTROLS_MOUSE_POS):
                    ingame_menu(background, car_colour)

        pygame.display.update()

def pause():

    paused = True

    while paused:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


        blit_text_center(WIN, MAIN_FONT, "Paused")
        pygame.display.update()
        
def get_player_name():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([800,800])
    base_font = pygame.font.Font(None,32)
    player_text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                   player_text = player_text[:-1]
                else:
                   player_text += event.unicode
    
        screen.fill((0,0,0))
        text_surface = base_font.render(player_text,True,(255,255,255))
        screen.blit(text_surface,(0,0))

        pygame.display.flip()
        clock.tick(60)








main_menu()