from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductCategory, GalleryImage, Testimonial, Enquiry

def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:6]
    testimonials = Testimonial.objects.all()[:6]
    gallery_images = GalleryImage.objects.all()[:6]
    categories = ProductCategory.objects.all()
    context = {
        'featured_products': featured_products,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def products_list(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.select_related('category').all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'core/products.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'core/product_detail.html', context)

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'core/gallery.html', {'images': images})

def contact(request):
    if request.method == 'POST':
        try:
            Enquiry.objects.create(
                name=request.POST.get('name', ''),
                phone=request.POST.get('phone', ''),
                email=request.POST.get('email', ''),
                city=request.POST.get('city', ''),
                message=request.POST.get('message', ''),
            )
            messages.success(request, 'Thank you! Your enquiry has been submitted successfully. We will contact you shortly.')
        except Exception:
            messages.error(request, 'Something went wrong. Please try again.')
        return redirect('contact')
    return render(request, 'core/contact.html')
