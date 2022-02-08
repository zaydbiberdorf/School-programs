# Pre-Poke Framework
# Implements a general game template for games with animation
# You must use this template for all your graphical lab assignments
# and you are only allowed to inlclude additional modules that are part of
# the Python Standard Library; no other modules are allowed

import pygame
import math
import random
import time

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((550, 450))
   # set the title of the display window
   pygame.display.set_caption('A template for graphical games with two moving dots')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # implement score 
   
   
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.count = 0
      self.tiles = []
      self.compare_images = False
      self.game_score = 0
      self.update_time = 1000
      pygame.time.set_timer(pygame.USEREVENT, self.update_time)
      index = 0
      # making the grid of images 
      for i in range(1, 9):
         for m in range(2):
            index += 1
            img_tag = "image" + str(i) + ".bmp"
            self.tiles.append(Tile(img_tag, index))
      # randomizing the tieles
      self.randomize_tiles()
      

      


   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()  
         if self.continue_game:
            self.update()
            self.decide_continue()
         else:
            self.update_time = 0
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down_handler(event)
         if self.continue_game:
            if event.type == pygame.USEREVENT:
               self.game_score += 1
            


   def mouse_down_handler(self, event):
      # main objectives is to determine where the user is pressig the mouse and flip the card 
      if event.button == 1:
         pos = [-100, -100]
         self.index= -1
         for i in range(4):
            pos[1] += 110
            pos[0] = -100
            for m in range(4):
               pos[0] += 110
               self.index+= 1
               if self.check((pos[0], pos[0] + 110), (pos[1], pos[1] + 110)):
                  self.tiles[self.index].revealed = True
                  self.update()
                  self.count += 1
                  if self.count == 1:
                     self.first_tile_index = self.index
                  elif self.count == 2:
                     self.second_tile_index = self.index
                     self.count = 0
                     self.compare_images = True
                     
               
                  
                  
            
      



   # this funciton cecks the mouses position vs the cards position to determine which card is being pressed 
   def check(self, x_params, y_params):
        self.mouse_pos = pygame.mouse.get_pos()
        in_square = (self.mouse_pos[0] >= x_params[0] and self.mouse_pos[0] < x_params[1]) and (self.mouse_pos[1] >= y_params[0] and self.mouse_pos[1] < y_params[1])
        return in_square

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      
      #display score
      font = pygame.font.Font('freesansbold.ttf' , 50)
      text = font.render(str(self.game_score), True, pygame.Color('white'))
      text_rect = text.get_rect()
      text_rect.center = (490, 50)
      self.surface.blit(text, text_rect)

      count = 0
      pos = [-100, -100]
      for i in range(4):
         pos[1] += 110
         pos[0] = -100
         for m in range(4):
            pos[0] += 110
            self.surface.blit(self.tiles[count].tile_img, (pos[0], pos[1]))
            count += 1

   
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      # update 
     
      for i in range(len(self.tiles)):
         self.tiles[i].update_img()

      if self.compare_images:
         time.sleep(0.5)
         self.compare_images = False
         if self.tiles[self.first_tile_index].paired == True:
            self.tiles[self.second_tile_index].revealed = False
         elif self.tiles[self.second_tile_index].paired == True:
            self.tiles[self.first_tile_index].revealed = False
         elif self.tiles[self.first_tile_index].compare_img(self.tiles[self.second_tile_index]) == False: 
            
            self.tiles[self.first_tile_index].revealed = False
            self.tiles[self.second_tile_index].revealed = False
         else:
            self.tiles[self.first_tile_index].revealed = True
            self.tiles[self.second_tile_index].revealed = True
            self.tiles[self.first_tile_index].paired = True
            self.tiles[self.second_tile_index].paired = True
            


   def randomize_tiles(self):
      # randomizing the poition of the tiles 
      self.tile_index = len(self.tiles) - 1
      for rand_num in range(0, random.randint(500, 1000)):
         # chose two random cards from the deck and swap them
         self.tile_one_index = random.randrange(0, self.tile_index)
         self.tile_two_index = random.randrange(0, self.tile_index)
         self.tiles[self.tile_one_index], self.tiles[self.tile_two_index] = self.tiles[self.tile_two_index], self.tiles[self.tile_one_index]
      

        


      
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      for i in range(len(self.tiles)):
         if self.tiles[i].revealed == False:
            self.continue_game = True
            break
         else:
            self.continue_game = False

  
     


class Tile:
    def __init__(self, img, tile_id):
        self.img = img
        self.revealed = False
        self.tile_img = pygame.image.load('image0.bmp')
        self.tile_id = tile_id
        self.paired = False
        

    def update_img(self):
        if self.revealed == False:
            self.tile_img = pygame.image.load('image0.bmp')
        elif self.revealed == True:
            self.tile_img = pygame.image.load(self.img)

    def compare_img(self, other_img):
       if self.paired == False and other_img.paired == False:
            if self.tile_id == other_img.tile_id:
               return False
            elif self.img != other_img.img:
               
               return False
       
          


          
main()

