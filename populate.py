import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayaaqua_proj.settings')
django.setup()

from core.models import Product, ProductCategory, GalleryImage

def populate():
    # Clear existing to prevent duplicates
    Product.objects.all().delete()
    ProductCategory.objects.all().delete()
    GalleryImage.objects.all().delete()

    # Create Categories
    industrial = ProductCategory.objects.create(name='Industrial Systems', icon='fa-solid fa-industry')
    commercial = ProductCategory.objects.create(name='Commercial Purifiers', icon='fa-solid fa-building-water')

    # Create Products
    Product.objects.create(
        name='Water Softener Plant',
        category=industrial,
        image='gallery/gallery_1.jpeg',
        description='High-capacity industrial water softener plant designed for large scale water treatment. Effectively removes hardness minerals to protect equipment and pipelines.',
        features='Fully automatic operation\nFRP/Stainless Steel vessel options\nHigh flow rate\nLow maintenance\nDigital control valve',
        is_featured=True
    )

    Product.objects.create(
        name='Multimedia Filter System',
        category=industrial,
        image='gallery/gallery_2.jpeg',
        description='Advanced multimedia filtration system utilizing multiple layers of sand, gravel, and anthracite to remove suspended solids and turbidity from water.',
        features='Multi-layer filtration\nAutomatic backwash\nHigh dirt holding capacity\nCost-effective\nDurable construction',
        is_featured=True
    )

    Product.objects.create(
        name='Iron Remover Filter',
        category=industrial,
        image='gallery/gallery_3.jpeg',
        description='Specialized iron removal filter system that eliminates dissolved iron and manganese from groundwater sources, preventing staining and improving water quality.',
        features='High iron removal efficiency\nNo chemical regeneration required\nLong life media\nCompact design\nLow pressure drop',
        is_featured=True
    )

    Product.objects.create(
        name='Commercial RO Plant',
        category=commercial,
        image='gallery/gallery_4.jpeg',
        description='State-of-the-art commercial Reverse Osmosis (RO) plant providing premium purification. Ideal for institutions, commercial buildings, and bottling plants.',
        features='99% dissolved solids removal\nHigh-pressure multistage pumps\nStainless steel skid\nAdvanced RO membranes\nReal-time TDS monitoring',
        is_featured=True
    )

    # Create Gallery Images
    for i in range(1, 6):
        GalleryImage.objects.create(
            image=f'gallery/gallery_{i}.jpeg',
            caption=f'Maya Aqua Solutions Installation #{i}'
        )
    
    # Add new basic RO images
    GalleryImage.objects.create(image='gallery/gallery_6.png', caption='Standard Reverse Osmosis System')
    GalleryImage.objects.create(image='gallery/gallery_7.png', caption='Industrial Water Filter System')
    
    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
