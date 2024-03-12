-Burak Soylu-

İlk olarak, Google News haberlere gittim ve oradan istenilen başlıklardaki linkleri almak için kütüphaneden requests, bs4 ve BeautifulSoup'u kullandım. Verileri çekmek için önce linkleri aldım. Daha sonra, "def google_news" fonksiyonunu kullanarak linkleri kategorilere ayırdım. Haberleri çekmek için bu kategorilere göre işlemler gerçekleştirdim.

Verileri çekerken döngü kullanarak URL, haber başlığı, kısa açıklama, haber kaynağı, yayınlanma tarihi ve sıralama bilgilerini çektim. Kısa açıklama ve Url için o anki sıradaki haber kaynağı sitesine gidip, sitedeki "p" ve "URL" yi çekmek için bir fonksiyon oluşturdum.

Döngü öncesinde bir dosya oluşturdum ve Türkçe karakter düzenlemesi için "utf-8" kodlamasını kullandım. Daha sonra, belirli başlıklar altında düzenli bir şekilde çıkması için verdiğim kategorileri dosyaya sıralı bir şekilde yazdım. Google News olarak oluşturduğum verileri çekerken de sıralı bir şekilde düzenleme sağladım.