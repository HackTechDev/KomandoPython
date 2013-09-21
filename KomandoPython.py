import pygame
import random

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)

class GraphicSprite(pygame.sprite.Sprite):

    def setGraphic(self,tilex,tiley,tilewidth,tileheight,x,y,width,height):
        myimage = pygame.image.load("sprites/wall/int_wall_bricks.png").convert()

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])

        for row in range(height//tileheight+1):
            for column in range(width//tilewidth+1):
                self.image.blit(myimage,(column*tilewidth,row*tileheight),(tilex,tiley,tilewidth,tileheight))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.image.set_colorkey(black)

    def setGraphic2(self,image, tilex,tiley,x,y,width,height):
        myimage = pygame.image.load(image).convert()

        self.image = pygame.Surface([width, height])

        self.image.blit(myimage,(0,0),(tilex,tiley,32,32))
        for column in range(width//32-2):
            self.image.blit(myimage,((column+1)*32,0),(tilex+32,tiley,32,32))
        self.image.blit(myimage,( (width//32-1)*32,0),(tilex+64,tiley,32,32))

        for row in range(height//32+1):
            self.image.blit(myimage,(0,(row+1)*32),(tilex,tiley+32,32,32))
            for column in range(width//32+1):
                self.image.blit(myimage,((column+1)*32,(row+1)*32),(tilex+32,tiley+32,32,32))
            self.image.blit(myimage,((width//32-1)*32,(row+1)*32),(tilex+64,tiley+32,32,32))

        self.image.blit(myimage,(0,(height//32-1)*32),(tilex,tiley+64,32,32))
        for column in range(width//32-2):
            self.image.blit(myimage,((column+1)*32,(height//32-1)*32),(tilex+32,tiley+64,32,32))
        self.image.blit(myimage,( (width//32-1)*32,(height//32-1)*32),(tilex+64,tiley+64,32,32))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.image.set_colorkey(black)

class Block(GraphicSprite):
    def __init__(self, x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        image = "sprites/item/toys.png"
        tilex=32*0
        tiley=32*0
        x = x*32
        y = y*32
        self.setGraphic2(image, tilex,tiley,x,y,width,height)



class Wall(GraphicSprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        image = "sprites/wall/int_wall_bricks.png"
        tilex=32*1
        tiley=32*1
        x = x*32
        y = y*32
        self.setGraphic2(image, tilex,tiley,x,y,width,height)

class Ground(GraphicSprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        image = "sprites/ground/brown_paving.png"
        tilex=32*0
        tiley=32*0
        x = x*32
        y = y*32
        self.setGraphic2(image, tilex,tiley,x,y,width,height)

class BulletVertical(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = "vertical"
        self.direction = 0
        self.image = pygame.Surface([4, 10])
        self.image.fill(red)

        self.rect = self.image.get_rect()

class BulletHorizontal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = "horizontal"
        self.direction = 0
        self.image = pygame.Surface([10, 4])
        self.image.fill(red)

        self.rect = self.image.get_rect()

# Sprite size: width = 48 / height = 64

class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x=0
    change_y=0

    # This is a frame counter used to determing which image to draw
    frame = 0

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]

        # Number of sprite + 1 = 13
        for i in range(1,13):
            img = pygame.image.load("sprites/player/player"+str(i)+".png").convert_alpha()
            img.set_colorkey(white)
            self.images.append(img)

        # By default, use image 0
        self.image = self.images[0]

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

        # Moving right to left
        if self.change_y < 0:
            self.frame += 1

            # We go from 0...3. If we are above image 3, reset to 0
            # Multiply by 4 because we flip the image every 4 frames
            if self.frame > 2*3:
                self.frame = 0

            # Grab the image, do floor division by 4 because we flip
            # every 4 frames.
            # Frames 0...3 -> image[0]
            # Frames 4...7 -> image[1]
            # etc.
            self.image = self.images[self.frame//3]

        # Move left to right. About the same as before, but use
        # images 4...7 instead of 0...3. Note that we add 4 in the last
        # line to do this.
        if self.change_x > 0:
            self.frame += 1
            if self.frame > 2*3:
                self.frame = 0
            self.image = self.images[self.frame//3+3]

        # Move bottom to top
        if self.change_y > 0:
            self.frame += 1
            if self.frame > 2*3:
                self.frame = 0
            self.image = self.images[self.frame//3+3+3]

        if self.change_x < 0:
            self.frame += 1
            if self.frame > 2*3:
                self.frame = 0
            self.image = self.images[self.frame//3+3+3+3]

class Level():
    # Constructor function
    def __init__(self, filename):
        file = open("map01.txt", "r")
        line_list = file.readlines()
        file.close()

        for line in line_list:
            line = line[:-1]
            print(line)
            

# Call this function so the Pygame library can initialize itself
pygame.init()

# 48*25
screen_width=1200
# 64*12
screen_height=640
screen=pygame.display.set_mode([screen_width,screen_height])

pygame.display.set_caption('Komando Python')

background = pygame.Surface(screen.get_size())

background = background.convert()

background.fill(black)

player = Player(32, 64)
movingsprites = pygame.sprite.RenderPlain()
movingsprites.add(player)

# Load level
map1 = Level("map01.txt")

# Make the walls. (x_pos, y_pos, width, height)
all_sprites_list=pygame.sprite.RenderPlain()

# List of each block in the game
block_list = pygame.sprite.RenderPlain()

# List of each bullet
bullet_list = pygame.sprite.RenderPlain()

ground_list = pygame.sprite.RenderPlain()


for x in range(1, 30):
    for y in range(1, 15):
        ground = Ground(x, y, 32, 32)
        ground_list.add(ground)


# Top Wall
posx = 0
posy = 0
lengthx = 30
for x in range(lengthx):
    wall=Wall(posx+x,posy,32,32)
    all_sprites_list.add(wall)

# Left Wall
posx = 0
posy = 1
lengthx = 14
for x in range(lengthx):
    wall=Wall(posx,posy+x,32,32)
    all_sprites_list.add(wall)

# Bottom Wall
posx = 0
posy = 15
lengthx = 30
for x in range(lengthx):
    wall=Wall(posx+x,posy,32,32)
    all_sprites_list.add(wall)

# Left Wall
posx = 29
posy = 1
lengthx = 14
for x in range(lengthx):
    wall=Wall(posx,posy+x,32,32)
    all_sprites_list.add(wall)

for i in range(10):
    block = Block(1+random.randrange(28), 1+random.randrange(14), 32, 32)

    block_list.add(block)
    all_sprites_list.add(block)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

done = False

speed = 5

score = 0

ammunition = 20

direction = 8

while done == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-speed,0)
                direction = 4
            if event.key == pygame.K_RIGHT:
                player.changespeed(speed,0)
                direction = 6
            if event.key == pygame.K_UP:
                player.changespeed(0,-speed)
                direction = 8
            if event.key == pygame.K_DOWN:
                player.changespeed(0,speed)
                direction = 2
            if event.key == pygame.K_SPACE :
                if ammunition > 0:
                    if direction == 8:
                        bullet = BulletVertical()
                        bullet.direction = 8
                        bullet.rect.x = player.rect.x + 24
                        bullet.rect.y = player.rect.y
                    if direction == 6:
                        bullet = BulletHorizontal()
                        bullet.direction = 6
                        bullet.rect.x = player.rect.x + 48
                        bullet.rect.y = player.rect.y + 32
                    if direction == 4:
                        bullet = BulletHorizontal()
                        bullet.direction = 4
                        bullet.rect.x = player.rect.x 
                        bullet.rect.y = player.rect.y + 32
                    if direction == 2:
                        bullet = BulletVertical()
                        bullet.direction = 2
                        bullet.rect.x = player.rect.x + 24
                        bullet.rect.y = player.rect.y + 64

                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)
                    ammunition -=1



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(speed,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-speed,0)
            if event.key == pygame.K_UP:
                player.changespeed(0,speed)
            if event.key == pygame.K_DOWN:
                player.changespeed(0,-speed)

    player.update(all_sprites_list)

    # Calculate mechanics for each bullet
    for bullet in bullet_list:
        if bullet.name == "vertical" :
            if bullet.direction == 8:
                bullet.rect.y -= 5
            if bullet.direction == 2:
                bullet.rect.y += 5
        if bullet.name == "horizontal" :
            if bullet.direction == 6:
                bullet.rect.x += 5
            if bullet.direction == 4:
                bullet.rect.x -= 5

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bollet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1

        # Remove the bullet if it flies up off the screen
        if bullet.rect.x > (29*32) or bullet.rect.x < (1*32) or bullet.rect.y > (15*32) or bullet.rect.y < (1*32):
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    screen.fill(black)

    ground_list.draw(screen)

    movingsprites.draw(screen)

    all_sprites_list.draw(screen)

    textScore=font.render("Score : "+str(score), True, blue)
    screen.blit(textScore, [0, 32*16])

    textAmmunition=font.render("Ammunition : "+str(ammunition), True, blue)
    screen.blit(textAmmunition, [0, 32*17])

    pygame.display.flip()

    clock.tick(40)

pygame.quit()
