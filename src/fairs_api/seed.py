import click
import datetime
import random
import faker
from flask import current_app

from .models import *

cities = ["New York", "Los Angeles", "Chicago", "Houston", "Miami",
          "San Francisco", "Boston", "Seattle", "Dallas", "Atlanta"]
streets = ["Main Street", "Oak Avenue", "Elm Street", "Broadway", "Maple Drive",
           "Pine Road", "Cedar Lane", "Sunset Boulevard", "River Street", "Park Avenue"]
zip_codes = ["10-001", "90-001", "60-601", "77-001", "33-101", "94-101",
             "02-101", "98-101", "75-201", "30-301"]
fantasy_words = [
    "Mystic", "Dragon", "Frost", "Shadow", "Elven", "Enchanted", "Crystal", "Sorcerer", "Celestial", "Phoenix",
    "Starlight", "Moonshadow", "Dreamweaver", "Firestorm", "Stormrider", "Abyssal", "Eternal", "Nebula", "Whisperwind", "Faerie",
    "Spellbound", "Lorekeeper", "Wyrmbane", "Shadowfury", "Twilight", "Serpent", "Sapphire", "Amethyst", "Wraith", "Thunderheart"
]

# Initialize a fake data generator
fake = faker.Faker(locale="en_US")


@click.command('seed')
def seed_db():
    clean_database()

    click.echo("Creating industries")
    create_industries()
    click.echo("Creating users")
    create_users()
    click.echo("Creating companies")
    create_companies()
    click.echo("Creating halls")
    create_halls()
    click.echo("Creating fairs")
    create_fairs()
    click.echo("Database has been populated")


def clean_database():
    meta = db.metadata
    with current_app.app_context():
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


def create_fairs():
    base_date = datetime.date.today() + datetime.timedelta(days=30)
    fairs = [
        { "hall_id": 1, "image": "/assets/fair_1.jpg", "published": True, "organizer_id": 21, "name": "Tech Odyssey Expo", "description": "Embark on a captivating journey into the heart of technology at the Tech Odyssey Expo. Get ready to be amazed by the relentless march of innovation and the boundless possibilities of the digital realm. This immersive event is a testament to human ingenuity, showcasing the latest advancements in artificial intelligence, virtual reality, and groundbreaking tech marvels. Dive into a futuristic realm where imagination meets reality, and the boundaries of what's possible are pushed to new horizons. Engage with visionaries, attend thought-provoking seminars, and witness technology's transformative power firsthand. At Tech Odyssey, the future is now, and the possibilities are endless." },
        { "hall_id": 2, "image": "/assets/fair_2.jpg", "published": True, "organizer_id": 22, "name": "PharmaLife Showcase", "description": "The PharmaLife Showcase is a grand celebration of humanity's pursuit of wellness and healing. It's not just an event; it's a profound journey through the corridors of medical discovery, where hope and healing intersect. This is your chance to explore the world of life-saving medications, groundbreaking treatments, and medical wonders. The showcase is a testament to the tireless efforts of medical professionals and researchers who strive to improve lives. Immerse yourself in a world of science, compassion, and progress, where medical marvels and innovative therapies come to life. At PharmaLife, we believe in a world where health knows no bounds, and this showcase is your gateway to a brighter future." },
        { "hall_id": 3, "image": "/assets/fair_3.jpg", "published": True, "organizer_id": 23, "name": "Finance Frontier Summit", "description": "Welcome to the Finance Frontier Summit, where financial wisdom and opportunity collide. This extraordinary event is your gateway to a world of financial prosperity and security. Explore the dynamic landscape of banking, investments, and insurance services. The summit offers you an insider's view of financial stability, wealth building, and the protection of your assets. Join industry experts and thought leaders as they unravel the secrets to financial success. Engage in interactive workshops, discover investment strategies, and take the reins of your financial future. At the Finance Frontier Summit, we believe that a secure financial future is within your reach, and this is where your journey begins." },
        { "hall_id": 4, "image": "/assets/fair_4.jpg", "published": True, "organizer_id": 24, "name": "ShopWonders Extravaganza", "description": "Enter a realm of retail and e-commerce like no other at the ShopWonders Extravaganza. This spectacular extravaganza is a shopping adventure of epic proportions, where fashion, electronics, and home decor combine in a dazzling showcase of choice and style. With a vast array of options, you'll find items that speak to your individuality and enhance your lifestyle. From the latest fashion trends to cutting-edge technology and exquisite home furnishings, this is where dreams come true and desires are fulfilled. ShopWonders Extravaganza is not just a shopping experience; it's a journey of discovery and self-expression. Join us in celebrating the wonder of choice and the magic of retail." },
        { "hall_id": 5, "image": "/assets/fair_5.jpg", "published": True, "organizer_id": 25, "name": "RenewaTech Symposium", "description": "Join us for the RenewaTech Symposium, a gateway to sustainable energy solutions. This extraordinary event brings together the brightest minds and pioneering technologies in the field of renewable energy. Explore the vast potential of solar, wind, and eco-friendly energy sources. Engage with experts, discover innovative solutions, and step into a world where environmental consciousness meets technological innovation." },
        { "hall_id": 6, "image": "/assets/fair_6.jpg", "published": True, "organizer_id": 26, "name": "AutoFusion Showcase", "description": "Rev up your engines at the AutoFusion Showcase. Get up close and personal with the latest in automotive excellence, from electric vehicles to sleek sports cars. This showcase is a testament to the future of transportation, where innovation and performance converge." },
        { "hall_id": 7, "image": "/assets/fair_7.jpg", "published": True, "organizer_id": 27, "name": "AeroTech Expo", "description": "The AeroTech Expo is your passport to the skies and beyond. Discover cutting-edge aircraft, aerospace technologies, and defense systems that safeguard our world. This expo is your window to the future of aviation, space exploration, and global security." },
        { "hall_id": 8, "image": "/assets/fair_8.jpg", "published": True, "organizer_id": 28, "name": "Culinary Delights Expo", "description": "Satisfy your culinary curiosity at the Culinary Delights Expo. Indulge in the exquisite flavors, aromas, and innovations of the culinary world. This expo is a journey through the gastronomic arts, where renowned chefs, food artisans, and connoisseurs gather to showcase their culinary mastery. Experience the joy of food, the thrill of new tastes, and the art of the culinary craft." },
        { "hall_id": 9, "image": "/assets/fair_9.jpg", "published": True, "organizer_id": 29, "name": "Entertainment Galaxy Expo", "description": "The Entertainment Galaxy Expo is your portal to the world of entertainment. Immerse yourself in the captivating realms of cinema, television, music, and digital art. This expo is where creative minds converge to shape pop culture and redefine entertainment. Discover what makes your favorite movies, shows, and music so mesmerizing." },
        { "hall_id": 10, "image": "/assets/fair_10.jpg", "published": True, "organizer_id": 30, "name": "Traveler's Oasis Festival", "description": "Escape to the Traveler's Oasis Festival, where wanderlust meets exploration. This festival is your ticket to a world of adventure and discovery. Explore exotic destinations, unique travel experiences, and the joys of exploration. Whether you're an avid traveler or a dreamer, this festival is your guide to the wonders of the world." },
        { "hall_id": 11, "image": "/assets/fair_11.jpg", "published": True, "organizer_id": 21, "name": "EduSphere Learning Innovations Expo", "description": "Immerse yourself in the world of education and e-learning at the EduSphere Learning Innovations Expo. This remarkable expo is a tribute to knowledge, growth, and the ever-evolving field of education. Join educators, e-learning experts, and lifelong learners as they showcase the latest innovations in teaching and learning. Explore the realms of online education, digital resources, and the exciting potential of e-learning. It's an event where the pursuit of knowledge knows no boundaries, and the transformative power of education takes center stage. Join us in celebrating the journey of learning, the possibilities of digital education, and the quest for knowledge that shapes our world. Discover the joy of lifelong learning and the impact it has on personal and professional growth." },
        { "hall_id": 12, "image": "/assets/fair_12.jpg", "published": True, "organizer_id": 22, "name": "Harvest Fest Agribusiness Expo", "description": "Immerse yourself in the world of agriculture and agribusiness at the Harvest Fest Agribusiness Expo. This extraordinary expo celebrates the art and science of farming, where agricultural experts, innovative agribusinesses, and farming enthusiasts come together. Explore the latest advancements in sustainable farming, discover cutting-edge agricultural technologies, and witness the beauty of bountiful harvests. Join us in celebrating the essence of agriculture, growth, and the vital connection between agribusiness and our daily lives. It's an event where the seeds of knowledge and growth are sown, and the future of agriculture is cultivated." },
        { "hall_id": 13, "image": "/assets/fair_13.jpg", "published": True, "organizer_id": 23, "name": "LegalPro Symposium and Expo", "description": "Discover the path to holistic wellness at the Wellness Oasis Retreat. This retreat is a sanctuary for the mind, body, and soul. Immerse yourself in wellness practices, self-care, and the secrets of well-being. Explore the realms of relaxation, fitness, and inner harmony. Join us for a transformative experience where you find your balance, embrace serenity, and unlock the potential of a healthier, happier you." },
        { "hall_id": 14, "image": "/assets/fair_14.jpg", "published": True, "organizer_id": 24, "name": "SportsMania Recreation Extravaganza", "description": "Immerse yourself in the exhilarating world of sports and recreation at the SportsMania Recreation Extravaganza. This thrilling extravaganza is a celebration of physical activity, competition, and the spirit of play. Join sports enthusiasts, athletes, and recreational fanatics as they come together to explore a world of high-energy fun and excitement. Experience a wide range of sports, from adrenaline-pumping games to leisurely pastimes, all in one place. It's an event where energy knows no bounds, and the love of sports and recreation unites us all. Join us in celebrating the power of play, teamwork, and the pursuit of physical excellence. Discover the joy of staying active and experiencing the thrill of sports and recreation!" },
        { "hall_id": 15, "image": "/assets/fair_15.jpg", "published": True, "organizer_id": 25, "name": "BioTech Innovations Showcase", "description": "Immerse yourself in the cutting-edge world of biotechnology at the BioTech Innovations Showcase. This remarkable showcase is a testament to the boundless possibilities of biotechnology, where scientific breakthroughs, life-changing innovations, and health advancements come to life. Join leading biotech experts, researchers, and enthusiasts as they unveil the latest advancements in genetic engineering, medical breakthroughs, and the quest to improve human health. Explore the realms of innovation, health, and trust in the world of biotechnology. It's an event where science meets hope, and the future of healthcare is transformed. Join us in celebrating the power of biotechnology to shape a healthier, more promising future for all." },
        { "hall_id": 16, "image": "/assets/fair_16.jpg", "published": True, "organizer_id": 26, "name": "GameFusion Entertainment Extravaganza", "description": "Immerse yourself in the thrilling world of gaming and entertainment at the GameFusion Entertainment Extravaganza. This spectacular event is a celebration of all things gaming, from video games and board games to immersive VR experiences. Dive into a world of creativity and excitement, where gaming enthusiasts, industry leaders, and passionate gamers come together. Experience the latest gaming innovations, participate in esports tournaments, and meet your favorite gaming celebrities. It's an extravaganza of fun, competition, and the magic of gaming. Join us in celebrating the power of play, creativity, and the boundless adventures that gaming and entertainment offer. Get ready to level up your entertainment experience!" },
        { "hall_id": 17, "image": "/assets/fair_17.jpg", "published": True, "organizer_id": 27, "name": "ArchiVisions Design and Architecture Expo", "description": "Immerse yourself in the world of architecture and design at the ArchiVisions Design and Architecture Expo. This exceptional expo is a tribute to the elegance and sophistication of architectural marvels. Join visionary architects, design experts, and architectural enthusiasts as they unveil the latest in architectural innovation, creativity, and elegance. Explore the beauty of structural design, the art of space utilization, and the aesthetic harmony of architectural creations. It's an event where form meets function, and architectural visions come to life. Join us in celebrating the power of architecture to shape our surroundings, enrich our lives, and inspire our imaginations. Discover the beauty of design and the impact it has on our built environment." },
        { "hall_id": 18, "image": "/assets/fair_18.jpg", "published": True, "organizer_id": 28, "name": "StyleSpectra Fashion Extravaganza", "description": "Immerse yourself in the world of fashion and apparel at the StyleSpectra Fashion Extravaganza. This glamorous extravaganza is a tribute to style, luxury, and the art of dressing. Join fashion enthusiasts, designers, and trendsetters as they unveil the latest in couture, streetwear, and haute couture. Explore a world of colors, fabrics, and designs that redefine elegance and self-expression. It's an event where fashion becomes a canvas for individuality, creativity, and self-confidence. Join us in celebrating the diversity of styles, the beauty of self-expression, and the ever-evolving world of fashion. Discover the power of style to influence, inspire, and transform lives. It's your opportunity to make a fashion statement and celebrate the art of dressing!" },
        { "hall_id": 19, "image": "/assets/fair_19.jpg", "published": True, "organizer_id": 29, "name": "EcoSolutions Environmental Services Expo", "description": "Immerse yourself in the world of environmental sustainability at the EcoSolutions Environmental Services Expo. This exceptional expo is a tribute to eco-friendliness, green technologies, and the preservation of our planet. Join environmental experts, eco-conscious organizations, and sustainability advocates as they showcase innovative solutions for a cleaner and greener future. Explore the latest advancements in renewable energy, eco-friendly practices, and responsible conservation. It's an event where the commitment to a sustainable world takes center stage. Join us in celebrating the beauty of our planet and the collective efforts to protect it. Discover how each of us can make a positive impact on the environment and create a brighter, more sustainable future." },
        { "hall_id": 20, "image": "/assets/fair_20.jpg", "published": True, "organizer_id": 30, "name": "BuildVisions Real Estate Showcase", "description": "Immerse yourself in the world of real estate and construction at the BuildVisions Real Estate Showcase. This prestigious showcase is a tribute to growth, stability, and the art of building. Join real estate professionals, architects, and property enthusiasts as they unveil the latest developments in the world of real estate, housing, and construction. Explore architectural marvels, modern housing designs, and the innovative trends that are shaping our living spaces. It's an event where homes become dreams, communities take shape, and the real estate industry thrives. Join us in celebrating the power of real estate to create homes, build neighborhoods, and shape the way we live. Discover the art of property development and the impact it has on our living environments." },
    ]

    fairs = [Fair(**f) for f in fairs]

    industries = {}
    for fair in fairs:
        fair.start = base_date + datetime.timedelta(days=random.randint(1, 30))
        fair.end = fair.start + datetime.timedelta(days=random.randint(0, 7))
    flat = [[i, i] for i in range(1, 21)]
    with current_app.app_context():
        db.session.add_all(fairs)
        db.session.flush()
        db.session.execute(db.insert(fair_industry).values(flat))
        db.session.commit()



def create_industries():
    dset = [
        {"name": "Technologies & Software", "icon": "devices", "color": "blue"},
        {"name": "Healthcare", "icon": "medication", "color": "red"},
        {"name": "Financial Services", "icon": "monetization_on", "color": "amber-lighten-1"},
        {"name": "Retail & E-commerce", "icon": "storefront", "color": "black"},
        {"name": "Energy", "icon": "bolt", "color": "yellow"},
        {"name": "Automotive", "icon": "garage", "color": "grey-darken-1"},
        {"name": "Aerospace", "icon": "flight", "color": "blue-lighten-3"},
        {"name": "Food & Beverage", "icon": "restaurant", "color": "red"},
        {"name": "Entertainment & Media", "icon": "live_tv", "color": "purple"},
        {"name": "Transportation & Logistics", "icon": "local_shipping", "color": "grey-darken-1"},
        {"name": "Education & E-learning", "icon": "school", "color": "blue"},
        {"name": "Agriculture & Agribusiness", "icon": "agriculture", "color": "green"},
        {"name": "Legal Services", "icon": "gavel", "color": "brown-darken-1"},
        {"name": "Sports & Recreation", "icon": "fitness_center", "color": "red-lighten-1"},
        {"name": "Biotechnology", "icon": "biotech", "color": "green"},
        {"name": "Gaming & Entertainment", "icon": "sports_esports", "color": "red"},
        {"name": "Architecture", "icon": "architecture", "color": "green"},
        {"name": "Fashion", "icon": "diamond", "color": "pink-lighten-2"},
        {"name": "Environmental Services", "icon": "water_drop", "color": "blue"},
        {"name": "Real Estate", "icon": "apartment", "color": "grey-darken-1"}
    ]

    ind = [Industry(**par) for par in dset]
    with current_app.app_context():
        db.session.add_all(ind)
        db.session.commit()


def create_users():
    male_exhibitors = [
        [1, "James", "Anderson"], [2, "Daniel", "Williams"],
        [3, "Christopher", "Brown"], [4, "Matthew", "Davis"],
        [5, "Benjamin", "Martinez"], [6, "Alexander", "Wilson"],
        [7, "William", "Clark"], [8, "Samuel", "Taylor"],
        [9, "Micheal", "Turner"], [10, "Nicholas", "Harris"]]
    male_organizers = [
        [11, "Ethan", "Johnson"], [12, "Liam", "Davis"],
        [13, "Mason", "Martinez"], [14, "Logan", "Smith"],
        [15, "Noah", "Adams"]]
    female_exhibitors = [
        [1, "Emily", "Johnson"], [2, "Olivia", "Smith"],
        [3, "Sophia", "Walker"], [4, "Ava", "Turner"],
        [5, "Mia", "Robinson"], [6, "Charlotte", "Evans"],
        [7, "Isabella", "Mitchell"], [8, "Grace", "Davis"],
        [9, "Amelia", "White"], [10, "Harper", "Thompson"]]
    female_organizers = [
        [11, "Emma", "Parker"], [12, "Chloe", "Anderson"],
        [13, "Lily", "Ramirez"], [14, "Zoe", "Martin"],
        [15, "Hannah", "Adams"]]

    male_exhibitors = [_create_user(x[1], x[2], "exhibitor", x[0], True) for x
                       in male_exhibitors]
    female_exhibitors = [_create_user(x[1], x[2], "exhibitor", x[0], False) for x
                         in female_exhibitors]
    male_organizers = [_create_user(x[1], x[2], "organizer", x[0], True) for x
                       in male_organizers]
    female_organizers = [_create_user(x[1], x[2], "organizer", x[0], False) for x
                         in female_organizers]

    db.session.add_all(male_exhibitors)
    db.session.add_all(female_exhibitors)
    db.session.add_all(male_organizers)
    db.session.add_all(female_organizers)
    db.session.commit()


def _create_user(name: str, surname: str, role: str, idx: int, male: bool):
    if role == "exhibitor":
        obj = Exhibitor()
    else:
        obj = Organizer()
    obj.update({
        "name": name,
        "surname": surname,
        "email": f"{name.lower()}@email.com",
        "image": f"/assets/{'man' if male else 'woman'}_{idx}.jpg",
        "password": "Test1234"
    })
    obj.make_password_hash()
    return obj


def create_companies():
    companies = [
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 1,
            "name": "Tech Innovators Inc.",
            "description": "Tech Innovators Inc. is a leading software development company specializing in cutting-edge mobile app development, web solutions, and artificial intelligence technologies to transform businesses and enhance user experiences."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 2,
            "name": "MediCare Pharmaceuticals",
            "description": "MediCare Pharmaceuticals is a pharmaceutical company dedicated to producing high-quality, life-saving medications, with a focus on research and development in the healthcare sector."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 3,
            "name": "SecureFinance Group",
            "description": "SecureFinance Group is a full-service financial institution offering banking, investment, and insurance solutions, committed to providing clients with financial security and peace of mind."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 4,
            "name": "ShopHub Online",
            "description": "ShopHub Online is an e-commerce giant, offering a wide range of products, from fashion and electronics to home decor, delivering convenience and choice to shoppers worldwide."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 5,
            "name": "EcoPower Solutions",
            "description": "EcoPower Solutions is a renewable energy company that specializes in solar and wind energy solutions, promoting eco-friendly power generation for a sustainable future."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 6,
            "name": "AutoMasters Inc.",
            "description": "AutoMasters Inc. is a leading automotive manufacturer, producing innovative and high-performance vehicles, from electric cars to luxury automobiles."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 7,
            "name": "AeroTech Dynamics",
            "description": "AeroTech Dynamics is a key player in the aerospace and defense industry, designing and manufacturing cutting-edge aircraft and defense systems for global security."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 8,
            "name": "FreshHarvest Farms",
            "description": "FreshHarvest Farms is a farm-to-table company committed to delivering fresh, organic produce and artisanal food products to promote healthy eating and sustainable farming practices."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 9,
            "name": "StarVision Entertainment",
            "description": "StarVision Entertainment is a multimedia conglomerate, producing films, television shows, music, and digital content that captivates audiences and shapes pop culture."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 10,
            "name": "TransGlobal Logistics",
            "description": "TransGlobal Logistics is a leading logistics company specializing in the efficient and secure transportation of goods, offering supply chain solutions to businesses across various industries."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 11,
            "name": "EduVision Learning",
            "description": "EduVision Learning is an innovative e-learning platform that offers a diverse range of online courses and educational resources, empowering learners to acquire knowledge and skills from the comfort of their homes."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 12,
            "name": "HarvestPro Farms",
            "description": "HarvestPro Farms is a leading agribusiness company that specializes in the cultivation and distribution of high-quality agricultural products, contributing to global food security."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 13,
            "name": "LegalTrust Advisors",
            "description": "LegalTrust Advisors is a law firm that offers legal expertise and trustworthy counsel to clients in various legal matters, ensuring justice and protection of their rights."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 14,
            "name": "ActiveLife Sports",
            "description": "ActiveLife Sports is a sports and recreation company that provides high-quality equipment and gear for active lifestyles."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 15,
            "name": "BioGen Innovations",
            "description": "BioGen Innovations is a biotechnology company at the forefront of scientific advancements in biopharmaceuticals and genetic research."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 16,
            "name": "PixelFusion Entertainment",
            "description": "PixelFusion Entertainment is a leading name in the world of gaming and entertainment, creating immersive gaming experiences and captivating content."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 17,
            "name": "DesignCraft Architects",
            "description": "DesignCraft Architects is an architecture and design firm that specializes in creating innovative and aesthetically pleasing spaces."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 18,
            "name": "TrendSetter Couture",
            "description": "TrendSetter Couture is a fashion and apparel company known for setting trends in the world of style and luxury."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 19,
            "name": "EcoSolutions Environmental",
            "description": "EcoSolutions Environmental is an environmental services company dedicated to sustainable waste management, recycling, and eco-conscious solutions to protect the planet."
        },
        {
            "image": "/assets/docker.png",
            "exhibitor_id": 20,
            "name": "GreenScape Construction",
            "description": "GreenScape Construction is a real estate development and construction firm that focuses on sustainable and eco-friendly building practices, creating homes and spaces that harmonize with the environment."
        }
    ]

    # Generate 60 random addresses
    addresses = []
    for idx in range(40):
        address = {
            "city": random.choice(cities),
            "street": fake.street_address(),
            "zipcode": fake.postcode(),
        }
        addresses.append(Address(**address))

    companies = [Company(**c) for c in companies]
    ind = []
    for i in range(0, len(addresses), 2):
        idx = int(i / 2)
        cmpny = companies[idx]
        cmpny.addresses.append(addresses[i])
        cmpny.addresses.append(addresses[i+1])
        ind.append({"company_id": idx + 1, "industry_id": idx + 1})

    with current_app.app_context():
        db.session.add_all(companies)
        db.session.execute(db.insert(company_industry).values(ind))
        db.session.commit()


def create_halls():
    halls = []

    for idx in range(20):
        hall = {
            "parking": random.choice([True, False]),
            "internet": random.choice([True, False]),
            "dissability": random.choice([True, False]),
            "pets": random.choice([True, False]),
            "public": True,
            "size": random.randint(300, 1500),
            "price": random.randint(500, 5000),
            "city": random.choice(cities),
            "street": fake.street_address(),
            "zipcode": fake.postcode(),
            "name": random.choice(fantasy_words) + " Hall",
            "description": fake.paragraph(nb_sentences=5)  #
        }
        halls.append(Hall(**hall))

    for hall in halls:
        for i in range(3):
            hall.images.append(
                Image(path=f"/assets/hall_{random.choice(range(1, 21))}.jpg",
                      description=fake.paragraph(nb_sentences=1)))
            amt = int(random.uniform(1, 20))
            hall.stalls.append(
                Stall(
                    size=random.randint(2, 20),
                    electricity=random.choice([True, False]),
                    network=random.choice([True, False]),
                    support=random.choice([True, False]),
                    image=f"/assets/stall_{random.choice(range(1, 6))}.jpg",
                    max_amount=amt
                ))

    with current_app.app_context():
        db.session.add_all(halls)
        db.session.commit()
