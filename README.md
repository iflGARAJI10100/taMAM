![image](https://github.com/iflGARAJI10100/taMAM/blob/main/taMAM%20Proje%20Logo.png)

# taMAM | Tarayıcı Mevzuat Arama Motoru

## Proje Bağlılık Listesi
### Projenin Çalışması için Gerekli Dosyalar

|Dosya Adı|İşlevi|
|:---:|:---:|
|[main.py](https://github.com/iflGARAJI10100/taMAM/blob/main/main.py)|Yarışmada kullanılacak bütün kodları içeren toplam kod|
|[kanunum-nlp-doc-analysis-dataset.csv](https://www.kanunum.com/)|Kanunum (Karakullukçu Danışmanlık A.Ş.) tarafından hazırlanan Veri Seti|

### Projenin Çalışması için Gerekli Kurulumlar
Ayrıca [Gereksinimler.txt](https://github.com/iflGARAJI10100/taMAM/blob/main/Gereksinimler.txt) dosyasını da inceleyebilirsiniz.

|Dosya Adı|Pip ile İndirme|PyPI Sitesi|
|:---:|:---:|:---:|
|pip 22.2.2|-|https://pypi.org/project/pip/|
|transformers 4.20.1|pip install transformers|https://pypi.org/project/transformers/|
|pandas 1.3.5|pip install pandas|https://pypi.org/project/pandas/|
|google colab 1.0.0|-|-|
|datetime 4.5|pip install DateTime|https://pypi.org/project/DateTime/|
|matplotlib 3.2.2|pip install matplotlib|https://pypi.org/project/matplotlib/|
|numpy 1.21.6|pip install numpy|https://pypi.org/project/numpy/|

### Proje'nin Community Standarts Dosyaları

|Dosya Adı|Link|
|:---:|:---:|
|README.md|https://github.com/iflGARAJI10100/taMAM/blob/main/README.md|
|CODE_OF_CONDUCT.md|https://github.com/iflGARAJI10100/taMAM/blob/main/CODE_OF_CONDUCT.md|
|CONTRIBUTING.md|https://github.com/iflGARAJI10100/taMAM/blob/main/CONTRIBUTING.md|
|LICENSE|https://github.com/iflGARAJI10100/taMAM/blob/main/LICENSE|

## taMAM | Tarayıcı Arama Motoru'nun Modülleri, İşlevleri ve Doğruluk Değerleri
Daha detaylı bilgilendrime için [ProjeGelişimDokumani.md](https://github.com/iflGARAJI10100/taMAM/blob/main/ProjeGeli%C5%9FimDok%C3%BCman%C4%B1.md) dosyasını inceleyebilirsiniz.

### 1. Kural Bazlı Madde Sayısı Tespit Modülü
 - Belge Dökümantasyonuna [Buradan](https://github.com/iflGARAJI10100/taMAM/blob/main/aramaProjesiMaddeSayisiBulmaMod%C3%BCl%C3%BC.ipynb) ulaşabilirsiniz. 
 - YÖNTEM: "Madde XX -" bu yapı doküman içinde parça parça aranır, yapı tespit edildiğinde XX sayısı alınır, mevcut madde sayısında takip eden sayı bulunmuşsa mevcut madde sayısı güncellenir. İstisnalar olarak EK ve GEÇİCİ için kontrol yapılır.
 
### 2. Kural Bazlı Data_text İçinden Veri Çıkarım Modülü
  - TDDİ yerine kural bazlı çözüm kullanılmıştır.
  - Kural bazlı sistemin ana avantajı TDDİ ye göre oldukça daha hızlı olması, ancak kuralın her kategoride uygulanabilecek bir yöntem olup olmadığı hala test ediliyor.
  - Bulgularımız:
  
  <a href="https://imgur.com/8fmKDCY"><img src="https://i.imgur.com/8fmKDCY.jpg" title="source: imgur.com" /></a>
  
### 3. Belgelerde Kategori Bulma Mödülü
  - YÖNTEM: Kategorilerin "Madde 1"lerine kadar olan kısımları içerisinde kategorilerin türlerini tespit etmeye yarayan özel ifadeleri kural bazlı bir arama ile bulur. Bulunan sonuçlara göre Karmaşıklık Matrisi değerleri çıkartılır.
  
### 4. Mükerrer No Bulma Modülü
  - Belge Dökümantasyonuna [Buradan](https://github.com/iflGARAJI10100/taMAM/blob/main/aramaProjesiVeriIslemeMukerrerNoTespitModulu.ipynb) ulaşabilirsiniz.
  - YÖNTEM: Belgelerin Data_Text alanlarından ilk 310 karakteri çeker ve içlerinde kural bazlı Mükerrer No araması yapar.

## Katkılarından Ötürü Teşekkür Ederiz
- Sayın Furkan KADIOĞLU | Mentör |
- Değerli Sertaç ATEŞ | Danışman Öğretmen |

## Takım Üyeleri
- Eray AKIN               | Takım Kaptanı | [ErAk042](https://github.com/ErAk042)
- Seyithan Toprak GÜNGÖR  | Takım Üyesi | [S-Toprak](https://github.com/S-Toprak)
- Sertaç ATEŞ             | Danışman Öğretmen | [sertacates](https://github.com/sertacates)

## Hakkımızda
**taMAM | Tarayıcı Mevzuat Arama Motoru**, **İFL Garajı 10100** takımı tarafından **Teknofest 2022 Türkçe Doğal Dil İşleme Yarışması** kapsamında düzenlenen Kamuda Arama Motoru Geliştirme alanında yarışması için oluşturulan bir NLP projesidir.

Takımımız İzmir Fen Lisesi 11. Sınıf öğrencilerinden oluşmakta olup adımız olan İFL Garajı 10100 günümüz Arama Motorları arasında akla ilk gelen isimlerden biri olan **Google şirketinin kuruluşuna** ve **Googol** sayısına bir göndermedir.

taMAM projesi **Jupyter Notebook'la yazılmış dökümantasyonlar**, **Python** diliyle hazırlanmış olan ana kodumuz ve Community Standart'la ilgli olan **MarkDown dosyalarından** oluşmaktadır. Proje adı ise Teknofest Organizatörleri tarafından yarışmaya hazırlanmamız için bize verilen Veri Setin'den **veri elde etme şeklimizle** oluşturulmuş bir kısaltmadır.
