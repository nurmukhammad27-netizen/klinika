import random
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q, Sum
from django.contrib import messages
from django.contrib.auth.models import User

from .models import (
    Patient, Doctor, Appointment, Department, Room, Partner, 
    Expense, Card, ProcedureService, Uzi, Ward, Laboratory, 
    Medicine, Reagent, MedicalMaterial, HouseholdItem, Setting
)
from .forms import (
    PatientForm, DoctorForm, PartnerForm, ExpenseForm, CardForm, 
    ProcedureServiceForm, UziForm, WardForm, LaboratoryForm, 
    MedicineForm, ReagentForm, MedicalMaterialForm, HouseholdItemForm, 
    RoomForm, SettingForm
)

# 1. QABULXONA VA BEMORLAR (RO'YXATGA OLISH)
def patients_list(request):
    search_query = request.GET.get('q', '').strip()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        birth_date = request.POST.get('birth_date') or None
        gender = request.POST.get('gender', 'M')
        doctor_id = request.POST.get('doctor_id')

        if full_name and phone and doctor_id:
            # Bemor mavjud bo'lsa topamiz, aks holda yaratamiz
            patient, _ = Patient.objects.get_or_create(
                phone=phone,
                defaults={'full_name': full_name, 'birth_date': birth_date, 'gender': gender}
            )

            doctor = get_object_or_404(Doctor, id=doctor_id)
            today = timezone.now().date()
            
            # Bugungi shifokor qabullari sonini hisoblash
            today_count = Appointment.objects.filter(doctor=doctor, created_at__date=today).count()
            next_queue = today_count + 1

            receipt_no = f"CH-{random.randint(10000, 99999)}"

            appointment = Appointment.objects.create(
                receipt_no=receipt_no,
                patient=patient,
                doctor=doctor,
                queue_number=next_queue,
                total_amount=doctor.price_per_visit,
                status='waiting'
            )

            messages.success(request, f"{patient.full_name} muvaffaqiyatli navbatga qo'shildi.")
            return redirect('print_receipt', appointment_id=appointment.id)

    appointments = Appointment.objects.select_related('patient', 'doctor').all().order_by('-created_at')
    if search_query:
        appointments = appointments.filter(
            Q(patient__full_name__icontains=search_query) | 
            Q(patient__phone__icontains=search_query) |
            Q(receipt_no__icontains=search_query)
        )

    doctors = Doctor.objects.all()

    context = {
        'appointments': appointments,
        'doctors': doctors,
        'search_query': search_query,
    }
    return render(request, 'clinic/patients.html', context)

# 2. SHIFOKORLAR
def doctors_list(request):
    form = DoctorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Yangi shifokor muvaffaqiyatli qo'shildi.")
        return redirect('doctors_list')
        
    doctors = Doctor.objects.select_related('department').all()
    return render(request, 'clinic/doctors.html', {'doctors': doctors, 'form': form})

# 3. XONALAR
def rooms_list(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Xona muvaffaqiyatli saqlandi.")
        return redirect('rooms_list')

    rooms = Room.objects.select_related('department').all()
    departments = Department.objects.all()
    return render(request, 'clinic/rooms.html', {'rooms': rooms, 'departments': departments, 'form': form})

# 4. CHEK CHOP ETISH
def print_receipt(request, appointment_id):
    appointment = get_object_or_404(Appointment.select_related('patient', 'doctor'), id=appointment_id)
    return render(request, 'clinic/receipt.html', {'appointment': appointment})

# ---------------- BO'LIMLAR VA SEKSIYALAR ----------------

def dashboard_view(request):
    today = timezone.now().date()
    total_patients = Patient.objects.count()
    today_appointments = Appointment.objects.filter(created_at__date=today).count()
    
    total_income = Appointment.objects.filter(is_paid=True).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'title': "Ma'lumotlar Taxtasi",
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income - total_expenses
    }
    return render(request, 'clinic/sections/dashboard.html', context)

def partners_view(request):
    form = PartnerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Hamkor saqlandi.")
        return redirect('partners')
    items = Partner.objects.all().order_by('-id')
    return render(request, 'clinic/sections/partners.html', {'title': 'Hamkorlar', 'items': items, 'form': form})

def staff_view(request):
    staff_members = User.objects.filter(is_staff=True)
    return render(request, 'clinic/sections/staff.html', {'title': 'Xodimlar', 'staff_members': staff_members})

def expenses_view(request):
    form = ExpenseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Chiqim muvaffaqiyatli kiritildi.")
        return redirect('expenses')
    items = Expense.objects.all().order_by('-date', '-id')
    return render(request, 'clinic/sections/expenses.html', {'title': 'Chiqimlar', 'items': items, 'form': form})

def cards_view(request):
    form = CardForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Karta saqlandi.")
        return redirect('cards')
    items = Card.objects.select_related('patient').all().order_by('-id')
    return render(request, 'clinic/sections/cards.html', {'title': 'Kartalar', 'items': items, 'form': form})

def procedures_view(request):
    form = ProcedureServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Muolaja xizmati saqlandi.")
        return redirect('procedures')
    items = ProcedureService.objects.all()
    return render(request, 'clinic/sections/procedures.html', {'title': 'Muolaja xizmatlari', 'items': items, 'form': form})

def ultrasound_view(request):
    form = UziForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "UZI xizmati saqlandi.")
        return redirect('ultrasound')
    items = Uzi.objects.all()
    return render(request, 'clinic/sections/ultrasound.html', {'title': 'UZI', 'items': items, 'form': form})

def wards_view(request):
    form = WardForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Palata ma'lumoti saqlandi.")
        return redirect('wards')
    items = Ward.objects.all()
    return render(request, 'clinic/sections/wards.html', {'title': 'Palatalar', 'items': items, 'form': form})

def lab_view(request):
    form = LaboratoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Tahlil turi saqlandi.")
        return redirect('lab')
    items = Laboratory.objects.all()
    return render(request, 'clinic/sections/lab.html', {'title': 'Laboratoriya', 'items': items, 'form': form})

def medicines_view(request):
    form = MedicineForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Dori vositasi saqlandi.")
        return redirect('medicines')
    items = Medicine.objects.all()
    return render(request, 'clinic/sections/medicines.html', {'title': 'Dori vositalari', 'items': items, 'form': form})

def reagents_view(request):
    form = ReagentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Reagent kiritildi.")
        return redirect('reagents')
    items = Reagent.objects.all()
    return render(request, 'clinic/sections/reagents.html', {'title': 'Reagentlar', 'items': items, 'form': form})

def supplies_view(request):
    form = MedicalMaterialForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Tibbiy material saqlandi.")
        return redirect('supplies')
    items = MedicalMaterial.objects.all()
    return render(request, 'clinic/sections/supplies.html', {'title': 'Tibbiy material', 'items': items, 'form': form})

def household_view(request):
    form = HouseholdItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Xo'jalik tovari saqlandi.")
        return redirect('household')
    items = HouseholdItem.objects.all()
    return render(request, 'clinic/sections/household.html', {'title': "Xo'jalik tovarlar", 'items': items, 'form': form})

def financial_report_view(request):
    income = Appointment.objects.filter(is_paid=True).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'clinic/sections/financial_report.html', {
        'title': 'Moliyaviy hisobotlar', 
        'income': income, 
        'expenses': expenses,
        'profit': income - expenses
    })

def doctors_report_view(request):
    doctors = Doctor.objects.annotate(
        total_visits=Sum('appointments__total_amount')
    ).all()
    return render(request, 'clinic/sections/doctors_report.html', {'title': 'Shifokorlar hisoboti', 'doctors': doctors})

def settings_view(request):
    setting = Setting.objects.first()
    form = SettingForm(request.POST or None, instance=setting)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Sozlamalar yangilandi.")
        return redirect('settings')
    return render(request, 'clinic/sections/settings.html', {'title': 'Sozlamalar', 'form': form, 'setting': setting})

def users_view(request):
    users = User.objects.all()
    return render(request, 'clinic/sections/users.html', {'title': 'Foydalanuvchilar', 'users': users})

# GENERIC O'CHIRISH FUNKSIYASI
def delete_item(request, model_name, item_id):
    models_dict = {
        'partner': Partner, 'expense': Expense, 'card': Card,
        'procedure': ProcedureService, 'uzi': Uzi, 'ward': Ward,
        'lab': Laboratory, 'medicine': Medicine, 'reagent': Reagent,
        'material': MedicalMaterial, 'household': HouseholdItem
    }
    model = models_dict.get(model_name)
    if model:
        item = get_object_or_404(model, id=item_id)
        item.delete()
        messages.info(request, "Ma'lumot muvaffaqiyatli o'chirildi.")
    return redirect(request.META.get('HTTP_REFERER', '/'))