from .Editor_lib import *

def Inicializador_terminal():
    ed = Editor()
    param = Editor_screen_parameters()

    while True:
        op = input('deseja criar ou editar?[c/e]\n')
        if op == 'c':
            name = input('qual o nome da nova imagem?\n')
            name = name + '.png'
            w = int(input('largura: '))
            h = int(input('altura: '))
            img = Image.new('RGBA', (w, h), (255, 255, 255, 255))
            img.save(name , 'PNG')
            edit = False
        elif op == 'e':
            name = input('qual o nome da imagem?\n')
            if '.' not in name:
                name = name + '.png'
            edit = True

        try:
            ed.load_image(name)
            break
        except:
            print('\nerro\n')

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
    param.width, param.height = ed.img.size


    print('(recomendado uma proporção pixel X ajuste = 450 pixeis de altura)')
    print(f'o tamanho da imagem é:({param.width}, {param.height})')
    adjustment = input('deseja ajustar a tela?\n[m] manualmente\n[a] automaticamente\n[n] não\n')
    param.pix = 1
        
    if adjustment == 'm':
        try:
            param.pix = int(input('deseja usar qual escala?[x:1] '))
        except:
            print('\nalgo invalido foi digitado, ajustando automaticamente\n')
    elif adjustment == 'n':
        pass
    else:
        aux = 0
        while param.height*param.pix < 450:
            param.pix = int((450+aux)/param.height)
            if param.height*param.pix < 450:
                aux += 10
                if aux > 200:
                    break
            else:
                break
    
    print(f'tamanho final é: ({param.width*param.pix}, {param.height*param.pix}) param.pixeis')
    print(name)
    
    return ed, param, cache, edit