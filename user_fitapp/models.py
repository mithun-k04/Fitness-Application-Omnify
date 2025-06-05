from django.db import models

class FitnessClass(models.Model):  
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    description = models.TextField(max_length=1000,default='')
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} - {self.date_time.strftime('%Y-%m-%d %H:%M')}"

    def book_slot(self):
        if self.available_slots > 0:
            slot = self.available_slots
            self.available_slots -= 1
            self.save(update_fields=['available_slots'])
            return slot
        return False

class User(models.Model):  
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15)  
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Booking(models.Model):  
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=100, default='')
    slot = models.IntegerField(default=0)
    booked_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name} @ {self.fitness_class.date_time}"
