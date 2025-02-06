from django.contrib import admin
from .models import Service, Customer, ServiceRequest, CompanyContact
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment
from .models import Brand, BoilerModel, ErrorCode,FAQ,VideoContent,BlogPost,Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_date', 'is_active')  # Görüntülenecek sütunlar
    list_filter = ('category', 'author', 'is_active', 'created_date')  # Filtreleme seçenekleri
    search_fields = ('title', 'content', 'author', 'category')  # Arama yapılacak alanlar
    prepopulated_fields = {'slug': ('title',)}  # Slug alanını otomatik doldur
    ordering = ('-created_date',)  # Varsayılan sıralama
    list_editable = ('is_active',)  # Doğrudan liste görünümünde düzenlenebilir alanlar
    date_hierarchy = 'created_date'  # Tarih bazlı gezinme

    # Detay sayfasındaki düzenleme görünümü
    fieldsets = (
        ("Temel Bilgiler", {
            'fields': ('title', 'slug', 'category', 'author', 'is_active')
        }),
        ("İçerik ve Görsel", {
            'fields': ('content', 'image')
        }),
        ("Zaman Bilgisi", {
            'fields': ('created_date',),
            'classes': ('collapse',),  # Gizlenebilir
        }),
    )

@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'is_featured', 'views', 'created_at')
    list_filter = ('brand', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    readonly_fields = ('views',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("brand", "question")
    search_fields = ("brand__name", "question")
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(BoilerModel)
class BoilerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')

@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ('boiler_model', 'code', 'description', 'solution')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone', 'email')

@admin.register(CompanyContact)
class CompanyContactAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'email', 'address')
    search_fields = ('company_name', 'phone', 'email')


@admin.action(description="Servis taleplerini Excel olarak indir")
def export_service_requests_to_excel(modeladmin, request, queryset):
    # Yeni bir Excel çalışma kitabı oluşturun
    wb = Workbook()
    ws = wb.active
    ws.title = "Servis Talepleri"

    # Başlık satırını ekleyin
    headers = [
        "Müşteri Adı", "Hizmet Adı", "Randevu Tarihi", "Durum",
        "Sorun Açıklaması", "Adres", "Telefon"
    ]
    ws.append(headers)

    # Hücre başlıkları için hizalama
    for cell in ws[1]:
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Verileri ekleyin ve hücre genişliklerini ayarlayın
    for request in queryset:
        # Zaman dilimi bilgisini kaldırıyoruz
        appointment_date = request.appointment_date.replace(tzinfo=None) if request.appointment_date else None

        row = [
            request.customer.name,
            request.service.name,
            appointment_date,  # Zaman dilimsiz tarih
            request.get_status_display(),
            request.problem_description,
            request.customer.address,
            request.customer.phone,
        ]

        # Satırı ekleyin
        ws.append(row)

        # Hücre genişliğini her satır için güncelleyin
        for col_num, value in enumerate(row, 1):
            column_letter = chr(64 + col_num)
            # Hücreyi düzgün gösterebilmek için genişliği ayarlayın
            max_length = max(len(str(value)) for value in row)
            column_width = max_length + 2  # Hücreyi biraz daha geniş yapıyoruz
            ws.column_dimensions[column_letter].width = column_width

    # HTTP yanıtını oluşturun ve UTF-8 karakter seti ile indirilebilir dosya olarak ayarlayın
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="service_requests.xlsx"'
    wb.save(response)

    return response

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'appointment_date', 'status', 'created_at')
    list_filter = ('status', 'service', 'appointment_date')
    search_fields = ('customer__name', 'problem_description')
    actions = [export_service_requests_to_excel]  # Excel raporu indirme özelliği







