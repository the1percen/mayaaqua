from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'products', 'gallery', 'contact']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse('product_detail', args=[obj.pk])
