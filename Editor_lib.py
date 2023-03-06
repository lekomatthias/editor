from os import path
from PIL import Image, ImageEnhance
import pygame
from pygame.locals import *

from numpy import square, absolute, sqrt

# operacao de imagem
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
            print('imagem aberta')
            self.img_format = self.img.format
            print('formato adquirido')
            self.img_local = path.dirname(path.realpath(image))
            print('caminho adquirido')
            self.image_name, self.img_ext = path.splitext(path.basename(image))
            print('extencao adquirida')
            print('\nloading success!\n')
            return True
        except:
            print('\nloading error!\n')
            return False

    def save(self, name_image):
        ln = self.img_local + '/' + name_image + self.img_ext
        self.img.save(ln, self.img_format)


    def rotate_image(self, clockwise = True, angle = 90):
        if clockwise is True:
            self.img = self.img.rotate(angle * (-1), expand=True)
        else:
            self.img = self.img.rotate(angle, expand=True)

    def add_color(self, pos, color):
        # garante que a localizacao e dentro da imagem
        if pos[0] >= 0 and pos[0] < self.img.width and pos[1] >= 0 and pos[1] < self.img.height:
            self.img.putpixel(pos, color)

    def add_circle(self, pos, color, radius):
        # quadrado que engloba o circulo desejado
        for x in range(pos[0]-radius+1, pos[0]+radius):
            for y in range(pos[1]-radius+1, pos[1]+radius):
                # dentro do circulo
                if square(x-pos[0]) + square(y-pos[1]) <= square(radius):
                    self.add_color((x, y), color)

    def add_line(self, ix, iy, fx, fy, color, radius=0):
        x = fx - ix
        y = fy - iy
        aux = 1
        # linha horizontal
        if y == 0:
            if x > 0:
                for cont in range(ix+1, fx):
                    self.add_color((cont, iy), color)
            else:
                for cont in range(ix-1, fx, -1):
                    self.add_color((cont, iy), color)
        # linha vertical
        elif x == 0:
            if y > 0:
                for cont in range(iy+1, fy):
                    self.add_color((ix, cont), color)
            else:
                for cont in range(iy-1, fy, -1):
                    self.add_color((ix, cont), color)
        # primeiro e quarto quadrante
        elif x > 0:
            # derivada <= 1
            if x >= absolute(y):
                a = y / x
                for cont in range(ix+1, fx):
                    self.add_color((cont, int(aux*a) + iy), color)
                    aux += 1
            # derivada > 1
            elif abs(y) > x and y < 0:
                a = x / y
                for cont in range(fy+1, iy):
                    self.add_color((int(aux*a) + fx, cont), color)
                    aux += 1
            else:
                a = x / y
                for cont in range(iy+1, fy):
                    self.add_color((int(aux*a) + ix, cont), color)
                    aux += 1

        # segundo e terceiro quadrante
        else:
            # derivada <= 1
            if (x <= y and y < 0) or (absolute(x) >= y and y > 0):
                a = y / x
                for cont in range(ix-1, fx, -1):
                    self.add_color((cont, -int(aux*a) + iy), color)
                    aux += 1
            # derivada > 1
            elif absolute(x) < y and y > 0:
                a = x / y
                for cont in range(iy+1, fy):
                    self.add_color((int(aux*a) + ix, cont), color)
                    aux += 1
            else:
                a = x / y
                for cont in range(iy-1, fy, -1):
                    self.add_color((-int(aux*a) + ix, cont), color)
                    aux += 1

    def add_line_with_radius(self, ix, iy, fx, fy, color, radius):
        x = fx - ix
        y = fy - iy
        # o arredondamento faz a linha sobrar, diminuir o raio em 1
        # ajusta o erro do ponto extra que fica nas bordas do circulo completo
        radius -= 1
        hip = sqrt(square(x) + square(y))
        # quando o mouse permanece no mesmo lugar hip == 0, portanto não há linha a ser feita
        if hip == 0:
            return 
        sen = abs(x/hip)
        cos = abs(y/hip)
        # linhas que passam pela corda de seno do circulo (pela "direita")
        if (x > 0 and y <0) or (x < 0 and y > 0):
            for cont in range(-round(radius*sen), round(radius*sen)+1):
                self.add_line(ix + round(radius*cos), iy + cont, 
                              fx + round(radius*cos), fy + cont, 
                              color)
        # linhas que passam pela corda de seno do circulo (pela "esquerda")
        else:
            for cont in range(-round(radius*sen), round(radius*sen)+1):
                self.add_line(ix - round(radius*cos), iy + cont, 
                              fx - round(radius*cos), fy + cont, 
                              color)
        # linhas que passam pela corda de cosseno do circulo (por "baixo")
        for cont in range(-round(radius*cos), round(radius*cos)+1):
            self.add_line(ix + cont, iy - round(radius*sen), 
                          fx + cont, fy - round(radius*sen), 
                          color)

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
        img = self.img.crop((pos1[0], pos1[1], pos2[0]+1, pos2[1]+1))
        # name = name.replace('.png', '(cortado).png')
        img.save(self.image_name + '(cortado).png', 'PNG')


    # O motodo recursivo da funcao paint da erro por quantidade de memoria utilizada
    # o metodo nao recursivo da time out, falta resolver isso


    # # nao sei onde esta o erro, mas ele nao consegue pintar regioes muito grandes
    # def Paint(self, pos, color, base):
    #     if color != base:
    #         self.add_color(pos, color)

    #         if pos[0]-1 >= 0 and pos[1]-1 >= 0 and pos[0] <= self.img.width and pos[1] <= self.img.height :
    #             if self.img.getpixel((pos[0], pos[1]-1)) == base :
    #                 self.paint((pos[0], pos[1]-1), color, base)

    #             if self.img.getpixel((pos[0], pos[1]+1)) == base :
    #                 self.paint((pos[0], pos[1]+1), color, base)
                
    #             if self.img.getpixel((pos[0]-1, pos[1])) == base :
    #                 self.paint((pos[0]-1, pos[1]), color, base)
                
    #             if self.img.getpixel((pos[0]+1, pos[1])) == base :
    #                 self.paint((pos[0]+1, pos[1]), color, base)

    # def Paint_init(self, pos, color):
    #     base_color = self.img.getpixel(pos)
    #     new_color = (color[0], color[1], color[2], color[3])
    #     if base_color != new_color :
    #         # return
    #         self.Paint(pos, new_color, base_color)

    def Not_in_list(self, list1, item):
        try:
            # verifica se o item esta na lista e da erro se n estiver
            list1.index(item)
            # se o item esta na lista retorna false
            return False
        except:
            # se o item nao esta na lista retorna true
            return True

    def Paint_check(self, pos, base, list1):
        # verifica se a direita deve ser pintada
        if pos[0]+1 < self.img.width and self.Not_in_list(list1,(pos[0]+1, pos[1])):
            if self.img.getpixel((pos[0]+1, pos[1])) == base:
                list1.append((pos[0]+1, pos[1]))
        # verifica se a esquerda deve ser pintada
        if self.img.getpixel((pos[0]-1, pos[1])) == base and pos[0]-1 >= 0 and self.Not_in_list(list1,(pos[0]-1, pos[1])):
            list1.append((pos[0]-1, pos[1]))
        # verifica se em baixo deve ser pintdo
        if pos[1]+1 < self.img.height and self.Not_in_list(list1,(pos[0], pos[1]+1)):
            if self.img.getpixel((pos[0], pos[1]+1)) == base:
                list1.append((pos[0], pos[1]+1))
        # verifica se em cima deve ser pintado
        if self.img.getpixel((pos[0], pos[1]-1)) == base and pos[1]-1 >= 0 and self.Not_in_list(list1,(pos[0], pos[1]-1)):
            list1.append((pos[0], pos[1]-1))

    def Paint_init(self, pos, color):
        # lista de posicoes que devem ser pintadas
        to_paint = []
        cont = 0
        to_paint.append(pos)
        # cor da base pintada
        base = self.img.getpixel(pos)
        while cont < len(to_paint):
            self.add_color(to_paint[cont], color)
            self.Paint_check(to_paint[cont], base, to_paint)
            cont += 1


class Editor_screen_parameters():
    width = None
    height = None
    pix = None
    scale_on = None
    color_scale = None

# coloca um texto na tela
def Text(screen, text, color, size, width, height):
    font = pygame.font.SysFont(None, size)
    text1 = font.render(text, True, color)
    screen.blit(text1, (int(width), int(height)))

# delinea onde imagem sera cortada
def cutting_outline(screen, pos1, pos2, color):
    if pos2[0] - pos1[0] > 0 and pos2[1] - pos1[1] > 0:
        pygame.draw.rect(screen, color, [pos1[0], pos1[1], 1, (pos2[1]-pos1[1])])
        pygame.draw.rect(screen, color, [pos1[0], pos1[1], (pos2[0]-pos1[0]), 1])
        pygame.draw.rect(screen, color, [pos2[0], pos1[1], 1, (pos2[1]-pos1[1])])
        pygame.draw.rect(screen, color, [pos1[0], pos2[1], (pos2[0]-pos1[0]), 1])


if __name__ == "__main__":

    from time import sleep
    ed = Editor()
    ed.load_image("oi.png")
    sleep(2)