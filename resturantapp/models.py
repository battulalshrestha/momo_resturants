from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Address(models.Model):
    name    = models.CharField(max_length=255)
    email   = models.EmailField()
    phone   = models.CharField(max_length=20)          # was IntegerField — phone numbers aren't integers
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f'{self.name} – {self.phone}'


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('buff',    'Buff'),
        ('chicken', 'Chicken'),
        ('veg',     'Vegetarian'),
    ]
    TYPE_CHOICES = [
        ('steam', 'Steam'),
        ('fried', 'Fried'),
        ('chilly', 'Chilly'),
    ]

    name         = models.CharField(max_length=200)
    category     = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    momo_type    = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price        = models.DecimalField(max_digits=8, decimal_places=2)
    description  = models.TextField(blank=True)
    image        = models.ImageField(upload_to='menu/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_featured  = models.BooleanField(default=False)
    created_at   = models.DateTimeField()

    class Meta:
        ordering = ['category', 'momo_type']

    def __str__(self):
        return f'{self.get_category_display()} {self.get_momo_type_display()} Momo – रु{self.price}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('preparing',  'Preparing'),
        ('ready',      'Ready'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} by {self.user.username} – {self.status}'


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item     = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2,db_default=0)  # snapshot at order time

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.quantity}× {self.item} in Order #{self.order.id}'


class CartItem(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    item     = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')

    def subtotal(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f'{self.user.username}: {self.quantity}× {self.item.name}'


class Review(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating        = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    comment       = models.TextField()
    is_approved   = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reviewer_name} – {self.rating}★'

    def stars(self):
        return range(self.rating)

    def empty_stars(self):
        return range(5 - self.rating)



class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.date} {self.time}'