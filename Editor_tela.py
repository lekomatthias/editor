import pygame
from Editor_lib import Text

# desenha a interface do editor
def Editor_interface(screen, parameters, zoom, radius, background_color=(150, 150, 150), letter_color=(0, 0, 0)):

    pygame.draw.rect(screen, background_color, [parameters.width*parameters.pix, 0, 100, parameters.height*parameters.pix])
    pygame.draw.rect(screen, [parameters.color_scale[0], parameters.color_scale[1], parameters.color_scale[2]], [parameters.width*parameters.pix+20, 20, 60, 60])
    Text(screen, f'{parameters.scale_on[0]} RED: {parameters.color_scale[0]}', letter_color, 20, parameters.width*parameters.pix+10, 100)
    Text(screen, f'{parameters.scale_on[1]} GREEN: {parameters.color_scale[1]}', letter_color, 20, parameters.width*parameters.pix+10, 120)
    Text(screen, f'{parameters.scale_on[2]} BLUE: {parameters.color_scale[2]}', letter_color, 20, parameters.width*parameters.pix+10, 140)
    Text(screen, f'{parameters.scale_on[3]} ALPHA: {parameters.color_scale[3]}', letter_color, 20, parameters.width*parameters.pix+10, 160)
    
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+11, 253, 15, 15])
    Text(screen, '+', letter_color, 20, parameters.width*parameters.pix+15, 252)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+11, 275, 15, 15])
    Text(screen, '-', letter_color, 20, parameters.width*parameters.pix+17, 275)
    Text(screen, f'ZOOM: {zoom}:1', letter_color, 20, parameters.width*parameters.pix+5, 302)

    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+80, 265, 15, 15])
    Text(screen, '>', letter_color, 20, parameters.width*parameters.pix+84, 264)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+40, 265, 15, 15])
    Text(screen, '<', letter_color, 20, parameters.width*parameters.pix+44, 264)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+60, 285, 15, 15])
    Text(screen, 'v', letter_color, 20, parameters.width*parameters.pix+64, 285)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+60, 245, 15, 15])
    Text(screen, '^', letter_color, 20, parameters.width*parameters.pix+64, 247)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+60, 265, 15, 15])
    Text(screen, 'o', letter_color, 20, parameters.width*parameters.pix+64, 265)
    

    # pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+5, 320, 70, 22])
    Text(screen, f'RADIUS: {radius}', letter_color, 20, parameters.width*parameters.pix+5, 326)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+80, 315, 15, 15])
    Text(screen, '+', letter_color, 20, parameters.width*parameters.pix+84, 314)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+80, 333, 15, 15])
    Text(screen, '-', letter_color, 20, parameters.width*parameters.pix+86, 333)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+5, 350, 70, 22])
    Text(screen, 'SAVE', letter_color, 25, parameters.width*parameters.pix+16, 353)
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+5, 375, 70, 22])
    Text(screen, 'TRANSP', letter_color, 24, parameters.width*parameters.pix+7, 378)

    pygame.draw.rect(screen, (0, 0, 0, 255), [parameters.width*parameters.pix+5, 200, 10, 10])
    pygame.draw.rect(screen, (255, 255, 255, 255), [parameters.width*parameters.pix+20, 200, 10, 10])
    pygame.draw.rect(screen, (255, 0, 0, 255), [parameters.width*parameters.pix+35, 200, 10, 10])
    pygame.draw.rect(screen, (0, 255, 0, 255), [parameters.width*parameters.pix+50, 200, 10, 10])
    pygame.draw.rect(screen, (0, 0, 255, 255), [parameters.width*parameters.pix+65, 200, 10, 10])
    pygame.draw.rect(screen, (100, 100, 100, 255), [parameters.width*parameters.pix+5, 215, 10, 10])
    pygame.draw.rect(screen, (200, 200, 200, 255), [parameters.width*parameters.pix+20, 215, 10, 10])
    pygame.draw.rect(screen, (255, 130, 0, 255), [parameters.width*parameters.pix+35, 215, 10, 10])
    pygame.draw.rect(screen, (255, 255, 0, 255), [parameters.width*parameters.pix+50, 215, 10, 10])
    pygame.draw.rect(screen, (0, 255, 255, 255), [parameters.width*parameters.pix+65, 215, 10, 10])
    pygame.draw.rect(screen, (150, 75, 0, 255), [parameters.width*parameters.pix+5, 230, 10, 10])
    pygame.draw.rect(screen, (255, 0, 255, 255), [parameters.width*parameters.pix+20, 230, 10, 10])
    pygame.draw.rect(screen, (160, 0, 255, 255), [parameters.width*parameters.pix+35, 230, 10, 10])
    # pygame.draw.rect(screen, (0, 0, 0, 255), [parameters.width*parameters.pix+50, 215, 10, 10])
    # pygame.draw.rect(screen, (0, 0, 0, 255), [parameters.width*parameters.pix+65, 215, 10, 10])