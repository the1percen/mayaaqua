from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text='FontAwesome class e.g. fa-solid fa-filter')

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField()
    features = models.TextField(help_text='One feature per line', blank=True)
    is_featured = models.BooleanField(default=False)

    def features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.caption or f'Gallery Image {self.pk}'

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.name

class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f'{self.name} - {self.city}'

class CompanySetting(models.Model):
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, help_text='International format without +, e.g. 919876543210')
    address = models.TextField()
    email = models.EmailField(default="mayaaqua26@gmail.com")
    tagline = models.CharField(max_length=200)
    stats_happy_clients = models.IntegerField(default=500)
    stats_products_installed = models.IntegerField(default=1200)
    stats_cities_served = models.IntegerField(default=25)
    stats_years_experience = models.IntegerField(default=10)

    class Meta:
        verbose_name_plural = 'Company Settings'

    def __str__(self):
        return 'Company Settings'
