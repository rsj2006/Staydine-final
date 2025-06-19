from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=75, unique=True)
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    mobile_no = models.CharField(max_length=15)
    aadhaar_no = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class StaffRole(models.Model):
    role_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.role_name


class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    mobile_no = models.DecimalField(max_digits=10, decimal_places=0)
    manager = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(StaffRole, on_delete=models.CASCADE)
    hire_date = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Suite(models.Model):
    room_number = models.IntegerField(primary_key=True)
    room_type = models.CharField(max_length=50)
    bed_type = models.CharField(max_length=20, default='Double')
    price_per_night = models.DecimalField(max_digits=15, decimal_places=2)
    max_occupants = models.PositiveSmallIntegerField(default=2)
    is_available = models.BooleanField(default=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Room {self.room_number} ({self.room_type})'


class RestaurantDiner(models.Model):
    table_number = models.IntegerField(primary_key=True)
    capacity = models.PositiveIntegerField(default=2)
    is_available = models.BooleanField(default=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Table {self.table_number}'


class StaffAssignment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    room = models.ForeignKey(Suite, on_delete=models.CASCADE, null=True, blank=True)
    table = models.ForeignKey(RestaurantDiner, on_delete=models.CASCADE, null=True, blank=True)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Assignment for {self.staff} on {self.assigned_date}'


class Booking(models.Model):
    STATUSES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Suite, on_delete=models.CASCADE, null=True, blank=True)
    table = models.ForeignKey(RestaurantDiner, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateField()
    event_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stat = models.CharField(max_length=10, choices=STATUSES, default='Pending')

    def __str__(self):
        return f'Booking {self.pk} by {self.user}'


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUSES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    stat = models.CharField(max_length=10, choices=STATUSES, default='Pending')

    def __str__(self):
        return f'Order {self.pk} by {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'Item {self.menu_item} in Order {self.order}'


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    max_guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name


class EventBooking(models.Model):
    STATUSES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    stat = models.CharField(max_length=10, choices=STATUSES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Event Booking {self.pk} for {self.event}'
