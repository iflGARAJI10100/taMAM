#Gerekli kütüphanelerin eklenmesi

from tkinter import *
from PIL import ImageTk, Image

def hide(widget): #Kullanılmayacak elemanları gizlenmesi için onları pack_forget yapacak olan fonksiyon
    widget.pack_forget()

def Arama(): #Arama sonuçlarının eklenmesi örneği
  Label(aramaFrame,text=secilenTip.get(),font="Roboto 14").pack()
    
def SonrakiAdım():
    #Önceki ekrandan kalan elemanların gizlenmesi
    hide(anaFrame)
    hide(logo)
    hide(aramaCubugu)
    hide(aramaButonu)
    
    #Önceden eklenen gizli elemanların görünür hale getirilmesi
    ustFrame.place(relx=0,rely=0,relheight=0.05,relwidth=1)
    aramaFrame.place(relx=0.1,rely=0.07,relheight=0.85,relwidth=0.45)
    logoKucuk.pack(padx=5,side='left')
    aramaCubugu1.pack(padx=10,side='left')
    aramaButonu1.pack(padx=5,side="left")
    siralamaTip.pack(padx=5, side="left")

#Tkinter kütüphanesinden ekranın temelini oluşturacak "root" objesini oluşturma 
root = Tk()

#Arayuz içinde kullanılacak logoların görsel objelerine atanması
img = ImageTk.PhotoImage(Image.open("Arayuz\Logo 10.png"))
img1 = ImageTk.PhotoImage(Image.open("Arayuz\\taMAM.png"))

#root elemanının özelliklerini belirleme
root.state("zoomed") #Ekranı kaplaması için
root.title("taMAM - Tarayıcı Mevzuat Arama Motoru") #Başlık Ayarı
root.configure(background='white') #Arkaplan rengi

#Başlangıçta diğer elemanları kapsayacak "anaFrame" Frame widgetını oluşturma
anaFrame = Frame(root,background='white') #Özellikleri
anaFrame.place(relx=0.3,rely=0.1,relwidth=0.4,relheight=0.5) #Ekranda kaplayacağı alanı ve ekrana koyulması

#Büyük logo elemanının oluşturulması
logo = Label(anaFrame,image=img) #Özellikleri (img görsel nesnesine bağlı)
logo.pack(pady=5) #anaFrame içine koyulması ve ekrana eklenmesi

#Kullanıcının arama yapacağı metni gireceği Text objesinin oluşturulması
aramaCubugu = Text(anaFrame,height=1,font='Roboto 14',border=5) #Özellikleri
aramaCubugu.pack(padx=5,pady=10,side=TOP) #anaFrame içine koyulması ve ekrana eklenmesi

#Kullanıcının arama yaptığını belirtmesi için arama Butonu elemanının oluşturulması
aramaButonu = Button(anaFrame,text="Veritabanında Ara",font="Roboto 12",command=SonrakiAdım) #Özellikleri
aramaButonu.pack(side=TOP) #anaFrame içine koyulması ve ekrana eklenmesi

#Ekranın altındaki görsel amaçlı gri alanın oluşturulması
AltGri = Frame(root,background="#f5f5f5") #Özellikleri
AltGri.place(relx=0,rely=0.95,relwidth=1,relheight=0.05) #anaFrame içine koyulması ve ekrana eklenmesi

#Sonraki adımlarda görünecek ama şu an gizli olan elemanların oluşturulması
aramaFrame = Frame(root,bg="#f5f5f5")
ustFrame = Frame(root,bg="#f5f5f5")
logoKucuk = Label(ustFrame,image=img1)
aramaCubugu1 = Text(ustFrame,height=1,width=75,font='Roboto 14',border=5)
aramaButonu1 = Button(ustFrame,text="Veritabanında Ara",font="Roboto 12",command=Arama)

#Sıralama türünü seçmeyi sağlayacak Optionmenu elemanı için gereken kodlar
secilenTip = StringVar(root)
secilenTip.set("Sıralama Türü:")
siralamaTip = OptionMenu(ustFrame,secilenTip,
"Popüler Aramalar",
"En Son Eklenenler")

root.mainloop() #Kullanıcının girişini bekleyecek sonsuz döngüyü oluşturma
