from os import path
from PIL import Image, ImageEnhance
import pygame
from pygame.locals import *
import numpy as np
import cv2 as cv

# from numba import njit
from time import time
from numpy import square, absolute, sqrt

# operacao de imagem
class Editor():
    img = None
    full_img = None
    img_format = None
    img_local = None
    image_name = None
    image_cache_name = ''
    img_ext = None
    width = 0
    height = 0

    def reset(self):
        self.img = None
        self.full_img = None
        self.img_format = None
        self.img_local = None
        self.image_name = None
        self.img_ext = None
        self.width = 0
        self.height = 0

    def load_image(self, image):
        try:
            self.img = Image.open(image)
            print('imagem aberta')
            print('imagem do tipo:' + str(type(self.img)))
            self.img_format = self.img.format
            print('formato adquirido')
            self.img_local = path.dirname(path.realpath(image))
            print('caminho adquirido')
            self.image_name, self.img_ext = path.splitext(path.basename(image))
            print('extencao adquirida')
            self.width = self.img.width
            self.height = self.img.height
            print(np.array(self.img).shape)
            print('tamanho da imagem adquirida')
            print('\nloading success!\n')
            self.full_img = self.img.copy()
            return True
        except:
            print('loading error!\n')
            return False

    def save(self, name_image):
        path = self.img_local + '/' + name_image + self.img_ext
        self.img.save(path, self.img_format)


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
        # quando o mouse permanece no mesmo lugar hip == 0, portanto nao ha linha a ser feita
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
    
    def cut_img(self, pos1, pos2, zoom=False, namezoom=''):
        # print(pos1 + pos2)
        img = self.img.crop((pos1[0], pos1[1], pos2[0]+1, pos2[1]+1))
        # name = name.replace('.png', '(cortado).png')
        if not zoom:
            img.save(self.image_name + '(cortado).png', 'PNG')
        else:
            img.save(namezoom + '.png', 'PNG')

    def Paint_init(self, pos, color):
        print('função de pintr iniciada')
        # transforma a imagens em um array numpy
        initial_time = time()
        mask = np.array(self.img)
        new_img = mask.copy()
        colornp = np.array(color)

        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
        mask = Binarizated_especific(mask, mask[pos[1], pos[0]])
        mask = Hole_filling(mask, (pos[1], pos[0]))

        tam = mask.shape
        for j in range(tam[1]):
            for i in range(tam[0]):
                if mask[i, j] == 1:
                    new_img[i, j] = colornp
        print('----tempo para pintar: ' + str(time() - initial_time))
        # volta ao formato original 
        self.img = Image.fromarray(new_img)

    def Filter(self, fType):
        # transforma a imagens em um array numpy
        matrixnp = np.array(self.img)

        # aplica um filtro
        # realce monocromatico
        if fType == 'rm':
            matrixnp = Filtro_realce_monocromatico(matrixnp)
        elif fType == 'r':
            matrixnp = Filtro_realce(matrixnp)

        # volta ao formato original
        self.img = Image.fromarray(matrixnp)


class Editor_screen_parameters():
    width = None
    height = None
    pix = None
    scale_on = None
    color_scale = None

# atualiza a imagem cortada
def Image_update(editor, img_name, parameters, zoom):
    editor.save(img_name)
    # editor.full_img.paste(editor.img, (x, y))
    image = pygame.image.load(img_name + '.png')
    image = pygame.transform.scale(image, (parameters.width*parameters.pix*zoom, parameters.height*parameters.pix*zoom))
    return image

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

# filtros

def Filtro_realce_monocromatico(img):
    switch = False
    if img.shape == 3:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        switch = True

    tam = img.shape
    hist,bins = np.histogram(img.flatten(),256,[0,256])
    pdf = hist/(tam[0]*tam[1])
    pdf_padr = pdf*255

    cdf_padr = pdf_padr
    for i in range(1, 256):
        cdf_padr[i] += cdf_padr[i-1]

    for i in range(0, tam[0]):
        for j in range(0, tam[1]):
            img[i][j] = cdf_padr[img[i][j]]
    
    if switch:
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    return img

def Filtro_realce(img, YCbCr=False):
    if not YCbCr:
        img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        tam = img.shape
        hist,bins = np.histogram(img2.flatten(),256,[0,256])
        pdf = hist/(tam[0]*tam[1])
        pdf_padr = pdf*255

        cdf_padr = pdf_padr
        for i in range(1, 256):
            cdf_padr[i] += cdf_padr[i-1]

        for k in range(0, 3):
            for i in range(0, tam[0]):
                for j in range(0, tam[1]):
                    img[i][j][k] = cdf_padr[img[i][j][k]]
    else:
        img = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)
        img[:, :, 0] = Filtro_realce_monocromatico(img[:, :, 0])
        img = cv.cvtColor(img, cv.COLOR_YCR_CB2BGR)
    
    return img

# morfologia

def Circle(diameter):
    matrix = np.zeros((diameter, diameter), np.uint8)
    radius = diameter//2
    for j in range(-radius, radius+1):    
        for i in range(-radius, radius+1):
            if radius**2 >= i**2 + j**2:
                matrix[i, j] = 1
    matrix = np.roll(matrix, radius, axis=0)
    matrix = np.roll(matrix, radius, axis=1)
    return matrix

def Open(img, r=10):
    kernel = Circle(2*r)
    return cv.dilate(cv.erode(img, kernel), kernel)
def Close(img, r=10):
    kernel = Circle(2*r)
    return cv.erode(cv.dilate(img, kernel), kernel)

def Intercection(matrix1, matrix2):
    tam = matrix1.shape
    intercec = np.zeros((tam[0], tam[1]))
    return Intercec_otm(matrix1, matrix2, intercec, tam)
# @njit
def Intercec_otm(matrix1, matrix2, intercec, tam):
    for j in range(tam[1]):
        for i in range(tam[0]):
            if matrix1[i, j] == 1 and matrix2[i, j] == 1:
                intercec[i, j] = 1
    return intercec

def Complement(img):
    tam = img.shape
    for j in range(tam[1]):
        for i in range(tam[0]):
            if img[i, j] == 1:
                img[i, j] = 0
            else:
                img[i, j] = 1
    return img

def Binarizated_especific(img, color):
    tam = img.shape
    aux = np.zeros((tam[0], tam[1]))
    for j in range(tam[1]):
        for i in range(tam[0]):
            if img[i, j] == color:
                aux[i, j] = 0
            else:
                aux[i, j] = 1
    return aux

def Hole_filling(img, pos_init):
    tam = img.shape
    template = np.zeros((tam[0], tam[1]))
    template[pos_init[0], pos_init[1]] = 1
    complement = Complement(img.copy())
    kernel = Circle(3)
    aux = np.zeros((tam[0], tam[1]))
    while((template != aux).any()):
        aux = template.copy()
        template = cv.dilate(template, kernel)
        # template = Intercection(template, complement)
        template = template*complement
    return template


if __name__ == "__main__":

    from time import sleep
    ed = Editor()
    ed.load_image("oi.png")
    sleep(2)