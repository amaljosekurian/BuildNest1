from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class Usertable(AbstractUser):
    username = models.CharField(max_length=150, unique=True)  # Add username field
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_contractor = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_purchase_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    

class PlotBasicData(models.Model):
    approximate_budget = models.DecimalField(max_digits=10, decimal_places=2)
    plot_address = models.TextField()
    plot_id_document = models.FileField(upload_to='plot_id_documents/')
    plot_location = models.CharField(max_length=255)
    square_feet = models.PositiveIntegerField()
    

class ProjectData(models.Model):
    num_floors = models.PositiveIntegerField()
    work_area_required = models.BooleanField(default=False)
    store_room_required = models.BooleanField(default=False)
    dining_room_required = models.BooleanField(default=False)
    kitchen_type = models.CharField(max_length=10, choices=[('open', 'Open Kitchen'), ('normal', 'Normal Kitchen')])
    additional_amenities = models.TextField(blank=True, null=True)

class FloorDetails(models.Model):
    project = models.ForeignKey(ProjectData, on_delete=models.CASCADE)
    floor_number = models.PositiveIntegerField()
    num_rooms = models.PositiveIntegerField()
    num_bathrooms = models.PositiveIntegerField()

class PlotData(models.Model):
    plot_user = models.ForeignKey(Usertable, on_delete=models.CASCADE, null=True, blank=True)
    plotBaseData = models.ForeignKey(PlotBasicData, on_delete=models.CASCADE, null=True)
    projectdata = models.ForeignKey(ProjectData, on_delete=models.CASCADE, null=True)
    contractor = models.ForeignKey(Usertable, on_delete=models.CASCADE, null=True, related_name='contractor', limit_choices_to={'is_contractor': True})
    engineer = models.ForeignKey(Usertable, on_delete=models.CASCADE, null=True, related_name='engineer', limit_choices_to={'is_engineer': True})
    payment_is_Done = models.BooleanField(default=False)
    plan_pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)
    plan_fee = models.BigIntegerField(null=True)
    payment_request = models.BooleanField(default=False)

class PlotImages(models.Model):
    plot = models.ForeignKey(PlotData, on_delete=models.CASCADE, null=True)
    plot_images = models.ImageField(upload_to='plot_images/', blank=True, null=True)
    
    
class ConstructionSite(models.Model):
    site_name = models.CharField(max_length=100,null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    upload_permits = models.FileField(upload_to='permits/')
    approximate_budget = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    additional_description = models.TextField(null=True)
    site_location = models.CharField(max_length=255,null=True)

    # Foreign key relationship to UserTable
    user = models.ForeignKey(Usertable, on_delete=models.CASCADE)
    

class Worker(models.Model):
    name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    aadhar_document = models.FileField(upload_to='aadhar_documents/',null=True, blank=True)
    mobile_number = models.CharField(max_length=15)
    user = models.ForeignKey(Usertable, on_delete=models.CASCADE)
    site = models.ForeignKey('ConstructionSite', on_delete=models.CASCADE)
    salary_frequency = models.CharField(max_length=10,null=True) 
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    def __str__(self):
        return self.site_name
    
    
class Product(models.Model):
    category = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100,null=True)
    brand_name = models.CharField(max_length=100)
    color = models.CharField(max_length=100, blank=True, null=True)
    stocks = models.IntegerField()
    product_description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    price_per_unit = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.brand_name
    

class CartItem(models.Model):
    user = models.ForeignKey(Usertable, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have a Product model
    quantity       =     models.IntegerField(default=1)
    price       =     models.IntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product}"
    
    

class ConstructionSiteAssociation(models.Model):
    construction_site = models.ForeignKey(ConstructionSite, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Usertable, on_delete=models.CASCADE)
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


