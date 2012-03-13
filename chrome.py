import pygame

#import pygame.font
#import sys

class Chrome(pygame.sprite.Group):
    # this group will hold the various ui elements
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.font = pygame.font.Font(None, 20)
        
        self.add(Sidebar())
        
    def draw(self, surface, player):
        for c in self:
            c.draw(surface, self.font, player)


class Sidebar(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        
        self.add(unitText())
    
    def update(self):
        pass
        
    def draw(self, font, player):
        print "Sidebar?"
        for t in self:
            t.draw(surface, font, player)

class unitText(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
    def draw(self, surface, font, player):
        if player.selection:
            text = (player.selection.name)
#            text.append(player.selection.x)
        else:
            text = ""
            
            
        size = font.size(text)      #this is probably why the s in frowns stays

        fg = 250, 240, 230
        bg = 5, 5, 5

        a_sys_font = pygame.font.SysFont("Arial", 10)

        #no AA, no transparancy, normal
        ren = font.render(text, 0, fg, bg)
        surface.blit(ren, (330, 10))