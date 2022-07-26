![image](https://github.com/iflGARAJI10100/taMAM/blob/main/taMAM%20Proje%20Logo.png)

# MODÜLLER VE GELİŞİM AŞAMALARI
## 1. Kural Bazlı Madde Sayısı Tespit Modülü
 - YÖNTEM: "Madde XX -" bu yapı doküman içinde parça parça aranır, yapı tespit edildiğinde XX sayısı alınır, mevcut madde sayısında takip eden sayı bulunmuşsa mevcut madde sayısı güncellenir. İstisnalar olarak EK ve GEÇİCİ için kontrol yapılır. İşlenmemiş Madde fonksiyonu düşük verimde çalışmaktadır.
 - Kural bazlı ilk çözümümüz ile ilgili bulgular: 
 
|Kategori|Toplam Belge|Doğru|Yanlış|Doğruluk Oranı|
|---|---|---|---|---|
|Kanun|514|494|20|0.961|
|KHK|91|86|5|0.945|
|Resmi Gazete|546|546|0|1.0|
|Komisyon Raporu|500|500|0|1.0|
|Genelge|385|385|0|1.0|
|Cumhurbaşkanlığı Kararnamesi|54|53|1|0.981|
|Tüzük|82|76|6|0.927|
|Yönetmelik|597|589|8|0.987|
|Tebliğ|623|623|0|1.0|
|Özelge|750|750|0|1.0|
 
## 2. Data_text İçinden Veri Çıkarım Modülü
  - TDDİ yerine kural bazlı çözüm konması ve kıyası
  - Kural bazlı sistemin ana avantajı TDDİ ye göre oldukça daha hızlı olması, ancak kuralın her kategoride uygulanabilecek bir yöntem olup olmadığı hala test ediliyor.
  - Doğruluk oranları:
 <a href="https://imgur.com/8fmKDCY"><img src="https://i.imgur.com/8fmKDCY.jpg" title="source: imgur.com" /></a>

## 3. Belgelerde Kategori Bulma Mödülü
  - YÖNTEM: Kategorilerin "Madde 1"lerine kadar olan kısımları içerisinde kategorilerin türlerini tespit etmeye yarayan özel ifadeleri kural bazlı bir arama ile bulur. Bulunan sonuçlara göre Karmaşıklık Matrisi değerleri çıkartılır.
  - Belge Kategorilerine göre Kural bazlı yöntemlerimiz hakkındaki bulgular:
  - Özellikle Keskinlik alanında çalışmlar yapılması gerekmektedir.
  
  | Yöntem ve Kategori | Doğruluk (Accuracy) | Keskinlik (Precision) | Hassasiyet (Sensisivity) / Duyarlılık (Recall) | Özgüllük (Specifity) | F1 Puanı (F1 Score) |
  |---|---|---|---|---|---|
  |Kural Bazlı Kanun Bulma Yöntemi|0.9864799613713182|0.9017543859649123|1.0|0.9845644983461963|0.9560996218242673|
  |Kural Bazlı Kanun Hükmünde Kararname Bulma Yöntemi|0.9920328343795268|0.7338709677419355|1.0|0.9918538632436436|0.8505075137880636|
  |Kural Bazlı Resmi Gazete Bulma Yöntemi|0.8157894736842105|0.2447058823529412|0.19047619047619047|0.910734149054505|0.080680334748185|
  |Kural Bazlı Komisyon Raporu Bulma Yöntemi|0.9181554804442298|0.5959475566150179|1.0|0.9069192751235585|0.7930809889863655|
  |Kural Bazlı Genelge Bulma Yöntemi|0.9587155963302753|0.6931407942238267|0.9974025974025974|0.9547511312217195|0.8390603993494585| 
  |Kural Bazlı Cumhurbaşkanlığı Kararnamesi Bulma Yöntemi|1.0|1.0|1.0|1.0|1.0|
  |Kural Bazlı Tüzük Bulma Yöntemi|1.0|1.0|1.0|1.0|1.0|
  |Kural Bazlı Yönetmelik Bulma Yöntemi|0.8570738773539353|0.5021132713440406|0.9949748743718593|0.8338504936530324|0.7479096397155272|
  |Kural Bazlı Tebliğ Bulma Yöntemi|0.8027522935779816|0.43226256983240224|0.9935794542536116|0.7689684569479965|0.7150784464491825|
  |Kural Bazlı Özelge Bulma Yöntemi|0.751569290197972|0.42140845070422533|0.9973333333333333|0.6972287735849056|0.751422687731069|
  

## 4. Mükerrer No Bulma Modülü
  - YÖNTEM: Belgelerin Data_Text alanlarından ilk 310 karakteri çeker ve içlerinde kural bazlı Mükerrer No araması yapar.
  - Data_text alanından Mükerrer No'yu bulan Kural Bazlı Modülümüz hakkındaki bulgularımız:
  - Yapyığımız geliştirmeler sonucunda modül, 4142 dosya arasından **22** hata ile **0.99** doğruluk oranı ile çalışmaktadır.
  - Data_text içinde geçen "Mükerrer" ifadelerinin Maddeler içinde olup olmadığının tespit edilmesi konusunda çalışmlar yapılması gerekmektedir.

  |Kategori|Toplam Belge|Doğru|Yanlış|Doğruluk Oranı|
  |---|---|---|---|---|
  |Kanun|514|514|0|1.0|
  |Kanun Hükmünde Kararname|91|91|0|1.0|
  |Resmi Gazete|546|546|0|1.0|
  |Komisyon Raporu|500|500|0|1.0|
  |Genelge|385|385|0|1.0|
  |Cumhurbaşkanlığı Kararnamesi|54|54|0|1.0|
  |Tüzük|82|82|0|1.0|
  |Yönetmelik|597|596|1|0.998|
  |Tebliğ|623|602|21|0.966|
  |Özelge|750|750|0|1.0|
