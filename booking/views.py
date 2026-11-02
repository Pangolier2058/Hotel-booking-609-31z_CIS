from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Room, Booking, Guest

def index(request):
    rooms = Room.objects.all()
    return render(request, 'booking/index.html', {'rooms': rooms})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'booking/login.html', {'error': 'Неверное имя пользователя или пароль'})
    return render(request, 'booking/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            return render(request, 'booking/register.html', {'error': 'Пароли не совпадают'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'booking/register.html', {'error': 'Пользователь с таким именем уже существует'})
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('index')
    
    return render(request, 'booking/register.html')

def user_logout(request):
    logout(request)
    return redirect('index')

def book_room(request, room_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        num_people = request.POST.get('num_people')
        
        # Проверка 1: количество человек не больше вместимости
        try:
            num_people = int(num_people)
            if num_people < 1 or num_people > room.capacity:
                return render(request, 'booking/book.html', {
                    'room': room,
                    'error': f'Количество человек должно быть от 1 до {room.capacity}'
                })
        except (ValueError, TypeError):
            return render(request, 'booking/book.html', {
                'room': room,
                'error': 'Некорректное количество человек'
            })
        
        # Проверка 2: даты корректны
        from datetime import date
        try:
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)
        except (ValueError, TypeError):
            return render(request, 'booking/book.html', {
                'room': room,
                'error': 'Некорректный формат даты'
            })
        
        today = date.today()
        
        if start < today:
            return render(request, 'booking/book.html', {
                'room': room,
                'error': 'Дата заезда не может быть в прошлом'
            })
        
        if end <= start:
            return render(request, 'booking/book.html', {
                'room': room,
                'error': 'Дата выезда должна быть позже даты заезда'
            })
        
        # Проверка 3: нет пересечения с существующими бронированиями
        overlapping = Booking.objects.filter(
            room=room,
            start_date__lte=end,
            end_date__gte=start
        ).exists()
        
        if overlapping:
            return render(request, 'booking/book.html', {
                'room': room,
                'error': 'Номер уже забронирован на эти даты. Выберите другие даты.'
            })
        
        # Создание бронирования
        guest, created = Guest.objects.get_or_create(full_name=guest_name)
        
        Booking.objects.create(
            room=room,
            guest=guest,
            start_date=start_date,
            end_date=end_date,
            num_people=num_people
        )
        return redirect('success')
    
    return render(request, 'booking/book.html', {'room': room})

def success(request):
    return render(request, 'booking/success.html')