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
        image='products/water_softener_plant.png',
        description='High-capacity industrial water softener plant designed for large scale water treatment. Effectively removes hardness minerals to protect equipment and pipelines.',
        features='Fully automatic operation\nFRP/Stainless Steel vessel options\nHigh flow rate\nLow maintenance\nDigital control valve',
        is_featured=True
    )

    Product.objects.create(
        name='Multimedia Filter System',
        category=industrial,
        image='products/multimedia_filter.png',
        description='Advanced multimedia filtration system utilizing multiple layers of sand, gravel, and anthracite to remove suspended solids and turbidity from water.',
        features='Multi-layer filtration\nAutomatic backwash\nHigh dirt holding capacity\nCost-effective\nDurable construction',
        is_featured=True
    )

    Product.objects.create(
        name='Iron Remover Filter',
        category=industrial,
        image='products/iron_remover.png',
        description='Specialized iron removal filter system that eliminates dissolved iron and manganese from groundwater sources, preventing staining and improving water quality.',
        features='High iron removal efficiency\nNo chemical regeneration required\nLong life media\nCompact design\nLow pressure drop',
        is_featured=True
    )

    Product.objects.create(
        name='Commercial RO Plant',
        category=commercial,
        image='products/ro_plant.png',
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
    
    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
