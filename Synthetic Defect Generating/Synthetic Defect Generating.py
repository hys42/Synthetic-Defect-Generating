from itertools import product
from mailbox import mboxMessage
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2 as cv
import numpy as np

from tkinter import messagebox

import os
import cv2
import numpy as np

drawing=False
mode=True

image_dim = (832,128)
def GoruntuTahminEt(img):
    return img

tempt_image=None
def mysmoting(img_patch, mask_patch, Kal):
    flitre = np.zeros(img_patch.shape)
    cv.waitKey(1)
    global tempt_image
    if tempt_image is None:
        tempt_image=np.copy(img_patch)
        return img_patch , mask_patch
    else:

        path= 'defectTemplate/asd_2_'
        cv2.circle(flitre, (flitre.shape[0] // 2, flitre.shape[1] // 2), 1, int(255), Kal)
        cv2.imwrite(path+'1.jpg', flitre)
        blur = cv2.blur(flitre, (10, 10), cv2.BORDER_DEFAULT)
        cv2.imwrite(path + '2.jpg', blur)
        blur = blur / np.max(blur)
        img_patch= tempt_image * blur + img_patch * (1 - blur)
        cv2.imwrite(path + '3.jpg', tempt_image)
        cv2.imwrite(path + '4.jpg', img_patch)
        cv2.imwrite(path + '5.jpg', img_patch)
        tempt_image=None
        blur = (blur > 0.1).astype(np.uint8)*255
        kernel = np.ones((10, 10), np.uint8)
        blur = cv2.erode(blur, kernel, iterations=1)

        mask_patch= mask_patch + blur

        cv2.imwrite(path + '6.jpg', mask_patch)

        cv2.imwrite(path + '7.jpg', blur)

        mask_patch = mask_patch.astype(np.uint8)
        cv2.imwrite(path + '8.jpg', mask_patch)

        return img_patch, mask_patch



    #
    # img2=np.copy(img)
    # for i in range(0,img.shape[0]-5,5):
    #     img2[(i+yon1)*5:(i+1)*5,:]=img[(i+1)*5:(i+2)*5,:]
    #
    # for j in range(0,img.shape[1]-5,5):
    #     img2[:,i*5:(i+1)*5]=img[:,(i+1)*5:(i+2)*5]



def GoruntuGause(image, mask, x, y, renk, patch_size,Kal):

    xbas = x - patch_size // 2
    ybas = y - patch_size // 2

    img_patch, mask_patch = mysmoting(image[ybas:ybas + patch_size, xbas:xbas + patch_size],
                                      mask[ybas:ybas + patch_size, xbas:xbas + patch_size],
                                      Kal)
    image[ybas:ybas + patch_size, xbas:xbas + patch_size] = img_patch
    mask[ybas:ybas + patch_size, xbas:xbas + patch_size] = mask_patch
    try:
        pass

    except:
        global tempt_image
        tempt_image = None
        print('Hataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        pass
    return image, mask

def GoruntuBlurHatasi(image, mask, x, y, renk, secenek, patch_size, Kal):
    image, mask =GoruntuGause(image, mask,x, y, renk,patch_size,Kal)
    return image, mask



def GoruntuPuskutmeHatasi(image, mask, x, y, renk, secenek, patch_size, Kal):
    if secenek == 21:
        image, mask =GoruntuGause(image, mask,x, y, renk,patch_size,Kal)
        return image, mask
    patch= cv.imread('defectTemplate/t.png', 0)
    p = patch.reshape(25, 20, 25)
    patch=p[:, secenek, :]
    patch = (patch > 150).astype(np.uint8)
    cv2.imshow('aaa',patch*255)
    cv.waitKey(1)
    patch = cv2.resize(patch, (patch_size,patch_size), interpolation=cv2.INTER_AREA)
    xbas = x - patch_size // 2
    ybas = y - patch_size // 2
    for i in range(patch_size):
        for j in range(0,patch_size):
            xx= xbas+ i
            yy = ybas + j
            # patch[i, j]
            if xx<0 or yy<0:
                continue
            try:
                if patch[j,i]!=1:
                    image[yy,xx]=renk
                    mask[yy,xx]=255
            except:
                pass

    return image, mask


class Paint(Frame):
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):

        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_paint()

    # Creation of init_window
    def init_paint(self):

        # changing the title of our master widget
        self.master.title("Image Synthetic Defect Generation ")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        self.create_widgets()
        # creating a menu instance
        # menu = Menu(self.master)
        # self.master.config(menu=menu)
        # # create the file object)
        # file = Menu(menu)
        # # adds a command to the menu option, calling it exit, and the
        # # command it runs on event is client_exit
        # file.add_command(label="Exit", command=self.client_exit)
        #
        # # added "file" to our menu
        # menu.add_cascade(label="File", menu=file)

    def create_widgets(self):
        # self.btn_Basla = Button(self)
        # self.btn_Basla["text"] = "Görüntü Al"
        # self.btn_Basla["command"] = self.select_image
        # self.btn_Basla.place(x=10, y=10)

        self.sifirlaKontrol=False
        self.btn_Dur = Button(self)
        self.btn_Dur["text"] = "Select File Path"
        self.btn_Dur["command"] = self.Goruntu_Dosya
        self.btn_Dur.place(x=450, y=45)

        self.btn_Dur = Button(self)
        self.btn_Dur["text"] = ">>"
        self.btn_Dur["command"] = self.ileri
        self.btn_Dur.place(x=650, y=45)

        self.btn_Dur = Button(self)
        self.btn_Dur["text"] = "<<"
        self.btn_Dur["command"] = self.geri
        self.btn_Dur.place(x=600, y=45)

        self.Kayıt_L = Label(self)
        self.Kayıt_L["text"] = "Save Path:"
        self.Kayıt_L.place(x=450, y=80)

        self.Kayıt_maske_L = Label(self)
        self.Kayıt_maske_L["text"] = "Mask Save Path:"
        self.Kayıt_maske_L.place(x=620, y=80)

        self.Kayıt_Ana_L = Label(self)
        self.Kayıt_Ana_L["text"] = "Save Path:"
        self.Kayıt_Ana_L.place(x=260, y=10)


        self.maskfilead_L = Label(self)
        self.maskfilead_L["text"] = "Mask File"
        self.maskfilead_L.place(x=10, y=5)



        self.maskfilead = Entry(self)
        self.maskfilead.place(x=70, y=5)
        self.maskfilead.insert(0, "mask")

        self.Anafilead_L = Label(self)
        self.Anafilead_L["text"] = "Main Folder"
        self.Anafilead_L.place(x=10, y=25)

        self.Anafilead = Entry(self)
        self.Anafilead.place(x=70, y=25)
        self.Anafilead.insert(0, "_defcet_4")



        self.maskValuDegeri_L = Label(self)
        self.maskValuDegeri_L["text"] = "defect pixel Value:"
        self.maskValuDegeri_L.place(x=945, y=10)

        self.maskValuDegeri = Entry(self)
        self.maskValuDegeri.place(x=1055, y=10)
        self.maskValuDegeri.insert(0, "30")


        self.maskpatchsize_L = Label(self)
        self.maskpatchsize_L["text"] = "Template Patch Size:"
        self.maskpatchsize_L.place(x=945, y=50)

        self.maskpatchsize = Entry(self)
        self.maskpatchsize.place(x=1055, y=50)
        self.maskpatchsize.insert(0, "40")
        # maskpatchsize
        #
        self.Kalınlık_L = Label(self)
        self.Kalınlık_L["text"] = "Thickness"
        self.Kalınlık_L.place(x=10, y=45)

        self.Kalınlık = Entry(self)
        self.Kalınlık.place(x=70, y=45)
        self.Kalınlık.insert(0, "5")




        # self.Barkod_L = Label(self)
        # self.Barkod_L["text"] = "Kayıt Yeri:"
        # self.Barkod_L.place(x=180, y=45)
        #
        # self.Barkod = Entry(self)
        # self.Barkod.place(x=260, y=45)
        # self.Barkod.insert(0, "./")



        self.btn_Basla = Button(self)
        self.btn_Basla["text"] = "Transpose"
        self.btn_Basla["command"] = self.Dondur
        self.btn_Basla.place(x=955, y=80)

        self.btn_Basla = Button(self)
        self.btn_Basla["text"] = "reset"
        self.btn_Basla["command"] = self.reset
        self.btn_Basla.place(x=1055, y=80)

        self.btn_Basla = Button(self)
        self.btn_Basla["text"] = "Image Save"
        self.btn_Basla["command"] = self.save_image
        self.btn_Basla.place(x=730, y=45)


        self.btn_Basla = Button(self)
        self.btn_Basla["text"] = "Take it back"
        self.btn_Basla["command"] = self.geriAl
        self.btn_Basla.place(x=730, y=10)

        var = IntVar()
        self.secenek=-1

        def sel():
            selection = "You selected the option " + str(var.get())
            self.secenek = var.get()
            print(selection)

        R1 = Radiobutton(root, text="Yarn-Pencel", variable=var, value=1,
                         command=sel)
        R1.place(x=10, y=75)

        R2 = Radiobutton(root, text="Yarn-Line", variable=var, value=2,
                         command=sel)
        R2.place(x=110, y=75)

        R3 = Radiobutton(root, text="Yarn-Rectangle", variable=var, value=3,
                         command=sel)
        R3.place(x=220, y=75)



        R4 = Radiobutton(root, text="Stains", variable=var, value=4,
                         command=sel)
        R4.place(x=150, y=101)


        R5 = Radiobutton(root, text="Color Bleeding", variable=var, value=5,
                         command=sel)

        R5.place(x=10, y=101)


        self.masksecenek_L = Label(self)
        self.masksecenek_L["text"] = "Stains Id (1-20):"
        self.masksecenek_L.place(x=250, y=103)


        self.masksecenek  = Entry(self)
        self.masksecenek.place(x=350, y=103)
        self.masksecenek.insert(0, "1")







        self.panelA = Label(self)
        self.panelA.place(x=10, y=130)

        # while the second panel will store the edge map
        self.panelB = Label(self)
        self.panelB.place(x=10, y=330)

        self.panelC = Label(self)
        self.panelC.place(x=10, y=530)


        self.panelD = Label(self)
        self.panelD.place(x=10, y=730)



        self.IschcTranspose = IntVar()
        self.chcKayit = Checkbutton(self)
        self.chcKayit.place(x=255, y=50)
        self.chcKayit["text"] = "Transpose"
        self.chcKayit["variable"] = self.IschcTranspose

        self.IschcSeriKayit = IntVar()
        self.chcSeriKayit= Checkbutton(self)
        self.chcSeriKayit.place(x=600, y=10)
        self.chcSeriKayit["text"] = "Always Save"
        self.chcSeriKayit["variable"] = self.IschcSeriKayit



        def tiklaBas(event):
            Kal = int(self.Kalınlık.get())
            x, y = event.x, event.y
            self.drawing = True
            self.ix, self.iy = x, y
            print('basss')

            # image = self.image
            self.panelDegistir()

        def motion(event):
            Kal = int(self.Kalınlık.get())
            x, y = event.x, event.y
            if self.drawing == True:
                if (self.secenek == 1):
                    cv2.circle(self.mask, (x, y), 1, int(255), Kal)
                    cv2.circle(self.image, (x, y), 1, int(self.maskValuDegeri.get()), Kal)
                elif (self.secenek == 4):

                    if int(self.masksecenek.get()) not in range(1,21):
                        self.masksecenek.delete(0, END)
                        self.masksecenek.insert(0, str(1))
                    self.image, self.mask=GoruntuPuskutmeHatasi(self.image, self.mask, x, y, int(self.maskValuDegeri.get()),
                                                                int(self.masksecenek.get()), int(self.maskpatchsize.get()), Kal)
                elif (self.secenek == 5):
                    if int(self.masksecenek.get()) != 21:
                        self.masksecenek.delete(0, END)
                        self.masksecenek.insert(0, str(21))
                    self.image, self.mask=GoruntuBlurHatasi(self.image, self.mask, x, y, int(self.maskValuDegeri.get()),
                                                                int(self.masksecenek.get()), int(self.maskpatchsize.get()), Kal)

            self.panelDegistir()


        def tiklaBırak(event):
            Kal = int(self.Kalınlık.get())
            x, y = event.x, event.y
            ix, iy=self.ix, self.iy
            self.drawing = False
            print(self.secenek)
            # print(x, y,self.image[x,y])
            print(x, y)
            if (self.secenek == 1):
                cv2.circle(self.mask, (x, y), 1, 255, Kal)
                cv2.circle(self.image, (x, y), 1, int(self.maskValuDegeri.get()), Kal)
            elif (self.secenek == 2):
                cv2.line(self.mask, (ix, iy), (x, y), 255, Kal)
                cv2.line(self.image, (ix, iy), (x, y), int(self.maskValuDegeri.get()), Kal)
            elif (self.secenek == 3):
                cv2.rectangle(self.mask, (ix, iy), (x, y), 255, -1)
                cv2.rectangle(self.image, (ix, iy), (x, y), int(self.maskValuDegeri.get()), -1)
            elif (self.secenek == 4):
                if int(self.masksecenek.get()) not in range(1,21):
                    self.masksecenek.delete(0, END)
                    self.masksecenek.insert(0, str(1))
                self.image, self.mask=GoruntuPuskutmeHatasi(self.image, self.mask, x, y, int(self.maskValuDegeri.get()),
                                                                int(self.masksecenek.get()), int(self.maskpatchsize.get()), Kal)
            elif (self.secenek == 5):
                if int(self.masksecenek.get()) != 21:
                    self.masksecenek.delete(0, END)
                    self.masksecenek.insert(0, str(Kal))
                self.image, self.mask=GoruntuBlurHatasi(self.image, self.mask, x, y, int(self.maskValuDegeri.get()),
                                                                int(self.masksecenek.get()), int(self.maskpatchsize.get()), Kal)
            ix = x
            iy = y
            print('Kaldırrrr')

            self.panelDegistir()


        self.drawing = False
        self.panelA.bind("<Button-1>", tiklaBas)
        self.panelA.bind("<ButtonRelease-1>", tiklaBırak)
        self.panelA.bind('<Motion>', motion)

        def Ana_tiklaBas(event):
            x, y = event.x, event.y
            print(x,y,'<< Bull')
        self.bind("<Button-1>", Ana_tiklaBas)

    def saveimage(self):

        self.yedek_image= np.copy(self.image)
        self.yedek_mask=np.copy(self.mask)

        path_arr = self.Goruntu_dosya.split('/')
        path_arr[-1] = path_arr[-1] + self.Anafilead.get()+'_'+self.maskfilead.get()
        seperator = '/'
        path_mask = seperator.join(path_arr)




        path_arr = self.Goruntu_dosya.split('/')
        path_arr[-1] = path_arr[-1] + self.Anafilead.get()
        seperator = '/'
        path_Ana_image = seperator.join(path_arr)


        try:
            os.mkdir(path_mask)
        except OSError as exc:
            print("ERORR")
            pass
        try:
            os.mkdir(path_Ana_image)
        except OSError as exc:
            print("ERORR")
            pass

        yedek_image = np.copy(self.image)
        yedek_mask = np.copy(self.yedek_mask)

        if self.IschcTranspose.get():
            yedek_mask = yedek_mask.transpose()
            yedek_image = yedek_image.transpose()


        cv2.imwrite(path_mask + '/' +self.mask_ad, yedek_mask)
        if True:
            cv2.imwrite(path_Ana_image + '/' +self.img_ad, yedek_image )
        else:
            print('Kaydetmiyorrr++++++---------------+-+-++\-+-+-\-++\++-+\++++++++++++++++++++++++++++++++++++++')

        # print(path_mask + '/' + self.mask_ad,'\n+++++++++++++\n',path_Ana_image + '/' + self.img_ad)

    def GoruntuDEgistir(self):

        img_ad = self.files[self.index_img]
        mask_ad_arr = img_ad.split('.')
        self.mask_ad = mask_ad_arr[0] + '_mask_.' + mask_ad_arr[1]
        self.img_ad=img_ad
        self.Kayıt_L["text"] = str(self.index_img) + '  --> ' + img_ad
        self.Kayıt_maske_L["text"] = self.mask_ad
        path_img = self.Goruntu_dosya + '/' + img_ad

        print(path_img)
        image = cv.imread(path_img, 0)
        pred = GoruntuTahminEt(image)
        # self.pred =image
        if self.IschcTranspose.get():
            image = image.transpose()


        path_arr = self.Goruntu_dosya.split('/')
        path_arr[-1] = path_arr[-1] + self.Anafilead.get()+'_'+self.maskfilead.get()
        seperator = '/'
        path_mask = seperator.join(path_arr)


        path_mask= path_mask + '/' + self.mask_ad
        print(path_mask)
        mask = cv.imread(path_mask, 0)
        print(self.sifirlaKontrol)
        if mask is None or self.sifirlaKontrol:

            mask = np.zeros(image.shape, np.uint8)
            # mask=np.copy(image)
            if self.IschcTranspose.get():
                mask = mask.transpose()


        scale_percent = (200 * 100) / image.shape[0]
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # image = cv.resize(image, dim, interpolation=cv.INTER_AREA)
        # mask = cv.resize(mask, dim, interpolation=cv.INTER_AREA)
        # pred = cv.resize(pred, dim, interpolation=cv.INTER_AREA)

        self.image = np.copy(image)
        self.mask = np.copy(mask)
        self.pred = np.copy(pred)

        self.yedek_image = np.copy(image)
        self.yedek_mask = np.copy(mask)

        self.panelDegistir()


    def Dondur(self):
        self.yedek_image= np.copy(self.image)
        self.yedek_mask=np.copy(self.mask)

    def reset(self):
        self.sifirlaKontrol=True
        mask = np.zeros(self.image.shape, np.uint8)
        # mask = np.copy(self.image)
        self.mask = np.copy(mask)
        self.yedek_mask = np.copy(mask)
        self.GoruntuDEgistir()

        self.sifirlaKontrol=False

    def  geriAl(self):
        self.image = np.copy(self.yedek_image)
        self.mask = np.copy(self.yedek_mask)

        self.panelDegistir()

    def Goruntu_Dosya(self):
        srat_path= './SimpleImage'
        path = filedialog.askdirectory(initialdir=srat_path)
        print(path)
        pathArray=path.split('/')
        self.Goruntu_dosya=path

        self.Kayıt_Ana_L["text"]=self.Goruntu_dosya


        # path = 'c:\\projects\\hc2\\'

        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.' in file:
                    files.append(file)

        self.files=files
        # for f in files:
        #     print(f)
        # print(self.files.__len__())
        self.index_img=0
        self.GoruntuDEgistir()

    def  ileri(self):
        if not(self.files.__len__()-1==self.index_img):
            if self.IschcSeriKayit.get():
                self.saveimage()

            self.index_img += 1

            self.GoruntuDEgistir()

        else:
            messagebox.showinfo("Hata", "index hatası")

    def  geri(self):

        if not(0==self.index_img):
            if self.IschcSeriKayit.get():
                self.saveimage()

            self.index_img -= 1

            self.GoruntuDEgistir()




        else:
            messagebox.showinfo("Hata", "index hatası")


    def  save_image(self):

        self.saveimage()


    def client_exit(self):
        self.camera.StopGrabbing()
        self.camera.Close()
        exit()

    def panelDegistir(self):
        image = self.image
        mask = self.mask
        pred = self.pred

        if np.max(pred) !=0:
            pred___ = pred / np.max(pred)
            image=image+pred___ * 20


            mask___ = mask / (np.max(mask))
            maskPred=pred___-mask___
            maskPred=np.abs(maskPred)*255
        else:
            maskPred=mask

        image = Image.fromarray(image)
        mask = Image.fromarray(mask)
        pred = Image.fromarray(pred)
        maskPred = Image.fromarray(maskPred)

        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)
        mask = ImageTk.PhotoImage(mask)
        pred = ImageTk.PhotoImage(pred)
        maskPred = ImageTk.PhotoImage(maskPred)

        # update the pannels
        self.panelA.configure(image=image)
        self.panelA.image = image
        self.panelB.configure(image=mask)
        self.panelB.image = mask
        self.panelC.configure(image=pred)
        self.panelC.image = pred
        self.panelD.configure(image=maskPred)
        self.panelD.image = maskPred


# root window created. Here, that would be the only window, but
# you can later have windows within windows.


root = Tk()
root.geometry("1224x600")

# creation of an instance
app = Paint(root)

root.mainloop()