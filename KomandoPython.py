import pygame
import random

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)

# This class represents the block
class Block(pygame.sprite.Sprite):
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])
        self.image.fill(color)

        self.rect = self.image.get_rect()



# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(blue)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


        
        
# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x=0
    change_y=0

    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Set height, width
        self.image = pygame.Surface([20, 20])
        self.image.fill(white)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    
    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
        
    # Find a new position for the player
    def update(self,walls):
        # Get the old position, in case we need to go back to it
        old_x=self.rect.x
        new_x=old_x+self.change_x
        self.rect.x = new_x
        
        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.x=old_x

        old_y=self.rect.y
        new_y=old_y+self.change_y
        self.rect.y = new_y
        
        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.y=old_y

score = 0
# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
# Set the height and width of the screen
screen_width=800
screen_height=600
screen=pygame.display.set_mode([screen_width,screen_height])


# Set the title of the window
pygame.display.set_caption('Komando Python')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)

# Create the player paddle object
player = Player( 20,20 )
movingsprites = pygame.sprite.RenderPlain()
movingsprites.add(player)

# Make the walls. (x_pos, y_pos, width, height)
wall_list=pygame.sprite.RenderPlain()

# List of each block in the game
block_list = pygame.sprite.RenderPlain()

# Left Wall
wall=Wall(0,0,20,600)
wall_list.add(wall)

# Right Wall
wall=Wall(780,20,20,580)
wall_list.add(wall)

# Top Wall
wall=Wall(20,0,780,20)
wall_list.add(wall)

# Bottom Wall
wall=Wall(20,580,780,20)
wall_list.add(wall)

for i in range(10):
    # This represents a block
    block = Block(red)

    # Set a random location for the block
    block.rect.x = 20 + random.randrange(38) * 20  
    block.rect.y = 20 + random.randrange(28) * 20

    # Add the block to the list of objects
    block_list.add(block)
    wall_list.add(block)


clock = pygame.time.Clock()

done = False

speed = 5

while done == False:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-speed,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(speed,0)
            if event.key == pygame.K_UP:
                player.changespeed(0,-speed)
            if event.key == pygame.K_DOWN:
                player.changespeed(0,speed)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(speed,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-speed,0)
            if event.key == pygame.K_UP:
                player.changespeed(0,speed)
            if event.key == pygame.K_DOWN:
                player.changespeed(0,-speed)
                
    player.update(wall_list)
    
    screen.fill(black)
    
    movingsprites.draw(screen)
    wall_list.draw(screen)
    block_list.draw(screen)
    pygame.display.flip()

    clock.tick(40)
            
pygame.quit()
