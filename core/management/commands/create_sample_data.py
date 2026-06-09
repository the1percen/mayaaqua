import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from core.models import ProductCategory, Product, GalleryImage, Testimonial, CompanySetting
from PIL import Image, ImageDraw, ImageFont


def create_gradient_image(width, height, color1, color2, text, filepath):
    """Create a gradient image with centered text."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    # Draw text
    try:
        font = ImageFont.truetype('arial.ttf', 20)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - tw) / 2, (height - th) / 2), text, fill='white', font=font)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)


class Command(BaseCommand):
    help = 'Creates sample data for Maya Aqua Solutions website'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Color pairs for gradients
        color_pairs = [
            ((10, 74, 110), (29, 158, 117)),    # Deep blue to green
            ((29, 158, 117), (0, 198, 255)),     # Green to cyan
            ((10, 74, 110), (0, 198, 255)),      # Deep blue to cyan
            ((15, 100, 130), (29, 158, 117)),    # Mid blue to green
        ]

        # --- Step 1: Create Product Categories ---
        self.stdout.write('Creating product categories...')
        categories_data = [
            {'name': 'RO Water Purifiers', 'icon': 'fa-solid fa-filter'},
            {'name': 'Water Softeners', 'icon': 'fa-solid fa-shower'},
            {'name': 'Commercial Plants', 'icon': 'fa-solid fa-industry'},
            {'name': 'Accessories & Spares', 'icon': 'fa-solid fa-gear'},
        ]
        categories = []
        for cat_data in categories_data:
            cat, created = ProductCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon']}
            )
            categories.append(cat)
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'  {status}: {cat.name}')

        # --- Step 2: Create Products (2 per category) ---
        self.stdout.write('Creating products...')
        products_data = [
            # RO Water Purifiers
            {
                'name': 'AquaPure Pro 7-Stage RO',
                'category': categories[0],
                'description': 'Advanced 7-stage RO water purifier with UV+UF technology. Ensures 100% safe and pure drinking water for your family. Features a large 10-litre storage tank with food-grade ABS plastic body.',
                'features': 'RO + UV + UF Purification\n10-Litre Storage Tank\nTDS Controller\nMineralizer Technology\nAuto-Flush System\nLED Purification Indicator',
                'is_featured': True,
            },
            {
                'name': 'AquaShield Compact RO',
                'category': categories[0],
                'description': 'Space-saving compact RO water purifier ideal for small kitchens. Features 5-stage purification with copper-infused alkaline technology for enhanced health benefits.',
                'features': '5-Stage RO Purification\n8-Litre Storage Capacity\nCopper Alkaline Filter\nSmart LED Display\nFilter Change Alert\nWall-Mount Design',
                'is_featured': True,
            },
            # Water Softeners
            {
                'name': 'SoftFlow Whole-House System',
                'category': categories[1],
                'description': 'Premium whole-house water softening system that removes hardness minerals, preventing scale buildup in pipes and appliances. Perfect for homes with hard water problems.',
                'features': 'Ion Exchange Technology\n2000 LPH Flow Rate\nAutomatic Regeneration\nDigital Control Valve\nLow Salt Consumption\n5-Year Warranty',
                'is_featured': True,
            },
            {
                'name': 'SoftTouch Bathroom Softener',
                'category': categories[1],
                'description': 'Compact bathroom water softener designed for shower and tap use. Enjoy soft water for healthier hair and skin. Easy installation without plumbing changes.',
                'features': 'Compact Design\n500 LPH Capacity\nEasy DIY Installation\nNo Electricity Required\nReusable Resin Cartridge\n1-Year Warranty',
                'is_featured': False,
            },
            # Commercial Plants
            {
                'name': 'IndustraPure 500 LPH Plant',
                'category': categories[2],
                'description': 'Industrial-grade RO plant with 500 LPH capacity suitable for small to medium businesses, restaurants, and offices. Built with SS304 frame and high-rejection membranes.',
                'features': '500 LPH Production Capacity\nSS304 Stainless Steel Frame\nHigh-Rejection RO Membranes\nAutomatic Operation\nPressure Gauges & Flow Meters\nPLC Control Panel',
                'is_featured': True,
            },
            {
                'name': 'IndustraPure 2000 LPH Plant',
                'category': categories[2],
                'description': 'High-capacity industrial RO plant designed for large-scale water purification. Ideal for factories, hospitals, and municipal water treatment with 2000 LPH output.',
                'features': '2000 LPH Production Capacity\nSS316 Stainless Steel Frame\nMulti-Stage Filtration\nSCADA Integration Ready\nChemical Dosing System\nOnsite Installation & Training',
                'is_featured': False,
            },
            # Accessories & Spares
            {
                'name': 'RO Membrane Filter Pack',
                'category': categories[3],
                'description': 'High-quality replacement RO membrane filter pack compatible with most domestic RO water purifiers. Ensures optimal purification performance for up to 12 months.',
                'features': '75 GPD Capacity\nHigh Rejection Rate (95%+)\n12-Month Lifespan\nUniversal Compatibility\nEasy Replacement\nTesting Certificate Included',
                'is_featured': False,
            },
            {
                'name': 'Complete Annual Service Kit',
                'category': categories[3],
                'description': 'All-in-one annual maintenance kit for RO water purifiers. Includes sediment filter, carbon filter, RO membrane, and all necessary connectors and O-rings.',
                'features': 'Pre-Filter Set (3 Filters)\nRO Membrane 80 GPD\nPost-Carbon Filter\nAll Connectors & O-Rings\nInstallation Guide\nFree Video Support',
                'is_featured': False,
            },
        ]

        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        for i, prod_data in enumerate(products_data):
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': prod_data['category'],
                    'description': prod_data['description'],
                    'features': prod_data['features'],
                    'is_featured': prod_data['is_featured'],
                }
            )
            if created:
                # Generate placeholder image
                color_pair = color_pairs[i % len(color_pairs)]
                img_filename = f'product_{i + 1}.png'
                img_filepath = os.path.join(media_products_dir, img_filename)
                create_gradient_image(300, 300, color_pair[0], color_pair[1], prod_data['name'], img_filepath)
                product.image = f'products/{img_filename}'
                product.save()
                self.stdout.write(f'  Created: {product.name}')
            else:
                self.stdout.write(f'  Already exists: {product.name}')

        # --- Step 3: Create Testimonials ---
        self.stdout.write('Creating testimonials...')
        testimonials_data = [
            {
                'name': 'Rajesh Kumar',
                'message': 'Maya Aqua installed an RO purifier at our home and the water quality has been exceptional. The service team was professional and the installation was done within an hour. Highly recommended!',
                'rating': 5,
            },
            {
                'name': 'Priya Sharma',
                'message': 'We had terrible hard water issues in our apartment. The whole-house softener from Maya Aqua completely solved the problem. Our skin and hair feel so much better now. Great product!',
                'rating': 5,
            },
            {
                'name': 'Arun Venkatesh',
                'message': 'Got the commercial RO plant installed for our restaurant. The water tastes pure and our customers have noticed the difference. Excellent after-sales support from the Maya Aqua team.',
                'rating': 4,
            },
            {
                'name': 'Deepa Mohan',
                'message': 'Been using Maya Aqua\'s RO purifier for 2 years now. The annual maintenance service is prompt and affordable. The water quality is consistently good. Very satisfied with the product.',
                'rating': 5,
            },
        ]
        for test_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=test_data['name'],
                defaults={
                    'message': test_data['message'],
                    'rating': test_data['rating'],
                }
            )
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'  {status}: {testimonial.name}')

        # --- Step 4: Create Gallery Images ---
        self.stdout.write('Creating gallery images...')
        gallery_data = [
            'Water Purifier Installation',
            'Commercial RO Plant Setup',
            'Happy Customer Family',
            'Service Team at Work',
            'Water Testing Lab',
            'Product Showroom',
        ]
        media_gallery_dir = os.path.join(settings.MEDIA_ROOT, 'gallery')
        for i, caption in enumerate(gallery_data):
            gallery_img, created = GalleryImage.objects.get_or_create(
                caption=caption,
            )
            if created:
                color_pair = color_pairs[i % len(color_pairs)]
                img_filename = f'gallery_{i + 1}.png'
                img_filepath = os.path.join(media_gallery_dir, img_filename)
                create_gradient_image(600, 400, color_pair[0], color_pair[1], caption, img_filepath)
                gallery_img.image = f'gallery/{img_filename}'
                gallery_img.save()
                self.stdout.write(f'  Created: {caption}')
            else:
                self.stdout.write(f'  Already exists: {caption}')

        # --- Step 5: Create Company Settings ---
        self.stdout.write('Creating company settings...')
        CompanySetting.objects.all().delete()
        company = CompanySetting.objects.create(
            phone='+91 7550208154',
            whatsapp='917550208154',
            address='6/35, Astalakshmi Nagar, 2nd Street, Porur, Chennai - 600 116',
            email='mayaaqua26@gmail.com',
            tagline='Transforming Yellow Water to White Clean Water',
            stats_happy_clients=500,
            stats_products_installed=1200,
            stats_cities_served=25,
            stats_years_experience=20,
        )
        self.stdout.write('  Created: Company Settings')

        # --- Step 6: Create Superuser ---
        self.stdout.write('Creating superuser...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@mayaaqua.com', 'admin123')
            self.stdout.write('  Created superuser: admin / admin123')
        else:
            self.stdout.write('  Superuser already exists')

        self.stdout.write(self.style.SUCCESS('\nAll sample data created successfully!'))
