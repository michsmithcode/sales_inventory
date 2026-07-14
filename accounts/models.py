from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#from django.contrib.auth.models import User


ROLE_CHOICES = [
    ("super_admin", "SUPER ADMIN"),
    ("manager", "MANAGER"),
    ("sales_rep", "SALES REPRESENTATIVE"),
    ("store_keeper", "STORE KEEPER"),
    ("accountant", "ACCOUNTANT"),
    ("auditor", "AUDITOR")
    
    ]



GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female")
    ]


"""
This line Changes from username login to email
"""
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # hash user password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)




class CustomUser(AbstractUser):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) ###
    """
    Custom User Model
    """

    middle_name = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100)
    email= models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    profile_photo = models.ImageField(upload_to="profile_picture/", blank=True,  null=True)
    is_otp_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    username =None
    
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []
 
 
 
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
 

class StaffProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="staff_profile")
    employee_code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"

    def __str__(self):
        return f"{self.employee_code} - {self.user.get_full_name()}"


