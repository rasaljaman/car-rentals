from django import forms
from django.contrib.auth import authenticate
from apps.accounts.models import CustomUser, SignUpSession, Profile
from apps.cars.models import Car, CarImage


class SignUpStep1Form(forms.Form):
    """First step of signup - basic information."""
    
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Email Address'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': '+1 (555) 000-0000'
        })
    )
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'City, Country'
        })
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Password (min. 8 characters)'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Confirm Password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        
        return cleaned_data


class OTPVerificationForm(forms.Form):
    """OTP verification form."""
    
    otp_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg text-center text-2xl tracking-widest focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': '000000',
            'maxlength': '6'
        })
    )


class LoginForm(forms.Form):
    """Login form with email and password."""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Email Address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid email or password")
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")
        
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    """Edit user profile form."""
    
    class Meta:
        model = Profile
        fields = ['profile_photo', 'bio']
        widgets = {
            'profile_photo': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600',
                'rows': 4,
                'placeholder': 'Tell us about yourself'
            })
        }


class CarListingForm(forms.ModelForm):
    """Form for creating/editing car listings (NO FILE UPLOADS)."""

    class Meta:
        model = Car
        fields = [
            "title",
            "brand",
            "model",
            "year",
            "fuel_type",
            "price_per_day",
            "location",
            "description",
            "registration_number",
            "mileage",
            "transmission",
            "seats",
            "color",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
                "placeholder": "e.g., Honda City 2020",
            }),
            "brand": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
                "placeholder": "Brand",
            }),
            "model": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
                "placeholder": "Model",
            }),
            "year": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
            }),
            "fuel_type": forms.Select(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
            }),
            "price_per_day": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
                "step": "0.01",
            }),
            "location": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
                "placeholder": "City",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
                "rows": 4,
                "placeholder": "Describe your car",
            }),
            "registration_number": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
            }),
            "mileage": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
            }),
            "transmission": forms.Select(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
            }),
            "seats": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
            }),
            "color": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600",
            }),
        }
