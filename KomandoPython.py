import pygame
import random

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)

class Block(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])
        self.image.fill(color)

        self.rect = self.image.get_rect()

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(blue)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class BulletVertical(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = "vertical"
        self.direction = 0
        self.image = pygame.Surface([4, 10])
        self.image.fill(white)

        self.rect = self.image.get_rect()

class BulletHorizontal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = "horizontal"
        self.direction = 0
        self.image = pygame.Surface([10, 4])
        self.image.fill(white)

        self.rect = self.image.get_rect()



class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x=0
    change_y=0

    # This is a frame counter used to determing which image to draw
    frame = 0


    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
 
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

player = Player(20, 100)
movingsprites = pygame.sprite.RenderPlain()
movingsprites.add(player)

# Make the walls. (x_pos, y_pos, width, height)
all_sprites_list=pygame.sprite.RenderPlain()

# List of each block in the game
block_list = pygame.sprite.RenderPlain()

# List of each bullet
bullet_list = pygame.sprite.RenderPlain()

# Left Wall
wall=Wall(0,0,20,600)
all_sprites_list.add(wall)

# Right Wall
wall=Wall(780,20,20,580)
all_sprites_list.add(wall)

# Top Wall
wall=Wall(20,0,780,20)
all_sprites_list.add(wall)

# Bottom Wall
wall=Wall(20,580,780,20)
all_sprites_list.add(wall)

for i in range(10):
    block = Block(red)

    block.rect.x = 20 + random.randrange(38) * 20  
    block.rect.y = 20 + random.randrange(28) * 20

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
                    if direction == 6:
                        bullet = BulletHorizontal()
                        bullet.direction = 6
                    if direction == 4:
                        bullet = BulletHorizontal()
                        bullet.direction = 4
                    if direction == 2:
                        bullet = BulletVertical()
                        bullet.direction = 2

                    bullet.rect.x = player.rect.x
                    bullet.rect.y = player.rect.y
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
        print(bullet.name)            
        print(bullet.direction)

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
        if bullet.rect.y < -30 :
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    screen.fill(black)

    movingsprites.draw(screen)

    all_sprites_list.draw(screen)

    textScore=font.render("Score : "+str(score), True, blue)
    screen.blit(textScore, [20, 20])

    textAmmunition=font.render("Ammunition : "+str(ammunition), True, blue)
    screen.blit(textAmmunition, [20, 40])

    pygame.display.flip()

    clock.tick(40)

pygame.quit()
