"""
Seed the database with sample data.

Usage:
    python manage.py seed_data

Sample credentials:
    Admin:   admin@ghardekho.in   /  admin123
    Agents:  rajesh@primerealty.in, priya@blrhomes.in  /  agent123
    Buyers:  amit@email.com, sneha@email.com  /  buyer123
"""

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed the database with sample users, properties, leads and blog posts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n Seeding GharDekho database...\n'))
        self._create_users()
        self._create_blog_categories()
        self._create_properties()
        self._create_leads()
        self._create_blog_posts()
        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!\n'))
        self.stdout.write('Sample credentials:')
        self.stdout.write('  Admin : admin@ghardekho.in      / admin123')
        self.stdout.write('  Agent : rajesh@primerealty.in   / agent123')
        self.stdout.write('  Agent : priya@blrhomes.in       / agent123')
        self.stdout.write('  Buyer : amit@email.com          / buyer123')
        self.stdout.write('  Buyer : sneha@email.com         / buyer123\n')

    def _create_users(self):
        from accounts.models import User
        if not User.objects.filter(email='admin@ghardekho.in').exists():
            User.objects.create_superuser(email='admin@ghardekho.in', name='GharDekho Admin', password='admin123', phone='9000000001')
            self.stdout.write('  admin created')
        agents = [
            dict(email='rajesh@primerealty.in', name='Rajesh Sharma', phone='9876543210', city='Mumbai',    agency='Prime Realty India',        rera_number='P51800047290',          experience=12),
            dict(email='priya@blrhomes.in',     name='Priya Nair',    phone='9765432109', city='Bangalore', agency='Bangalore Homes Pvt. Ltd.', rera_number='PRM/KA/RERA/1251/310',  experience=8),
            dict(email='sunil@ncrlands.in',     name='Sunil Gupta',   phone='9654321098', city='Gurgaon',   agency='NCR Lands & Properties',    rera_number='RC/REP/HARERA/GGM/2024/01', experience=10),
            dict(email='kavitha@hyd.in',        name='Kavitha Reddy', phone='9543210987', city='Hyderabad', agency='Hyderabad Rentals',         rera_number='P02400003396',          experience=6),
        ]
        self.agents = []
        for a in agents:
            u, created = User.objects.get_or_create(email=a['email'], defaults={**a, 'role': 'agent', 'is_verified': True})
            if created:
                u.set_password('agent123')
                u.save()
            self.agents.append(u)
        self.stdout.write(f'  {len(self.agents)} agents created')
        buyers = [
            dict(email='amit@email.com',  name='Amit Kumar',  phone='9432109876', city='Mumbai'),
            dict(email='sneha@email.com', name='Sneha Joshi', phone='9321098765', city='Pune'),
            dict(email='rohit@email.com', name='Rohit Verma', phone='9210987654', city='Bangalore'),
        ]
        self.buyers = []
        for b in buyers:
            u, created = User.objects.get_or_create(email=b['email'], defaults={**b, 'role': 'buyer'})
            if created:
                u.set_password('buyer123')
                u.save()
            self.buyers.append(u)
        self.stdout.write(f'  {len(self.buyers)} buyers created')

    def _create_blog_categories(self):
        from blog.models import Category
        cats = ['Investment', 'Guide', 'Market Trends', 'Legal', 'Finance', 'City Guide']
        self.categories = {}
        for name in cats:
            obj, _ = Category.objects.get_or_create(name=name)
            self.categories[name] = obj
        self.stdout.write(f'  {len(cats)} blog categories created')

    def _create_properties(self):
        from properties.models import Property, PropertyAmenity
        props = [
            dict(owner=self.agents[0], title='3 BHK Luxury Apartment in Bandra West',       listing_type='sell', prop_type='Flat',       status='active', city='Mumbai',    locality='Bandra West',    address='Sea Breeze Apartments, Bandra West, Mumbai - 400050',         description='Stunning 3 BHK apartment with breathtaking sea views. Fully furnished with premium fittings, modular kitchen, and spacious balconies.', price=18500000, area=1450, bhk='3 BHK', floor='8th of 14', age='2 years',  furnishing='Fully Furnished', facing='West',      negotiable=True,  rera_number='P51800047290',               is_featured=True,  is_verified=True,  amenities=['Parking','Gym','Swimming Pool','Lift','Security','Power Backup','Club House','Garden']),
            dict(owner=self.agents[1], title='4 BHK Independent Villa in Whitefield',        listing_type='sell', prop_type='Villa',      status='active', city='Bangalore', locality='Whitefield',     address='Green Valley Villas, ITPL Road, Whitefield, Bangalore - 560066', description='Spacious villa in a gated community. Features 4 bedrooms, home theatre, terrace garden, and private car park.', price=32000000, area=3200, bhk='4 BHK', floor='G+2',    age='5 years',  furnishing='Semi Furnished',  facing='East',      negotiable=False, rera_number='PRM/KA/RERA/1251/310',       is_featured=True,  is_verified=True,  amenities=['Parking','Garden','Security','Power Backup','Rain Water Harvesting','CCTV']),
            dict(owner=self.agents[0], title='2 BHK Modern Flat in Powai',                   listing_type='sell', prop_type='Flat',       status='active', city='Mumbai',    locality='Powai',          address='Hiranandani Gardens, Powai, Mumbai - 400076',                    description='Well-designed 2 BHK in Hiranandani Gardens township. Excellent connectivity to major IT hubs.', price=9800000,  area=950,  bhk='2 BHK', floor='5th of 20', age='3 years',  furnishing='Unfurnished',     facing='North',     negotiable=True,  rera_number='',                           is_featured=False, is_verified=False, amenities=['Parking','Gym','Lift','Security','Power Backup']),
            dict(owner=self.agents[2], title='Residential Plot in Gurgaon Sector 85',         listing_type='sell', prop_type='Plot',       status='active', city='Gurgaon',   locality='Sector 85',      address='Sector 85, Gurgaon, Haryana - 122004',                           description='Prime residential plot. Corner plot with wide road frontage. Clear title, all approvals in place.', price=7500000,  area=250,  bhk='',      floor='',         age='',         furnishing='',                facing='North-East', negotiable=True,  rera_number='RC/REP/HARERA/GGM/2024/01', is_featured=False, is_verified=True,  amenities=['Corner Plot','Wide Road','24/7 Security','Gated Colony']),
            dict(owner=self.agents[3], title='3 BHK Premium Flat for Rent in Banjara Hills',  listing_type='rent', prop_type='Flat',       status='active', city='Hyderabad', locality='Banjara Hills',  address='Road No. 12, Banjara Hills, Hyderabad - 500034',                 description='Luxuriously furnished 3 BHK for rent. Walking distance to top restaurants, malls and hospitals.', price=55000,    area=1800, bhk='3 BHK', floor='4th of 8',  age='4 years',  furnishing='Fully Furnished', facing='South',     negotiable=True,  rera_number='',                           is_featured=True,  is_verified=True,  amenities=['Parking','Gym','Swimming Pool','Lift','Security','Power Backup']),
            dict(owner=self.agents[1], title='1 BHK Cozy Apartment for Rent in Koramangala',  listing_type='rent', prop_type='Flat',       status='active', city='Bangalore', locality='Koramangala',    address='5th Block, Koramangala, Bangalore - 560095',                     description='Well-maintained 1 BHK in the heart of Koramangala. Ideal for young professionals.', price=22000,    area=580,  bhk='1 BHK', floor='2nd of 6',  age='6 years',  furnishing='Semi Furnished',  facing='East',      negotiable=False, rera_number='',                           is_featured=False, is_verified=False, amenities=['Parking','Lift','Security','Power Backup']),
            dict(owner=self.agents[3], title='5 BHK Luxury Villa in Jubilee Hills',           listing_type='sell', prop_type='Villa',      status='active', city='Hyderabad', locality='Jubilee Hills',  address='Road No. 36, Jubilee Hills, Hyderabad - 500033',                 description='Ultra-luxury villa with home theatre, heated pool, landscaped garden and premium Italian fittings.', price=75000000, area=5500, bhk='5 BHK', floor='G+2',    age='1 year',   furnishing='Fully Furnished', facing='North',     negotiable=False, rera_number='P02400003396',               is_featured=True,  is_verified=True,  amenities=['Parking','Swimming Pool','Garden','Security','Home Theatre','Solar Power','EV Charging']),
            dict(owner=self.agents[2], title='2 BHK Apartment in Aundh, Pune',                listing_type='sell', prop_type='Flat',       status='active', city='Pune',      locality='Aundh',          address='Aundh Road, Pune - 411007',                                      description='Bright and airy 2 BHK in prime Aundh locality. Well-ventilated rooms with modular kitchen.', price=7200000,  area=1050, bhk='2 BHK', floor='3rd of 10', age='4 years',  furnishing='Semi Furnished',  facing='South-East', negotiable=True,  rera_number='P52100015167',               is_featured=False, is_verified=True,  amenities=['Parking','Gym','Lift','Security','Power Backup','Kids Play Area']),
        ]
        self.properties = []
        for p in props:
            amenities = p.pop('amenities')
            obj, created = Property.objects.get_or_create(title=p['title'], defaults=p)
            if created:
                for name in amenities:
                    PropertyAmenity.objects.create(property=obj, name=name)
            self.properties.append(obj)
        self.stdout.write(f'  {len(self.properties)} properties created')

    def _create_leads(self):
        from leads.models import Lead
        leads_data = [
            dict(property=self.properties[0], buyer=self.buyers[0], name=self.buyers[0].name, email=self.buyers[0].email, phone='9432109876', message='Very interested. Please share more details.', status='new'),
            dict(property=self.properties[1], buyer=self.buyers[2], name=self.buyers[2].name, email=self.buyers[2].email, phone='9210987654', message='Can we schedule a site visit this weekend?',   status='visit_set'),
            dict(property=self.properties[4], buyer=self.buyers[1], name=self.buyers[1].name, email=self.buyers[1].email, phone='9321098765', message='Is rent negotiable? Looking for 11-month agreement.', status='contacted'),
        ]
        count = sum(1 for ld in leads_data if Lead.objects.get_or_create(property=ld['property'], buyer=ld['buyer'], defaults=ld)[1])
        self.stdout.write(f'  {count} leads created')

    def _create_blog_posts(self):
        from blog.models import BlogPost
        posts = [
            dict(title='Best Areas to Invest in Patna Real Estate in 2024', author=self.agents[0], category=self.categories['Investment'], excerpt='Patna is rapidly transforming into a real estate hotspot. Top localities: Boring Road, Bailey Road, Danapur.', content='Patna has seen rapid development with the Metro, new ring roads, and AIIMS hospital driving real estate demand.\n\nTop areas: Boring Road (Rs.45-80L for 2BHK), Bailey Road (mid-segment), Danapur (affordable plots), Rajendra Nagar (established), Phulwarisharif (upcoming).', status='published', is_featured=True,  read_time=6,  tags='patna,investment,bihar',    published_at=timezone.now()),
            dict(title='Complete Guide for First-Time Home Buyers in India', author=self.agents[1], category=self.categories['Guide'],      excerpt='Step-by-step guide covering everything from home loan eligibility to registration charges.',                   content='Step 1: Budget - use the 40% EMI rule.\nStep 2: Check home loan eligibility at 2-3 banks.\nStep 3: Shortlist 5-6 properties.\nStep 4: Legal due diligence - RERA, title documents.\nStep 5: Negotiate - sellers quote 5-15% above floor price.', status='published', is_featured=True,  read_time=10, tags='guide,home buying,loan',    published_at=timezone.now()),
            dict(title='Mumbai Property Market Trends 2024',                 author=self.agents[0], category=self.categories['Market Trends'], excerpt='Mumbai saw 14% price increase in 2023. Analysis across Bandra, Powai and Thane.',                          content='Mumbai market analysis:\nBandra West: Rs.35,000-55,000/sqft\nPowai: Rs.18,000-28,000/sqft\nThane: Rs.9,000-16,000/sqft\nStrong demand from IT professionals and HNIs continues in 2024.', status='published', is_featured=False, read_time=8,  tags='mumbai,market,2024',        published_at=timezone.now()),
            dict(title='RERA Explained: What Every Buyer Must Know',          author=self.agents[1], category=self.categories['Legal'],      excerpt='RERA is your shield as a buyer. Learn protections and how to verify registration.',                            content='RERA 2016 mandates registration of projects above 500 sqmt. Protects buyers from delays and fund diversion.\nVerify on state RERA website. Always check RERA number before booking.', status='published', is_featured=False, read_time=7,  tags='rera,legal,buyer',          published_at=timezone.now()),
            dict(title='10 Tips to Get the Best Home Loan Rate',              author=self.agents[0], category=self.categories['Finance'],   excerpt='A 0.5% difference saves lakhs over the loan tenure. Here are 10 proven tips.',                                   content='1. Maintain CIBIL above 750\n2. Apply to multiple banks\n3. Prefer floating rate\n4. Higher down payment\n5. Balance transfer after 2 years if rates drop\n6. Add co-applicant\n7. Choose shorter tenure\n8. Pre-pay when possible\n9. Avoid defaults\n10. Compare NBFCs too', status='published', is_featured=False, read_time=5,  tags='home loan,finance,tips',    published_at=timezone.now()),
        ]
        count = sum(1 for p in posts if BlogPost.objects.get_or_create(title=p['title'], defaults=p)[1])
        self.stdout.write(f'  {count} blog posts created')
