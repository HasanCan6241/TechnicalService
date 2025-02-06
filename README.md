# Gültekin Teknik Servis - Web Uygulaması

Bu proje, Tunceli'nin en güvenilir teknik servislerinden biri olan **Gültekin Teknik Servis** için geliştirilmiş bir **Django** tabanlı web uygulamasıdır. Web sitesi, firmanın **hizmetleri**, **blog yazıları**, **bilgilendirici videoları**, **hakkımızda** ve **iletişim** gibi bölümlerini içermektedir. Admin paneli sayesinde sayfa içerikleri kolayca düzenlenebilir ve güncellenebilir.

## ✨ Projenin Özellikleri
- **Ana Sayfa:** Firmanın hizmetlerini ve genel tanıtımını içeren modern bir arayüz.
- **Hizmetler Sayfası:** Verilen hizmetler ve detaylı açıklamalar.
- **Blog Sayfası:** Kullanıcılara teknik bilgiler sunan blog yazıları.
- **Bilgilendirici Videolar:** Kullanıcılar için ısıtma-soğutma sistemlerine dair eğitici videolar.
- **Hakkımızda Sayfası:** Firma hakkında genel bilgiler.
- **İletişim Sayfası:** Kullanıcıların firmayla kolayca iletişime geçmesini sağlayan form ve iletişim bilgileri.
- **Markalar ve Bilgiler:** Viessmann, ECA, İmmergas gibi önde gelen markalar hakkında detaylı bilgiler.
- **Admin Paneli:** Sayfa içeriklerinin kolayca güncellenmesini sağlayan yönetici paneli.
- **AWS Deployment:** Proje **AWS Elastic Beanstalk** kullanılarak yayınlanmıştır.
- **SSL Sertifikası:** Route 53 ve AWS Certificate Manager kullanılarak **SSL** entegrasyonu gerçekleştirilmiştir.

## 🛠 Kullanılan Teknolojiler ve Kütüphaneler
Proje **Django 3.2.9** çatısı kullanılarak geliştirildi. Kullanılan başlıca kütüphaneler:

```txt
asgiref==3.7.2
Django==5.1.4
python-dotenv==1.0.0
sqlparse==0.4.4
Werkzeug==2.3.7
Pillow==8.4.0
openpyxl==3.1.5
django-ckeditor==6.7.2
django-jazzmin==3.0.1
python-decouple==3.8
django-js-asset==2.0.0
django-widget-tweaks==1.5.0
```

## 🌐 AWS Deploy (Elastic Beanstalk)
Proje, **AWS Elastic Beanstalk** kullanılarak yayınlanmıştır. AWS'de deploy için aşağıdaki adımlar izlenmiştir:

- **Elastic Beanstalk** ortamı oluşturuldu ve **Django** uygulaması deploy edildi.
- **Route 53** kullanılarak alan adı yönlendirmesi yapıldı.
- **AWS Certificate Manager** ile SSL sertifikaları entegre edildi.


## ⚡ Kurulum
Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/HasanCan6241/TechnicalService.git
cd proje-adi
```

### 2. Sanal Ortamı Oluşturun
```bash
python -m venv env
source env/bin/activate  # MacOS/Linux
env\Scripts\activate  # Windows
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Veritabanını Oluşturun
```bash
python manage.py migrate
```

### 5. Admin Kullanıcısı Oluşturun
```bash
python manage.py createsuperuser
```

### 6. Sunucuyu Başlatın
```bash
python manage.py runserver
```

Artık projeniz **http://127.0.0.1:8000/** adresinde çalışıyor olmalıdır.


**Teşekkürler!** 🚀

