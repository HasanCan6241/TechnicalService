from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ServiceRequestForm, CustomerForm
from .models import Service,CompanyContact,BoilerModel,FAQ,VideoContent,Brand,BlogPost,Region
from .forms import ServiceRequestForm, CustomerForm, ContactForm  # ContactForm'u ekleyin
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.views.generic import ListView,DetailView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.templatetags.static import static


def home(request):
    services = Service.objects.all()[:6]
    featured_videos = VideoContent.objects.filter(is_featured=True)[:3] if VideoContent.objects.exists() else []
    latest_blogs = BlogPost.objects.filter(is_active=True)[:3] if BlogPost.objects.exists() else []
    brands = Brand.objects.all()
    regions = Region.objects.all()

    context = {
            'featured_videos': featured_videos,
            'latest_blogs': latest_blogs,
            'services':services,
            'brands':brands,
            'regions':regions
        }
    return render(request, 'pages/home.html', context)

def about(request):
    return render(request,'pages/about.html')

def combi_service(request):
    return render(request,'service/kombi_service.html')

def boiler_service(request):
    return render(request,'service/kazan_service.html')

def airconditioning(request):
    return render(request,'service/klima_service.html')

def su_aritma(request):
    return render(request,'service/su_aritma.html')

def sofben_bakimi(request):
    return render(request,'service/sofben_bakimi.html')

def repair(request):
    return render(request,'service/bakım_onarım.html')

def eca_about(request):
    eca_boilers = BoilerModel.objects.filter(brand__name="ECA").prefetch_related('error_codes')
    eca_faqs=FAQ.objects.filter(brand__name="ECA")
    return render(request, 'pages/eca-about.html', {
        'boiler_models': eca_boilers,
        'faqs': eca_faqs
    })

def viessmann_about(request):
    viessmann_about = BoilerModel.objects.filter(brand__name="Viessmann").prefetch_related('error_codes')
    viessmann_faqs = FAQ.objects.filter(brand__name="Viessmann")
    return render(request, 'pages/viessmann_about.html', {
        'boiler_models': viessmann_about,
        'faqs': viessmann_faqs
    })

def immergas_about(request):
    immergas_about = BoilerModel.objects.filter(brand__name="İmmergas").prefetch_related('error_codes')
    immergas_faqs=FAQ.objects.filter(brand__name="İmmergas")
    return render(request, 'pages/immergas_about.html', {
        'boiler_models': immergas_about,
        'faqs': immergas_faqs
    })

class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand_detail/brand_detail.html'
    context_object_name = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.get_object()
        context['boiler_models'] = BoilerModel.objects.filter(
            brand=brand
        ).prefetch_related('error_codes')
        context['faqs'] = FAQ.objects.filter(brand=brand)
        return context

def blog_list(request):
    posts = BlogPost.objects.filter(is_active=True)
    paginator = Paginator(posts, 6)  # Her sayfada 6 blog göster
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = BlogPost.objects.get(slug=slug)
    return render(request, 'blog/blog_detail.html', {'post': post})


class VideoGalleryView(ListView):
    model = VideoContent
    template_name = 'pages/video_gallery.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_videos'] = VideoContent.objects.filter(is_featured=True)
        context['brands'] = Brand.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            brand_id = request.GET.get('brand')
            if brand_id == 'all':
                videos = VideoContent.objects.all()
            else:
                videos = VideoContent.objects.filter(brand_id=brand_id)

            data = [{
                'title': video.title,
                'description': video.description,
                'embed_url': video.get_youtube_embed_url(),
                'thumbnail': video.thumbnail.url if video.thumbnail else None,
            } for video in videos]

            return JsonResponse({'videos': data})

        return super().get(request, *args, **kwargs)

# views.py
def service_request(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        service_form = ServiceRequestForm(request.POST)

        if customer_form.is_valid() and service_form.is_valid():
            try:
                customer = customer_form.save()
                service_request = service_form.save(commit=False)
                service_request.customer = customer
                service_request.full_clean()  # Model validasyonunu çalıştır
                service_request.save()

                messages.success(request, 'Servis talebiniz başarıyla oluşturuldu.')
                return redirect('/service_request/')
            except ValidationError as e:
                # Model seviyesindeki validasyon hatalarını form hatalarına ekle
                for field, errors in e.message_dict.items():
                    for error in errors:
                        if field == 'appointment_date':
                            service_form.add_error('appointment_time', error)
                        else:
                            service_form.add_error(field, error)

        # Form geçerli değilse veya validation hatası varsa
        if service_form.errors:
            for field in service_form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
        if customer_form.errors:
            for field in customer_form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")

    else:
        customer_form = CustomerForm()
        service_form = ServiceRequestForm()

    return render(request, 'pages/service_request.html', {
        'customer_form': customer_form,
        'service_form': service_form
    })

def services(request):
    services = Service.objects.all()
    return render(request, 'pages/services.html', {'services': services})


def contact_info(request):
    # En son güncellenen CompanyContact kaydını al
    contact = CompanyContact.objects.latest('updated_at')  # En son güncellenen kaydı al

    # Sosyal medya bilgilerini JSON'dan al
    social_media = contact.social_media if contact.social_media else {}

    # Logo URL'sini kontrol et (logo yoksa default bir static dosya ayarla)
    logo_url = contact.logo.url if contact.logo else static('images/gültekin_teknik_logo.jpg')

    return {
        "contact_info": {
            "phone": contact.phone if contact.phone else "Telefon bilgisi bulunamadı",
            "email": contact.email if contact.email else "E-posta bilgisi bulunamadı",
            "address": contact.address if contact.address else "Adres bilgisi bulunamadı",
            "working_hours": contact.working_hours if contact.working_hours else "Çalışma saatleri bilgisi bulunamadı",
            "social_media": {
                "facebook": social_media.get("facebook", "Sosyal medya linki bulunamadı"),
                "instagram": social_media.get("instagram", "Sosyal medya linki bulunamadı"),
                "whatsapp": social_media.get("whatsapp", "Sosyal medya linki bulunamadı"),
            },
            "logo": logo_url  # Logo URL'sini döndür
        }
    }

def contact(request):
    company_contact = CompanyContact.objects.first()  # İlk kayıt varsa al
    brand=Brand.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Formdan gelen veriler
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            # E-posta içeriği (HTML formatında)
            subject = f"Yeni İletişim Talebi: {name}"
            message_body = f"""
            <html>
                <body>
                    <h2>Yeni İletişim Talebi</h2>
                    <p><strong>Ad:</strong> {name}</p>
                    <p><strong>E-posta:</strong> {email}</p>
                    <p><strong>Telefon:</strong> {phone}</p>
                    <p><strong>Mesaj:</strong><br>{message}</p>
                </body>
            </html>
            """
            from_email = 'ulasgultekin6278@gmail.com'
            recipient_list = [company_contact.email] if company_contact and company_contact.email else [
                'ulasgultekin6278@gmail.com']

            # E-posta gönderimi (HTML formatında)
            send_mail(
                subject,
                message_body,  # Bu, metin formatındaki mesajdır
                from_email,
                recipient_list,
                html_message=message_body  # Bu, HTML formatındaki mesajdır
            )

            messages.success(request, 'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.')
            return redirect('mainapp:contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'company_contact': company_contact,
        'brand':brand,
    }
    return render(request, 'pages/contact.html', context)
