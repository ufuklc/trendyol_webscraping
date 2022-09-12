import pandas as pd
from bs4 import BeautifulSoup
import time
import re
import requests




class trendyol():
    def __init__(self,programad):
        self.programad=programad
        self.dongu=True

    def program(self):
        secim=self.menu()

        if secim=="1":
            print("Arama menüsüne yönlendiriliyorsunuz...")
            time.sleep(2)
            self.arama()
        
        if secim=="2":
            self.cikis()
        
    

    def menu(self):


        def kontrol(secim):
            if re.search("[^1-2]",secim):
                raise Exception("Lütfen Geçerli Bir Seçim Yapınız... ")
            elif len(secim)!=1:
                raise Exception("Lütfen Geçerli Bir Seçim Yapınız... ")
        while True:
            try:
                secim=input("Merhaba, {} Uygulamasına Hoşgeldin.\nYapmak İstediğiniz Giriniz.\n\n[1]-Arama\n[2]-Çıkış\n\n".format(self.programad))
                kontrol(secim)
            except Exception as hata:
                print(hata)
                time.sleep(2)
            else:
                break
        return secim



    def arama(self):
        aranacak=input("Lütfen verilerini çekmek istediğiniz ürünün ismini giriniz :  ")
        sayfa=int(input("Taramak istediğiniz sayfa sayısını giriniz :  "))
        ürünisim=list()
        ürünfiyat=list()
        
        for syf in range(1,sayfa):
            url=("https://www.trendyol.com/sr?q={}&pi={}".format(aranacak,syf))
            link=requests.get(url).content
            parset=BeautifulSoup(link,'lxml')
            ürünler=parset.find("div",{"class":"prdct-cntnr-wrppr"}).find_all("div",{"class":"p-card-wrppr"})
            


            for ürün in ürünler:
                isim=ürün.find("span",{"class":"prdct-desc-cntnr-name"}).text
                ürünisim.append(isim)
            ### Ürün Fiyatları
            for ürün in ürünler:
                fiyat = ürün.find("div",{"class":"prc-box-dscntd"}).text
                ürünfiyat.append(fiyat)

        ### Veriyi Dataframe'e çevirme

        seri=dict(zip(ürünisim,ürünfiyat))

        veri=pd.DataFrame(seri.items())
        veri.rename(columns={0:"Ürün",1:"Fiyat"},inplace=True)
        

        veri.to_excel("{}.xlsx".format(aranacak))

        print("Veri Çekme İşlemi Başarıyla Tamamlandı...")

        self.menudon()


    def menudon(self):
        while True:
            x=input("Ana Menüye Dönmek İçin 4 , Çıkış Yapmak İçin 3'e Basınız ...")
            if x=="4":
                print("Ana Menüye Dönülüyor...")
                time.sleep(3)
                self.program()
                break
            elif x=="3":
                self.cikis()
                break
            else:   
                print("Lütfen Geçerli Bir Değer Giriniz...")

    def cikis(self):
        print("Programdan Çıkış Yapılıyor. Teşekkürler...")
        time.sleep(3)
        self.dongu=False
        exit()





















sistem=trendyol("Trendyol Veri Çekme")
while sistem.dongu:
    sistem.program()