import pygame,sys,random,os


background = pygame.image.load("images/carpet.png")
def funding():
    try:
        data=open('funds.txt','r')
        c=data.readline()
        funds=float(c)
        data.close()
    except:
        data=open('funds.txt','w')
        data.write('100')
        data.close()
        funds=100
    return funds

all_sprites_list = pygame.sprite.Group()

class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self,all_sprites_list)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class User(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(User, self).__init__(x, y, width, height)



class Table(Entity):
    """
    table class
    """

    def __init__(self, x, y, width, height,type):
        super(Table, self).__init__(x, y, width, height)

        self.image = pygame.Surface([self.width, self.height])
        if type=="BLACKJACK":
            blackjack_table = pygame.image.load('images/blackjack100x100.png')
            self.image.blit(blackjack_table, (0, 0))
        elif type=="CRAPS":
            craps_table=pygame.image.load('images/craps200x100.png')
            self.image.blit(craps_table, (0, 0))
        elif type=="ROULETTE":
            roulette_table=pygame.image.load('images/roulette100x131.png')
            self.image.blit(roulette_table, (0, 0))

class Player(Entity):
    """The player"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player should move on a given frame.
        self.y_change = 0
        self.x_change = 0
        # How many pixels the User should move each frame a key is pressed.
        self.y_dist = 10
        self.x_dist=10
        self.image = pygame.Surface([self.width, self.height])
        char = pygame.image.load('images/user80x112.png')
        self.image.set_colorkey((0,0,0))
        self.image.blit(char, (0, 0))

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_UP):
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist
        elif (key==pygame.K_LEFT):
            self.x_change+=-self.x_dist
        elif (key==pygame.K_RIGHT):
            self.x_change+=self.x_dist

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist
        elif (key==pygame.K_LEFT):
            self.x_change+=self.x_dist
        elif(key==pygame.K_RIGHT):
            self.x_change+=-self.x_dist


    def update(self):
        """
        Moves the User while ensuring it stays in bounds
        """
        # Moves it relative to its current location.
        self.rect.move_ip(self.x_change, self.y_change)
        # If the User moves off the screen, put it back on.
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height
        if self.rect.x<0: #Cannot do with an elif, otherwise it can go off screen for a sec
            self.rect.x=0
        elif self.rect.x>window_width-self.width:
            self.rect.x = window_width - self.width
def play_blackjack():
    os.system("blackjack.py")
def tablecheck():
    if player.rect.colliderect(table1.rect):
        player.rect.x = 21
        player.rect.y = 201
        play_blackjack()

    elif player.rect.colliderect(table2.rect):
        print('craps')
    elif player.rect.colliderect(table3.rect):
        print('roulette')
pygame.init()

window_width = 800
window_height = 800

screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("The Casino")

clock = pygame.time.Clock()

player = Player(20, window_height / 2, 80, 112)

table1=Table(20, 100, 100, 100,"BLACKJACK")
table2=Table(500,100,200,100,"CRAPS")
table3=Table(300,100,100,131,"ROULETTE")

#all_sprites_list.add(player)
#all_sprites_list.add(enemy) <--- this will be tables
cash=funding()
while True:
    cash = funding()
    screen.blit(background, (0, 0))
    tablecheck()
    # Event processing here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.MoveKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            player.MoveKeyUp(event.key)

    for ent in all_sprites_list:
        ent.update()

    all_sprites_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)
