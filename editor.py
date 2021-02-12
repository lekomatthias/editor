from os import path
from PIL import Image, ImageEnhance
import pygame
from pygame.locals import *

# operaçao de imagem
class Editor():
    img = None
    img_format = None
    img_local = None
    image_name = None
    img_ext = None

    def reset(self):
        self.img = None
        self.img_format = None
        self.img_local = None
        self.image_name = None
        self.img_ext = None

    def load_image(self, image):
        try:
            self.img = Image.open(image)
            self.img_format = self.img.format
            self.img_local = path.dirname(path.realpath(image))
            self.image_name, self.img_ext = path.splitext(path.basename(image))
            print('loading success!')
            return True
        except:
            print('loading error!')
            return False

    def save(self, name_image):
        ln = self.img_local + '/' + name_image + self.img_ext
        self.img.save(ln, self.img_format)


    def rotate_image(self, clockwise = True, angle = 90):
        if clockwise is True:
            self.img = self.img.rotate(angle * -1, expand=True)
        else:
            self.img = self.img.rotate(angle, expand=True)

    def add_color(self, pos, color):    
        self.img.putpixel(pos, color)

    def add_circle(self, pos, color, radius):
        if radius != 0:
            for x in range(pos[0]-radius+1, pos[0]+radius):
                for y in range(pos[1]-radius+1, pos[1]+radius):
                    if (x-pos[0])**2 + (y-pos[1])**2 <= radius**2:
                        try:
                            if x >= 0 and y >= 0:
                                self.add_color((x, y), color)
                        except:
                            pass
        else:
            self.add_color(pos, color)

    def add_line(self, ix, iy, fx, fy, color, radius, zoom, PIX):
        x = fx - ix
        y = fy - iy
        if x >= 0:
            if y <= 0:
                if x < -y:
                    a = float(x / y)
                    for cont in range(fy+1, iy):
                        self.add_circle((int(a*(cont-fy) + fx) , cont), color, radius)
                elif x >= y:
                    a = float(y / x)
                    for cont in range(ix+1, fx):
                        self.add_circle((cont, int(a*(cont-ix) + iy) ), color, radius)
            else:
                if x >= y:
                    a = float(y / x)
                    for cont in range(ix+1, fx):
                        self.add_circle((cont, int(a*(cont-ix) + iy) ), color, radius)
                elif x <= y:
                    a = float(x / y)
                    for cont in range(iy+1, fy):
                        self.add_circle((int(a*(cont-iy) + ix) , cont), color, radius)
        else:
            if y > 0:
                if -x >= y:
                    a = float(y / x)
                    for cont in range(fx+1, ix):
                        self.add_circle((cont, int(a*(cont-fx) + fy) ), color, radius)
                elif x <= y:
                    a = float(x / y)
                    for cont in range(iy+1, fy):
                        self.add_circle((int(a*(cont-iy) + ix) , cont), color, radius)
            else:
                if x >= y:
                    a = float(x / y)
                    for cont in range(fy+1, iy):
                        self.add_circle((int(a*(cont-fy) + fx) , cont), color, radius)
                elif x < y:
                    a = float(y / x)
                    for cont in range(fx+1, ix):
                        self.add_circle((cont, int(a*(cont-fx) + fy) ), color, radius)

        pass

    def get_pix(self, pos):
        tuple1 = self.img.getpixel(pos)
        list1 = []
        for x in range(0, len(tuple1)):
            list1.append(tuple1[x])
        list1.append(255)
        return list1

    def remove_color(self):
        conv = ImageEnhance.Color(self.img)
        self.img = conv.enhance(0)

    def transparet(self, color = [255, 255, 255, 255]):
        datas = self.img.getdata()
        new_data = []
        for item in datas:
            if item[0] == color[0] and item[1] == color[1] and item[2] == color[2]:
                new_data.append((color[0], color[1], color[2], 0))
            else:
                new_data.append(item)
        self.img.putdata(new_data)
    
    def cut_img(self, pos1, pos2):
        # print(pos1 + pos2)
        img = ed.img.crop((pos1[0], pos1[1], pos2[0]+1, pos2[1]+1))
        # name = name.replace('.png', '(cortado).png')
        img.save('(cortado)' + name , 'PNG')

    def paint(self, pos, color, base):
        if base == self.img.getpixel(pos) and self.img.getpixel(pos) != color:
            try:
                self.img.putpixel(pos, color)
                self.paint((pos[0]+1, pos[1]), color, base)
                self.paint((pos[0]-1, pos[1]), color, base)
                self.paint((pos[0], pos[1]+1), color, base)
                self.paint((pos[0], pos[1]-1), color, base)
            except:
                pass
        pass

    def paint_init(self, pos, color):
        base = self.img.getpixel(pos)
        self.paint(pos, color, base)
        pass


# coloca um texto na tela
def text(text, color, size, width, height):
    font = pygame.font.SysFont(None, size)
    text1 = font.render(text, True, color)
    screen.blit(text1, (int(width), int(height)))

# delinea onde imagem sera cortada
def cutting_outline(pos1, pos2, color):
    if pos2[0] - pos1[0] > 0 and pos2[1] - pos1[1] > 0:
        pygame.draw.rect(screen, color, [pos1[0]-2, pos1[1], 1, (pos2[1]-pos1[1]+2)])
        pygame.draw.rect(screen, color, [pos1[0], pos1[1]-2, (pos2[0]-pos1[0]+2), 1])
        pygame.draw.rect(screen, color, [pos2[0]+1, pos1[1], 1, (pos2[1]-pos1[1]+1)])
        pygame.draw.rect(screen, color, [pos1[0], pos2[1]+1, (pos2[0]-pos1[0]+1), 1])


ed = Editor()

while True:
    try:
        op = input('deseja criar ou editar?[c/e]\n')
        if op == 'c':
            name = input('qual o nome da nova imagem?\n')
            name = name + '.png'
            w = int(input('largura: '))
            h = int(input('altura: '))
            img = Image.new('RGBA', (w, h), (255, 255, 255, 255))
            img.save(name , 'PNG')
            edit = 0
        elif op == 'e':
            name = input('qual o nome da imagem?\n')
            edit = 1

        ed.load_image(name)
        break
    except:
        print('\n\nerro\n\n')

# cria uma imagem do formato png caso a aberta seja jpeg
if ed.img_format == 'JPEG':
    img = Image.open(name)
    name = name.replace('jpeg', 'png')
    print('tipo de imagem mudado para PNG')
    img.save (name)
    ed.reset()
    ed.load_image(name)

# cria uma imagem auxiliar
ed.img = ed.img.convert('RGBA')
cache = 'img_cache'
ed.save(cache)
WIDTH, HEIGHT = ed.img.size

print('(recomendado uma proporção pixel X ajuste = 450 pixeis de altura)')
print(f'o tamanho da imagem é:({WIDTH}, {HEIGHT})')
adjustment = input('deseja ajustar a tela?\n[m] manualmente\n[a] automaticamente\n[n] não\n')
PIX = 1
    
if adjustment == 'm':
    try:
        PIX = int(input('deseja usar qual escala?[x:1] '))
    except:
        print('\nalgo invalido foi digitado, ajustando automaticamente\n')
elif adjustment == 'n':
    pass
else:
    aux = 0
    while HEIGHT*PIX < 450:
        PIX = int((450+aux)/HEIGHT)
        if HEIGHT*PIX < 450:
            aux += 10
            if aux > 200:
                break
        else:
            break


print(f'tamanho final é: ({WIDTH*PIX}, {HEIGHT*PIX}) pixeis')

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH*PIX+100, HEIGHT*PIX))
pygame.display.set_caption('editor')
image = pygame.image.load(name)
image = pygame.transform.scale(image, (WIDTH*PIX, HEIGHT*PIX))
timer = pygame.time.Clock()
FPS = 120
BLACK = (0, 0, 0)
posx = 0
posy = 0
zoom = 1

scale_on = []
for x in range(0, 4):
    scale_on.append(int(0))

adding = []
for x in range(0, 4):
    adding.append(int(0))
color_scale = []
for x in range(0, 4):
    color_scale.append(int(0))
color_scale[3] = 255
paint = 0
search_color = 0
cut = 0
cut_aux = (-1, -1)
radius = 0
painter = 0
move = []
x = 0
y = 0
for x in range(0, 4):
    move.append(int(0))
quit_edit = False
while quit_edit is not True:
    timer.tick(FPS)
    screen.fill((50, 50, 50))
    screen.blit(image, (posx*zoom*PIX, posy*zoom*PIX))
    ex_x, ex_y = x, y
    x, y = pygame.mouse.get_pos()

    # desenha a interface do editor
    pygame.draw.rect(screen, (150, 150, 150), [WIDTH*PIX, 0, 100, HEIGHT*PIX])
    pygame.draw.rect(screen, [color_scale[0], color_scale[1], color_scale[2]], [WIDTH*PIX+20, 20, 60, 60])
    text(f'{scale_on[0]} RED: {color_scale[0]}', BLACK, 20, WIDTH*PIX+10, 100)
    text(f'{scale_on[1]} GREEN: {color_scale[1]}', BLACK, 20, WIDTH*PIX+10, 120)
    text(f'{scale_on[2]} BLUE: {color_scale[2]}', BLACK, 20, WIDTH*PIX+10, 140)
    text(f'{scale_on[3]} ALPHA: {color_scale[3]}', BLACK, 20, WIDTH*PIX+10, 160)
    text(f'x:{int(x/PIX/zoom-posx)}, y:{int(y/PIX/zoom-posy)}', BLACK, 20, WIDTH*PIX+2, HEIGHT*PIX-20)

    if search_color == 0:
        pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+5, 175, 90, 22])
    else:
        pygame.draw.rect(screen, (255, 255, 100, 255), [WIDTH*PIX+5, 175, 90, 22])
    text('SEARCH COLOR', BLACK, 15, WIDTH*PIX+8, 181)

    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+11, 253, 15, 15])
    text('+', BLACK, 20, WIDTH*PIX+15, 252)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+11, 275, 15, 15])
    text('-', BLACK, 20, WIDTH*PIX+17, 275)
    text(f'ZOOM: {zoom}:1', BLACK, 20, WIDTH*PIX+5, 302)

    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+80, 265, 15, 15])
    text('>', BLACK, 20, WIDTH*PIX+84, 264)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+40, 265, 15, 15])
    text('<', BLACK, 20, WIDTH*PIX+44, 264)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+60, 285, 15, 15])
    text('v', BLACK, 20, WIDTH*PIX+64, 285)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+60, 245, 15, 15])
    text('^', BLACK, 20, WIDTH*PIX+64, 247)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+60, 265, 15, 15])
    text('o', BLACK, 20, WIDTH*PIX+64, 265)
    

    # pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+5, 320, 70, 22])
    text(f'RADIUS: {radius}', BLACK, 20, WIDTH*PIX+5, 326)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+80, 315, 15, 15])
    text('+', BLACK, 20, WIDTH*PIX+84, 314)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+80, 333, 15, 15])
    text('-', BLACK, 20, WIDTH*PIX+86, 333)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+5, 350, 70, 22])
    text('SAVE', BLACK, 25, WIDTH*PIX+16, 353)
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+5, 375, 70, 22])
    text('TRANSP', BLACK, 24, WIDTH*PIX+7, 378)
    if cut == 0:
        pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+5, 400, 70, 22])
    else:
        pygame.draw.rect(screen, (255, 255, 0, 255), [WIDTH*PIX+5, 400, 70, 22])
    text('CUT IMG', BLACK, 20, WIDTH*PIX+10, 404)

    pygame.draw.rect(screen, (0, 0, 0, 255), [WIDTH*PIX+5, 200, 10, 10])
    pygame.draw.rect(screen, (255, 255, 255, 255), [WIDTH*PIX+20, 200, 10, 10])
    pygame.draw.rect(screen, (255, 0, 0, 255), [WIDTH*PIX+35, 200, 10, 10])
    pygame.draw.rect(screen, (0, 255, 0, 255), [WIDTH*PIX+50, 200, 10, 10])
    pygame.draw.rect(screen, (0, 0, 255, 255), [WIDTH*PIX+65, 200, 10, 10])
    pygame.draw.rect(screen, (100, 100, 100, 255), [WIDTH*PIX+5, 215, 10, 10])
    pygame.draw.rect(screen, (200, 200, 200, 255), [WIDTH*PIX+20, 215, 10, 10])
    pygame.draw.rect(screen, (255, 130, 0, 255), [WIDTH*PIX+35, 215, 10, 10])
    pygame.draw.rect(screen, (255, 255, 0, 255), [WIDTH*PIX+50, 215, 10, 10])
    pygame.draw.rect(screen, (0, 255, 255, 255), [WIDTH*PIX+65, 215, 10, 10])
    pygame.draw.rect(screen, (150, 75, 0, 255), [WIDTH*PIX+5, 230, 10, 10])
    pygame.draw.rect(screen, (255, 0, 255, 255), [WIDTH*PIX+20, 230, 10, 10])
    pygame.draw.rect(screen, (160, 0, 255, 255), [WIDTH*PIX+35, 230, 10, 10])
    # pygame.draw.rect(screen, (0, 0, 0, 255), [WIDTH*PIX+50, 215, 10, 10])
    # pygame.draw.rect(screen, (0, 0, 0, 255), [WIDTH*PIX+65, 215, 10, 10])

    for event in pygame.event.get():
        if event.type is QUIT:
            quit_edit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_edit = True
            # if event.key == pygame.K_RIGHT:
            #     ed.rotate_image()
            #     ed.save(cache)
            #     image = pygame.image.load(cache + '.png')
            #     image = pygame.transform.scale(image, (WIDTH*PIX*zoom, HEIGHT*PIX*zoom))
            # if event.key == pygame.K_LEFT:
            #     ed.rotate_image(clockwise=False)
            #     ed.save(cache)
            #     image = pygame.image.load(cache + '.png')
            #     image = pygame.transform.scale(image, (WIDTH*PIX*zoom, HEIGHT*PIX*zoom))
            if event.key == pygame.K_UP:
                move[0] = 1
            if event.key == pygame.K_DOWN:
                move[1] = 1
            if event.key == pygame.K_RIGHT:
                move[2] = 1
            if event.key == pygame.K_LEFT:
                move[3] = 1
            if event.key == pygame.K_r:
                if scale_on[0] == 0:
                    scale_on[0] = 1
                else:
                    scale_on[0] = 0
            if event.key == pygame.K_g:
                if scale_on[1] == 0:
                    scale_on[1] = 1
                else:
                    scale_on[1] = 0
            if event.key == pygame.K_b:
                if scale_on[2] == 0:
                    scale_on[2] = 1
                else:
                    scale_on[2] = 0
            if event.key == pygame.K_a:
                if scale_on[3] == 0:
                    scale_on[3] = 1
                else:
                    scale_on[3] = 0
            if event.key == pygame.K_p:
                if painter == 0:
                    painter = 1
                else:
                    painter = 0
            if event.key == pygame.K_EQUALS:
                for c in range(0, 4):
                    if scale_on[c] == 1:
                        adding[c] += 1
            if event.key == pygame.K_MINUS:
                for c in range(0, 4):
                    if scale_on[c] == 1:
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

            if x < WIDTH*PIX:
                if search_color == 1:
                    color_scale = ed.get_pix((x/PIX//zoom-posx, y/PIX//zoom-posy))
                    search_color = 0
                elif cut == 1:
                    if cut_aux == (-1, -1):
                        cut_aux = ((x)//PIX//zoom-posx, (y)//PIX//zoom-posy)
                    else:
                        ed.cut_img(cut_aux, [x//PIX//zoom-posx, y//PIX//zoom-posy])
                        cut_aux = (-1, -1)
                        cut = 0
                elif painter == 1:
                    ed.paint_init((x//PIX//zoom-posx,y//PIX//zoom-posy),(color_scale[0],color_scale[1],color_scale[2],color_scale[3]))
                    ed.save(cache)
                    image = pygame.image.load(cache + '.png')
                    image = pygame.transform.scale(image, (WIDTH*PIX*zoom, HEIGHT*PIX*zoom))
                else:
                    paint = 1

            # ativa o modo de busca de cor
            elif x >= WIDTH*PIX+5 and x < WIDTH*PIX+95 and y >= 175 and y < 197:
                if search_color == 0:
                    search_color = 1
                else:
                    search_color = 0

            # zoom e posicao da tela
            elif x >= WIDTH*PIX+11 and x < WIDTH*PIX+26 and y >= 253 and y < 268:
                zoom += 1
                image = pygame.transform.scale(image, (WIDTH*PIX*zoom, HEIGHT*PIX*zoom))
            elif x >= WIDTH*PIX+11 and x < WIDTH*PIX+26 and y >= 275 and y < 290:
                if zoom > 1:
                    zoom -= 1
                    image = pygame.transform.scale(image, (WIDTH*PIX*zoom, HEIGHT*PIX*zoom))
            elif x >= WIDTH*PIX+80 and x < WIDTH*PIX+95 and y >= 265 and y < 280:
                posx -= 1
            elif x >= WIDTH*PIX+40 and x < WIDTH*PIX+55 and y >= 265 and y < 280:
                posx += 1
            elif x >= WIDTH*PIX+60 and x < WIDTH*PIX+75 and y >= 285 and y < 300:
                posy -= 1
            elif x >= WIDTH*PIX+60 and x < WIDTH*PIX+75 and y >= 245 and y < 260:
                posy += 1
            elif x >= WIDTH*PIX+60 and x < WIDTH*PIX+75 and y >= 265 and y < 280:
                posx = 0
                posy = 0

            # aumenta ou diminui o raio do traco
            elif x >= WIDTH*PIX+80 and x < WIDTH*PIX+95 and y >= 315 and y < 330:
                radius += 1
            elif x >= WIDTH*PIX+80 and x < WIDTH*PIX+95 and y >= 333 and y < 348:
                radius -= 1
                if radius < 0:
                    radius = 0

            # salva
            elif x >= WIDTH*PIX+5 and x < WIDTH*PIX+75 and y >= 350 and y < 372:
                if edit == 1:
                    name = name.replace('.png', '(editado)')
                else:
                    name = name.replace('.png', '')
                ed.save(name)

            # deixa os pixeis da cor selecionada transparentes
            elif x >= WIDTH*PIX+5 and x < WIDTH*PIX+75 and y >= 375 and y < 397:
                ed.transparet(color_scale)
                ed.save(cache)
                image = pygame.image.load(cache + '.png')
                image = pygame.transform.scale(image, (WIDTH*PIX*zoom, HEIGHT*PIX*zoom))

            # ativa o modo de corte de imagem
            elif x >= WIDTH*PIX+5 and x < WIDTH*PIX+75 and y >= 400 and y < 422:
                if cut == 0:
                    cut = 1
                else:
                    cut = 0
                    cut_aux = (-1, -1)

            # verifica qual cor o usuario selecionou
            elif x >= WIDTH*PIX+5 and x < WIDTH*PIX+15 and y >= 200 and y < 210:
                color_scale = [0, 0, 0, 255]
            elif x >= WIDTH*PIX+20 and x < WIDTH*PIX+30 and y >= 200 and y < 210:
                color_scale = [255, 255, 255, 255]
            elif x >= WIDTH*PIX+35 and x < WIDTH*PIX+45 and y >= 200 and y < 210:
                color_scale = [255, 0, 0, 255]
            elif x >= WIDTH*PIX+50 and x < WIDTH*PIX+60 and y >= 200 and y < 210:
                color_scale = [0, 255, 0, 255]
            elif x >= WIDTH*PIX+65 and x < WIDTH*PIX+75 and y >= 200 and y < 210:
                color_scale = [0, 0, 255, 255]

            elif x >= WIDTH*PIX+5 and x < WIDTH*PIX+15 and y >= 215 and y < 225:
                color_scale = [100, 100, 100, 255]
            elif x >= WIDTH*PIX+20 and x < WIDTH*PIX+30 and y >= 215 and y < 225:
                color_scale = [200, 200, 200, 255]
            elif x >= WIDTH*PIX+35 and x < WIDTH*PIX+45 and y >= 215 and y < 225:
                color_scale = [255, 130, 0, 255]
            elif x >= WIDTH*PIX+50 and x < WIDTH*PIX+60 and y >= 215 and y < 225:
                color_scale = [255, 255, 0, 255]
            elif x >= WIDTH*PIX+65 and x < WIDTH*PIX+75 and y >= 215 and y < 225:
                color_scale = [0, 255, 255, 255]

            elif x >= WIDTH*PIX+5 and x < WIDTH*PIX+15 and y >= 230 and y < 240:
                color_scale = [150, 75, 0, 255]
            elif x >= WIDTH*PIX+20 and x < WIDTH*PIX+30 and y >= 230 and y < 240:
                color_scale = [255, 0, 255, 255]
            elif x >= WIDTH*PIX+35 and x < WIDTH*PIX+45 and y >= 230 and y < 240:
                color_scale = [160, 0, 255, 255]

        if event.type == pygame.MOUSEBUTTONUP:
            paint = 0

    # aumenta ou diminui a saturacao das cores
    for c in range(0, 4):
        color_scale[c] += adding[c]
        if color_scale[c] < 0:
            color_scale[c] = 0
        if color_scale[c] > 255:
            color_scale[c] = 255

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
    if cut_aux != (-1, -1) and x < WIDTH*PIX:
        cutting_outline(cut_aux, ((x)//PIX*PIX+PIX, (y)//PIX*PIX+PIX), color_scale)

    # desenha na tela de acordo com o tamanho do raio
    if paint == 1 and x < WIDTH*PIX:
        try:
            c = (color_scale[0], color_scale[1], color_scale[2], color_scale[3])
            ed.add_circle((x//PIX//zoom - posx, y//PIX//zoom - posy), c, radius)

            if (x != ex_x or y != ex_y) and radius < 11:
                ed.add_line(ex_x//zoom//PIX-posx, ex_y//zoom//PIX-posy, x//zoom//PIX-posx, y//zoom//PIX-posy, c, radius, zoom, PIX)

            ed.save(cache)
            image = pygame.image.load(cache + '.png')
            image = pygame.transform.scale(image, (WIDTH*PIX*zoom, HEIGHT*PIX*zoom))
        except:
            pass

    pygame.display.update()


print('programa encerrado.')
pygame.font.quit()
pygame.quit()
