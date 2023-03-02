from Editor_lib import *
from Editor_tela import *
from Editor_inicializador import *
import Editor_inicializador2

# ed, param, cache, edit = Inicializador_terminal()

ed, param, cache, edit = Editor_inicializador2.Inicializador_GUI()

name = ed.image_name + '.png'

pygame.init()
pygame.font.init()
# inicio do menu
menu = param.width*param.pix
screen = pygame.display.set_mode((menu+100, param.height*param.pix))
pygame.display.set_caption('Editor')
image = pygame.image.load(name)
image = pygame.transform.scale(image, (menu, param.height*param.pix))
try:
    tinta = pygame.image.load('balde_de_tinta.png')
except:
    print('Erro ai abrir a imagem do balde de tinta.')
timer = pygame.time.Clock()
FPS = 120
BLACK = (0, 0, 0)
posx = 0
posy = 0
zoom = 1

param.scale_on = []
for x in range(0, 4):
    param.scale_on.append(int(0))

adding = []
for x in range(0, 4):
    adding.append(int(0))
param.color_scale = []
for x in range(0, 4):
    param.color_scale.append(int(0))
param.color_scale[3] = 255
paint = 0
search_color = 0
cut = 0
cut_aux = (-1, -1)
radius = 0
painter = 0
move = []
x = 0
y = 0
menu_keys = {}
menu_keys['menu'] = menu
menu_keys['background_color'] = (150, 150, 150)
menu_keys['letter_color'] = BLACK
menu_keys['balde_de_tinta'] = tinta
menu_keys['zoom'] = zoom
for x in range(0, 4):
    move.append(int(0))


quit_edit = False
while quit_edit != True:
    timer.tick(FPS)
    screen.fill((50, 50, 50))
    screen.blit(image, (posx*zoom*param.pix, posy*zoom*param.pix))
    ex_x, ex_y = x, y
    x, y = pygame.mouse.get_pos()
    x_img_pos, y_img_pos = x//param.pix//zoom, y//param.pix//zoom

    menu_keys['parameters'] = param
    menu_keys['x_img_pos'] = x_img_pos
    menu_keys['y_img_pos'] = y_img_pos
    menu_keys['radius'] = radius
    menu_keys['cut'] = cut
    menu_keys['search_color'] = search_color
    menu_keys['painter'] = painter
    menu_keys['zoom'] = zoom

    Editor_interface(screen, menu_keys)

    Text(screen, f'x:{int(x/param.pix)}, y:{int(y/param.pix)}', BLACK, 20, menu+2, param.height*param.pix-20)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_edit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_edit = True
            # if event.key == pygame.K_RIGHT:
            #     ed.rotate_image()
            #     ed.save(cache)
            #     image = pygame.image.load(cache + '.png')
            #     image = pygame.transform.scale(image, (menu*zoom, param.height*param.pix*zoom))
            # if event.key == pygame.K_LEFT:
            #     ed.rotate_image(clockwise=False)
            #     ed.save(cache)
            #     image = pygame.image.load(cache + '.png')
            #     image = pygame.transform.scale(image, (menu*zoom, param.height*param.pix*zoom))
            if event.key == pygame.K_UP:
                move[0] = 1
            if event.key == pygame.K_DOWN:
                move[1] = 1
            if event.key == pygame.K_RIGHT:
                move[2] = 1
            if event.key == pygame.K_LEFT:
                move[3] = 1
            if event.key == pygame.K_r:
                if param.scale_on[0] == 0:
                    param.scale_on[0] = 1
                else:
                    param.scale_on[0] = 0
            if event.key == pygame.K_g:
                if param.scale_on[1] == 0:
                    param.scale_on[1] = 1
                else:
                    param.scale_on[1] = 0
            if event.key == pygame.K_b:
                if param.scale_on[2] == 0:
                    param.scale_on[2] = 1
                else:
                    param.scale_on[2] = 0
            if event.key == pygame.K_a:
                if param.scale_on[3] == 0:
                    param.scale_on[3] = 1
                else:
                    param.scale_on[3] = 0
            if event.key == pygame.K_p:
                if painter == 0:
                    painter = 1
                else:
                    painter = 0
            if event.key == pygame.K_EQUALS:
                for c in range(0, 4):
                    if param.scale_on[c] == 1:
                        adding[c] += 1
            if event.key == pygame.K_MINUS:
                for c in range(0, 4):
                    if param.scale_on[c] == 1:
                        adding[c] -= 1


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_EQUALS:
                for c in range(0, 4):
                    adding[c] = 0
            if event.key == pygame.K_MINUS:
                for c in range(0, 4):
                    adding[c] = 0
            if event.key == pygame.K_UP:
                move[0] = 0
            if event.key == pygame.K_DOWN:
                move[1] = 0
            if event.key == pygame.K_RIGHT:
                move[2] = 0
            if event.key == pygame.K_LEFT:
                move[3] = 0

        if event.type == pygame.MOUSEBUTTONDOWN:

            if x < menu:
                if search_color == 1:
                    param.color_scale = ed.get_pix((x_img_pos-posx-posx, y_img_pos-posx-posy))
                    search_color = 0
                elif cut == 1:
                    if cut_aux == (-1, -1):
                        cut_aux = (x_img_pos-posx, y_img_pos-posy)
                    else:
                        ed.cut_img(cut_aux, [x_img_pos-posx, y_img_pos-posy])
                        cut_aux = (-1, -1)
                        cut = 0
                elif painter == 1:
                    ed.Paint_init((x_img_pos - posx, y_img_pos - posy), 
                                  (param.color_scale[0], param.color_scale[1], param.color_scale[2], param.color_scale[3]))
                    ed.save(cache)
                    image = pygame.image.load(cache + '.png')
                    image = pygame.transform.scale(image, (menu*zoom, param.height*param.pix*zoom))
                else:
                    paint = 1

            # ativa o modo de busca de cor
            elif x >= menu+5 and x < menu+95 and y >= 175 and y < 197:
                if search_color == 0:
                    search_color = 1
                else:
                    search_color = 0

            # zoom e posicao da tela
            elif x >= menu+11 and x < menu+26 and y >= 253 and y < 268:
                zoom += 1
                image = pygame.transform.scale(image, (menu*zoom, param.height*param.pix*zoom))
            elif x >= menu+11 and x < menu+26 and y >= 275 and y < 290:
                if zoom > 1:
                    zoom -= 1
                    image = pygame.transform.scale(image, (menu*zoom, param.height*param.pix*zoom))
            elif x >= menu+80 and x < menu+95 and y >= 265 and y < 280:
                posx -= 1
            elif x >= menu+40 and x < menu+55 and y >= 265 and y < 280:
                posx += 1
            elif x >= menu+60 and x < menu+75 and y >= 285 and y < 300:
                posy -= 1
            elif x >= menu+60 and x < menu+75 and y >= 245 and y < 260:
                posy += 1
            elif x >= menu+60 and x < menu+75 and y >= 265 and y < 280:
                posx = 0
                posy = 0

            # aumenta ou diminui o raio do traço
            elif x >= menu+80 and x < menu+95 and y >= 315 and y < 330:
                radius += 1
            elif x >= menu+80 and x < menu+95 and y >= 333 and y < 348:
                radius -= 1
                if radius < 0:
                    radius = 0

            # salva
            elif x >= menu+5 and x < menu+75 and y >= 350 and y < 372:
                if edit:
                    name = name.replace('.png', '(editado)')
                else:
                    name = name.replace('.png', '')
                ed.save(name)

            # deixa os param.pixeis da cor selecionada transparentes
            elif x >= menu+5 and x < menu+75 and y >= 375 and y < 397:
                ed.transparet(param.color_scale)
                ed.save(cache)
                image = pygame.image.load(cache + '.png')
                image = pygame.transform.scale(image, (menu*zoom, param.height*param.pix*zoom))

            # ativa o modo de corte de imagem
            elif x >= menu+5 and x < menu+75 and y >= 400 and y < 422:
                if cut == 0:
                    cut = 1
                else:
                    cut = 0
                    cut_aux = (-1, -1)

            # ativa o modo pintar
            elif x >= menu+78 and x < menu+98 and y >= 200 and y < 220:
                if painter == 1:
                    painter = 0
                else:
                    painter = 1

            # verifica qual cor o usuario selecionou
            elif x >= menu+5 and x < menu+15 and y >= 200 and y < 210:
                param.color_scale = [0, 0, 0, 255]
            elif x >= menu+20 and x < menu+30 and y >= 200 and y < 210:
                param.color_scale = [255, 255, 255, 255]
            elif x >= menu+35 and x < menu+45 and y >= 200 and y < 210:
                param.color_scale = [255, 0, 0, 255]
            elif x >= menu+50 and x < menu+60 and y >= 200 and y < 210:
                param.color_scale = [0, 255, 0, 255]
            elif x >= menu+65 and x < menu+75 and y >= 200 and y < 210:
                param.color_scale = [0, 0, 255, 255]

            elif x >= menu+5 and x < menu+15 and y >= 215 and y < 225:
                param.color_scale = [100, 100, 100, 255]
            elif x >= menu+20 and x < menu+30 and y >= 215 and y < 225:
                param.color_scale = [200, 200, 200, 255]
            elif x >= menu+35 and x < menu+45 and y >= 215 and y < 225:
                param.color_scale = [255, 130, 0, 255]
            elif x >= menu+50 and x < menu+60 and y >= 215 and y < 225:
                param.color_scale = [255, 255, 0, 255]
            elif x >= menu+65 and x < menu+75 and y >= 215 and y < 225:
                param.color_scale = [0, 255, 255, 255]

            elif x >= menu+5 and x < menu+15 and y >= 230 and y < 240:
                param.color_scale = [150, 75, 0, 255]
            elif x >= menu+20 and x < menu+30 and y >= 230 and y < 240:
                param.color_scale = [255, 0, 255, 255]
            elif x >= menu+35 and x < menu+45 and y >= 230 and y < 240:
                param.color_scale = [160, 0, 255, 255]

        if event.type == pygame.MOUSEBUTTONUP:
            paint = 0

    # aumenta ou diminui a saturacao das cores
    for c in range(0, 4):
        param.color_scale[c] += adding[c]
        if param.color_scale[c] < 0:
            param.color_scale[c] = 0
        if param.color_scale[c] > 255:
            param.color_scale[c] = 255

    # move a imagem
    if move[0] == 1:
        posy += 1
    if move[1] == 1:
        posy -= 1
    if move[2] == 1:
        posx -= 1
    if move[3] == 1:
        posx += 1

    # atualiza a area que sera cortada da imagem de acordo com o mouse
    if cut_aux != (-1, -1) and x < menu:
        cutting_outline(screen, (cut_aux[0]*param.pix*zoom+posx, cut_aux[1]*param.pix*zoom+posy), (x, y), param.color_scale)

    # desenha na tela de acordo com o tamanho do raio
    if paint == 1 and x < menu:
        try:
            c = (param.color_scale[0], param.color_scale[1], param.color_scale[2], param.color_scale[3])
            if radius == 0:
                ed.add_color((x_img_pos - posx, y_img_pos - posy), c)
            else:
                ed.add_circle((x_img_pos - posx, y_img_pos - posy), c, radius)

            if x != ex_x or y != ex_y:
                
                # ed.add_line(ex_x//param.pix//zoom - posx, ex_y//param.pix//zoom - posy,
                #             x_//param.pix//zoom - posx, y//param.pix//zoom - posy,
                #             c, radius=radius)

                if radius == 0:
                    ed.add_line(ex_x//param.pix//zoom - posx, ex_y//param.pix//zoom - posy,
                                x_img_pos - posx, y//param.pix//zoom - posy,
                                c)
                else:
                    ed.add_line_with_radius(ex_x//param.pix//zoom - posx, ex_y//param.pix//zoom - posy,
                                x_img_pos - posx, y//param.pix//zoom - posy,
                                c, radius)

            ed.save(cache)
            image = pygame.image.load(cache + '.png')
            image = pygame.transform.scale(image, (menu*zoom, param.height*param.pix*zoom))
        except:
            pass

    pygame.display.update()

pygame.font.quit()
pygame.quit()
