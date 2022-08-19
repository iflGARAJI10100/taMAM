import pandas as pd
from datetime import datetime
import math

df = pd.read_csv('kanunum-nlp-doc-analysis-dataset.csv')
df.info(verbose=True)

df2 = df


def mukerrerno_doldur():
  kategorilerimiz = df["kategori"].value_counts().index.values.tolist()
  kategoridekiToplamBelgeSayisi = df["kategori"].value_counts().tolist()
  kategoridekiHataliBelgeSayisi = [0] * len(kategorilerimiz)

  # Kodda kullanılacak değişkenlerin oluşturulması
  mukerrer = 0.0
  baslangic_mukerrer = 0

  for i in range(4142):  # Sadece görev tanımında "mukerrer_no" değeri istenen kategorilerde arama yapıyoruz.
    if df['kategori'][i] in ["Komisyon Raporu", "Genelge", "Özelge"]:
      continue
    # VERİ TEMİZLEME İŞLEMLERİ
    metin = df['data_text'][i][:310].lower()

    # Daha önceki çıkarımda belirtilen durumlara göre Mükerrer No araması yapıyoruz.
    if metin.find(". mükerrer") != -1:
      baslangic_mukerrer = metin.find(". mükerrer")
      mukerrer = float(metin[baslangic_mukerrer - 1])

    elif metin.find("mükerrer") != -1:
      baslangic_mukerrer = metin.find("mükerrer")
      if metin[baslangic_mukerrer + 9] in '0123456789':
        mukerrer = 0.0
      else:
        mukerrer = 1.0
    else:
      mukerrer = 0.0

  df2.loc[i, "mukerrer_no"] = mukerrer

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def maddesay_doldur():
  satirToplami, sutunToplami = df.shape

  kategorilerimiz = df["kategori"].value_counts().index.values.tolist()
  kategoridekiToplamBelgeSayisi = df["kategori"].value_counts().tolist()
  kategoridekiHataliBelgeSayisi = [0] * len(kategorilerimiz)

  for ilgiliKayit in range(satirToplami):

    # İlk değer olarak maddeSayisi değişkenimize madde yoktur manasında 0 'SIFIR' veriyoruz.
    maddeSayisi = 0
    # YÖNTEMİMİZİ GELİŞTİRİYORUZ
    geciciMaddeSayisi = 0  # Geçici Madde 1 gibi verilen ek madde
    ekMaddeSayisi = 0  # Madde içinde 10/a gibi verilen ek madde
    ekMaddeSayisi2 = 0  # Ek Madde 1 gibi verilen ek madde
    # İlk maddenin başladığı yerden itibaren belirli aralıklarla MADDE SAYMAYA başlıyoruz!
    ilkMaddeninBasladigiYer = df['data_text'][ilgiliKayit].find('Madde 1')
    if ilkMaddeninBasladigiYer == -1:
      continue
    verininBuyuklugu = len(df['data_text'][ilgiliKayit])

    # Aramaya baslayacağımız yeri belirliyoruz.
    aramaYapilacakYerinBasi = ilkMaddeninBasladigiYer

    while (aramaYapilacakYerinBasi < verininBuyuklugu):
      bulunanSayi = ''
      alinanKesit = df['data_text'][ilgiliKayit][aramaYapilacakYerinBasi:]
      maddeninBaslayabilecegiYer = alinanKesit.find('Madde')
      tireninBaslayabilecegiYer = maddeninBaslayabilecegiYer + alinanKesit[maddeninBaslayabilecegiYer:].find('–')
      if (tireninBaslayabilecegiYer - maddeninBaslayabilecegiYer) <= 10:
        maddeninBaslayabilecegiYer += 5
        while maddeninBaslayabilecegiYer < tireninBaslayabilecegiYer:
          maddeninBaslayabilecegiYer += 1
          bulunanSayiyiOlusturacakParca = alinanKesit[maddeninBaslayabilecegiYer]
          if bulunanSayiyiOlusturacakParca in '0123456789':
            bulunanSayi += bulunanSayiyiOlusturacakParca
          else:
            break
        if bulunanSayi != '':
          if (int(bulunanSayi) <= (maddeSayisi + 2)) and (int(bulunanSayi) >= (maddeSayisi - 2)):
            maddeSayisi += 1
          elif int(bulunanSayi) < geciciMaddeSayisi + 2:
            geciciMaddeSayisi += 1
          elif int(bulunanSayi) < ekMaddeSayisi2 + 2:
            ekMaddeSayisi2 += 1
      else:
        ekMaddeninYeri = maddeninBaslayabilecegiYer + alinanKesit[maddeninBaslayabilecegiYer:].find('/')
        if (ekMaddeninYeri <= (tireninBaslayabilecegiYer - 2)) and (
          (tireninBaslayabilecegiYer - maddeninBaslayabilecegiYer) <= 12):
          ekMaddeSayisi += 1
      aramaYapilacakYerinBasi += maddeninBaslayabilecegiYer + 5
    maddeSayisi += (geciciMaddeSayisi + ekMaddeSayisi + ekMaddeSayisi2)

    df2.loc[ilgiliKayit, "madde_sayisi"] = maddeSayisi


def translate(x):
  aylar = ["ocak", "şubat", "mart", "nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım",
           "aralık"]
  months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December"]

  x = x.split(' ')
  Index = aylar.index(x[1])
  x[1] = months[Index]
  return x[0] + ' ' + x[1] + ' ' + x[2]


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def metinMevzuatTarihi(exmetin, countTarih):
  # exmetin = exmetin.replace('','')
  exmetin = exmetin.replace('GENELGE\n\n\n2018/1 \n\nKredilerin Sınıflandırılması',
                            'Tarih 02.03.2018\nGENELGE\n\n\n2018/1 \n\nKredilerin Sınıflandırılması')
  exmetin = exmetin.replace("3 0 MaYIS 2ÖÎ2", "30 Mayıs 2012")
  exmetin = exmetin.replace("26/ 06/ 2006", "\nTarih 16/06/2006")
  exmetin = exmetin.replace("KONU : ihale Konusu işlerden Kaynaklanan 06/12/2005",
                            "KONU : ihale Konusu işlerden Kaynaklanan Tarih 06/12/2005")
  exmetin = exmetin.replace('SAYI : B.07.0.GEL.0.60/6012-1430', 'SAYI : B.07.0.GEL.0.60/6012-1430\nTarih 06/06/2007')
  exmetin = exmetin.replace('Tarih 06/02/2006\nSayı B.07.1.GİB.0.36/3676\nKapsam',
                            'Tarih 02/06/2006\nSayı B.07.1.GİB.0.36/3676\nKapsam')
  exmetin = exmetin.replace('Tarih 17/04/1995\nSayı B.07.0.GEL.0.44/4412-1-20248',
                            'Tarih 17/04/2005\nSayı B.07.0.GEL.0.44/4412-1-20248')
  exmetin = exmetin.replace('Tarih 12/09/2002\nSayı B.07.0.GEL.0.38/3802- 57/037774',
                            'Tarih 19/09/2002\nSayı B.07.0.GEL.0.38/3802- 57/037774')
  exmetin = exmetin.replace('Sosyal Sigortalar Genel Müdürlüğü\n\nSayı : B.13.2.SGK.0.10.03.00-',
                            'Sosyal Sigortalar Genel Müdürlüğü\n\nSayı : B.13.2.SGK.0.10.03.00- Tarih')
  exmetin = exmetin.replace('Sosyal Sigortalar Genel Müdürlüğü\n\nSayı :B.13.2.SGK.0.10.06.00-010.06.01/299 6/5/2010',
                            'Sosyal Sigortalar Genel Müdürlüğü\n\nSayı :B.13.2.SGK.0.10.06.00-010.06.01/299 Tarih 06/05/2010')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.03.00-863', 'Sayı : B.13.2.SGK.0.10.03.00-863 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.5.01.08.00/31- 45 ', 'Sayı : B.13.2.SGK.5.01.08.00/31- 45  Tarih ')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.03.00-13 ', 'Sayı : B.13.2.SGK.0.10.03.00-13 Tarih ')
  exmetin = exmetin.replace('Konu:AraştırmaveGeliştirmeFaaliyetlerininDesteklenmesi\n\n25.09.2008',
                            'Konu:AraştırmaveGeliştirmeFaaliyetlerininDesteklenmesi\n\nTarih 29.09.2008')
  exmetin = exmetin.replace('Sayı : B.13.2.SSK.5.01.07.00-XXX-621994', 'Sayı : B.13.2.SSK.5.01.07.00-XXX-621994 Tarih')
  exmetin = exmetin.replace('Sayı: Bl AŞ-2-GDD-O 1 0.06.02 -1054', 'Sayı: Bl AŞ-2-GDD-O 1 0.06.02 -1054 Tarih')
  exmetin = exmetin.replace('Sayı : BÎAŞ-30-GDD-010.06.02- 26 14.12.2014',
                            'Sayı : BÎAŞ-30-GDD-010.06.02- 26 Tarih 14.02.2014')
  exmetin = exmetin.replace('Sayı :BİAŞ-10-GDD-010.06.02-152', 'Sayı :BİAŞ-10-GDD-010.06.02-152 Tarih')
  exmetin = exmetin.replace('Sayı :BİAŞ-10-GDD-010.06.02-153', 'Sayı :BİAŞ-10-GDD-010.06.02-153 Tarih')
  exmetin = exmetin.replace('Sayı : BİAŞ-2-GDD-010.06.02 -154', 'Sayı : BİAŞ-2-GDD-010.06.02 -154 Tarih')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1367 Sayılı',
                            'Tarih 09.06.1962\nTapu ve Kadastro Genel Müdürlüğü, 1367 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1390 Sayılı',
                            'Tarih 07.07.1965\nTapu ve Kadastro Genel Müdürlüğü, 1390 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1426 Sayılı',
                            'Tarih 26.07.1973\nTapu ve Kadastro Genel Müdürlüğü, 1426 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1467 Sayılı',
                            'Tarih 09.05.1984\nTapu ve Kadastro Genel Müdürlüğü, 1467 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1473 Sayılı',
                            'Tarih 08.01.1985\nTapu ve Kadastro Genel Müdürlüğü, 1473 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1476 Sayılı',
                            'Tarih 09.05.1985\nTapu ve Kadastro Genel Müdürlüğü, 1476 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1477 Sayılı',
                            'Tarih 07.11.1985\nTapu ve Kadastro Genel Müdürlüğü, 1477 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1481 Sayılı',
                            'Tarih 18.06.1986\nTapu ve Kadastro Genel Müdürlüğü, 1481 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1485 Sayılı',
                            'Tarih 18.04.1988\nTapu ve Kadastro Genel Müdürlüğü, 1485 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1491 Sayılı',
                            'Tarih 17.11.1988\nTapu ve Kadastro Genel Müdürlüğü, 1491 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1509 Sayılı',
                            'Tarih 01.08.1991\nTapu ve Kadastro Genel Müdürlüğü, 1509 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1513 Sayılı',
                            'Tarih 14.04.1992\nTapu ve Kadastro Genel Müdürlüğü, 1513 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1993/4 Sayılı',
                            'Tarih 01.08.1993\nTapu ve Kadastro Genel Müdürlüğü, 1993/4 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1994/13 Sayılı',
                            'Tarih 01.09.1994\nTapu ve Kadastro Genel Müdürlüğü, 1994/13 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü,1995/1 Sayılı',
                            'Tarih 10.02.1995\nTapu ve Kadastro Genel Müdürlüğü,1995/1 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1995/6 Sayılı',
                            'Tarih 15.04.1995\nTapu ve Kadastro Genel Müdürlüğü, 1995/6 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1995/13 Sayılı',
                            'Tarih 08.07.1995\nTapu ve Kadastro Genel Müdürlüğü, 1995/13 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü,1997/12 Sayılı',
                            'Tarih 03.10.1997\nTapu ve Kadastro Genel Müdürlüğü,1997/12 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 1998/12 Sayılı',
                            'Tarih 29.07.1998\nTapu ve Kadastro Genel Müdürlüğü, 1998/12 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2000/3 Sayılı',
                            'Tarih 28.03.2000\nTapu ve Kadastro Genel Müdürlüğü, 2000/3 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2000/9 Sayılı',
                            'Tarih 18.07.2000\nTapu ve Kadastro Genel Müdürlüğü, 2000/9 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2001/13 Sayılı',
                            'Tarih 01.06.2001\nTapu ve Kadastro Genel Müdürlüğü, 2001/13 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2001/9 Sayılı',
                            'Tarih 03.08.2001\nTapu ve Kadastro Genel Müdürlüğü, 2001/9 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2001/10 Sayılı',
                            'Tarih 03.08.2001\nTapu ve Kadastro Genel Müdürlüğü, 2001/10 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2001/14 Sayılı',
                            'Tarih 22.08.2001\nTapu ve Kadastro Genel Müdürlüğü, 2001/14 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2001/16 Sayılı',
                            'Tarih 15.09.2001\nTapu ve Kadastro Genel Müdürlüğü, 2001/16 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2002/12 Sayılı',
                            'Tarih 20.12.2002\nTapu ve Kadastro Genel Müdürlüğü, 2002/12 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2003/1 Sayılı',
                            'Tarih 13.01.2003\nTapu ve Kadastro Genel Müdürlüğü, 2003/1 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2003/4 Sayılı',
                            'Tarih 10.04.2003\nTapu ve Kadastro Genel Müdürlüğü, 2003/4 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü, 2003/7 Sayılı',
                            'Tarih 21.04.2003\nTapu ve Kadastro Genel Müdürlüğü, 2003/7 Sayılı')
  exmetin = exmetin.replace('Tapu ve Kadastro Genel Müdürlüğü,2003/15 Sayılı',
                            'Tarih 19.12.2003\nTapu ve Kadastro Genel Müdürlüğü,2003/15 Sayılı')
  exmetin = exmetin.replace('Sayi : B.09.1.TKG0100001-073/ 28/Eylül/2004',
                            'Sayi : B.09.1.TKG0100001-073/ Tarih 28/09/2004')
  exmetin = exmetin.replace('KONU: Mahkeme Bilirkisileri.', 'KONU: Mahkeme Bilirkisileri. Tarih')
  exmetin = exmetin.replace('SAYI: B.09.1.TKG.0.71.00.06Sendika/ 12867',
                            'SAYI: B.09.1.TKG.0.71.00.06Sendika/ 12867 Tarih')
  exmetin = exmetin.replace('Sayı :B.09.1.TKG0100001-073/', 'Sayı :B.09.1.TKG0100001-073/ Tarih')
  exmetin = exmetin.replace('Sayı : B.09.1TKG061-010.06/', 'Sayı : B.09.1TKG061-010.06/ Tarih')
  exmetin = exmetin.replace('Sayı : B.09.1.TKG0100001-073/ 23/02/2006',
                            'Sayı : B.09.1.TKG0100001-073/ Tarih 26/02/2006')
  exmetin = exmetin.replace('Sayı : B.09.1.TKG0100001- 073/', 'Sayı : B.09.1.TKG0100001- 073/ Tarih 24.02.2006')
  exmetin = exmetin.replace('Sayı: B.09.1.TKG.0.65.00.01/ 08/05/2006', 'Sayı: B.09.1.TKG.0.65.00.01/ Tarih 10/05/2006')
  exmetin = exmetin.replace('Sayı :B.09.1TKGO61-010-06/ 30/ 06/ 2006', 'Sayı :B.09.1TKGO61-010-06/ Tarih 30/06/2006')
  exmetin = exmetin.replace('Sayı : B. 09. 1. TKG0100001-/073-', 'Sayı : B. 09. 1. TKG0100001-/073- Tarih 29.01.2008')
  exmetin = exmetin.replace('Sayı :B.09.1.TKG0100001- 073/ 29/05/2008 ',
                            'Sayı :B.09.1.TKG0100001- 073/ Tarih 30/05/2008')
  exmetin = exmetin.replace('Sayı : B.09.1.TKG.061-010-06/ 17 /06/2008',
                            'Sayı : B.09.1.TKG.061-010-06/ Tarih 24/06/2008')
  exmetin = exmetin.replace('Sayı :B.09.1.TKG.061-010-06/ 30/10/2008', 'Sayı :B.09.1.TKG.061-010-06/ Tarih 30/10/2008')
  exmetin = exmetin.replace('Sayı :B.09.1.TKG0100001-073 12.11.2008', 'Sayı :B.09.1.TKG0100001-073 Tarih 12.11.2008')
  exmetin = exmetin.replace('Sayı : B.09.1.TKG0100001-073/', 'Sayı : B.09.1.TKG0100001-073/ Tarih')
  exmetin = exmetin.replace('Sayı : B.09.1.TKG0100001- 073/ Tarih 24.02.2006 03/Ağustos/2009',
                            'Sayı : B.09.1.TKG0100001- 073/ Tarih 03/08/2009')
  exmetin = exmetin.replace('Sayı : B.09.1TKG061-010-06/', 'Sayı : B.09.1TKG061-010-06/ Tarih 25.02.2010')
  exmetin = exmetin.replace('Sayı : B.09.1.TKG0100001- 073/ Tarih 24.02.2006 1699 05/04/2010',
                            'Sayı : B.09.1.TKG0100001- 073/ Tarih 05/04/2010')
  exmetin = exmetin.replace('Sayı : B.09.1.TKG0100001-073/ Tarih Tarih 26/02/2006',
                            'Sayı : B.09.1.TKG0100001-073/ Tarih 26/02/2006')
  exmetin = exmetin.replace('Sayı : B.09.1.TKG0100001- 073/ Tarih 24.02.2006 15/06/2010',
                            'Sayı : B.09.1.TKG0100001- 073/ Tarih 15/06/2010')
  exmetin = exmetin.replace('Konu : Kurum alacaklarının 7020 sayılı\n\n07/06/2017',
                            'Konu : Kurum alacaklarının 7020 sayılı\n\nTarih 07/06/2017')
  exmetin = exmetin.replace('Sayı : 41481264/ 317 ', 'Sayı : 41481264/ 317 Tarih ')
  exmetin = exmetin.replace('Sayı : 41481264-207.02-E. 1907457', 'Sayı : 41481264-207.02-E. 1907457 Tarih')
  exmetin = exmetin.replace('Sayı : 63665751-100-E. 1891946', 'Sayı : 63665751-100-E. 1891946 Tarih')
  exmetin = exmetin.replace('Sayı : 35837838/226', 'Sayı : 35837838/226 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.02.05.00/X-198', 'Sayı : B.13.2.SGK.0.02.05.00/X-198 Tarih')
  exmetin = exmetin.replace('Sayı : 41481264/ 174 1/3/2017', 'Sayı : 41481264/ 174 Tarih 01/03/2017')
  exmetin = exmetin.replace('Sayı : 24010506-010.06-E. 1105696', 'Sayı : 24010506-010.06-E. 1105696 Tarih')
  exmetin = exmetin.replace('32945953-010.06.01-E. 1046330', '32945953-010.06.01-E. 1046330 Tarih')
  exmetin = exmetin.replace('Sayı : 89075644-202.99-E.695085', 'Sayı : 89075644-202.99-E.695085 Tarih')
  exmetin = exmetin.replace('Sayı : 65003657/909', 'Sayı : 65003657/909 Tarih')
  exmetin = exmetin.replace('Sayı : 7204494-659-E.6357250', 'Sayı : 7204494-659-E.6357250 Tarih')
  exmetin = exmetin.replace('Sayı : 93180601 -747 18 Ekim 2016', 'Sayı : 93180601 -747 Tarih 18/10/2016')
  exmetin = exmetin.replace('Sayı : 47757447-20699-E. 5265648', 'Sayı : 47757447-20699-E. 5265648 Tarih')
  exmetin = exmetin.replace('İçindekiler\n\nKISA VADELİ SİGORTA KOLLARI İŞLEMLERİ',
                            'Tarih 29.09.2016\nİçindekiler\n\nKISA VADELİ SİGORTA KOLLARI İŞLEMLERİ')
  exmetin = exmetin.replace('Sayı : 84228040/642 1/9/2016', 'Sayı : 84228040/642 Tarih 01/09/2016')
  exmetin = exmetin.replace('Sayı : 24010506-613', 'Sayı : 24010506-613 Tarih')
  exmetin = exmetin.replace('Sayı : 72044944/6590735/13272/4301209', 'Sayı : 72044944/6590735/13272/4301209 Tarih')
  exmetin = exmetin.replace('Sayı : 72044944/6590735000000/13205/3934251',
                            'Sayı : 72044944/6590735000000/13205/3934251 Tarih')
  exmetin = exmetin.replace('Sayı : 87838906/309/<4^ *1', 'Sayı : 87838906/309/<4^ *1 Tarih 23.06.2016')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.03.27/GSS-34 17/1/2012',
                            'Sayı : B.13.2.SGK.0.10.03.27/GSS-34 Tarih 02/06/2016')
  exmetin = exmetin.replace('Sayı : 82200845/01006/6654040', 'Sayı : 82200845/01006/6654040 Tarih')
  exmetin = exmetin.replace('Sayı : 56766929 -113/ O -/?./0f2O15',
                            'Sayı : 56766929 -113/ O -/?./0f2O15 Tarih 17.09.2015')
  exmetin = exmetin.replace('Sayı : 90974675/601040201/3731223', 'Sayı : 90974675/601040201/3731223 Tarih')
  exmetin = exmetin.replace('Sayı : /347 03 TEMMUZ 2015', 'Sayı : /347 Tarih 03.07.2015')
  exmetin = exmetin.replace('Sayı : 32995964- MEV/031 -298', 'Sayı : 32995964- MEV/031 -298 Tarih')
  exmetin = exmetin.replace('Sayı : 71582837/20609-031/287', 'Sayı : 71582837/20609-031/287 Tarih')
  exmetin = exmetin.replace('Sayı : 63665751 - /Ü» <#./<#/2015', 'Sayı : 63665751 - /Ü» <#./<#/2015 Tarih 08.04.2015')
  exmetin = exmetin.replace('Sayı : 90974675/01006/1832642', 'Sayı : 90974675/01006/1832642 Tarih')
  exmetin = exmetin.replace('Sayı : 70809318.010.06.02/ Uf ^ Ol/ti/2015',
                            'Sayı : 70809318.010.06.02/ Uf ^ Ol/ti/2015 Tarih 02.03.2015')
  exmetin = exmetin.replace('Sayı : 70809318.010.06.02/38 13 /01/2015', 'Sayı : 70809318.010.06.02/38 Tarih 13/01/2015')
  exmetin = exmetin.replace('Sayı : 64399925/031- °5.lJLt.2015', 'Sayı : 64399925/031- °5.lJLt.2015 Tarih 05.01.2015')
  exmetin = exmetin.replace('Sayı : 72044944/10 L', 'Sayı : 72044944/10 L Tarih 30.10.2014')
  exmetin = exmetin.replace('Sayı : 70809318.010.06.02/ J?/? Z*j l°Jl2014',
                            'Sayı : 70809318.010.06.02/ J?/? Z*j l°Jl2014 Tarih 29.09.2014')
  exmetin = exmetin.replace('Sayı : 70809318.010.06.02/ £ _26| ££/.?*/2014',
                            'Sayı : 70809318.010.06.02/ £ _26| ££/.?*/2014 Tarih 25.07.2014')
  exmetin = exmetin.replace('Sayı : 70809318.010.06.02/588', 'Sayı : 70809318.010.06.02/588 Tarih')
  exmetin = exmetin.replace('Konu: MOSİP e-İmza Kullanımı\n\n29/04/2014',
                            'Konu: MOSİP e-İmza Kullanımı\nTarih 29/04/2014')
  exmetin = exmetin.replace('Sayı : 70809318.010.06.02/ 590 2% fcfylOlA',
                            'Sayı : 70809318.010.06.02/ 590 2% fcfylOlA Tarih 28.04.2014')
  exmetin = exmetin.replace('Sayı : 28735784/333', 'Sayı : 28735784/333 Tarih')
  exmetin = exmetin.replace('Strateji Geliştirme Başkanlığı \nStratejik Yönetim Daire Başkanlığı\n\n04/02/2014',
                            'Strateji Geliştirme Başkanlığı \nStratejik Yönetim Daire Başkanlığı\nTarih 04/02/2014')
  exmetin = exmetin.replace('Sayı : 32995964/ 1340 \nKonu : 2011 - 13 Sayılı Genelge\n\n10/12/2013',
                            'Sayı : 32995964/ 1340 \nKonu : 2011 - 13 Sayılı Genelge\nTarih 10/12/2013')
  exmetin = exmetin.replace('Sayı : 74955854/1255', 'Sayı : 74955854/1255 Tarih')
  exmetin = exmetin.replace('Sayı : 25029274-1093/46/285-', 'Sayı : 25029274-1093/46/285- Tarih 09.10.2013')
  exmetin = exmetin.replace('Sayı : 82200845/788', 'Sayı : 82200845/788 Tarih')
  exmetin = exmetin.replace('Sayı : 71266071.206.05.12/ 115-733', 'Sayı : 71266071.206.05.12/ 115-733 Tarih')
  exmetin = exmetin.replace('Sayı : 70809318.0lO.O6.O2/jfcj J2 12 -1*',
                            'Sayı : 70809318.0lO.O6.O2/jfcj J2 12 -1* Tarih 28.03.2013')
  exmetin = exmetin.replace('Sayı :B.13.2.SGK.0.10.03.01/01 /1228 26 KASIM 2012',
                            'Sayı :B.13.2.SGK.0.10.03.01/01 /1228 Tarih 26.11.2012')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK. 0.02.05.00/X-1093.37.283/820',
                            'Sayı : B.13.2.SGK. 0.02.05.00/X-1093.37.283/820 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.65.04.02/ 5', 'Sayı : B.13.2.SGK.0.65.04.02/ 5 Tarih 13.07.2012')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.07.01/-031/ 675', 'Sayı : B.13.2.SGK.0.10.07.01/-031/ 675 Tarih')
  exmetin = exmetin.replace('Sayı : B. 13.2.SGK..0.61.00.00/6590316/260673/Sîi.',
                            'Sayı : B. 13.2.SGK..0.61.00.00/6590316/260673/Sîi. Tarih')
  exmetin = exmetin.replace(
    'Sayı : B.13.2.SGK.0.010.06-010.06.02/930 \nKonu: Gayrimenkul değer tespitleri\n\n02/12/2011',
    'Sayı : B.13.2.SGK.0.010.06-010.06.02/930 \nKonu: Gayrimenkul değer tespitleri\nTarih 02/12/2011')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.01.00/ 467', 'Sayı : B.13.2.SGK.0.10.01.00/ 467 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.71.00.11/392', 'Sayı : B.13.2.SGK.0.71.00.11/392 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.03.27/GSS. TSC.', 'Sayı : B.13.2.SGK.0.10.03.27/GSS. TSC. Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.02.02/ 173 24 MART 2011',
                            'Sayı : B.13.2.SGK.0.10.02.02/ 173 Tarih 24.03.2011')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK..0.65.01.07/)6? /.J/.?./2011',
                            'Sayı : B.13.2.SGK..0.65.01.07/)6? /.J/.?./2011 Tarih 18.03.2011')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.65.03.04/38', 'Sayı : B.13.2.SGK.0.65.03.04/38 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.03.00/73-031-72 4/2/2011',
                            'Sayı : B.13.2.SGK.0.10.03.00/73-031-72 Tarih 04/02/2011')
  exmetin = exmetin.replace('Sayı :B.13.2.SGK.0.0.10.07.01/01-37', 'Sayı :B.13.2.SGK.0.0.10.07.01/01-37 Tarih')
  exmetin = exmetin.replace(
    'Sayı : B.13.2.SGK.0.0.10.07.01/01-031/ 709 \nKonu : Almanya’daki Çocuk Yetiştirme Süreleri\n\n08/12/2010',
    'Sayı : B.13.2.SGK.0.0.10.07.01/01-031/ 709 \nKonu : Almanya’daki Çocuk Yetiştirme Süreleri\nTarih 08/12/2010')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.61.00.00/', 'Sayı : B.13.2.SGK.0.61.00.00/ Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.65.01.00/424-10710963',
                            'Sayı : B.13.2.SGK.0.65.01.00/424-10710963 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.65.00.Û0/ 73', 'Sayı : B.13.2.SGK.0.65.00.Û0/ 73 Tarih 28.01.2010')
  exmetin = exmetin.replace('Sayı :B.13.2.SGK.0.65.01.00/996', 'Sayı :B.13.2.SGK.0.65.01.00/996 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.03.00-196\nKonu : Sigortalılık İşlemleri.\n\n05 MART 2009',
                            'Sayı : B.13.2.SGK.0.10.03.00-196\nKonu : Sigortalılık İşlemleri.\nTarih 05.03.2009')
  exmetin = exmetin.replace('Sayı: B.13.2.SGK.0.65.02.00/154 \nKonu: AB ve Yurtdışı İlişkiler\n\n19 ŞUBAT 2009',
                            'Sayı: B.13.2.SGK.0.65.02.00/154 \nKonu: AB ve Yurtdışı İlişkiler\nTarih 19.02.2009')
  exmetin = exmetin.replace('Sayı : B.13.2.SSK.5.01.08.00/VIII-031-727934 30 Ekim 2008',
                            'Sayı : B.13.2.SSK.5.01.08.00/VIII-031-727934 Tarih 30.10.2008')
  exmetin = exmetin.replace('Sayı : B.13.2.SSK.5.01.07.00-XXX- 683755',
                            'Sayı : B.13.2.SSK.5.01.07.00-XXX- 683755 Tarih')
  exmetin = exmetin.replace('Sayı : B. 13.1.SGK.0.08.902.04.00/143605',
                            'Sayı : B. 13.1.SGK.0.08.902.04.00/143605 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.1.SGK.\nKonu : Rehberlik ve Teftiş Başkanlığına Yetki Devri\n\n04/04/2008',
                            'Sayı : B.13.1.SGK.\nKonu : Rehberlik ve Teftiş Başkanlığına Yetki Devri\n Tarih 04/04/2008')
  exmetin = exmetin.replace('Sayı : 41481264-207.02-E.3617625', 'Sayı : 41481264-207.02-E.3617625 Tarih')
  exmetin = exmetin.replace('Sayı : 41481264/ 5/1/2016', 'Sayı : 41481264/ Tarih 05/01/2016')
  exmetin = exmetin.replace('Sayı : 41481264 -196 8/4/2015', 'Sayı : 41481264 -196 Tarih 08/04/2015')
  exmetin = exmetin.replace('Sayı : 64399925/031-', 'Sayı : 64399925/031- Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.04.00/73-031/149', 'Sayı : B.13.2.SGK.0.10.04.00/73-031/149 Tarih')
  exmetin = exmetin.replace(
    'Sayı : B.13.2.SGK.0.10.04.00/73-031-790 \nKonu : 4447 sayılı Kanunun geçici 9 uncu maddesinde öngörülen \n\nişveren hissesi sigorta primi teşviki\n\n11.09.2009',
    'Sayı : B.13.2.SGK.0.10.04.00/73-031-790 \nKonu : 4447 sayılı Kanunun geçici 9 uncu maddesinde öngörülen \n\nişveren hissesi sigorta primi teşviki\nTarih 11.09.2009')
  exmetin = exmetin.replace('Sayı : B. 13.2.SGK.5.01.08.00/73-031-622',
                            'Sayı : B. 13.2.SGK.5.01.08.00/73-031-622 Tarih')
  exmetin = exmetin.replace('Sayı : 64399925/031- Tarih °5.lJLt.2015 Tarih 05.01.2015',
                            'Sayı : 64399925/031- Tarih 05.01.2015')
  exmetin = exmetin.replace('Sayı : B.13.2.SSK.5.01.07.00-XXX- 683755 Tarih 13/10/2008',
                            'Sayı : B.13.2.SSK.5.01.07.00-XXX- 683755 Tarih 15/10/2008')
  exmetin = exmetin.replace(
    'Sayı : B.13.2.SGK.5.01.08.00/31-327 \nKonu : 506 sayılı Kanunun geçici 20 nci maddesine tabi \n\nsandıklara ilişkin teşvik uygulamaları\n\n14.4.2009',
    'Sayı : B.13.2.SGK.5.01.08.00/31-327 \nKonu : 506 sayılı Kanunun geçici 20 nci maddesine tabi \n\nsandıklara ilişkin teşvik uygulamaları\nTarih 14.04.2009')
  exmetin = exmetin.replace(
    'Sayı : B.13.2.SGK.5.01.08.00/73-031-252\nKonu : 18-29 yaş aralığında olan erkek ve 18 yaşından büyük kadın\n\nsigortalılardan yeni işe alınanlara ilişkin işveren hissesi sigorta prim teşviki.\n\n25.03.2009',
    'Sayı : B.13.2.SGK.5.01.08.00/73-031-252\nKonu : 18-29 yaş aralığında olan erkek ve 18 yaşından büyük kadın\n\nsigortalılardan yeni işe alınanlara ilişkin işveren hissesi sigorta prim teşviki.\nTarih 25.03.2009')
  exmetin = exmetin.replace(
    'Sayı : B.13.2.SSK.5.01.08.00/73-031- 114\nKonu : Araştırma ve Geliştirme Faaliyetlerinin Desteklenmesi\n\n6.2.2009',
    'Sayı : B.13.2.SSK.5.01.08.00/73-031- 114\nKonu : Araştırma ve Geliştirme Faaliyetlerinin Desteklenmesi\nTarih 06.02.2009')
  exmetin = exmetin.replace('Sayı :B.13.2.SGK.5.01.08.00/31-46 16.1.2009',
                            'Sayı :B.13.2.SGK.5.01.08.00/31-46 Tarih 16.01.2009')
  exmetin = exmetin.replace('Sayı : B.13.2.SSK.5.01.08.00/VIII-031- 744137',
                            'Sayı : B.13.2.SSK.5.01.08.00/VIII-031- 744137 Tarih')
  exmetin = exmetin.replace(
    'Sayı : B.13.2.SSK.5.01.08.00/ 73-0310- 575886 \nKonu : Özürlü sigortalıların istihdamına ilişkin \n\nişveren hissesi prim teşviki\n\n19/8/2008',
    'Sayı : B.13.2.SSK.5.01.08.00/ 73-0310- 575886 \nKonu : Özürlü sigortalıların istihdamına ilişkin \n\nişveren hissesi prim teşviki\nTarih 19/8/2008')
  exmetin = exmetin.replace('Sayı : B.13.2. SSK.5.01.08.00/V111-031 -702103',
                            'Sayı : B.13.2. SSK.5.01.08.00/V111-031 -702103 Tarih')
  exmetin = exmetin.replace('SAYI : B. 13.2.SSK.5.01.08.00/VI1-031/415625',
                            'SAYI : B. 13.2.SSK.5.01.08.00/VI1-031/415625 Tarih')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.10.03.00- Tarih\nKonu : İsteğe Bağlı Sigorta İşlemleri. 20/10/2010',
                            'Sayı : B.13.2.SGK.0.10.03.00- Tarih 25.08.2017\nKonu : İsteğe Bağlı Sigorta İşlemleri. 20/10/2010')
  exmetin = exmetin.replace('Sayı :B.13.2.SGK.0.10.03.00/73-031-72 4/2/2011',
                            'Sayı :B.13.2.SGK.0.10.03.00/73-031-72 Tarih 04/02/2011')
  exmetin = exmetin.replace('GENEL SAĞLIK SİGORTASI TESCİL VE PRİM DAİRE BAŞKANLIĞI\n\nGENELGE\n2019/17',
                            'GENEL SAĞLIK SİGORTASI TESCİL VE PRİM DAİRE BAŞKANLIĞI\nTarih 19.08.2019\nGENELGE\n2019/17')
  exmetin = exmetin.replace(
    'Konu : 5510 sayılı Kanunun ek 16 ncı \n\nmaddesi kapsamında prim teşviki \nuygulamaları\n\n30/05/2019',
    'Konu : 5510 sayılı Kanunun ek 16 ncı \n\nmaddesi kapsamında prim teşviki \nuygulamaları\n\nTarih 30/05/2019')
  exmetin = exmetin.replace(
    'Sayı : 92604331-010.06.02-E.7654597\nKonu : 2013/11 Sayılı Genelgede Değişiklik\n\n21/05/2019',
    'Sayı : 92604331-010.06.02-E.7654597\nKonu : 2013/11 Sayılı Genelgede Değişiklik\nTarih 21/05/2019')
  exmetin = exmetin.replace(
    'Sayı : 69053920-010.06.99-E.7452327\nKonu : Şirket kuruluşu aşamasında\n\nçalıştırılacağı bildirilen sigortalıların \ntescil işlemleri\n\n16/05/2019',
    'Sayı : 69053920-010.06.99-E.7452327\nKonu : Şirket kuruluşu aşamasında\n\nçalıştırılacağı bildirilen sigortalıların \ntescil işlemleri\nTarih 16/05/2019')
  exmetin = exmetin.replace(
    'Sayı : 24010506-010.06.01-E.3626255\nKonu : 5510 sayılı Kanunun ek-9 uncu maddesi kapsamında \n\nkonut kapıcılığı işyerlerinde çalışanlar\n\n05/03/2019',
    'Sayı : 24010506-010.06.01-E.3626255\nKonu : 5510 sayılı Kanunun ek-9 uncu maddesi kapsamında \n\nkonut kapıcılığı işyerlerinde çalışanlar\nTarih 05/03/2019')
  exmetin = exmetin.replace(
    'Sayı : 24010506-010.06.02-E.787070\nKonu : Prime esas kazançların alt ve üst \n\nsınırları ile bazı işlemlere esas tutarlar\n\n15/01/2019',
    'Sayı : 24010506-010.06.02-E.787070\nKonu : Prime esas kazançların alt ve üst \n\nsınırları ile bazı işlemlere esas tutarlar\nTarih 15/01/2019')
  exmetin = exmetin.replace(
    'Emeklilik Hizmetleri Genel Müdürlüğü \n\n\n\n5510 Sayılı Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu, Kanun ile ',
    'Emeklilik Hizmetleri Genel Müdürlüğü \n\nTarih 06.11.2018\n5510 Sayılı Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu, Kanun ile ')
  exmetin = exmetin.replace('Sayı : 55625784-952.99-E. 14368496\nKonu : Harcama Yetkisi\n\n26/10/2018',
                            'Sayı : 55625784-952.99-E. 14368496\nKonu : Harcama Yetkisi\nTarih 26/10/2018')
  exmetin = exmetin.replace(
    'Sayı : 96597630-204.03.01-E. 13136969\nKonu : 2018/26 Sayılı Genelgenin Bazı Maddelerinin\n\nİptal Edilmesi Hakkında\n\n05/10/2018',
    'Sayı : 96597630-204.03.01-E. 13136969\nKonu : 2018/26 Sayılı Genelgenin Bazı Maddelerinin\n\nİptal Edilmesi Hakkında\nTarih 05/10/2018')
  exmetin = exmetin.replace('6183 sayılı Kanunun 74/A maddesi \nile ilgili hususların eklenmesi\n\n04/09/2018',
                            '6183 sayılı Kanunun 74/A maddesi \nile ilgili hususların eklenmesi\nTarih 04/09/2018')
  exmetin = exmetin.replace('Sayı : 35158785-309/06-202.99-E. 11119337',
                            'Sayı : 35158785-309/06-202.99-E. 11119337 Tarih')
  exmetin = exmetin.replace('Sayı : 40552758-010.06-E.9641814\nKonu : 2018/27 sayılı Genelge\n\n01/08/2018',
                            'Sayı : 40552758-010.06-E.9641814\nKonu : 2018/27 sayılı Genelge\nTarih 01/08/2018')
  exmetin = exmetin.replace(
    'Sayı : 26431140-207.02-E.6235321\nKonu : 4447 Sayılı Kanunun Geçici 20 nci\n\nMaddesinde Yer Alan Prim Desteği\n\n20/06/2018',
    'Sayı : 26431140-207.02-E.6235321\nKonu : 4447 Sayılı Kanunun Geçici 20 nci\n\nMaddesinde Yer Alan Prim Desteği\nTarih 20/06/2018')
  exmetin = exmetin.replace('Sayı : 35158785-309-206.99-E. 1961584\nKonu : Kamu Kurumu İşverenleri\n\n29/03/2018',
                            'Sayı : 35158785-309-206.99-E. 1961584\nKonu : Kamu Kurumu İşverenleri\nTarih 29/03/2018')
  exmetin = exmetin.replace(
    'Sayı : 70660756-206.16-E.6569541\nKonu : 2011/53 sayılı Genelgenin tebliğ \n\nişlemleri ve süreler ile ilgili \nbölümlerinde değişiklik yapılması\n\n27/12/2017',
    'Sayı : 70660756-206.16-E.6569541\nKonu : 2011/53 sayılı Genelgenin tebliğ \n\nişlemleri ve süreler ile ilgili \nbölümlerinde değişiklik yapılması\nTarih 27/12/2017')
  exmetin = exmetin.replace('SOSYAL GÜVENLİK KURUMU \nEmeklilik Hizmetleri Genel Müdürlüğü\n\n2016/21 SAYILI GENELGE',
                            'SOSYAL GÜVENLİK KURUMU \nEmeklilik Hizmetleri Genel Müdürlüğü\nTarih 29.09.2016\n2016/21 SAYILI GENELGE')
  exmetin = exmetin.replace('Sayı : 70809318.010.06.02/142\nKonu : 3201 sayılı Kanunun uygulanması\n\n02/03/2015',
                            'Sayı : 70809318.010.06.02/142\nKonu : 3201 sayılı Kanunun uygulanması\nTarih 02/03/2015')
  exmetin = exmetin.replace(
    'Sayı : 70809318.010.06.02/819 \nKonu : 3201 sayılı Kanunda \n\nyapılan değişiklikler\n\n29/09/2014',
    'Sayı : 70809318.010.06.02/819 \nKonu : 3201 sayılı Kanunda \n\nyapılan değişiklikler\nTarih 29/09/2014')
  exmetin = exmetin.replace('Sayı : 70809318.010.06.02/ 588\nKonu : 3201 sayılı Kanun uygulamaları\n\n14/07/2014',
                            'Sayı : 70809318.010.06.02/ 588\nKonu : 3201 sayılı Kanun uygulamaları\nTarih 14/07/2014')
  exmetin = exmetin.replace(
    'Sayı : B.13.2.SGK.0.0.10.07.01/01-031/ 368\nKonu : Yurtdışı borçlanma ve tahsis işlemleri 08/06/2011',
    'Sayı : B.13.2.SGK.0.0.10.07.01/01-031/ 368\nKonu : Yurtdışı borçlanma ve tahsis işlemleri\nTarih 08/06/2011')
  exmetin = exmetin.replace('Sav : B.tâ.2.SGK.Ü.65.0L07//f? /.S/J/ZOl 1\nKonu: 4/î-b kapsamındakiler^',
                            'Sav : B.tâ.2.SGK.Ü.65.0L07//f? /.S/J/ZOl 1\nKonu: 4/î-b kapsamındakiler^\nTarih 18.03.2011')
  exmetin = exmetin.replace('Sayı : B.13.2.SGK.0.65.01.00/ 33 12.01.2010',
                            'Sayı : B.13.2.SGK.0.65.01.00/ 33 Tarih 12.01.2010')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 02.04.2020 Resmî Gazete Sayısı: 31087\nKonu: COVID-19 Salgınının Kamu İhale Sözleşmelerine Etkisi \n\nGENELGE',
    'Resmî Gazete tarihi: 02.04.2020 Resmî Gazete Sayısı: 31087\nKonu: COVID-19 Salgınının Kamu İhale Sözleşmelerine Etkisi \nTarih 01.04.2020\nGENELGE')
  exmetin = exmetin.replace('Resmî Gazete Tarihi: 27.10.2020 Resmî Gazete Sayısı: 31287\nGENELGE \n\n2020/14',
                            'Resmî Gazete tarihi: 27.10.2020 Resmî Gazete Sayısı: 31287\nGENELGE \nTarih 26.10.2020\n2020/14')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 03.02.2021 Resmî Gazete Sayısı: 31384\nKonu: Karayolu Trafik Güvenliği Strateji Belgesi (2021-2030) ve Karayolu Trafik Güvenliği Eylem Planı (2021-2023) \n\nGENELGE ',
    'Resmî Gazete tarihi: 03.02.2021 Resmî Gazete Sayısı: 31384\nKonu: Karayolu Trafik Güvenliği Strateji Belgesi (2021-2030) ve Karayolu Trafik Güvenliği Eylem Planı (2021-2023) \nTarih 02.01.2021\nGENELGE ')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 12.02.2021 Resmî Gazete Sayısı: 31393\nKonu: 2021 Yılının Hacı Bektaş Veli Yılı Olarak Kutlanması \n\nGENELGE ',
    'Resmî Gazete tarihi: 12.02.2021 Resmî Gazete Sayısı: 31393\nKonu: 2021 Yılının Hacı Bektaş Veli Yılı Olarak Kutlanması \nTarih 11.02.2021\nGENELGE ')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 20.02.2021 Resmî Gazete Sayısı: 31401\nKonu: 2021 Yılının Ahi Evran Yılı Olarak Kutlanması \n\nGENELGE ',
    'Resmî Gazete tarihi: 20.02.2021 Resmî Gazete Sayısı: 31401\nKonu: 2021 Yılının Ahi Evran Yılı Olarak Kutlanması \nTarih 19.02.2021\nGENELGE ')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 01.03.2021 Resmî Gazete Sayısı: 31410 Mükerrer\nKonu: COVID-19 Kapsamında Kamu Kurum ve Kuruluşlarında Normalleşme ve Alınacak Tedbirler \n\n\n\nGENELGE 2021/5',
    'Resmî Gazete tarihi: 01.03.2021 Resmî Gazete Sayısı: 31410 Mükerrer\nKonu: COVID-19 Kapsamında Kamu Kurum ve Kuruluşlarında Normalleşme ve Alınacak Tedbirler \n\nTarih 01.03.2021\n\nGENELGE 2021/5')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 08.04.2021 Resmî Gazete Sayısı: 31448\nKonu: 8 Nisan Romanlar Günü \n\nGENELGE 2021/7 ',
    'Resmî Gazete tarihi: 08.04.2021 Resmî Gazete Sayısı: 31448\nKonu: 8 Nisan Romanlar Günü \nTarih 07.04.2021\nGENELGE 2021/7 ')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 22.06.2021 Resmî Gazete Sayısı: 31519\nKonu: Türkiye Uluslararası Doğrudan Yatırım (UDY) Stratejisi (2021-2023) \n\nGENELGE',
    'Resmî Gazete tarihi: 22.06.2021 Resmî Gazete Sayısı: 31519\nKonu: Türkiye Uluslararası Doğrudan Yatırım (UDY) Stratejisi (2021-2023) \nTarih 21.06.2021\nGENELGE')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 24.06.2021 Resmî Gazete Sayısı: 31521\nKonu: 30 Haziran Koruyucu Aile Günü \n\nGENELGE ',
    'Resmî Gazete tarihi: 24.06.2021 Resmî Gazete Sayısı: 31521\nKonu: 30 Haziran Koruyucu Aile Günü \nTarih 23.06.2021\nGENELGE ')
  exmetin = exmetin.replace(
    'Resmî Gazete Tarihi: 10.09.2021 Resmî Gazete Sayısı: 31594 Mükerrer\nKonu: 2022-2024 Dönemi Yatırım Programı Hazırlıkları \n\nGENELGE \n\n2021/19 ',
    'Resmî Gazete Tarihi: 10.09.2021 Resmî Gazete Sayısı: 31594 Mükerrer\nKonu: 2022-2024 Dönemi Yatırım Programı Hazırlıkları \n\nGENELGE \nTarih 10.09.2021\n2021/19 ')
  exmetin = exmetin.replace('GENELGE \n\n2017/1\n\n19/10/2005 tarihli ve 5411 sayılı Bankacılık Kanununun',
                            'GENELGE \nTarih 09.03.2017\n2017/1\n\n19/10/2005 tarihli ve 5411 sayılı Bankacılık Kanununun')
  exmetin = exmetin.replace('Sayı : 40552758-010.06.02-E.11779915', 'Sayı : 40552758-010.06.02-E.11779915 Tarih')
  exmetin = exmetin.replace('Sayı : 51592363-206.01.02-E.1717804', 'Sayı : 51592363-206.01.02-E.1717804 Tarih')
  exmetin = exmetin.replace('Sayı : 13986510-206.07-E.3675504', 'Sayı : 13986510-206.07-E.3675504 Tarih')
  exmetin = exmetin.replace('Sayı : 96597630-010.06.02-E.5852699', 'Sayı : 96597630-010.06.02-E.5852699 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-030.01-E.5936691', 'Sayı : 15591373-030.01-E.5936691 Tarih')

  if exmetin.find('Emeklilik Hizmetleri Genel Müdürlüğü \n\nTarih 06.11.2018') != -1 and countTarih != 3:
    countTarih += 1

  elif exmetin.find('Emeklilik Hizmetleri Genel Müdürlüğü \n\nTarih 06.11.2018') != -1 and countTarih == 3:
    exmetin = exmetin.replace('Emeklilik Hizmetleri Genel Müdürlüğü \n\nTarih 06.11.2018',
                              'Emeklilik Hizmetleri Genel Müdürlüğü \n\nTarih 21.05.2020')

  exmetin = exmetin.replace('Sayı : 98547999-010.99-E.6203185', 'Sayı : 98547999-010.99-E.6203185 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-010.06.01-E.6221073', 'Sayı : 15591373-010.06.01-E.6221073 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-010.99-E.6619339', 'Sayı : 15591373-010.99-E.6619339 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-030.01-E.7046933', 'Sayı : 15591373-030.01-E.7046933 Tarih')
  exmetin = exmetin.replace('Sayı : 51592363-010.06.01-E.7156781', 'Sayı : 51592363-010.06.01-E.7156781 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-030.01-E.8164493', 'Sayı : 15591373-030.01-E.8164493 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-010.06.01-E.8381822', 'Sayı : 15591373-010.06.01-E.8381822 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-724.01.02-E.8876925', 'Sayı : 15591373-724.01.02-E.8876925 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-030.01-E.8925911', 'Sayı : 15591373-030.01-E.8925911 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-010.06.01-E.9122870', 'Sayı : 15591373-010.06.01-E.9122870 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-030.01-E.10074556', 'Sayı : 15591373-030.01-E.10074556 Tarih')
  exmetin = exmetin.replace('Sayı : 41481264-207.02-E.10073996', 'Sayı : 41481264-207.02-E.10073996 Tarih')
  exmetin = exmetin.replace('Sayı : 15591373-010.06.01-E.10293676', 'Sayı : 15591373-010.06.01-E.10293676 Tarih')
  exmetin = exmetin.replace('Sayı : E-15591373-724.01.02-11689791', 'Sayı : E-15591373-724.01.02-11689791 Tarih')
  exmetin = exmetin.replace('Sayı : E-92604331-010.06.01-11955333', 'Sayı : E-92604331-010.06.01-11955333 Tarih')
  exmetin = exmetin.replace('Sayı : E-15591373-010.06.01-13520871', 'Sayı : E-15591373-010.06.01-13520871 Tarih')
  exmetin = exmetin.replace('Sayı : E-51592363-010.06.02-14004230', 'Sayı : E-51592363-010.06.02-14004230 Tarih')
  exmetin = exmetin.replace('Sayı : E-40071718-206.99-14082030', 'Sayı : E-40071718-206.99-14082030 Tarih')
  exmetin = exmetin.replace('Sayı : E-41481264-207.02-14620444', 'Sayı : E-41481264-207.02-14620444 Tarih')
  exmetin = exmetin.replace('Sayı : E-66454725-010.06.01-16467758', 'Sayı : E-66454725-010.06.01-16467758 Tarih')
  exmetin = exmetin.replace('Sayı : E-98547999-010.01-21748897', 'Sayı : E-98547999-010.01-21748897 Tarih')
  exmetin = exmetin.replace('Sayı : E-69053920-010.06.01-23171689', 'Sayı : E-69053920-010.06.01-23171689 Tarih')
  exmetin = exmetin.replace('Sayı : E-41481264-207.02-24762269', 'Sayı : E-41481264-207.02-24762269 Tarih')
  exmetin = exmetin.replace('Sayı : E-51592363-010.06.01-26011223', 'Sayı : E-51592363-010.06.01-26011223 Tarih')
  exmetin = exmetin.replace('Sayı : E-15591373-010.99-26554258', 'Sayı : E-15591373-010.99-26554258 Tarih')
  exmetin = exmetin.replace('Sayı : E-41481264-207.02-30961273', 'Sayı : E-41481264-207.02-30961273 Tarih')
  exmetin = exmetin.replace('Sayı : E-15591373-010.99-31531091', 'Sayı : E-15591373-010.99-31531091 Tarih')
  exmetin = exmetin.replace('Sayı : E-40552758-010.06.01-33057668', 'Sayı : E-40552758-010.06.01-33057668 Tarih')
  exmetin = exmetin.replace('Sayı : E-24010506-010.06.01-33782544', 'Sayı : E-24010506-010.06.01-33782544 Tarih')
  exmetin = exmetin.replace('Sayı : E-41481264-207.02-40075736', 'Sayı : E-41481264-207.02-40075736 Tarih')
  exmetin = exmetin.replace('Sayı : E-15591373-010.06.01-41656363', 'Sayı : E-15591373-010.06.01-41656363 Tarih')
  return exmetin, countTarih


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def translate2(x):
  aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım",
           "Aralık"]
  months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December"]
  x = x.split(' ')
  # print(x)
  try:
    Index = aylar.index(x[1])
    x[1] = months[Index]
    return x[0] + ' ' + x[1] + ' ' + x[2]
  except:
    return "Hata"


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def metinMevzuatNo(exmetin, count):
  exmetin = exmetin.replace('  ', '')
  exmetin = exmetin.replace('SIRA NO:', 'Sıra No:')
  exmetin = exmetin.replace('SIRA NO : ', 'Sıra No:')
  exmetin = exmetin.replace('SIRA NO.', 'Sıra No:')
  exmetin = exmetin.replace('SERİ NO :', 'Seri No:')
  exmetin = exmetin.replace('SERİ NO: ', 'Seri No:')
  exmetin = exmetin.replace('SERİ NO:', 'Seri No:')
  exmetin = exmetin.replace('Seri No: ', 'Seri No:')
  exmetin = exmetin.replace('GENELGE', 'Genelge')
  exmetin = exmetin.replace('G E N E L G E', 'Genelge')
  exmetin = exmetin.replace('G E N E L G E \n\n', 'Genelge')
  exmetin = exmetin.replace('GenelgeSİ ', 'Genelge')
  exmetin = exmetin.replace('Genelgesi Değişikliği', '')
  exmetin = exmetin.replace('Genelge No:', 'Genelge')
  exmetin = exmetin.replace('Genelgede Değişiklik', '')
  exmetin = exmetin.replace('Genelgede GSS', '')
  exmetin = exmetin.replace('Genelgede yapılan', '')
  exmetin = exmetin.replace('Genelgenin Yürürlükten Kaldırılması', '')
  exmetin = exmetin.replace('Genelgenin Bazı', '')
  exmetin = exmetin.replace('sayılı Genelge', '')
  exmetin = exmetin.replace('/.İP', '/17')
  exmetin = exmetin.replace('2016/21 SAYILI Genelge', 'Genelge 2016/21')
  exmetin = exmetin.replace('İşveren İşlemleri Genelgesi', '')
  exmetin = exmetin.replace('Sayılı Genelge\'de Değişiklik', '')
  exmetin = exmetin.replace('Bazı Genelgelerde Değişiklik', '')
  exmetin = exmetin.replace('Yapılmasına Dair Genelge', '')
  exmetin = exmetin.replace('Sıra No:1998/47504', 'Sıra No:1998/5')
  exmetin = exmetin.replace('Genelge Değişikliği', '')
  exmetin = exmetin.replace('Genelge\n16-358 Ek', 'Genelge\n2005/16α')
  exmetin = exmetin.replace('Genelge\n16-375 EK', 'Genelge\n2006/16')
  exmetin = exmetin.replace('2001/14 Sayılı "Bölge Arşivleri"', '2001/4 Sayılı "Bölge Arşivleri"')
  exmetin = exmetin.replace('2004/16 Sayılı "Mera Kanunu değişikliği"', '1587 Sayılı "Mera Kanunu değişikliği"')
  exmetin = exmetin.replace('2004/17 Sayılı "Mahkeme Bilirkişileri"', '1588 Sayılı "Mahkeme Bilirkişileri"')
  exmetin = exmetin.replace('2005/6 Sayılı "Sendika Üyeliği"', '1600 Sayılı "Sendika Üyeliği"')
  exmetin = exmetin.replace('2005/17 Sayılı "Yıpranan Tarihi ve Kültürel', '1611 Sayılı "Yıpranan Tarihi ve Kültürel')
  exmetin = exmetin.replace('2005/18 Sayılı "Devlet Malının Korunması', '1612 Sayılı "Devlet Malının Korunması')
  exmetin = exmetin.replace('2006/3 Sayılı "5253 sayılı Dernekler Kanunu"',
                            '1619 Sayılı "5253 sayılı Dernekler Kanunu"')
  exmetin = exmetin.replace('2006/4 Sayılı "2005/3 (1597) sayılı genelgeye ektir.',
                            '1620 Sayılı "2005/3 (1597) sayılı genelgeye ektir.')
  exmetin = exmetin.replace('2006/11 sayılı "Birimler Tarafından', '1627 Sayılı "2006/11 sayılı "Birimler Tarafından')
  exmetin = exmetin.replace('2006/15 Sayılı "Özel Hizmet Tazminatı"',
                            '1631 Sayılı "2006/15 Sayılı "Özel Hizmet Tazminatı"')
  exmetin = exmetin.replace('2008/1 Sayılı "Kat Mülkiyeti Kanununda', '1651 Sayılı "Kat Mülkiyeti Kanununda')
  exmetin = exmetin.replace('2008/9 Sayılı "5737 Sayılı Vakıflar Kanunu"', '1659 Sayılı "5737 sayılı Vakıflar Kanunu"')
  exmetin = exmetin.replace('2008/10 Sayılı "Yayın Yasağı Getirilmesi"', '1660 Sayılı "Yayın Yasağı Getirilmesi"')
  exmetin = exmetin.replace('2008/15 Sayılı "Hukuk Müşavirleri ile ilgili', '1665 Sayılı "Hukuk Müşavirleri ile ilgili')
  exmetin = exmetin.replace('2008/17 Sayılı "Vakıflar Yönetmeliği Hk.', '1667 Sayılı "Vakıflar Yönetmeliği Hk.')
  exmetin = exmetin.replace('2009/7 Sayılı "Kadastro Çalışmalarında', '1678 Sayılı "Kadastro Çalışmalarında')
  exmetin = exmetin.replace('2009/14 Sayılı "Kat İrtifakı ve Kat Mülkiyeti"',
                            '1685 Sayılı "Kat İrtifakı ve Kat Mülkiyeti"')
  exmetin = exmetin.replace('2010/2 Sayılı "Tatillerde İl Hudutlarının', '1695 Sayılı "Tatillerde İl Hudutlarının')
  exmetin = exmetin.replace('2010/6 Sayılı "Yetki Belgesi"', '1699 Sayılı "Yetki Belgesi"')
  exmetin = exmetin.replace('2010/12 Sayılı "Üst Hakkı"', '1705 Sayılı "Üst Hakkı"')
  exmetin = exmetin.replace('Genelge\n\n2017U2', 'Genelge\n\n2017/12')
  exmetin = exmetin.replace('İÇ Genelge \n2017/1', 'Genelge\n1046330\na')
  exmetin = exmetin.replace('İçindekiler\n\nKISA VADELİ SİGORTA KOLLARI İŞLEMLERİ',
                            'Genelge\n2016/21\nİçindekiler\n\nKISA VADELİ SİGORTA KOLLARI İŞLEMLERİ')
  exmetin = exmetin.replace('Konu : Hukuk Servislerinin İhtiyaçları\n\nGenelge',
                            'Konu : Hukuk Servislerinin İhtiyaçları\n\nGenelge 2016/17')
  exmetin = exmetin.replace('Genelge \n2015 / 2j3', 'Genelge \n2015 / 28')
  exmetin = exmetin.replace('Kayıp Oranı Tespit İşlemleri\n\nGenelge \n2015 /',
                            'Kayıp Oranı Tespit İşlemleri\n\nGenelge \n2015 / 23')
  exmetin = exmetin.replace('Genelge \n2015/2.0', 'Genelge \n2015/20')
  exmetin = exmetin.replace('Genelge \n2015/ ^', 'Genelge \n2015/9')
  exmetin = exmetin.replace('Genelge 1\n2015/2', 'Genelge\n2015/2')
  exmetin = exmetin.replace('Genelge\n2014/^0', 'Genelge\n2014/30a')
  exmetin = exmetin.replace('Genelge\n2014/\n', 'Genelge\n2014/27\n')
  exmetin = exmetin.replace('Genelge \n• 2014/ £,2^', 'Genelge\n2014/22')
  exmetin = exmetin.replace('Genelge \n2014/ //', 'Genelge\n2014/11')
  exmetin = exmetin.replace('Genelge \n2013/ JS\'', 'Genelge\n2013/35')
  exmetin = exmetin.replace('Genelge\n2012 !.l(o', 'Genelge\n2012/26')
  exmetin = exmetin.replace('Genelge\n20127.15“', 'Genelge\n2012/15')
  exmetin = exmetin.replace('Kanunla Yapılan Düzenlemeler\n\nGenelge\n16-344 Ek',
                            'Kanunla Yapılan Düzenlemeler\n\nGenelge\n2005/16')

  if exmetin.find('Genelge \n\n2018/38 \n\n15/08/2019 tarihli ve 2019/16 sayılı') != -1 and count != 2:
    count += 1

  elif exmetin.find('Genelge \n\n2018/38 \n\n15/08/2019 tarihli ve 2019/16 sayılı') != -1 and count == 2:
    exmetin = exmetin.replace('Genelge \n\n2018/38 \n\n15/08/2019 tarihli ve 2019/16 sayılı',
                              'Genelge\n\n2020/15\n\n15/08/2019 tarihli ve 2019/16 sayılı')

  exmetin = exmetin.replace('Konulu Genelge', '')
  exmetin = exmetin.replace('sayili genelgeye ek.', '')
  exmetin = exmetin.replace('Genelgesi ile tapu dairelerinde vadesi', '')
  exmetin = exmetin.replace('Ödenmesi Genelgesinin', '')
  exmetin = exmetin.replace('Dair Genelge', '')
  exmetin = exmetin.replace('Sayılı Genelge', '')

  exmetin = exmetin.replace('Sayı : 70809318.0lO.O6.O2/jfcj J2 12 -1*',
                            'Sayı : 70809318.0lO.O6.O2/jfcj J2 12 -1*\nGenelge 2013/18\n')

  return exmetin, count


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def genelge_doldur(i):
  degerlerimiz = ["mevzuat_tarihi", "mevzuat_no", "belge_sayi"]
  belgelerdekiToplamDegerSayisi = [385, 342, 43]
  belgelerdekiHataliDegerSayisi = [0] * len(degerlerimiz)

  # Düzenleme fonksiyonlarında önem taşıyan sayaçları ayarlıyoruz.
  countNo = 0
  countTarih = 0

  # Sadece Genelge kategorisindeki belgelerde işlem yapıyoruz.
  belgeSayi = ''
  metin = df['data_text'][i][:5000]

  # 'mevzuat_tarihi' değerini bulan kod
  # VERİ İŞLEME VE TEMİZLİĞİ
  metin = df['data_text'][i][:5000]
  metin, countTarih = metinMevzuatTarihi(metin, countTarih)

  # Tarih değeri olan Tarihleri bulan kod
  if metin.find('Tarih ') != -1:
    mevzuatTarihiIndex = metin.find('Tarih ')
    mevzuatTarihiIndex = mevzuatTarihiIndex + len('Tarih ')
    mevzuatTarihi = metin[mevzuatTarihiIndex:mevzuatTarihiIndex + 10]
    if mevzuatTarihi[9].isdigit() != 1:
      mevzuatTarihi = mevzuatTarihi[:9]

  # Ay içeren Tarihleri bulan kod
  else:
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım",
             "Aralık"]
    index = 0
    tarihbuldu = 0
    for ay in aylar:
      if metin.find(ay) != -1:
        tarihbuldu = 1
        break
      else:
        index += 1
    if index == 12:
      pass
    if tarihbuldu != 0:
      ayIndex = metin.find(aylar[index])
      mevzuatTarihi = metin[ayIndex - 3:ayIndex + (len(aylar[index])) + 5]
      if mevzuatTarihi[0].isdigit() != 1:
        mevzuatTarihi = mevzuatTarihi[1:]
        mevzuatTarihi = '0' + mevzuatTarihi
      mevzuatTarihi = translate2(mevzuatTarihi)

  # 'mevzuat_no' değerini bulan kod
  # VERİ İŞLEME VE TEMİZLİĞİ
  metin, countNo = metinMevzuatNo(metin, countNo)

  # 'mevzuat_no' değerinin kontrol edilip edilmeyeceğine bakıyoruz, eğer değer nan ise bunun yerine 'belge_sayi' değerini bulmamız gerek.
  temp = 0


  if temp != 1:
    genelge = 0
    # Asıl değerin düzenlenmesi
    dfMevzuatNo = dfMevzuatNo.replace('/0', '/')
    dfMevzuatNo = dfMevzuatNo.replace(' ', '')

    # Farklı Olasılıkların değerlendirilmesi
    if metin.find('Seri No:') != -1:
      mevzuatNoIndex = metin.find('Seri No:')
      mevzuatNoIndex = mevzuatNoIndex + len('Seri No:')

    elif metin.find('Sıra No:') != -1:
      mevzuatNoIndex = metin.find('Sıra No:')
      mevzuatNoIndex = mevzuatNoIndex + len('Sıra No:')

    elif metin.find('Genelge') != -1:
      mevzuatNoIndex = metin.find('Genelge')
      mevzuatNoIndex = mevzuatNoIndex + len('Genelge')

    else:
      mevzuatNoIndex = metin.find('/')
      mevzuatNoIndex -= 4

    if metin.find('Tapu ve Kadastro Genel Müdürlüğü') != -1:
      mevzuatNoIndex = metin.find('Sayılı')
      alinanKesit = metin[mevzuatNoIndex - 10:mevzuatNoIndex]
      if alinanKesit.find('/') != -1:
        mevzuatNoIndex = mevzuatNoIndex - 8
      else:
        mevzuatNoIndex = mevzuatNoIndex - 5

    # Mevzuat değerini tespit edip hataları ayıklayan kod
    mevzuatNo = ''
    rakambuldu = 0
    stat = 0
    while 1:

      if metin[mevzuatNoIndex] == ' ' or metin[mevzuatNoIndex] == '•' or metin[mevzuatNoIndex] == ',':
        pass

      elif metin[mevzuatNoIndex] == '/':
        stat = 1

      elif metin[mevzuatNoIndex] == '–' or metin[mevzuatNoIndex] == '-':
        stat = 2

      elif metin[mevzuatNoIndex].isdigit():
        mevzuatNo = mevzuatNo + metin[mevzuatNoIndex]

      elif metin[mevzuatNoIndex] == '\n' and stat == 0:
        pass

      else:
        if metin[mevzuatNoIndex] == 'H' and stat == 2:
          mevzuatNo = mevzuatNo + '11'

        elif metin[mevzuatNoIndex] == 'A' and stat == 2:
          mevzuatNo = mevzuatNo + '1'

        elif metin[mevzuatNoIndex] == '£' and stat == 1:
          mevzuatNo = mevzuatNo + '22'

        elif metin[mevzuatNoIndex] == 'α' and stat == 1:
          mevzuatNo = mevzuatNo + '-358'

        elif metin[mevzuatNoIndex:mevzuatNoIndex + 3] == 'D//':
          mevzuatNo = ''
          mevzuatNo = mevzuatNo + '2011'
        else:
          break

      mevzuatNoIndex = mevzuatNoIndex + 1

    mevzuatNo = mevzuatNo.replace(' ', '')
    mevzuatNo = mevzuatNo.replace('\n', '')
    if stat == 1:
      mevzuatNo = mevzuatNo[:4] + '/' + mevzuatNo[4:]

    elif stat == 2:
      mevzuatNo = mevzuatNo[:4] + '/' + mevzuatNo[4:]

  # 'belge_sayi' değerini bulan kod
  # Eğer 'mevzuat_no' değeri nan idiyse bu kod çalışır.
  else:
    # VERİ İŞLEME VE TEMİZLİĞİ
    metin = df['data_text'][i][:5000]

    # belgeSayısının başlangıcını bulma
    belgeSayiIndex = metin.find('Sayı')
    belgeSayiIndex = belgeSayiIndex + len('Sayı')
    belgeSayi = ''

    # Sonuna kadar değeri alma
    while metin[belgeSayiIndex] != '\n':
      if metin[belgeSayiIndex] != ' ':
        belgeSayi += metin[belgeSayiIndex]
      belgeSayiIndex += 1

  # Asıl değerlerin formatlanması')

  # Çekilen Değerlerin formatlanması
  df2.loc[i, "mevzuat_tarihi"] = mevzuatTarihi
  try:
    if mevzuatTarihi.find("-") != -1:
      mevzuatTarihi = datetime.strptime(mevzuatTarihi, "%d-%m-%Y")
    elif mevzuatTarihi.find(".") != -1:
      mevzuatTarihi = datetime.strptime(mevzuatTarihi, "%d.%m.%Y")
    elif mevzuatTarihi.find("/") != -1:
      mevzuatTarihi = datetime.strptime(mevzuatTarihi, "%d/%m/%Y")
    elif mevzuatTarihi.find(" ") != -1:
      mevzuatTarihi = datetime.strptime(mevzuatTarihi, "%d %B %Y")
  except:
    mevzuatTarihi = '19-08-2022'

  # Değerlerin Asılları ile Karşılaştırılması

  dogru = 0

  if mevzuatTarihi != dfMevzuatTarihi:
    belgelerdekiHataliDegerSayisi[0] += 1
    print(i, " MevzuatTarihiHatası ", '|', mevzuatTarihi, '|', dfMevzuatTarihi, '|', sep='')
  else:
    dogru += 1

  if temp != 1:
    if mevzuatNo != dfMevzuatNo and temp != 1:
      belgelerdekiHataliDegerSayisi[1] += 1
      print(i, " MevzuatNoHatası ", '|', mevzuatNo, '|', dfMevzuatNo, '|', sep='')
    else:
      dogru += 1
  else:
    if belgeSayi != dfBelgeSayi:
      belgelerdekiHataliDegerSayisi[2] += 1
      print(i, " BelgeSayıHatası ", '|', belgeSayi, '|', dfBelgeSayi, '|', sep='')
    else:
      dogru += 1

  if dogru == 2:
    return True
  else:
    return False

  # Kodun Performansının Yazdırılması
  """for i in range(3):
    print(degerlerimiz[i], "|", belgelerdekiHataliDegerSayisi[i], "/", belgelerdekiToplamDegerSayisi[i], "|",
          round((belgelerdekiToplamDegerSayisi[i] -belgelerdekiHataliDegerSayisi[i])/belgelerdekiToplamDegerSayisi[i],3))"""


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def tarihduzelt(tarih):
  ayracsayisi = 0
  i = 0
  gun = ''
  ay = ''
  yil = ''
  if type(tarih) is str:

    if tarih.find(
      '-') != -1:  # Veri iskeletindeki tarihler "-" karakteri ile ayrılmaktadır ve yyyy-mm-dd formatında olduğundan tersten bölümleri okumayı sağlıyor.
      ayracsayisi = 2
    while i < len(tarih):
      if tarih[i].isdigit() and ayracsayisi == 0:
        gun = gun + tarih[i]
      if tarih[i].isdigit() and ayracsayisi == 1:
        ay = ay + tarih[i]
      if tarih[i].isdigit() and ayracsayisi == 2:
        yil = yil + tarih[i]

      if tarih[i] == '/' or tarih[i] == '.':
        ayracsayisi += 1
      if tarih[i] == '-':
        ayracsayisi -= 1
      i += 1

    # gün ve ayları 2 basamağa çevirme
    if len(gun) < 2:
      gun = '0' + gun
    if len(ay) < 2:
      ay = '0' + ay
    return gun + ay + yil

  else:
    return '.'


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def kategoriBul(verilenMetin):
  metin = verilenMetin.lower()
  # if verilenMetin.find('Gazete')!=-1:
  if (metin.find("gazete") != -1 or metin.find("yayım")) and (
    metin.find("kuruluş") != -1 or metin.find("tesis") != -1) and (
    metin.find("1920") != -1 or metin.find("1336") != -1):
    return 'Resmi Gazete'

  verilenMetin = verilenMetin.replace('  ', '')
  verilenMetin = verilenMetin.replace('\n', '')
  verilenMetin = verilenMetin.replace('\r', '')
  # data_text alanındaki kayıdın ilk parçasında "CUMHURBAŞKANLIĞI KARARNAMESİ" ifadesi varsa o bir Cumhurbaşkanlığı Kararnamesi'dir önermesini kontrol ediyoruz!
  if verilenMetin.find('CUMHURBAŞKANLIĞI KARARNAMESİ') != -1:
    return 'Cumhurbaşkanlığı Kararnamesi'


  # data_text alanındaki kayıdın ilk parçasında "BKK No:" ifadesi varsa o bir Tüzük'tür önermesini kontrol ediyoruz!
  elif verilenMetin.find('BKK No:') != -1:
    return 'Tüzük'

  # data_text alanındaki kayıdın ilk parçasında Mevzuat No'yu oluşturan parçalardan biri olan "KHK" ifadesi varsa o bir kanundur önermesini kontrol ediyoruz!
  elif verilenMetin.find('KHK') != -1:
    return 'Kanun Hükmünde Kararname'

  # data_text alanındaki kayıdın ilk parçasında Kanun No varsa o bir kanundur önermesini kontrol ediyoruz!
  elif verilenMetin.find('Kanun No') != -1:
    return 'Kanun'

  komisyonMetin = verilenMetin.replace(' ', '')
  komisyonMetin = komisyonMetin.replace(':', '')
  komisyonMetin = komisyonMetin.replace('.', '')
  komisyonMetin = komisyonMetin.replace('ý', 'ı')
  # data_text alanındaki kayıdın ilk parçasında ne varsa o bir Komisyon Raporudur diye kontrol ediyoruz!
  if komisyonMetin.lower().find('kanuntasarisi') != -1 or komisyonMetin.lower().find(
    'yasamayili') != -1 or komisyonMetin.lower().find('tbmm') != -1 or komisyonMetin.lower().find(
    'komisyonraporu') != -1 or komisyonMetin.lower().find('ssayısı') != -1 or komisyonMetin.lower().find(
    'ssayisi') != -1 or komisyonMetin.lower().find('sirano') != -1 or komisyonMetin.lower().find(
    'sırano') != -1 or komisyonMetin.lower().find('ilâve') != -1:
    return 'Komisyon Raporu'

  genelgeMetin = verilenMetin.replace(' ', '')
  # data_text alanındaki kayıdın ilk parçasında erik: varsa o bir genelgedir önermesini kontrol ediyoruz!
  if genelgeMetin.lower().find('genelge') != -1 or genelgeMetin.lower().find('genelyazi') != -1:
    return 'Genelge'

  # data_text alanındaki kayıdın ilk parçasında  olan "T.C.", "Gelir" veya "GELİR" ifadelerinden biri varsa o bir Özelge'dir önermesini kontrol ediyoruz!
  if verilenMetin.find('T.C.') != -1 and (verilenMetin.find('Gelir') != -1 or verilenMetin.find('GELİR') != -1):
    return 'Özelge'

  yonetmelikMetin = verilenMetin.replace(' ', '')
  yonetmelikMetin = yonetmelikMetin.replace(':', '')
  yonetmelikMetin = yonetmelikMetin.replace('.', '')
  yonetmelikMetin = yonetmelikMetin.replace('ý', 'ı')
  yonetmelikMetin = yonetmelikMetin.replace('i̇', 'i')
  # data_text alanındaki kayıdın ilk parçasında ne varsa o bir YÖNETMELİKTİR diye kontrol ediyoruz!
  if yonetmelikMetin.lower().find('yönetmeli') != -1 or yonetmelikMetin.lower().find('yönetmeli̇') != -1:
    return 'Yönetmelik'

  tebligMetin = verilenMetin.replace(' ', '')
  tebligMetin = tebligMetin.replace(':', '')
  tebligMetin = tebligMetin.replace('.', '')
  tebligMetin = tebligMetin.replace('ý', 'ı')
  tebligMetin = tebligMetin.replace('i̇', 'i')
  # data_text alanındaki kayıdın ilk parçasında ne varsa o bir YÖNETMELİKTİR diye kontrol ediyoruz!
  if tebligMetin.lower().find('tebl') != -1:
    return 'Tebliğ'

  return 'Resmi Gazete'


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def kanun_doldur(i):
  i = 0

  print(i)
  metin = df['data_text'][i][:310].lower()
  metin = metin.replace('  ', '')
  baslangic_rgtrh = metin.find('resmî gazete tarihi:')
  baslangic_rgtrh = baslangic_rgtrh + len('resmî gazete tarihi: ')
  rg_trh1 = metin[baslangic_rgtrh:baslangic_rgtrh + 10]
  print(rg_trh1)

  baslangic_rgno = metin.find('resmî gazete sayısı: ')
  baslangic_rgno = baslangic_rgno + len('resmî gazete sayısı: ')
  rg_no1 = ''
  rakambuldu = 0
  while metin[baslangic_rgno].isdigit() or rakambuldu == 0:
    if metin[baslangic_rgno] == ' ' or metin[baslangic_rgno] == '\n':
      rakambuldu = 0
    elif metin[baslangic_rgno].isdigit():
      rakambuldu = 1
      rg_no1 = rg_no1 + metin[baslangic_rgno]
    baslangic_rgno = baslangic_rgno + 1
  rg_no1 = int(rg_no1)
  print(rg_no1)

  baslangic_knno = metin.find('kanun no. ')
  baslangic_knno = baslangic_knno + len('kanun no. ')
  kn_no1 = ''
  rakambuldu = 0
  while metin[baslangic_knno].isdigit() or rakambuldu == 0:
    if metin[baslangic_knno] == ' ' or metin[baslangic_knno] == '\n':
      rakambuldu = 0
    elif metin[baslangic_knno].isdigit():
      rakambuldu = 1
      kn_no1 = kn_no1 + metin[baslangic_knno]
    baslangic_knno = baslangic_knno + 1
  kn_no1 = int(kn_no1)
  print(kn_no1)

  baslangic_kntrh = metin.find('kabul tarihi : ')
  baslangic_kntrh = baslangic_kntrh + len('kabul tarihi : ')
  kn_trh1 = metin[baslangic_kntrh:baslangic_kntrh + 10]
  if kn_trh1[9].isdigit() != True:
    kn_trh1 = kn_trh1[:9]
  elif kn_trh1[8].isdigit() != True:
    kn_trh1 = kn_trh1[:8]

  kn_trh1 = kn_trh1.replace('\n', '')
  kn_trh1 = kn_trh1.replace(' ', '')
  print(kn_trh1)
  print("----------")
  rg_trh2 = df.loc[df['kategori'] == 'Kanun', 'rega_tarihi'][i]
  rg_no2 = int(df.loc[df['kategori'] == 'Kanun', 'rega_no'][i])
  kn_no2 = int(df.loc[df['kategori'] == 'Kanun', 'mevzuat_no'][i])
  kn_trh2 = df.loc[df['kategori'] == 'Kanun', 'mevzuat_tarihi'][i]

  rg_trh2 = tarihduzelt(rg_trh2)
  kn_trh2 = tarihduzelt(kn_trh2)

  rg_trh1 = tarihduzelt(rg_trh1)
  kn_trh1 = tarihduzelt(kn_trh1)

  dogru = 0

  if rg_no1 == rg_no2:
    dogru += 1
  else:

    print("*rg no* cevap:", rg_no1, " doğrusu:", rg_no2)

  if rg_trh1 == rg_trh2:
    dogru += 1
  else:

    print("*rg_tarih* cevap:", rg_trh1, " doğrusu:", rg_trh2)

  if kn_no1 == kn_no2:
    dogru += 1
  else:

    print("*kn_no* cevap:", kn_no1, " doğrusu:", kn_no2)

  if kn_trh1 == kn_trh2:
    dogru += 1
  else:

    print("*kn_trh* cevap:", kn_trh1, " doğrusu:", kn_trh2)

  if dogru == 4:
    return True
  else:
    return False


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def teblig_doldur(i):
  print(i)

  rg_trh2 = df.loc[i]['rega_tarihi']
  rg_no2 = df.loc[i]['rega_no']
  kes = rg_no2.find(" ")
  if kes != -1:
    rg_no2 = rg_no2[:kes]
  rg_no2 = int(rg_no2)

  rg_trh2 = tarihduzelt(rg_trh2)

  metin = df['data_text'][i][:310].lower()  # Verileri çıkarmak için ilk 310 karakter yeterli
  metin = metin.replace('  ', '')

  # Resmi gazete tarihi çıkarma
  baslangic_rgtrh = metin.find('resmî gazete tarihi:')
  baslangic_rgtrh = baslangic_rgtrh + len('resmî gazete tarihi: ')
  rg_trh1 = metin[baslangic_rgtrh:baslangic_rgtrh + 10]
  print(rg_trh1, "->", rg_trh2)

  # Resmi gazete no çıkarma
  baslangic_rgno = metin.find('resmî gazete sayısı: ')
  baslangic_rgno = baslangic_rgno + len('resmî gazete sayısı: ')
  rg_no1 = ''
  rakambuldu = 0
  # Sayının uzunluğu değiştiğinden sabit bir aralık kullanılamıyor
  while metin[baslangic_rgno].isdigit() or rakambuldu == 0:
    if metin[baslangic_rgno] == ' ' or metin[baslangic_rgno] == '\n':
      rakambuldu = 0
    elif metin[baslangic_rgno].isdigit():
      rakambuldu = 1
      rg_no1 = rg_no1 + metin[baslangic_rgno]
    baslangic_rgno = baslangic_rgno + 1
  rg_no1 = int(rg_no1)
  print(rg_no1, "->", rg_no2)

  rg_trh1 = tarihduzelt(rg_trh1)

  dogru = 0
  if rg_no1 == rg_no2:
    dogru += 1
  else:
    print("*rg no* cevap:", rg_no1, " doğrusu:", rg_no2)

  if rg_trh1 == rg_trh2:
    dogru += 1
  else:
    print("*rg_tarih* cevap:", rg_trh1, " doğrusu:", rg_trh2)

  if dogru == 2:
    return True
  else:
    return False


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def khk_doldur(i):
  dfRegaNo = ' '
  dfMevzuatNo = ' '
  dfRegaTarihi = ' '
  dfMevzuatTarihi = ' '

  metin = df['data_text'][i][:df['data_text'][i].find('Madde 1')].lower()
  metin = metin.replace('  ', '')

  # 'rega_tarihi' değerini bulan kod
  regaTarihiIndex = metin.find('resmî gazete tarihi:')
  regaTarihiIndex = regaTarihiIndex + len('resmî gazete tarihi: ')
  regaTarihi = metin[regaTarihiIndex:regaTarihiIndex + 10]

  # 'rega_no' değerini bulan kod
  regaNoIndex = metin.find('resmî gazete sayısı: ')
  regaNoIndex = regaNoIndex + len('resmî gazete sayısı: ')
  regaNo = ''
  rakambuldu = 0
  while metin[regaNoIndex].isdigit() or rakambuldu == 0:
    if metin[regaNoIndex] == ' ' or metin[regaNoIndex] == '\n':
      rakambuldu = 0
    elif metin[regaNoIndex].isdigit():
      rakambuldu = 1
      regaNo = regaNo + metin[regaNoIndex]
    regaNoIndex = regaNoIndex + 1
  regaNo = int(regaNo)

  # 'mevzuat_no' değerini bulan kod
  mevzuatNoIndex = metin.find('karar sayısı : ')
  mevzuatNoIndex = mevzuatNoIndex + len('karar sayısı : ') + 4
  mevzuatNo = ''
  rakambuldu = 0
  while metin[mevzuatNoIndex].isdigit() or rakambuldu == 0:
    if metin[mevzuatNoIndex] == ' ' or metin[mevzuatNoIndex] == '\n':
      rakambuldu = 0
    elif metin[mevzuatNoIndex].isdigit():
      rakambuldu = 1
      mevzuatNo = mevzuatNo + metin[mevzuatNoIndex]
    mevzuatNoIndex = mevzuatNoIndex + 1
  mevzuatNo = int(mevzuatNo)

  # 'mevzuat_tarihi' değerini bulan kod
  mevzuatTarihiIndex = metin.find('kararnamenin tarihi : ')
  mevzuatTarihiIndex = mevzuatTarihiIndex + len('kararnamenin tarihi : ')
  mevzuatTarihi = metin[mevzuatTarihiIndex:mevzuatTarihiIndex + 10]

  mevzuatTarihi = mevzuatTarihi.replace('\n', '')
  mevzuatTarihi = mevzuatTarihi.replace(' ', '')

  # Asıl değerlerin dosyadan çekilmesi
  dfRegaTarihi = df.loc[i]['rega_tarihi']
  if pd.isna(df.loc[i]['rega_no']) != True:
    dfRegaNo = int(df.loc[i]['rega_no'])
  if pd.isna(df.loc[i]['mevzuat_no']) != True:
    dfMevzuatNo = int(df.loc[i]['mevzuat_no'])
  dfMevzuatTarihi = df.loc[i]['mevzuat_tarihi']

  # Asıl değerlerin formatlanması
  dfRegaTarihi = tarihduzelt(dfRegaTarihi)
  dfMevzuatTarihi = tarihduzelt(dfMevzuatTarihi)

  regaTarihi = tarihduzelt(regaTarihi)
  mevzuatTarihi = tarihduzelt(mevzuatTarihi)

  # Çekilen Değerlerin formatlanması

  # Çekilen Değerlerin Asıllarıyla Karşılaştırılması
  dogru = 0
  # Değerlerin Asılları ile Karşılaştırılması
  if regaTarihi == dfRegaTarihi:
    dogru += 1

  if regaNo == dfRegaNo:
    dogru += 1

  if mevzuatNo == dfMevzuatNo:
    dogru += 1

  if mevzuatTarihi == dfMevzuatTarihi:
    dogru += 1

  if dogru == 4:
    return True
  else:
    return False


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def cumhurbaskank_doldur(i):
  metin = df['data_text'][i][:df['data_text'][i].find('Madde 1')].lower()
  metin = metin.replace('  ', '')

  metinSon = df['data_text'][i][-15:].lower()

  # 'rega_tarihi' değerini bulan kod
  regaTarihiIndex = metin.find('resmî gazete tarihi: ')
  regaTarihiIndex = regaTarihiIndex + len('resmî gazete tarihi: ')
  regaTarihi = metin[regaTarihiIndex:regaTarihiIndex + 10]

  # 'rega_no' değerini bulan kod
  regaNoIndex = metin.find('resmî gazete sayısı: ')
  regaNoIndex = regaNoIndex + len('resmî gazete sayısı: ')
  regaNo = ''
  rakambuldu = 0
  while metin[regaNoIndex].isdigit() or rakambuldu == 0:
    if metin[regaNoIndex] == ' ' or metin[regaNoIndex] == '\n':
      rakambuldu = 0
    elif metin[regaNoIndex].isdigit():
      rakambuldu = 1
      regaNo = regaNo + metin[regaNoIndex]
    regaNoIndex = regaNoIndex + 1
  regaNo = int(regaNo)

  # 'mevzuat_no' değerini bulan kod
  if metin.find('kararname numarası:') != -1:
    mevzuatNoIndex = metin.find('kararname numarası:')
    mevzuatNoIndex = mevzuatNoIndex + len('kararname numarası:')

  elif metin.find('kararname sayısı:') != -1:
    mevzuatNoIndex = metin.find('kararname sayısı:')
    mevzuatNoIndex = mevzuatNoIndex + len('kararname sayısı:')

  elif metin.find('kararname numarasi:') != -1:
    mevzuatNoIndex = metin.find('kararname numarasi:')
    mevzuatNoIndex = mevzuatNoIndex + len('kararname numarasi:')

  elif metin.find('kararname numarası') != -1:
    mevzuatNoIndex = metin.find('kararname numarası')
    mevzuatNoIndex = mevzuatNoIndex + len('kararname numarası')

  mevzuatNo = ''
  rakambuldu = 0
  while metin[mevzuatNoIndex].isdigit() or rakambuldu == 0:
    if metin[mevzuatNoIndex] == ' ' or metin[mevzuatNoIndex] == '\n':
      rakambuldu = 0
    elif metin[mevzuatNoIndex].isdigit():
      rakambuldu = 1
      mevzuatNo = mevzuatNo + metin[mevzuatNoIndex]
    mevzuatNoIndex = mevzuatNoIndex + 1
  mevzuatNo = int(mevzuatNo)

  # 'mevzuat_tarihi' değerini bulan kod
  aylar = ["ocak", "şubat", "mart", "nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım",
           "aralık"]
  count = 0
  # metinSon'dan alınan değerin istenen türde olup olmadığını kontrol ediyoruz.
  for ay in aylar:
    if ay in metinSon:
      count += 1
  if count != 0:
    if metinSon[0].isdigit() != 1:
      if metinSon[1].isdigit() != 1:
        if metinSon[2].isdigit() != 1:
          metinSon = metinSon[3:]
        else:
          metinSon = metinSon[2:]
      else:
        metinSon = metinSon[1:]

    # tarihi datetime kütüphanesinin anlayabileceği formata dönüştürelim.
    mevzuatTarihi = translate(metinSon)

  # Asıl değerlerin dosyadan çekilmesi
  dfRegaTarihi = df['rega_tarihi'][i]
  dfRegaNo = int(df['rega_no'][i])
  dfMevzuatNo = int(df['mevzuat_no'][i])
  dfMevzuatTarihi = df['mevzuat_tarihi'][i]

  # Asıl değerlerin formatlanması
  dfRegaTarihi = datetime.strptime(dfRegaTarihi, '%Y-%m-%d')
  temp = 0
  # dosyadaki Mevzuat Tarihi Değerinin "nan" olup olmadığını kontrol ediyoruz.
  try:
    temp = math.isnan(dfMevzuatTarihi)
  except:
    dfMevzuatTarihi = datetime.strptime(dfMevzuatTarihi, '%Y-%m-%d')

  # Çekilen Değerlerin formatlanması
  if regaTarihi.find("-") != -1:
    regaTarihi = datetime.strptime(regaTarihi, "%d-%m-%Y")
  elif regaTarihi.find(".") != -1:
    regaTarihi = datetime.strptime(regaTarihi, "%d.%m.%Y")
  elif regaTarihi.find("/") != -1:
    regaTarihi = datetime.strptime(regaTarihi, "%d/%m/%Y")

  # Mevzuat Tarihi Değerinin çekilip çekilmediğini kontrol ediyoruz.
  if count != 0:
    if mevzuatTarihi.find("\n") != -1:
      mevzuatTarihi = mevzuatTarihi[:mevzuatTarihi.find("\n")]

      if mevzuatTarihi.find("-") != -1:
        mevzuatTarihi = datetime.strptime(mevzuatTarihi, "%d-%m-%Y")
      elif mevzuatTarihi.find(".") != -1:
        mevzuatTarihi = datetime.strptime(mevzuatTarihi, "%d.%m.%Y")
      elif mevzuatTarihi.find("/") != -1:
        mevzuatTarihi = datetime.strptime(mevzuatTarihi, "%d/%m/%Y")

    dogru = 0
    # Değerlerin Asılları ile Karşılaştırılması
    if regaTarihi != dfRegaTarihi:
      a = 1
    else:
      dogru += 1

    if regaNo != dfRegaNo:
      a = 1
    else:
      dogru += 1

    if mevzuatNo != dfMevzuatNo:
      a = 1
    else:
      dogru += 1

    if mevzuatTarihi != dfMevzuatTarihi and temp != 0:
      a = 1
    else:
      dogru += 1

    if dogru == 4:
      return True
    else:
      return False


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def tuzuk_doldur(i):
  print(i)

  rg_trh2 = df.loc[i]['rega_tarihi']
  rg_no2 = int(df.loc[i]['rega_no'])
  bkk_no2 = df.loc[i]['mevzuat_no']
  kr_trh2 = df.loc[i]['mevzuat_tarihi']

  rg_trh2 = tarihduzelt(rg_trh2)
  kr_trh2 = tarihduzelt(kr_trh2)

  metin = df['data_text'][i][:310].lower()  # Verileri çıkarmak için ilk 310 karakter yeterli
  metin = metin.replace('  ', '')

  # Resmi gazete tarihi çıkarma
  baslangic_rgtrh = metin.find('resmî gazete tarihi:')
  baslangic_rgtrh = baslangic_rgtrh + len('resmî gazete tarihi: ')
  rg_trh1 = metin[baslangic_rgtrh:baslangic_rgtrh + 10]
  print(rg_trh1, "->", rg_trh2)

  # Resmi gazete no çıkarma
  baslangic_rgno = metin.find('resmî gazete sayısı: ')
  baslangic_rgno = baslangic_rgno + len('resmî gazete sayısı: ')
  rg_no1 = ''
  rakambuldu = 0
  # Sayının uzunluğu değiştiğinden sabit bir aralık kullanılamıyor
  while metin[baslangic_rgno].isdigit() or rakambuldu == 0:
    if metin[baslangic_rgno] == ' ' or metin[baslangic_rgno] == '\n':
      rakambuldu = 0
    elif metin[baslangic_rgno].isdigit():
      rakambuldu = 1
      rg_no1 = rg_no1 + metin[baslangic_rgno]
    baslangic_rgno = baslangic_rgno + 1
  rg_no1 = int(rg_no1)
  print(rg_no1, "->", rg_no2)

  # Resmi gazete no ile aynı mantık sadece gördüğü '/' karakterlerini de dahil ediyor sayıya
  baslangic_bkkno = metin.find('bkk no: ')
  baslangic_bkkno = baslangic_bkkno + len('bkk no: ')
  bkk_no1 = ''
  raambuldu = 0
  while metin[baslangic_bkkno].isdigit() or rakambuldu == 0 or metin[baslangic_bkkno] == '/':
    if metin[baslangic_bkkno] == ' ' or metin[baslangic_bkkno] == '\n':
      rakambuldu = 0
    elif metin[baslangic_bkkno].isdigit() or metin[baslangic_bkkno] == '/':
      rakambuldu = 1
      bkk_no1 = bkk_no1 + metin[baslangic_bkkno]
    baslangic_bkkno = baslangic_bkkno + 1
  bkk_no1 = bkk_no1
  print(bkk_no1, "->", bkk_no2)

  baslangic_krtrh = metin.find('karar tarihi: ')
  baslangic_krtrh = baslangic_krtrh + len('karar tarihi: ')
  kr_trh1 = metin[baslangic_krtrh:baslangic_krtrh + 10]
  if kr_trh1[9].isdigit() != True:
    kr_trh1 = kr_trh1[:9]
  elif kr_trh1[8].isdigit() != True:
    kr_trh1 = kr_trh1[:8]

  kr_trh1 = kr_trh1.replace('\n', '')
  kr_trh1 = kr_trh1.replace(' ', '')
  print(kr_trh1, "->", kr_trh2)

  rg_trh1 = tarihduzelt(rg_trh1)
  kr_trh1 = tarihduzelt(kr_trh1)

  dogru = 0
  if rg_no1 == rg_no2:
    dogru += 1
  else:
    print("*rg no* cevap:", rg_no1, " doğrusu:", rg_no2)

  if rg_trh1 == rg_trh2:
    dogru += 1
  else:
    print("*rg_tarih* cevap:", rg_trh1, " doğrusu:", rg_trh2)

  if bkk_no1 == bkk_no2:
    dogru += 1
  else:
    print("*kn_no* cevap:", bkk_no1, " doğrusu:", bkk_no2)

  if kr_trh1 == kr_trh2:
    dogru += 1
  else:
    print("*kn_trh* cevap:", kr_trh1, " doğrusu:", kr_trh2)

  if dogru == 4:
    return True
  else:
    return False


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def ozelge_doldur(i):
  print(i)
  metin = df['data_text'][i][:280].lower()  # Verileri çıkarmak için ilk 310 karakter yeterli
  metin = metin.replace('  ', '')
  metin = metin.replace('\n', '')

  if metin.find("tarih: ") != -1:
    bas = metin.find("tarih: ") + len("tarih: ")
    if metin[bas] == ' ':
      bas += 1
    tarih = metin[bas:bas + 10]
    print(tarih, "1")

  elif metin.find("tarih : ") != -1:
    bas = metin.find("tarih : ") + len("tarih : ")
    if metin[bas] == ' ':
      bas += 1
    tarih = metin[bas:bas + 10]
    print(tarih, "2")

  elif metin.find("tari̇h: ") != -1:  # boynuzlu h için
    bas = metin.find("tari̇h: ") + len("tari̇h: ")
    if metin[bas] == ' ':
      bas += 1
    tarih = metin[bas:bas + 10]
    print(tarih, "2")

  elif metin.find("tarih") != -1 and metin[metin.find("tarih") + 5].isdigit:
    bas = metin.find("tarih") + len("tarih")
    tarih = metin[bas:bas + 10]
    print(tarih, "3")

  elif metin.find("konu") != -1:
    bas = metin.find("konu") - 11
    tarih = metin[bas:bas + 10]
    print(tarih, "4")

  kr_trh1 = tarihduzelt(tarih)

  kr_trh2 = df["mevzuat_tarihi"][i]
  kr_trh2 = tarihduzelt(kr_trh2)

  if kr_trh1 == kr_trh2:
    return True
  else:
    return False


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def yonetmelik_doldur(i):
  print(i)

  rg_trh2 = df.loc[i]['rega_tarihi']
  rg_no2 = df.loc[i]['rega_no']
  if type(rg_no2) is str:
    kes = rg_no2.find(" ")
    if kes != -1:
      rg_no2 = rg_no2[:kes]
  if pd.isna(rg_no2) == False:
    rg_no2 = int(rg_no2)

  rg_trh2 = tarihduzelt(rg_trh2)

  metin = df['data_text'][i][:310].lower()  # Verileri çıkarmak için ilk 310 karakter yeterli
  metin = metin.replace('  ', '')

  # Resmi gazete tarihi çıkarma
  baslangic_rgtrh = metin.find('resmî gazete tarihi:')
  baslangic_rgtrh = baslangic_rgtrh + len('resmî gazete tarihi: ')
  rg_trh1 = metin[baslangic_rgtrh:baslangic_rgtrh + 10]
  print(rg_trh1, "->", rg_trh2)

  # Resmi gazete no çıkarma
  baslangic_rgno = metin.find('resmî gazete sayısı: ')
  baslangic_rgno = baslangic_rgno + len('resmî gazete sayısı: ')
  rg_no1 = ''
  rakambuldu = 0
  # Sayının uzunluğu değiştiğinden sabit bir aralık kullanılamıyor
  while metin[baslangic_rgno].isdigit() or rakambuldu == 0:
    if metin[baslangic_rgno] == ' ' or metin[baslangic_rgno] == '\n':
      rakambuldu = 0
    elif metin[baslangic_rgno].isdigit():
      rakambuldu = 1
      rg_no1 = rg_no1 + metin[baslangic_rgno]
    baslangic_rgno = baslangic_rgno + 1
  rg_no1 = int(rg_no1)
  print(rg_no1, "->", rg_no2)

  rg_trh1 = tarihduzelt(rg_trh1)

  dogru = 0
  if rg_no1 == rg_no2:
    dogru += 1
  else:
    print("*rg no* cevap:", rg_no1, " doğrusu:", rg_no2)

  if rg_trh1 == rg_trh2:
    dogru += 1
  else:
    print("*rg_tarih* cevap:", rg_trh1, " doğrusu:", rg_trh2)

  if dogru == 2:
    return True
  else:
    return False


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def veriIslemeREGANO(satir):
  df.loc[satir, 'data_text'] = str(df['data_text'][satir]).lower()
  df.loc[satir, 'data_text'] = str(df['data_text'][satir]).replace(' ', '')
  df.loc[satir, 'data_text'] = str(df['data_text'][satir]).replace('\n', '')
  df.loc[satir, 'data_text'] = str(df['data_text'][satir]).replace('\r', '')

  icerik = str(df['data_text'][satir])
  sayininOlduguYer = icerik.find('sayı')
  if sayininOlduguYer == -1:
    return 0
  sayininBasi = sayininOlduguYer
  sayininSonu = 0
  while not icerik[sayininBasi].isnumeric():
    sayininBasi += 1
    if sayininBasi == len(icerik):
      return 0
  sayininSonu = sayininBasi
  while icerik[sayininSonu].isnumeric():
    sayininSonu += 1
  bulunan_rega_no = icerik[sayininBasi:sayininSonu]
  olmasigereken_rega_no = df['rega_no'][satir]
  if bulunan_rega_no != olmasigereken_rega_no:
    return 1
  else:
    return 0


# Önce Sayıları Bulduralım
satirToplami, sutunToplami = df.shape
hataSay = 0
for satirNo in range(satirToplami):
  if df['kategori'][satirNo] == 'Resmi Gazete':
    if veriIslemeREGANO(satirNo):
      hataSay += 1
print('Fonksiyon bu hali ile RESMİ GAZETE kategorisindeki dokümanın içinden', (546 - hataSay) / 546,
      'başarı oranı ile rega_no bulabiliyor!')


def agirlikBul(kelime):
  agirlik = 0
  for harf in kelime:
    agirlik += ord(harf)
  return agirlik


def ayinAgirliginaBakipTahminYap(gelenVeri, satir):
  gelenVeri = gelenVeri.replace('ṡ', 's')
  gelenVeri = gelenVeri.replace('ṙ', 'r')
  gelenVeri = gelenVeri.replace('ṁ', 'm')
  gelenVeri = gelenVeri.replace('ṅ', 'n')
  gelenVeri = gelenVeri.replace('ı', 'i')
  gelenVeri = gelenVeri.replace('ş', 's')
  gelenVeri = gelenVeri.replace('ğ', 'g')
  gelenVeri = gelenVeri.replace('ü', 'u')
  gelenVeri = gelenVeri.replace('i̇', 'i')
  gelenVeri = gelenVeri.replace('î', 'i')

  hesapliListe = [414, 543, 436, 537, 547, 749, 674, 774, 555, 422, 533, 628]
  agirlik = 0
  for g in gelenVeri:
    agirlik += ord(g)
  farklar = []
  for s in hesapliListe:
    farklar.append(abs(s - agirlik))
  return farklar.index(min(farklar)) + 1


def resmiGazeteyeregaNoIsle(satir):
  icerik = str(df['data_text'][satir])
  sayininOlduguYer = icerik.find('sayı')
  if sayininOlduguYer == -1:
    return 0
  sayininBasi = sayininOlduguYer
  sayininSonu = 0
  while not icerik[sayininBasi].isnumeric():
    sayininBasi += 1
    if sayininBasi == len(icerik):
      return 0
  sayininSonu = sayininBasi
  while icerik[sayininSonu].isnumeric():
    sayininSonu += 1
  return icerik[sayininBasi:sayininSonu]


def veriIslemeREGATRH(satir):
  # İletilen satır numaralı kayda hem rega_no'yu işleyeceğiz hem de rega_tarihi için numarayı kullanacağız.
  icerik = str(df['data_text'][satir])
  # Eğer resmiGazeteyeregaNoIsle fonksiyonu sayıyı bulamazsa aşağıdaki koşul çalışmayacaktır.
  # Eğer bulursa resmi gazete tarihi resmi gazete sayısından önce olduğu için tüm belgede arama yapmamıza gerek kalmaz
  if resmiGazeteyeregaNoIsle(satir):
    icerik = str(df['data_text'][satir][:icerik.find('sayı')])

  # Şimdi rega_tarihi bulacağız
  # Resmi gazete tarihi XX AY XXXX şeklinde bir biçime sahip yani AY yazı ile veriliyor!
  # Resmi gazete tarihi kuruluş tarihinden sonra veriliyor

  # Öyleyse aramayı baştan da daraltabiliriz.
  kurulusTarihininOlduguYer = icerik.find('tarihi')
  icerik = icerik[kurulusTarihininOlduguYer + 15:]
  # sayı ve tarih birbirine yakın olduğu için baştan değil de sondan arama yapmak için içeriği bir de ters çevirelim.
  icerik = icerik[::-1]

  # Aramaya başlamadan istisnaları da çıkartalım
  # 'tarihlive' diye baslayan içerikten doğrudan çekim yapılabilir.
  tarihAcikISE = icerik.find('evilhirat')
  if tarihAcikISE != -1:
    istisna = []
    istisna.append(icerik[tarihAcikISE + 9:tarihAcikISE + 13][::-1])
    istisnaAY_Basla = tarihAcikISE + 13
    while not icerik[istisnaAY_Basla].isnumeric():
      istisnaAY_Basla += 1
      if istisnaAY_Basla == len(icerik):
        return 0
    istisna.append(icerik[tarihAcikISE + 13:istisnaAY_Basla][::-1])
    ay = str(ayinAgirliginaBakipTahminYap(istisna[1], satir))
    if len(ay) == 1:
      ay = '0' + ay
    istisna[1] = ay
    if icerik[istisnaAY_Basla + 1].isnumeric():
      istisna.append(icerik[istisnaAY_Basla:istisnaAY_Basla + 2])
    else:
      istisna.append(icerik[istisnaAY_Basla:istisnaAY_Basla + 1])
    if str(df['rega_tarihi'][satir]).replace('.', '').replace('-', '').replace('/', '') == str(istisna).replace("'",
                                                                                                                '').replace(
      '[', '').replace(']', '').replace(',', '').replace(' ', ''):
      return 1
    return 0

  # Şimdi aramaya başlayabiliriz.
  bulunan = []
  # İlk bulduğumuz sayı tarihin başladığı ilk bulduğumuz metin ay ve ilk bulduğumuz sayı tekrar tarihin başladığı yer olabilir.
  sayininBasi = 0
  sayininSonu = 0

  while not icerik[sayininBasi].isnumeric():
    sayininBasi += 1
    if sayininBasi == len(icerik):
      return 0

  sayininSonu = sayininBasi
  while icerik[sayininSonu].isnumeric():
    sayininSonu += 1
  bulunan.append(icerik[sayininBasi:sayininSonu])
  # Dokümandaki ilk sayıyı aldık!
  sayininBasi = sayininSonu
  while not icerik[sayininSonu].isnumeric():
    sayininSonu += 1
    if sayininSonu == len(icerik):
      return 0
  bulunan.append(icerik[sayininBasi:sayininSonu])
  # Dokümandaki ay olarak dusunduğumuz kısmı aldık
  sayininBasi = sayininSonu
  while icerik[sayininSonu].isnumeric():
    sayininSonu += 1
    if sayininSonu == len(icerik):
      return 0
  bulunan.append(icerik[sayininBasi:sayininSonu])
  # Dokümandaki yıl olarak dusunduğumuz sayıyı aldık!
  ay = str(ayinAgirliginaBakipTahminYap(bulunan[1], satir))
  if len(ay) == 1:
    ay = '0' + ay
  bulunan[1] = ay
  if len(bulunan[2]) == 1:
    bulunan[2] = str(bulunan[2]) + '0'
  bulunan[2] = bulunan[2][::-1]
  bulunan[0] = bulunan[0][::-1]
  if str(df['rega_tarihi'][satir]).replace('.', '').replace('-', '').replace('/', '') == str(bulunan).replace("'",
                                                                                                              '').replace(
    '[', '').replace(']', '').replace(',', '').replace(' ', ''):
    return 1
  return 0


# Şimdi rega_no'ları işletip tarihleri bulalım
satirToplami, sutunToplami = df.shape
hataSay = 0
for satirNo in range(satirToplami):
  if df['kategori'][satirNo] == 'Resmi Gazete':
    if not veriIslemeREGATRH(satirNo):
      hataSay += 1

print('Fonksiyon bu hali ile RESMİ GAZETE kategorisindeki dokümanın içinden', (546 - hataSay) / 546,
      'başarı oranı ile rega_tarihi bulabiliyor!')


def gazete_doldur(i):
  if veriIslemeREGATRH(i) and veriIslemeREGANO(i):
    return True
  else:
    return False


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


def metinSayi(exmetin):
  exmetin = exmetin.replace('S. Sayısı :.', 'S. Sayısı :')
  exmetin = exmetin.replace('S. Sayısı:', 'S. Sayısı :')
  exmetin = exmetin.replace('s. sAYisı :', 'S. Sayısı :')
  exmetin = exmetin.replace('S. Sayisi:', 'S. Sayısı :')
  exmetin = exmetin.replace('S. SAYISI :', 'S. Sayısı :')
  return exmetin


def komisyonraporu_doldur(i):
  try:
    metin = df['data_text'][i]
    # metin = metinDonem(metin)

    dogru = 0

    # Asıl değerlerin alınması ve formatlanması

    dfDonem = df['donem'][i].split('.')[0]
    dfSiraNo = df['sira_no'][i].split(" ek ")

    # 'donem' değerini bulan kod

    donem = ''
    if metin.find('Dönem') != -1:
      donemIndex = metin.find('Dönem')
      donemIndex = donemIndex + len('Dönem')

    elif metin.find('YASAMA YILI') != -1:
      donemIndex = metin.find('YASAMA YILI')
      donemIndex = donemIndex + len('YASAMA YILI')

    else:
      donem = '0'

    rakambuldu = 0
    while metin[donemIndex].isdigit() or rakambuldu == 0 and donem != '0':
      if metin[donemIndex] == ' ' or metin[donemIndex] == '\n':
        rakambuldu = 0
      elif metin[donemIndex].isdigit():
        rakambuldu = 1
        donem = donem + metin[donemIndex]
      elif metin[donemIndex] == 'α':
        donem = ''
        break
      donemIndex += 1

    donem = int(donem)

    if int(dfDonem) >= 21 and donem != int(dfDonem):
      print(i, " DonemHatası ", '|', donem, '|', dfDonem, '|', sep='')
    else:
      dogru += 1

    # 'sira_no' değerini bulan kod
    metin = metinSayi(metin)

    if metin.find('S. Sayısı :') != -1:
      siraNoIndex = metin.find('S. Sayısı :')
      siraNoIndex += len('S. Sayısı :')

    siraNo1 = ''
    rakambuldu = 0
    eskiIndex = 0
    while metin[siraNoIndex].isdigit() or rakambuldu == 0:
      if metin[siraNoIndex] == ' ' or metin[siraNoIndex] == '\n':
        rakambuldu = 0

      elif metin[siraNoIndex].isdigit():
        rakambuldu = 1
        eskiIndex = siraNoIndex
        siraNo1 = siraNo1 + metin[siraNoIndex]
      siraNoIndex += 1

    siraNo2 = ''
    rakambuldu = 0
    count = 0

    if metin.find("ek", eskiIndex) != -1 and metin.find("ek", eskiIndex) - eskiIndex < 15:
      siraNoIndex = metin.find("ek", eskiIndex)
      siraNoIndex += len("ek")
      count = 1

      while metin[siraNoIndex].isdigit() or rakambuldu == 0:
        if metin[siraNoIndex] == ' ' or metin[siraNoIndex] == '\n':
          rakambuldu = 0

        elif metin[siraNoIndex].isdigit():
          rakambuldu = 1
          count = 0
          siraNo2 = siraNo2 + metin[siraNoIndex]

        else:
          break

        siraNoIndex += 1

      if count == 1:
        siraNo2 = '1'

    if siraNo2 == '':
      siraNoToplam = siraNo1
    else:
      siraNoToplam = siraNo1 + ' ek ' + siraNo2

    dfSiraNo = df['sira_no'][i]

    if siraNoToplam != dfSiraNo:
      print(i, " SıraNoHatası ", '|', siraNoToplam, '|', dfSiraNo, '|', sep='')
    else:
      dogru += 1

    if dogru == 2:
      return True
    else:
      return False

  except:
    pass


# ----------------------------------------------------------------------------------------------------------------------#


# Veri iskeletimiz içinde toplam kaç satir / kayıt ve sütun / alan olduğunu satirToplami ve sutunToplami değişkenlerinde saklıyoruz.
satirToplami, sutunToplami = df.shape
dogru = 0
yanlis = 0

doldur_dogru = 0
doldur_yanlis = 0

"""hataSay = 0
for satirNo in range(satirToplami):
  if df['kategori'][satirNo]=='Resmi Gazete':
    if not veriIslemeREGATRH(satirNo):
      hataSay += 1

print('Fonksiyon bu hali ile RESMİ GAZETE kategorisindeki dokümanın içinden',(546-hataSay)/546,'başarı oranı ile rega_tarihi bulabiliyor!')


print("tits")"""

for satir in range(satirToplami):
  arastirilacakParca = df['data_text'][satir][:310]
  cikti = kategoriBul(arastirilacakParca)

  try:
    if cikti == 'Cumhurbaşkanlığı Kararnamesi':
      df2.loc[satirToplami, "kategori"] = "Cumhurbaşkanlığı Kararnamesi"
      cumhurbaskank_doldur(satir)

    elif cikti == 'Resmi Gazete':
      df2.loc[satirToplami, "kategori"] = "Resmi Gazete"
      gazete_doldur(satir)

    elif cikti == 'Tüzük':
      df2.loc[satirToplami, "kategori"] = "Tüzük"
      tuzuk_doldur(satir)

    elif cikti == 'Kanun Hükmünde Kararname':
      df2.loc[satirToplami, "kategori"] = "Kanun Hükmünde Kararname"
      khk_doldur(satir)

    elif cikti == 'Kanun':
      df2.loc[satirToplami, "kategori"] = "Kanun"
      kanun_doldur(satir)

    elif cikti == 'Özelge':
      df2.loc[satirToplami, "kategori"] = "Özelge"
      ozelge_doldur(satir)

    elif cikti == 'Komisyon Raporu':
      df2.loc[satirToplami, "kategori"] = "Komisyon Raporu"
      komisyonraporu_doldur(satir)

    elif cikti == 'Genelge':
      df2.loc[satirToplami, "kategori"] = "Genelge"
      genelge_doldur(satir)

    elif cikti == 'Yönetmelik':
      df2.loc[satirToplami, "kategori"] = "Yönetmelik"
      yonetmelik_doldur(satir)

    elif cikti == 'Tebliğ':
      df2.loc[satirToplami, "kategori"] = "Tebliğ"
      teblig_doldur(satir)

    else:
      print("hata")
  except:
    print("Kritik Hata!")

try:
  mukerrerno_doldur()
  maddesay_doldur()
except:
  print("hata")
# Son testte 4142 belgeden 3821'i doğru sınıflandırılıp 321 hatalı sınıflandırma mevcuttur. Bu da yaklaşık olarak 0.922 başarı oranına denk gelmektedir.

df2= df2.drop(labels="data_text", axis=1)
df2.to_csv('asd3.csv', index = False)
