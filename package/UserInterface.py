import pygame

def write(msg="", fontcolor=(255,0,255), fontsize=42, font=None):
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext
  

def setCodename(screen, question):  
    pygame.font.init()  
    text = ""
    pygame.display.flip()
    line1 = write("Codename:")
    while True:
        screen.fill((0,0,0)) #paint background black
        line2 = write("> " + text)
        screen.blit(line1, (20, 20))
        screen.blit(line2, (200, 20))
        pygame.time.wait(50)
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                sys.exit()   
            elif event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_BACKSPACE:
                text = text[0:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                return text
            else:
                text += event.unicode.encode("ascii")         
        pygame.display.flip()
