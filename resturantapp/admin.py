from django.contrib import admin
from unfold.admin import ModelAdmin
# from .models import Address, MenuItem, Order, OrderItem, CartItem, Review
from .models import Address,MenuItem,Order,OrderItem,CartItem,Review,Reservation
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display   = ('name', 'category', 'momo_type', 'price', 'is_available', 'is_featured')
    list_filter    = ('category', 'momo_type', 'is_available', 'is_featured')
    list_editable  = ('price', 'is_available', 'is_featured')
    search_fields  = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter   = ('status',)
    list_editable = ('status',)
    search_fields = ('user__username',)
    inlines       = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('reviewer_name', 'rating', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    list_filter   = ('rating', 'is_approved')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'added_at')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'guests', 'status', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_editable = ('status',)
    ordering = ('-created_at',)