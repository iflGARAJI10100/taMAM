# taMAM

## Takım Kaptanı
### Eray AKIN

## Takım Üyesi
### Seyithan Toprak GÜNGÖR

## Danışman Öğretmen
### Sertaç ATEŞ

#Alanlar:#
-id : İçerik kimliği
-kategori : İçerik Türü/Kategorisi
-baslik : İçerik Başlığı
-rega_no : İçeriğin yayınlandığı Resmi Gazete Sayısı
-mukerrer_no : İçeriğin yayınlandığı Resmi Gazete Mükerrer Numarası (0 ise mükerrer olmadığını belirtir)
-rega_tarihi : İçeriğin yayınlandığı Resmi Gazete Tarihi (date:yyyy-mm-dd formatında)
-kurum : İçeriği(Genelge, Cumhurbaşkanlığı(CB) Kararnamesi, Tüzük, Yönetmelik, Tebliğ) çıkaran --kurum adı
-mevzuat_no : İçeriğin ilgili numarası (Detaylar için ilgili kategoriye bakınız)
-belge_sayi : Genelge üzerindeki Sayı ifadesinin değeri (sadece işlenebilenler)
-mevzuat_tarihi : İçeriğin ilgili Tarihi (date:yyyy-mm-dd formatında)
-donem : Komisyon Raporunun dönemini (örn: "27. Dönem")
-sira_no : Komisyon Raporunun Sıra Sayısı (örn: "230", "42 ek 1" vb.)
-madde_sayisi : İçeriğin(Kanun, KHK, CB Kararnamesi, Tüzük, Yönetmelik) bölümlerini (Madde sayısını ve işlenemeyen hükümleri/maddeleri, madde metinlerinin içindeki "Madde - ..." ifadeleri hariç )
-data_text : İçerik metni (Büyük/Küçük Harf, Noktalama ve "\n" içermektedir)
-url : İçerik metninin esas alındığı websayfasının linki (kaynak linkler güncel olmayabilir)
-kanunum_url : İçeriğin Kanunum linki
-Kategori | İçerik Sayısı | İlgili alanlar (Üst Veriler)

#Kategoriler
-Kanun | 514 | kategori, baslik, rega_no, mukerrer_no, rega_tarihi, mevzuat_no, mevzuat_tarihi, madde_sayisi, data_text, url
-Kanun Hükmünde Kararname | 91 | kategori, baslik, rega_no, mukerrer_no, rega_tarihi, mevzuat_no, mevzuat_tarihi, madde_sayisi, data_text, url
-Resmi Gazete | 546 | kategori, baslik, rega_no, mukerrer_no, rega_tarihi, data_text, url
-Komisyon Raporu | 500 | kategori, baslik, donem, sira_no, data_text, url
-Genelge | 385 | kategori, baslik, kurum, mevzuat_no, belge_sayi, mevzuat_tarihi, data_text, url
-Cumhurbaşkanlığı Kararnamesi | 54 | kategori, baslik, rega_no, mukerrer_no, rega_tarihi, kurum, mevzuat_no, mevzuat_tarihi, madde_sayisi, data_text, url
-Tüzük | 82 | kategori, baslik, rega_no, mukerrer_no, rega_tarihi, kurum, mevzuat_no, mevzuat_tarihi, madde_sayisi, data_text, url
-Yönetmelik | 597 | kategori, baslik, rega_no, mukerrer_no, rega_tarihi, kurum, mevzuat_no, mevzuat_tarihi, madde_sayisi, data_text, url
-Tebliğ | 623 | kategori, baslik, rega_no, mukerrer_no, rega_tarihi, kurum, data_text, url
-Özelge | 750 | kategori, baslik, kurum, mevzuat_tarihi, data_text, url
