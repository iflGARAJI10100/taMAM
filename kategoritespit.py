import pandas as pd


def kategoriBul(verilenMetin):

  verilenMetin = verilenMetin.replace('  ','')
  verilenMetin = verilenMetin.replace('\n','')
  verilenMetin = verilenMetin.replace('\r','')
  # data_text alanındaki kayıdın ilk parçasında "CUMHURBAŞKANLIĞI KARARNAMESİ" ifadesi varsa o bir Cumhurbaşkanlığı Kararnamesi'dir önermesini kontrol ediyoruz!
  if verilenMetin.find('CUMHURBAŞKANLIĞI KARARNAMESİ')!=-1:
    return 'Cumhurbaşkanlığı Kararnamesi'

  # data_text alanındaki kayıdın ilk parçasında "BKK No:" ifadesi varsa o bir Tüzük'tür önermesini kontrol ediyoruz!
  elif verilenMetin.find('BKK No:')!=-1:
    return 'Tüzük'

  # data_text alanındaki kayıdın ilk parçasında Mevzuat No'yu oluşturan parçalardan biri olan "KHK" ifadesi varsa o bir kanundur önermesini kontrol ediyoruz!
  elif verilenMetin.find('KHK')!=-1:
    return 'Kanun Hükmünde Kararname'

  # data_text alanındaki kayıdın ilk parçasında Kanun No varsa o bir kanundur önermesini kontrol ediyoruz!
  elif verilenMetin.find('Kanun No')!=-1:
    return 'Kanun'

  komisyonMetin = verilenMetin.replace(' ','')
  komisyonMetin = komisyonMetin.replace(':','')
  komisyonMetin = komisyonMetin.replace('.','')
  komisyonMetin = komisyonMetin.replace('ý','ı')
  # data_text alanındaki kayıdın ilk parçasında ne varsa o bir Komisyon Raporudur diye kontrol ediyoruz!
  if komisyonMetin.lower().find('kanuntasarisi')!=-1 or komisyonMetin.lower().find('yasamayili')!=-1 or komisyonMetin.lower().find('tbmm')!=-1 or komisyonMetin.lower().find('komisyonraporu')!=-1 or komisyonMetin.lower().find('ssayısı')!=-1 or komisyonMetin.lower().find('ssayisi')!=-1 or komisyonMetin.lower().find('sirano')!=-1 or komisyonMetin.lower().find('sırano')!=-1 or komisyonMetin.lower().find('ilâve')!=-1:
    return 'Komisyon Raporu'

  genelgeMetin = verilenMetin.replace(' ','')
  # data_text alanındaki kayıdın ilk parçasında erik: varsa o bir genelgedir önermesini kontrol ediyoruz!
  if genelgeMetin.lower().find('genelge')!=-1 or genelgeMetin.lower().find('genelyazi')!=-1:
    return 'Genelge'

   # data_text alanındaki kayıdın ilk parçasında  olan "T.C.", "Gelir" veya "GELİR" ifadelerinden biri varsa o bir Özelge'dir önermesini kontrol ediyoruz!
  if  verilenMetin.find('T.C.') != -1  or verilenMetin.find('Gelir') != -1 or verilenMetin.find('GELİR') != -1 :
    return 'Özelge'

  yonetmelikMetin = verilenMetin.replace(' ','')
  yonetmelikMetin = yonetmelikMetin.replace(':','')
  yonetmelikMetin = yonetmelikMetin.replace('.','')
  yonetmelikMetin = yonetmelikMetin.replace('ý','ı')
  yonetmelikMetin = yonetmelikMetin.replace('i̇','i')
  # data_text alanındaki kayıdın ilk parçasında ne varsa o bir YÖNETMELİKTİR diye kontrol ediyoruz!
  if yonetmelikMetin.lower().find('yönetmeli')!=-1 or yonetmelikMetin.lower().find('yönetmeli̇')!=-1:
    return 'Yönetmelik'

  tebligMetin = verilenMetin.replace(' ','')
  tebligMetin = tebligMetin.replace(':','')
  tebligMetin = tebligMetin.replace('.','')
  tebligMetin = tebligMetin.replace('ý','ı')
  tebligMetin = tebligMetin.replace('i̇','i')
  # data_text alanındaki kayıdın ilk parçasında ne varsa o bir YÖNETMELİKTİR diye kontrol ediyoruz!
  if tebligMetin.lower().find('tebl')!=-1:
    return 'Tebliğ'

  # data_text alanındaki kayıdın ilk parçasında Mevzuat No'yu oluşturan parçalardan biri olan "KHK" ifadesi varsa o bir kanundur önermesini kontrol ediyoruz!
  metin = verilenMetin.lower()
  #if verilenMetin.find('Gazete')!=-1:
  if metin.find("gazete") != -1 and (metin.find("kuruluş") != -1 or metin.find("tesis") != -1) and (metin.find("1920") != -1 or metin.find("1336") != -1):
    return 'Resmi Gazete'

df = pd.read_csv('kanunum-nlp-doc-analysis-dataset.csv')
df.info(verbose=True)

# Veri iskeletimiz içinde toplam kaç satir / kayıt ve sütun / alan olduğunu satirToplami ve sutunToplami değişkenlerinde saklıyoruz.
satirToplami, sutunToplami = df.shape
dogru = 0
yanlis = 0

for satir in range(satirToplami):
  arastirilacakParca = df['data_text'][satir]
  cikti = kategoriBul(arastirilacakParca)

  if cikti == 'Cumhurbaşkanlığı Kararnamesi' and df['kategori'][satir] == 'Cumhurbaşkanlığı Kararnamesi':
    dogru += 1
    print(satir, cikti, 'CK')
  elif cikti == 'Resmi Gazete' and df['kategori'][satir] == 'Resmi Gazete':
    dogru += 1
  elif cikti == 'Tüzük' and df['kategori'][satir] == 'Tüzük':
    dogru += 1
    print(satir, cikti, 'Tüzük')
  elif cikti == 'Kanun Hükmünde Kararname' and df['kategori'][satir] == 'Kanun Hükmünde Kararname':
    dogru += 1
    print(satir, cikti, 'KHK')
  elif cikti == 'Kanun' and df['kategori'][satir] == 'Kanun':
    dogru += 1
    print(satir, cikti, 'Kanun')
  elif cikti == 'Özelge' and df['kategori'][satir] == 'Özelge':
    dogru += 1
    print(satir, cikti, 'Özelge')
  elif cikti == 'Komisyon Raporu' and df['kategori'][satir] == 'Komisyon Raporu':
    dogru += 1
    print(satir, cikti, 'KR')
  elif cikti == 'Genelge' and df['kategori'][satir] == 'Genelge':
    dogru += 1
    print(satir, cikti, 'Genelge')
  #özelge
  elif cikti == 'Yönetmelik' and df['kategori'][satir] == 'Yönetmelik':
    dogru += 1
    print(satir, cikti, 'Yönetmelik')
  elif cikti == 'Tebliğ' and df['kategori'][satir] == 'Tebliğ':
    dogru += 1
    print(satir, cikti, 'Tebliğ')

    print(satir, cikti, 'RG')
  else:
    yanlis += 1
    print(satir, cikti, df['kategori'][satir])

print(dogru, yanlis)