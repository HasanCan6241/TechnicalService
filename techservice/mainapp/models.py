from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.urls import reverse

class Service(models.Model):
    """Sunulan hizmet türleri için model"""
    name = models.CharField(max_length=100, verbose_name="Hizmet Adı")
    description = models.TextField(verbose_name="Hizmet Açıklaması")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='services/',
        verbose_name="Hizmet Görseli",
        null=True,  # Var olan kayıtlar için NULL değerine izin ver
        blank=True  # Admin panelinde bu alanın boş bırakılmasına izin ver
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hizmet"
        verbose_name_plural = "Hizmetler"

class Customer(models.Model):
    """Müşteri bilgileri için model"""
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    phone = models.CharField(max_length=15, verbose_name="Telefon")
    address = models.TextField(verbose_name="Adres")
    email = models.EmailField(blank=True, null=True, verbose_name="E-posta")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"


class ServiceRequest(models.Model):
    """Servis talepleri için model"""
    STATUS_CHOICES = [
        ('pending', 'Bekliyor'),
        ('in_progress', 'İşleme Alındı'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Müşteri")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Hizmet")
    problem_description = models.TextField(verbose_name="Sorun Açıklaması")
    appointment_date = models.DateTimeField(verbose_name="Randevu Tarihi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Durum")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.appointment_date:
            # Aynı zaman diliminde başka randevu var mı kontrolü
            existing_appointments = ServiceRequest.objects.filter(
                appointment_date=self.appointment_date
            ).exclude(id=self.id)

            if existing_appointments.exists():
                raise ValidationError({
                    'appointment_date': 'Bu zaman dilimi için başka bir randevu bulunmaktadır.'
                })

    def __str__(self):
        return f"{self.customer.name} - {self.service.name}"

    class Meta:
        verbose_name = "Servis Talebi"
        verbose_name_plural = "Servis Talepleri"


# Firma iletişim bilgileri için model
class CompanyContact(models.Model):
    """Firma iletişim bilgileri için model"""
    company_name = models.CharField(max_length=200, verbose_name="Firma Adı")
    working_hours = models.CharField(max_length=100, verbose_name="Çalışma Saatleri")
    social_media = models.JSONField(verbose_name="Sosyal Medya", blank=True, null=True)  # JSON formatında sosyal medya bağlantıları
    phone = models.CharField(max_length=15, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True, verbose_name="E-posta")
    address = models.TextField(verbose_name="Adres")
    logo = models.ImageField(
        upload_to="company_logos/",
        verbose_name="Firma Logosu",
        blank=True,
        null=True,
        default="company_logos/default_logo.png",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Firma Bilgileri"
        verbose_name_plural = "Firma Bilgileri"

class Region(models.Model):
    """Hizmet bölgeleri için model"""
    name = models.CharField(max_length=100, verbose_name="Bölge Adı")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hizmet Bölgesi"
        verbose_name_plural = "Hizmet Bölgeleri"



# models.py
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Marka Adı")
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='brand_logos/', verbose_name="Marka Logosu", null=True, blank=True)
    description = models.TextField(verbose_name="Marka Açıklaması", blank=True)
    service_email = models.EmailField(verbose_name="Yetkili Servis E-postası", null=True, blank=True)  # Yeni alan

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mainapp:brand-detail', kwargs={'slug': self.slug})

    def __str__(self):  # Burada değişiklik yapıldı
        return self.name

    class Meta:
        verbose_name = "Kombi Markaları"
        verbose_name_plural = "Kombi Markaları"


class BoilerModel(models.Model):
    """Kombi modelleri"""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="boilers", verbose_name="Marka")
    name = models.CharField(max_length=255, verbose_name="Model Adı")

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

    class Meta:
        verbose_name = "Kombi Modelleri"
        verbose_name_plural = "Kombi Modelleri"

class ErrorCode(models.Model):
    """Kombi hata kodları"""
    boiler_model = models.ForeignKey(BoilerModel, on_delete=models.CASCADE, related_name="error_codes")
    code = models.CharField(max_length=10, verbose_name="Hata Kodu")
    description = models.TextField(verbose_name="Hata Açıklaması")
    solution = models.TextField(verbose_name="Çözüm")

    def __str__(self):
        return f"{self.boiler_model.name} - {self.code}"

    class Meta:
        verbose_name = "Hata Kodları"
        verbose_name_plural = "Hata Kodları"


class FAQ(models.Model):
    """Sıkça Sorulan Sorular"""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="faqs", verbose_name="Marka")
    question = models.CharField(max_length=255, verbose_name="Soru")
    answer = models.TextField(verbose_name="Cevap")

    def __str__(self):
        return f"{self.brand.name} - {self.question}"

    class Meta:
        verbose_name = "Sıkça Sorulan Soru"
        verbose_name_plural = "Sıkça Sorulan Sorular"



class VideoContent(models.Model):
    title = models.CharField(max_length=200, verbose_name="Video Başlığı")
    description = models.TextField(verbose_name="Video Açıklaması")
    youtube_url = models.URLField(verbose_name="YouTube Video URL")
    thumbnail = models.ImageField(upload_to='video_thumbnails/', verbose_name="Video Küçük Resmi", null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    views = models.PositiveIntegerField(default=0, verbose_name="İzlenme Sayısı")
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name="Kombi Markası", related_name="videos")

    class Meta:
        verbose_name = 'Video İçeriği'
        verbose_name_plural = 'Video İçerikleri'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_youtube_embed_url(self):
        # YouTube URL'sinden video ID'sini ayıklama
        if 'youtube.com' in self.youtube_url or 'youtu.be' in self.youtube_url:
            if 'youtube.com/watch?v=' in self.youtube_url:
                video_id = self.youtube_url.split('watch?v=')[1]
            elif 'youtu.be/' in self.youtube_url:
                video_id = self.youtube_url.split('youtu.be/')[1]
            if '&' in video_id:
                video_id = video_id.split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return None

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Blog Başlığı")
    slug = models.SlugField(unique=True, verbose_name="URL")
    content = RichTextField(verbose_name="İçerik")
    image = models.ImageField(upload_to='blog/', verbose_name="Blog Görseli")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Oluşturulma Tarihi")
    category = models.CharField(max_length=100, verbose_name="Kategori")
    author = models.CharField(max_length=100, verbose_name="Yazar")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['-created_date']

    def __str__(self):
        return self.title