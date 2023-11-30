from .Editor_lib import *
from tkinter import *
import PIL.Image

class Tela_captura:
    def __init__(self, lista, master=None) -> None:

        # retorno
        self.lista = lista
        # definicoes
        self.defalt_size = 20
        self.default_font = ("Times", "15")
        # parametros
        self.create_new_img = False
        self.adjustment_m = False
        self.adjustment_a = True
        # tela principal
        self.tela = Frame(master)
        self.tela.pack()
        # espaco para o titulo
        self.title = Frame(self.tela)
        self.title["padx"] = self.defalt_size
        self.title.pack()
        # espaco para botao de criar ou abrir imagem
        self.create = Button(self.tela)
        self.create["text"] = "abrir"
        self.create["font"] = self.default_font
        self.create["command"] = self.Create_button
        self.create.pack()
        # espaco para colocar o nome da imagem
        self.name_space = Frame(self.tela)
        self.name_space["padx"] = self.defalt_size
        self.name_space.pack()
        # espaco para os tamanhos
        self.sizes_space = Frame(self.tela)
        self.sizes_space["padx"] = self.defalt_size
        self.sizes_wspace = Frame(self.sizes_space)
        self.sizes_wspace["padx"] = self.defalt_size
        self.sizes_wspace.pack()
        self.sizes_hspace = Frame(self.sizes_space)
        self.sizes_hspace["padx"] = self.defalt_size
        self.sizes_hspace.pack()
        # espaco para os ajustes de tamanho
        self.adjustments_space = Frame(self.sizes_space)
        self.adjustments_space["padx"] = self.defalt_size
        self.adjustments_space.pack()
        # espaco para parametros de ajuste
        self.adjustments_parameters_space = Frame(self.tela)
        self.adjustments_parameters_space["padx"] = self.defalt_size
        # botao de confirmar
        self.quit = Button(self.tela)
        self.quit["text"] = "confirmar"
        self.quit["font"] = self.default_font
        self.quit["command"] = self.Confirm_button
        self.quit.pack(side=BOTTOM)

        self.title_text = Label(self.title, text="Dados da imagem")
        self.title_text["font"] = self.default_font
        self.title_text.pack(side=TOP)

        self.name_label = Label(self.name_space, text="nome:")
        self.name_label["font"] = self.default_font
        self.name_label.pack(side=LEFT)

        self.name_capture = Entry(self.name_space)
        self.name_capture["font"] = self.default_font
        self.name_capture.pack()

        self.sizes_wLabel = Label(self.sizes_wspace, text="largura:")
        self.sizes_hLabel = Label(self.sizes_hspace, text="altura:")
        self.sizes_wLabel["font"] = self.default_font
        self.sizes_wLabel.pack(side=LEFT)
        self.sizes_hLabel["font"] = self.default_font
        self.sizes_hLabel.pack(side=LEFT)

        self.wcapture = Entry(self.sizes_wspace)
        self.wcapture["font"] = self.default_font
        self.wcapture.pack()
        self.hcapture = Entry(self.sizes_hspace)
        self.hcapture["font"] = self.default_font
        self.hcapture.pack()

        self.adjustments_automatic = Button(self.adjustments_space)
        self.adjustments_automatic["text"] = "automatico"
        self.adjustments_automatic["font"] = self.default_font
        self.adjustments_automatic["bg"] = "red"
        self.adjustments_automatic["command"] = self.Automatic_button
        self.adjustments_automatic.pack(side=LEFT)
        self.adjustments_manual = Button(self.adjustments_space)
        self.adjustments_manual["text"] = "manual"
        self.adjustments_manual["font"] = self.default_font
        self.adjustments_manual["command"] = self.Manual_button
        self.adjustments_manual.pack(side=RIGHT)

        self.adjustment_label = Label(self.adjustments_parameters_space)
        self.adjustment_label["text"] = "ajuste [x:1]"
        self.adjustment_label["font"] = self.default_font
        self.adjustment_label.pack(side=LEFT)
        self.adjustment_parameter = Entry(self.adjustments_parameters_space)
        self.adjustment_parameter["font"] = self.default_font
        self.adjustment_parameter.pack()


    def Create_button(self):
        if self.create["text"] == "criar":
            self.create_new_img = False
            self.create["text"] = "abrir"
            self.sizes_space.forget()

        else:
            self.create_new_img = True
            self.create["text"] = "criar"
            self.sizes_space.pack()

    def Automatic_button(self):
        if self.adjustment_a:
            self.adjustment_a = False
            self.adjustments_automatic["bg"] = "grey95"

        else:
            self.adjustment_a = True
            self.adjustment_m = False
            self.adjustments_automatic["bg"] = "red"
            self.adjustments_manual["bg"] = "grey95"
            self.adjustments_parameters_space.forget()

    def Manual_button(self):
        if self.adjustment_m:
            self.adjustment_m = False
            self.adjustments_manual["bg"] = "grey95"
            self.adjustments_parameters_space.forget()

        else:
            self.adjustment_m = True
            self.adjustment_a = False
            self.adjustments_manual["bg"] = "red"
            self.adjustments_automatic["bg"] = "grey95"
            self.adjustments_parameters_space.pack()

    def Confirm_button(self):
        self.lista.clear()

        self.lista.append(not self.create_new_img)

        if self.name_capture.get() != "":
            self.lista.append(self.name_capture.get())
        else:
            return

        if self.wcapture.get() != "":
            self.lista.append(int(self.wcapture.get()))
        else:
            self.lista.append(1)

        if self.hcapture.get() != "":
            self.lista.append(int(self.hcapture.get()))
        else:
            self.lista.append(1)

        if self.adjustment_a:
            self.lista.append('a')
        elif self.adjustment_m:
            self.lista.append('m')
        else:
            self.lista.append('n')

        if self.adjustment_parameter.get() != "":
            self.lista.append(int(self.adjustment_parameter.get()))
        else:
            self.lista.append(1)

        self.tela.quit()


def Inicializador_GUI():
    ed = Editor()
    param = Editor_screen_parameters()
    while(True):
        lista = []
        root = Tk()
        # coloca o icone da janela
        try:
            icon = PhotoImage(file=f'icons/logo_editor.png')
            root.iconphoto(False, icon)
        except:
            pass
        root.title("Editor")
        Tela_captura(lista, master=root)
        root.mainloop()
        root.destroy()

        print(lista)
        
        edit = lista[0]
        if not edit:
            name = lista[1]
            name = name + '.png'
            w = lista[2]
            h = lista[3]
            img = PIL.Image.new('RGBA', (w, h), (255, 255, 255, 255))
            img.save(name , 'PNG')

        name = lista[1]
        if '.' not in name:
            name = name + '.png'

        # cria uma imagem do formato png caso a aberta seja jpeg
        if ed.img_format == 'JPEG':
            img = Image.open(name)
            name = name.replace('jpeg', 'png')
            print('image type switching to PNG')
            img.save (name)
            ed.reset()

        not_error = ed.load_image(name)
        if not_error:
            break
        else:
            print('error in the data obtained, restarting...')

    # cria uma imagem auxiliar
    ed.img = ed.img.convert('RGBA')
    cache = 'img_cache'
    ed.save(cache)
    param.width, param.height = ed.img.size

    # ajustes
    adjustment = lista[4]
    param.pix = 1
        
    if adjustment == 'm':
        param.pix = lista[5]
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
    
    print (name)
    return ed, param, cache, edit

if __name__ == "__main__":

    from time import sleep
    Inicializador_GUI()
    sleep(3)