from django.db import models

# # Create your models here.
class Customer(models.Model):
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    mobile = models.IntegerField()
    status = models.IntegerField(default=1)
    image = models.ImageField(upload_to='profile', default = '', blank=True)
    # GENDER_CHOICES = [('male', 'Male'),('female', 'Female'),('other', 'Other'),]
    gender = models.CharField(max_length=6 )

class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    house_no = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=100, default='Unknown')  # ✅ with a safe default
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    address_type = models.CharField(
        max_length=100,
        choices=[('Home', 'Home'), ('Work', 'Work'), ('Other', 'Other')]
    )
    extra_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.house_no}, {self.area}, {self.city}, {self.pincode}, {self.state} ({self.address_type})"



class ContactMessage(models.Model):  # Use this and remove `Message` if not needed
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class OTPVerification(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.email}"


class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



# # OTP model
# class OTPVerification(models.Model):
#     email = models.EmailField(unique=True)
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
    


