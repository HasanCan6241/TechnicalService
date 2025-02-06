from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ServiceRequest, Customer
from datetime import datetime, time, timedelta


class ServiceRequestForm(forms.ModelForm):
    appointment_time = forms.ChoiceField(
        choices=[],
        label="Randevu Saati",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    appointment_date = forms.DateField(
        label="Randevu Tarihi",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': timezone.now().date().strftime('%Y-%m-%d')
        })
    )

    class Meta:
        model = ServiceRequest
        fields = ['service', 'problem_description', 'appointment_date', 'appointment_time']
        widgets = {
            'problem_description': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Lütfen sorununuzu detaylı bir şekilde açıklayın...'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Saat seçeneklerini oluştur
        time_choices = []
        start_time = time(9, 0)  # 09:00
        end_time = time(18, 0)  # 18:00
        current_time = datetime.combine(datetime.today(), start_time)
        end_datetime = datetime.combine(datetime.today(), end_time)

        while current_time <= end_datetime:
            time_str = current_time.strftime('%H:%M')
            time_choices.append((time_str, time_str))
            current_time += timedelta(minutes=30)

        self.fields['appointment_time'].choices = time_choices

    # forms.py içindeki ServiceRequestForm sınıfındaki clean metodunda güncelleme
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')

        if appointment_date and appointment_time:
            # Tarih ve saati birleştir
            hour, minute = map(int, appointment_time.split(':'))
            appointment_datetime = datetime.combine(
                appointment_date,
                time(hour, minute)
            )

            # Timezone aware yap
            appointment_datetime = timezone.make_aware(appointment_datetime)

            # Geçmiş tarih kontrolü
            if appointment_datetime < timezone.now():
                raise forms.ValidationError({
                    'appointment_time': "Geçmiş bir tarih seçemezsiniz!"
                })

            # Hafta sonu kontrolü
            if appointment_datetime.weekday() > 5:  # 6 = Pazar
                raise forms.ValidationError({
                    'appointment_date': "Pazar günü için randevu alamazsınız."
                })

            # Çakışma kontrolü
            existing_appointments = ServiceRequest.objects.filter(
                appointment_date=appointment_datetime
            )
            if existing_appointments.exists():
                raise forms.ValidationError({
                    'appointment_time': "Bu tarih ve saat için başka bir randevu bulunmaktadır. "
                                        "Lütfen farklı bir zaman dilimi seçiniz."
                })

            # Appointment date'i kaydet
            cleaned_data['appointment_date'] = appointment_datetime

        return cleaned_data


class CustomerForm(forms.ModelForm):
    # Telefon numarası için özel doğrulayıcı
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telefon numarası '+999999999' formatında olmalıdır. En fazla 15 rakam girebilirsiniz."
    )

    phone = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={'placeholder': 'Örn: +905xxxxxxxxx'})
    )

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ad Soyad'}),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Açık adresinizi giriniz...'
            }),
            'email': forms.EmailInput(attrs={'placeholder': 'ornek@gmail.com'})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Adınız',
        widget=forms.TextInput(attrs={'placeholder': 'Ad Soyad'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZğüşıöçĞÜŞİÖÇ\s]+$',
                message='İsim sadece harflerden oluşmalıdır.'
            )
        ]
    )

    email = forms.EmailField(
        label='E-posta Adresiniz',
        widget=forms.EmailInput(attrs={'placeholder': 'ornek@email.com'}),
        validators=[EmailValidator(message="Geçerli bir e-posta adresi giriniz.")]
    )

    phone = forms.CharField(
        max_length=15,
        label='Telefon Numaranız',
        widget=forms.TextInput(attrs={'placeholder': '+90XXXXXXXXXX'}),
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Geçerli bir telefon numarası giriniz.'
            )
        ]
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Mesajınızı buraya yazın...'
        }),
        label='Mesajınız',
        min_length=4,
        error_messages={
            'min_length': 'Mesajınız en az 4 karakter olmalıdır.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data