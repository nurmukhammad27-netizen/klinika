from django import forms
from .models import (
    Department, Room, Doctor, Patient, Appointment, Partner, Expense,
    Card, ProcedureService, Uzi, Ward, Laboratory, Medicine,
    Reagent, MedicalMaterial, HouseholdItem, Setting
)

# 1. Bemorlar formasi
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'phone', 'birth_date', 'gender', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bemor F.I.O', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998901234567', 'required': True}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yashash manzili'}),
        }

# 2. Shifokorlar formasi
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['full_name', 'specialty', 'department', 'phone', 'price_per_visit']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'F.I.O'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Kardiolog'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998901234567'}),
            'price_per_visit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }

# 3. Qabullar va Navbat formasi
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'status', 'total_amount', 'is_paid']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# 4. Bo'limlar formasi
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Bo'lim nomi"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Batafsil tavsif...'}),
        }

# 5. Xonalar formasi
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'department']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 101'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }

# 6. Hamkorlar formasi
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'phone', 'address', 'note']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hamkor nomi'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998901234567'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manzil'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Qo\'shimcha izoh'}),
        }

# 7. Chiqimlar formasi
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'comment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chiqim nomi'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Izoh'}),
        }

# 8. Kartalar formasi
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title', 'patient']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Karta nomi / Raqami'}),
            'patient': forms.Select(attrs={'class': 'form-select'}),
        }

# 9. Muolaja xizmatlari formasi
class ProcedureServiceForm(forms.ModelForm):
    class Meta:
        model = ProcedureService
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Muolaja xizmati nomi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }

# 10. UZI formasi
class UziForm(forms.ModelForm):
    class Meta:
        model = Uzi
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UZI turi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }

# 11. Palatalar formasi
class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ['number', 'capacity', 'price_per_day']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Palata №'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "O'rinlar soni"}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bir kunlik narxi'}),
        }

# 12. Laboratoriya formasi
class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tahlil nomi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }

# 13. Dori vositalari formasi
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'quantity', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dori nomi'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdori'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Narxi'}),
        }

# 14. Reagentlar formasi
class ReagentForm(forms.ModelForm):
    class Meta:
        model = Reagent
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reagent nomi'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdori'}),
        }

# 15. Tibbiy material formasi
class MedicalMaterialForm(forms.ModelForm):
    class Meta:
        model = MedicalMaterial
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Material nomi'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdori'}),
        }

# 16. Xo'jalik tovari formasi
class HouseholdItemForm(forms.ModelForm):
    class Meta:
        model = HouseholdItem
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tovar nomi'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdori'}),
        }

# 17. Sozlamalar formasi
class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['clinic_name', 'address', 'phone']
        widgets = {
            'clinic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }