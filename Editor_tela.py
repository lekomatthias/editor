import pygame
from Editor_lib import Text

# desenha a interface do editor
def Editor_interface(screen, keys):

    pygame.draw.rect(screen, keys['background_color'], [keys['menu'], 0, 100, keys['parameters'].height*keys['parameters'].pix])
    pygame.draw.rect(screen, [keys['parameters'].color_scale[0], keys['parameters'].color_scale[1], keys['parameters'].color_scale[2]], [keys['menu']+20, 20, 60, 60])
    Text(screen, f"{keys['parameters'].scale_on[0]} RED: {keys['parameters'].color_scale[0]}", keys['letter_color'], 20, keys['menu']+10, 100)
    Text(screen, f"{keys['parameters'].scale_on[1]} GREEN: {keys['parameters'].color_scale[1]}", keys['letter_color'], 20, keys['menu']+10, 120)
    Text(screen, f"{keys['parameters'].scale_on[2]} BLUE: {keys['parameters'].color_scale[2]}", keys['letter_color'], 20, keys['menu']+10, 140)
    Text(screen, f"{keys['parameters'].scale_on[3]} ALPHA: {keys['parameters'].color_scale[3]}", keys['letter_color'], 20, keys['menu']+10, 160)
    
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+11, 253, 15, 15])
    Text(screen, '+', keys['letter_color'], 20, keys['menu']+15, 252)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+11, 275, 15, 15])
    Text(screen, '-', keys['letter_color'], 20, keys['menu']+17, 275)
    Text(screen, f"ZOOM: {keys['zoom']}:1", keys['letter_color'], 20, keys['menu']+5, 302)

    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+80, 265, 15, 15])
    Text(screen, '>', keys['letter_color'], 20, keys['menu']+84, 264)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+40, 265, 15, 15])
    Text(screen, '<', keys['letter_color'], 20, keys['menu']+44, 264)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+60, 285, 15, 15])
    Text(screen, 'v', keys['letter_color'], 20, keys['menu']+64, 285)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+60, 245, 15, 15])
    Text(screen, '^', keys['letter_color'], 20, keys['menu']+64, 247)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+60, 265, 15, 15])
    Text(screen, 'o', keys['letter_color'], 20, keys['menu']+64, 265)
    

    # pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+5, 320, 70, 22])
    Text(screen, f"RADIUS: {keys['radius']}", keys['letter_color'], 20, keys['menu']+5, 326)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+80, 315, 15, 15])
    Text(screen, '+', keys['letter_color'], 20, keys['menu']+84, 314)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+80, 333, 15, 15])
    Text(screen, '-', keys['letter_color'], 20, keys['menu']+86, 333)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+5, 350, 70, 22])
    Text(screen, 'SAVE', keys['letter_color'], 25, keys['menu']+16, 353)
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+5, 375, 70, 22])
    Text(screen, 'TRNSP', keys['letter_color'], 24, keys['menu']+7, 378)

    if keys['search_color'] == 0:
        pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+5, 175, 90, 22])
    else:
        pygame.draw.rect(screen, (255, 255, 100, 255), [keys['menu']+5, 175, 90, 22])
    Text(screen, 'SEARCH COLOR',keys['letter_color'], 15, keys['menu']+8, 181)

    if keys['cut'] == 0:
        pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+5, 400, 70, 22])
    else:
        pygame.draw.rect(screen, (255, 255, 0, 255), [keys['menu']+5, 400, 70, 22])
    Text(screen, 'CUT IMG', keys['letter_color'], 20, keys['menu']+10, 404)

    try:
        if keys['painter'] == 0:
            pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+78, 200, 20, 20])
        else:
            pygame.draw.rect(screen, (255, 255, 0, 255), [keys['menu']+78, 200, 20, 20])
        screen.blit(keys['balde_de_tinta'], (keys['menu']+78, 200))
    except:
        pass

    pygame.draw.rect(screen, (0, 0, 0, 255), [keys['menu']+5, 200, 10, 10])
    pygame.draw.rect(screen, (255, 255, 255, 255), [keys['menu']+20, 200, 10, 10])
    pygame.draw.rect(screen, (255, 0, 0, 255), [keys['menu']+35, 200, 10, 10])
    pygame.draw.rect(screen, (0, 255, 0, 255), [keys['menu']+50, 200, 10, 10])
    pygame.draw.rect(screen, (0, 0, 255, 255), [keys['menu']+65, 200, 10, 10])
    pygame.draw.rect(screen, (100, 100, 100, 255), [keys['menu']+5, 215, 10, 10])
    pygame.draw.rect(screen, (200, 200, 200, 255), [keys['menu']+20, 215, 10, 10])
    pygame.draw.rect(screen, (255, 130, 0, 255), [keys['menu']+35, 215, 10, 10])
    pygame.draw.rect(screen, (255, 255, 0, 255), [keys['menu']+50, 215, 10, 10])
    pygame.draw.rect(screen, (0, 255, 255, 255), [keys['menu']+65, 215, 10, 10])
    pygame.draw.rect(screen, (150, 75, 0, 255), [keys['menu']+5, 230, 10, 10])
    pygame.draw.rect(screen, (255, 0, 255, 255), [keys['menu']+20, 230, 10, 10])
    pygame.draw.rect(screen, (160, 0, 255, 255), [keys['menu']+35, 230, 10, 10])
    # pygame.draw.rect(screen, (0, 0, 0, 255), [keys['menu']+50, 215, 10, 10])
    # pygame.draw.rect(screen, (0, 0, 0, 255), [keys['menu']+65, 215, 10, 10])