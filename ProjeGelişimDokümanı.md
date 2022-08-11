
# MODÜLLER VE GELİŞİM AŞAMALARI
## 1. Madde Sayısı Modülü
  - Kural bazlı ilk çözümümüz ile ilgili bulgular: 
  - Toplam kontrol edilen belge sayısı (Kanun): 514
  - Toplam hatalı kayıt sayısı (Kanun): 73
  - Doğruluk Oranı (Kanun): 0.857976653696498
  - YÖNTEM: "Madde XX -" bu yapı doküman içinde parça parça aranır, yapı tespit edildiğinde XX sayısı alınır, mevcut madde sayısında takip eden sayı bulunmuşsa mevcut madde sayısı güncellenir. İstisnalar olarak EK ve GEÇİCİ için kontrol yapılır. İşlenmemiş Madde fonksiyonu düşük verimde çalışmaktadır.

## 2. Data_text İçinden Veri Çıkarım Modülü
  - TDDİ yerine kural bazlı çözüm konması ve kıyası
  - Doğruluk oranları(Kanun kategorisinde)
    - TDDİ-"savasy/bert-base-turkish-squad" : 377/380
    - Kural bazlı çözüm : 513/513 
  - Kural bazlı sistemin ana avantajı TDDİ ye göre oldukça daha hızlı olması, ancak kuralın her kategoride uygulanabilecek bir yöntem olup olmadığı hala test ediliyor.
  
 <a href="https://imgur.com/qbhidSC"><img src="https://i.imgur.com/qbhidSC.png" title="source: imgur.com" /></a>

## 3. Belgelerde Kategori Bulma Mödülü
  - Belge Kategorilerine göre Kural bazlı yöntemlerimiz hakkındaki bulgular:
  - Özellikle Keskinlik alanında çalışmlar yapılması gerekmektedir.
  
  | Yöntem ve Kategori | Doğruluk (Accuracy) | Keskinlik (Precision) | Hassasiyet (Sensisivity) / Duyarlılık (Recall) | Özgüllük (Specifity) | F1 Puanı (F1 Score) |
  |---|---|---|---|---|---|
  |Kural Bazlı Kanun Bulma Yöntemi|0.9864799613713182|0.9017543859649123|1.0| 0.9845644983461963|0.9560996218242673|
  |Kural Bazlı Kanun Hükmünde Kararname Bulma Yöntemi|0.9587155963302753|0.6931407942238267|0.9974025974025974|0.9547511312217195|0.8390603993494585|
  |Kural Bazlı Resmi Gazete Bulma Yöntemi|0.8157894736842105|0.2447058823529412|0.19047619047619047|0.910734149054505|0.080680334748185|
  |Kural Bazlı Komisyon Raporu Bulma Yöntemi|0.9181554804442298|0.5959475566150179|1.0|0.9069192751235585|0.7930809889863655|
  |Kural Bazlı Tebliğ Bulma Yöntemi|0.8027522935779816|0.43226256983240224|0.9935794542536116|0.7689684569479965|0.7150784464491825|
  |Kural Bazlı Yönetmelik Bulma Yöntemi|0.8570738773539353|0.5021132713440406|0.9949748743718593|0.8338504936530324|0.7479096397155272|
