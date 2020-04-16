import pygame

class Option:
    hovered = False
    def __init__(self, text, pos,screen):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw(screen)

    def draw(self,screen):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        menu_font = pygame.font.Font("C:\Windows\Fonts\Ebrima.ttf", 30)
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 0, 0)
        else:
            return (0, 0, 0)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


class Title:
    hovered = False
    def __init__(self, text, pos,screen):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw(screen)

    def draw(self,screen):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        title_font = pygame.font.Font(None, 120)
        self.rend = title_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 0, 0)
        else:
            return (0, 0, 0)
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

class TitlePage:
    ### Title part ###
    def __init__(self,title1):
        self.title = title1

    def ModeSelect(self,screen,clock):
        black, white = (0, 0, 0), (255, 255, 255)
        box_length = 240
        box_height = 35
        box1_x = 50
        box1_y = 415
        box2_x = 50
        box2_y = 465
        box3_x = 320
        box3_y = 415
        box4_x = 320
        box4_y = 465
        box5_x = 180
        box5_y = 515
        # background initial
        img = pygame.image.load("./art/background.png")
        img = pygame.transform.scale(img, (600, 600))
        screen.blit(img, (0, 0))
        Title(self.title, (140, 50),screen)

        # selection box
        # pygame.draw.rect(screen, black, [125, 35, 145, 210])
        pygame.draw.rect(screen, black, [box1_x, box1_y, box_length, box_height])
        pygame.draw.rect(screen, white, [box1_x + 1, box1_y + 1, box_length - 2, box_height - 2])

        pygame.draw.rect(screen, black, [box2_x, box2_y, box_length, box_height])
        pygame.draw.rect(screen, white, [box2_x + 1, box2_y + 1, box_length - 2, box_height - 2])

        pygame.draw.rect(screen, black, [box3_x, box3_y, box_length, box_height])
        pygame.draw.rect(screen, white, [box3_x + 1, box3_y + 1, box_length - 2, box_height - 2])

        pygame.draw.rect(screen, black, [box4_x, box4_y, box_length, box_height])
        pygame.draw.rect(screen, white, [box4_x + 1, box4_y + 1, box_length - 2, box_height - 2])

        pygame.draw.rect(screen, black, [box5_x, box5_y, box_length, box_height])
        pygame.draw.rect(screen, white, [box5_x + 1, box5_y + 1, box_length - 2, box_height - 2])

        gameTypes = [Option("Vs. P2 (Flip)", (box1_x + 40, box1_y - 5),screen),
                     Option("Vs. P2 (No Flip)", (box2_x + 20, box2_y - 5),screen),
                     Option("Vs. DumbBot", (box3_x + 30, box3_y - 5),screen),
                     Option(" Vs. ComplexBot", (box4_x + 10, box4_y - 5),screen),
                     Option("Exit", (box5_x + 95, box5_y - 5),screen)]
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # get UI coordinate
                    cols, rows = pygame.mouse.get_pos()
                    # print(cols, rows)
                    if box1_x < cols < box1_x + 240 and box1_y < rows < box1_y + 30:
                        return "P2F"
                    if box2_x < cols < box2_x + 240 and box2_y < rows < box2_y + 30:
                        return "P2"
                    if box3_x < cols < box3_x + 240 and box3_y < rows < box3_y + 30:
                        return "DB"
                    if box4_x < cols < box4_x + 240 and box4_y < rows < box4_y + 30:
                        return "CB"
                    if box5_x < cols < box5_x + 240 and box5_y < rows < box5_y + 30:
                        return "Quit"

            # gameDisplay.fill(white)
            for gameType in gameTypes:
                if gameType.rect.collidepoint(pygame.mouse.get_pos()):
                    gameType.hovered = True
                else:
                    gameType.hovered = False
                gameType.draw(screen)
                pygame.display.update()
            # pygame.display.update()
            clock.tick(15)
    ### End Title part ###