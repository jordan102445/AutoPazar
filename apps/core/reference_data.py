from apps.core.models import City
from apps.listings.models import CarBrand, CarModel


CITY_DATA = [
    {"name": "Скопје", "slug": "skopje", "region": "Скопски", "aliases": ["Skopje"]},
    {"name": "Битола", "slug": "bitola", "region": "Пелагониски", "aliases": ["Bitola"]},
    {"name": "Тетово", "slug": "tetovo", "region": "Полошки", "aliases": ["Tetovo"]},
    {"name": "Охрид", "slug": "ohrid", "region": "Југозападен", "aliases": ["Ohrid"]},
    {"name": "Куманово", "slug": "kumanovo", "region": "Североисточен", "aliases": ["Kumanovo"]},
    {"name": "Струмица", "slug": "strumica", "region": "Југоисточен", "aliases": ["Strumica"]},
    {"name": "Велес", "slug": "veles", "region": "Вардарски", "aliases": ["Veles"]},
    {"name": "Прилеп", "slug": "prilep", "region": "Пелагониски", "aliases": ["Prilep"]},
    {"name": "Штип", "slug": "shtip", "region": "Источен", "aliases": ["Stip", "Shtip", "Štip"]},
    {"name": "Гостивар", "slug": "gostivar", "region": "Полошки", "aliases": ["Gostivar"]},
    {"name": "Струга", "slug": "struga", "region": "Југозападен", "aliases": ["Struga"]},
    {"name": "Кавадарци", "slug": "kavadarci", "region": "Вардарски", "aliases": ["Kavadarci"]},
    {"name": "Кочани", "slug": "kochani", "region": "Источен", "aliases": ["Kocani", "Kochani", "Kočani"]},
    {"name": "Кичево", "slug": "kicevo", "region": "Југозападен", "aliases": ["Kicevo", "Kičevo"]},
    {"name": "Гевгелија", "slug": "gevgelija", "region": "Југоисточен", "aliases": ["Gevgelija"]},
    {"name": "Свети Николе", "slug": "sveti-nikole", "region": "Вардарски", "aliases": ["Sveti Nikole"]},
    {"name": "Неготино", "slug": "negotino", "region": "Вардарски", "aliases": ["Negotino"]},
    {"name": "Радовиш", "slug": "radovish", "region": "Југоисточен", "aliases": ["Radovis", "Radovish", "Radoviš"]},
    {"name": "Ресен", "slug": "resen", "region": "Пелагониски", "aliases": ["Resen"]},
    {"name": "Дебар", "slug": "debar", "region": "Југозападен", "aliases": ["Debar"]},
    {"name": "Берово", "slug": "berovo", "region": "Источен", "aliases": ["Berovo"]},
    {"name": "Делчево", "slug": "delchevo", "region": "Источен", "aliases": ["Delcevo", "Delchevo", "Delčevo"]},
    {"name": "Виница", "slug": "vinica", "region": "Источен", "aliases": ["Vinica"]},
    {"name": "Крива Паланка", "slug": "kriva-palanka", "region": "Североисточен", "aliases": ["Kriva Palanka"]},
    {"name": "Кратово", "slug": "kratovo", "region": "Североисточен", "aliases": ["Kratovo"]},
    {"name": "Пробиштип", "slug": "probishtip", "region": "Источен", "aliases": ["Probistip", "Probishtip", "Probištip"]},
    {"name": "Валандово", "slug": "valandovo", "region": "Југоисточен", "aliases": ["Valandovo"]},
    {"name": "Богданци", "slug": "bogdanci", "region": "Југоисточен", "aliases": ["Bogdanci"]},
    {"name": "Демир Капија", "slug": "demir-kapija", "region": "Вардарски", "aliases": ["Demir Kapija"]},
    {"name": "Демир Хисар", "slug": "demir-hisar", "region": "Пелагониски", "aliases": ["Demir Hisar"]},
    {"name": "Крушево", "slug": "krusevo", "region": "Пелагониски", "aliases": ["Krusevo", "Kruševo"]},
    {
        "name": "Македонска Каменица",
        "slug": "makedonska-kamenica",
        "region": "Источен",
        "aliases": ["Makedonska Kamenica"],
    },
    {
        "name": "Македонски Брод",
        "slug": "makedonski-brod",
        "region": "Југозападен",
        "aliases": ["Makedonski Brod"],
    },
    {"name": "Пехчево", "slug": "pehchevo", "region": "Источен", "aliases": ["Pehcevo", "Pehchevo", "Pehčevo"]},
]


BRAND_MODEL_DATA = {
    "Abarth": ["500", "595", "124 Spider"],
    "Acura": ["ILX", "MDX", "RDX", "TLX"],
    "Alfa Romeo": ["147", "159", "Giulietta", "Giulia", "Stelvio"],
    "Alpine": ["A110"],
    "Aston Martin": ["DB11", "DBX", "Vantage"],
    "Audi": ["A1", "A3", "A4", "A6", "A8", "Q3", "Q5", "Q7", "TT"],
    "Bentley": ["Bentayga", "Continental GT", "Flying Spur"],
    "BMW": ["116", "320", "520", "730", "X1", "X3", "X5", "X6"],
    "Bugatti": ["Chiron", "Veyron"],
    "Buick": ["Encore", "Envision", "Regal"],
    "BYD": ["Atto 3", "Dolphin", "Han", "Seal", "Tang"],
    "Cadillac": ["ATS", "CT5", "Escalade", "SRX"],
    "Chevrolet": ["Aveo", "Captiva", "Cruze", "Malibu", "Spark"],
    "Chery": ["Arrizo 5", "Tiggo 2", "Tiggo 7"],
    "Chrysler": ["300C", "Pacifica", "PT Cruiser", "Voyager"],
    "Citroen": ["Berlingo", "C1", "C3", "C4", "C5"],
    "Cupra": ["Ateca", "Born", "Formentor", "Leon"],
    "Dacia": ["Duster", "Jogger", "Lodgy", "Logan", "Sandero"],
    "Daewoo": ["Kalos", "Lanos", "Matiz", "Nubira"],
    "Daihatsu": ["Charade", "Cuore", "Sirion", "Terios"],
    "Dodge": ["Caliber", "Challenger", "Charger", "Durango", "Journey"],
    "DS": ["DS 3", "DS 4", "DS 7"],
    "Ferrari": ["458 Italia", "488 GTB", "F8 Tributo", "Portofino", "Roma"],
    "Fiat": ["500", "Bravo", "Doblo", "Panda", "Punto", "Tipo"],
    "Fisker": ["Ocean", "Karma"],
    "Ford": ["Fiesta", "Focus", "Galaxy", "Kuga", "Mondeo", "Mustang", "Puma", "S-Max"],
    "Geely": ["Atlas", "Coolray", "Emgrand"],
    "Genesis": ["G70", "G80", "GV70", "GV80"],
    "GMC": ["Acadia", "Terrain", "Yukon"],
    "Great Wall": ["Hover", "Steed", "Voleex C30"],
    "Haval": ["Dargo", "H6", "Jolion"],
    "Honda": ["Accord", "Civic", "CR-V", "HR-V", "Jazz"],
    "Hummer": ["H2", "H3"],
    "Hyundai": ["i10", "i20", "i30", "Kona", "Santa Fe", "Tucson"],
    "Infiniti": ["FX30d", "Q30", "Q50", "QX70"],
    "Isuzu": ["D-Max", "Trooper"],
    "Jaguar": ["E-Pace", "F-Pace", "XE", "XF", "XJ"],
    "Jeep": ["Compass", "Grand Cherokee", "Renegade", "Wrangler"],
    "Kia": ["Ceed", "Picanto", "Rio", "Sorento", "Sportage"],
    "Lada": ["Granta", "Niva", "Samara", "Vesta"],
    "Lancia": ["Delta", "Lybra", "Musa", "Ypsilon"],
    "Land Rover": ["Defender", "Discovery", "Freelander", "Range Rover Evoque"],
    "Lexus": ["CT 200h", "IS 220", "NX 300h", "RX 450h"],
    "Lincoln": ["MKC", "MKX", "Navigator"],
    "Lotus": ["Elise", "Emira", "Exige"],
    "Lucid": ["Air"],
    "Lynk & Co": ["01", "03", "05"],
    "Maserati": ["Ghibli", "GranTurismo", "Levante", "Quattroporte"],
    "Mazda": ["2", "3", "6", "CX-3", "CX-5", "MX-5"],
    "McLaren": ["570S", "720S", "Artura"],
    "Mercedes-Benz": ["A 180", "C 220", "CLA 200", "E 220", "GLA 200", "GLC 220", "ML 320", "S 350"],
    "MG": ["HS", "MG3", "MG4", "MG5", "ZS"],
    "Mini": ["Clubman", "Cooper", "Countryman", "Paceman"],
    "Mitsubishi": ["ASX", "Colt", "Lancer", "Outlander", "Pajero"],
    "NIO": ["ES6", "ET5", "ET7"],
    "Nissan": ["Juke", "Micra", "Note", "Primera", "Qashqai", "X-Trail"],
    "Opel": ["Astra", "Corsa", "Insignia", "Mokka", "Vectra", "Zafira"],
    "Peugeot": ["107", "208", "308", "407", "508", "3008", "5008", "Partner"],
    "Polestar": ["2", "3", "4"],
    "Pontiac": ["G6", "Trans Sport", "Vibe"],
    "Porsche": ["911", "Cayenne", "Macan", "Panamera", "Taycan"],
    "Proton": ["Gen-2", "Persona", "Saga"],
    "Ram": ["1500"],
    "Renault": ["Captur", "Clio", "Kadjar", "Laguna", "Megane", "Scenic", "Talisman"],
    "Rolls-Royce": ["Cullinan", "Ghost", "Phantom"],
    "Rover": ["25", "45", "75"],
    "Saab": ["9-3", "9-5"],
    "Seat": ["Altea", "Arona", "Ateca", "Ibiza", "Leon", "Toledo"],
    "Skoda": ["Fabia", "Kamiq", "Karoq", "Kodiaq", "Octavia", "Scala", "Superb"],
    "Smart": ["Forfour", "Fortwo"],
    "SsangYong": ["Korando", "Rexton", "Tivoli"],
    "Subaru": ["Forester", "Impreza", "Legacy", "Outback", "XV"],
    "Suzuki": ["Ignis", "Jimny", "Swift", "SX4", "Vitara"],
    "Tata": ["Indica", "Nano", "Safari"],
    "Tesla": ["Model 3", "Model S", "Model X", "Model Y"],
    "Toyota": ["Avensis", "Aygo", "C-HR", "Corolla", "Land Cruiser", "Prius", "RAV4", "Yaris"],
    "Volkswagen": ["Golf", "Passat", "Polo", "T-Cross", "T-Roc", "Tiguan", "Touareg", "Touran", "Up"],
    "Volvo": ["S40", "S60", "S80", "V50", "V90", "XC60", "XC90"],
    "Yugo": ["45", "Florida", "Koral"],
    "Zastava": ["101", "Florida", "Yugo"],
}


REFERENCE_CITY_COUNT = len(CITY_DATA)
REFERENCE_BRAND_COUNT = len(BRAND_MODEL_DATA)
REFERENCE_MODEL_COUNT = sum(len(models) for models in BRAND_MODEL_DATA.values())


def sync_city_reference_data():
    cities = []
    created = 0
    updated = 0

    for index, city_data in enumerate(CITY_DATA, start=1):
        city = City.objects.filter(slug=city_data["slug"]).first()
        if not city:
            city = City.objects.filter(name__in=city_data.get("aliases", [])).first()

        if city:
            city.name = city_data["name"]
            city.slug = city_data["slug"]
            city.region = city_data["region"]
            city.display_order = index
            city.is_active = True
            city.save(update_fields=["name", "slug", "region", "display_order", "is_active", "updated_at"])
            is_created = False
        else:
            city = City.objects.create(
                name=city_data["name"],
                slug=city_data["slug"],
                region=city_data["region"],
                display_order=index,
                is_active=True,
            )
            is_created = True

        cities.append(city)
        if is_created:
            created += 1
        else:
            updated += 1

    return cities, created, updated


def sync_car_reference_data():
    brands = []
    models = []
    created_brands = 0
    updated_brands = 0
    created_models = 0
    updated_models = 0

    for brand_name, brand_models in BRAND_MODEL_DATA.items():
        brand, brand_created = CarBrand.objects.update_or_create(
            name=brand_name,
            defaults={"is_active": True},
        )
        brands.append(brand)
        if brand_created:
            created_brands += 1
        else:
            updated_brands += 1

        for model_name in brand_models:
            model, model_created = CarModel.objects.update_or_create(
                brand=brand,
                name=model_name,
                defaults={"is_active": True},
            )
            models.append(model)
            if model_created:
                created_models += 1
            else:
                updated_models += 1

    return {
        "brands": brands,
        "models": models,
        "created_brands": created_brands,
        "updated_brands": updated_brands,
        "created_models": created_models,
        "updated_models": updated_models,
    }
