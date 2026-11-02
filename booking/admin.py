from django.contrib import admin
from .models import Building, Room, Guest, Booking, Stay


@admin.action(description='✅ Подтвердить заселение (Создать Проживание)')
def confirm_checkin(modeladmin, request, queryset):
    for booking in queryset:
        Stay.objects.get_or_create(
            room=booking.room,
            guest=booking.guest,
            start_date=booking.start_date,
            end_date=booking.end_date,
            num_people=booking.num_people
        )
    modeladmin.message_user(request, f"Успешно создано записей о проживании: {queryset.count()}")


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'building_id', 'room_number', 'capacity', 'price')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    actions = [confirm_checkin]
    list_display = ('id', 'room_id', 'guest_id', 'start_date', 'end_date', 'num_people')


@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_id', 'guest_id', 'start_date', 'end_date', 'num_people')