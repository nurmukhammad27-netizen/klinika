from django.db import models
from django.contrib.auth.models import User

# 1. Bo'limlar
class Department(models.Model):
    title = models.CharField(max_length=100, verbose_name="Bo'lim nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return self.title


# 2. Xonalar
class Room(models.Model):
    room_number = models.CharField(max_length=20, verbose_name="Xona raqami")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rooms', verbose_name="Bo'lim")

    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"

    def __str__(self):
        return f"{self.room_number} - {self.department.title}"


# 3. Shifokorlar
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi hisobi")
    full_name = models.CharField(max_length=150, verbose_name="F.I.O")
    specialty = models.CharField(max_length=100, verbose_name="Mutaxassisligi (Masalan: UZI, LOR)")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bo'lim")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    price_per_visit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Qabul narxi (so'm)")

    class Meta:
        verbose_name = "Shifokor"
        verbose_name_plural = "Shifokorlar"

    def __str__(self):
        return f"{self.full_name} ({self.specialty})"


# 4. Bemorlar
class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    )
    full_name = models.CharField(max_length=150, verbose_name="F.I.O")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sanasi")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name="Jinsi")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Manzili")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatga olingan vaqti")

    class Meta:
        verbose_name = "Bemor"
        verbose_name_plural = "Bemorlar"

    def __str__(self):
        return f"{self.full_name} - {self.phone}"


# 5. Qabul / Navbat
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Kutmoqda'),
        ('in_doctor', 'Shifokor qabulida'),
        ('completed', 'Tugatildi'),
        ('canceled', 'Bekor qilindi'),
    )

    receipt_no = models.CharField(max_length=20, unique=True, verbose_name="Chek №")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name="Bemor")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name="Shifokor")
    queue_number = models.PositiveIntegerField(verbose_name="Navbat raqami")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name="Holat")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="To'lov summasi")
    is_paid = models.BooleanField(default=False, verbose_name="To'langanmi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    class Meta:
        verbose_name = "Qabul"
        verbose_name_plural = "Qabullar"

    def __str__(self):
        return f"{self.receipt_no} - {self.patient.full_name}"


# 6. Hamkorlar
class Partner(models.Model):
    name = models.CharField(max_length=255, verbose_name="Hamkor nomi")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telefon")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Manzil")
    note = models.TextField(blank=True, null=True, verbose_name="Izoh")

    class Meta:
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"

    def __str__(self):
        return self.name


# 7. Chiqimlar
class Expense(models.Model):
    title = models.CharField(max_length=255, verbose_name="Chiqim nomi")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Summa")
    date = models.DateField(auto_now_add=True, verbose_name="Sana")
    comment = models.TextField(blank=True, null=True, verbose_name="Izoh")

    class Meta:
        verbose_name = "Chiqim"
        verbose_name_plural = "Chiqimlar"

    def __str__(self):
        return f"{self.title} - {self.amount}"


# 8. Kartalar
class Card(models.Model):
    title = models.CharField(max_length=255, verbose_name="Karta / Bemor kartasi nomi")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name="cards", verbose_name="Bemor")
    created_at = models.DateField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "Karta"
        verbose_name_plural = "Kartalar"

    def __str__(self):
        return self.title


# 9. Muolaja xizmatlari
class ProcedureService(models.Model):
    name = models.CharField(max_length=255, verbose_name="Muolaja xizmati")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")

    class Meta:
        verbose_name = "Muolaja xizmati"
        verbose_name_plural = "Muolaja xizmatlari"

    def __str__(self):
        return f"{self.name} - {self.price}"


# 10. UZI
class Uzi(models.Model):
    name = models.CharField(max_length=255, verbose_name="UZI turi")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")

    class Meta:
        verbose_name = "UZI"
        verbose_name_plural = "UZI"

    def __str__(self):
        return f"{self.name} - {self.price}"


# 11. Palatalar
class Ward(models.Model):
    number = models.CharField(max_length=50, verbose_name="Palata raqami")
    capacity = models.PositiveIntegerField(default=1, verbose_name="O'rinlar soni")
    price_per_day = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Bir kunlik narxi")

    class Meta:
        verbose_name = "Palata"
        verbose_name_plural = "Palatalar"

    def __str__(self):
        return f"Palata №{self.number}"


# 12. Laboratoriya
class Laboratory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tahlil nomi")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")

    class Meta:
        verbose_name = "Laboratoriya"
        verbose_name_plural = "Laboratoriya"

    def __str__(self):
        return f"{self.name} - {self.price}"


# 13. Dori vositalari
class Medicine(models.Model):
    name = models.CharField(max_length=255, verbose_name="Dori nomi")
    quantity = models.IntegerField(default=0, verbose_name="Soni/Miqdori")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Narxi")

    class Meta:
        verbose_name = "Dori vositasi"
        verbose_name_plural = "Dori vositalari"

    def __str__(self):
        return f"{self.name} ({self.quantity} ta)"


# 14. Reagentlar
class Reagent(models.Model):
    name = models.CharField(max_length=255, verbose_name="Reagent nomi")
    quantity = models.IntegerField(default=0, verbose_name="Soni/Miqdori")

    class Meta:
        verbose_name = "Reagent"
        verbose_name_plural = "Reagentlar"

    def __str__(self):
        return f"{self.name} ({self.quantity})"


# 15. Tibbiy material
class MedicalMaterial(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tibbiy material")
    quantity = models.IntegerField(default=0, verbose_name="Miqdori")

    class Meta:
        verbose_name = "Tibbiy material"
        verbose_name_plural = "Tibbiy materiallar"

    def __str__(self):
        return self.name


# 16. Xo'jalik tovari
class HouseholdItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Xo'jalik tovari")
    quantity = models.IntegerField(default=0, verbose_name="Miqdori")

    class Meta:
        verbose_name = "Xo'jalik tovari"
        verbose_name_plural = "Xo'jalik tovarlari"

    def __str__(self):
        return self.name


# 17. Sozlamalar
class Setting(models.Model):
    clinic_name = models.CharField(max_length=255, default="Osiyo Medical Services", verbose_name="Klinika nomi")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Klinika manzili")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telefon raqamlar")

    class Meta:
        verbose_name = "Sozlama"
        verbose_name_plural = "Sozlamalar"

    def __str__(self):
        return self.clinic_name