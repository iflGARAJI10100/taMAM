
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

## 3. Belgelerde Kategori Bulma Mödülü
  - Belge Kategorilerine göre Kural bazlı yöntemlerimiz hakkındaki bulgular:
  
  
  | Yöntem ve Kategori | Doğruluk (Accuracy) | Keskinlik (Precision) | Hassasiyet (Sensisivity) / Duyarlılık (Recall) | Özgüllük (Specifity) | F1 Puanı (F1 Score) |
  |---|---|---|---|---|---|
  |Kural Bazlı Kanun Bulma Yöntemi|A|A|A|A|A|
  |Kural Bazlı Genelge Bulma Yöntemi|0.9587155963302753|0.6931407942238267|0.9974025974025974|0.9547511312217195|0.8390603993494585|
  |Kural Bazlı Komisyon Raporu Bulma Yöntemi|A|A|A|A|A|
  |Kural Bazlı Tebliğ Bulma Yöntemi|A|A|A|A|A|
  |Kural Bazlı Yönetmelik Bulma Yöntemi|A|A|A|A|A|
