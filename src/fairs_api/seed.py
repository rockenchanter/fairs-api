import datetime
import click
from flask import current_app

from . import models as md


def create_user(role, name, surname, num):
    if role == "exhibitor":
        usr = md.Exhibitor(email=f"{name.lower()}@email.com", password=f"{name}1234",
                           image=f"/assets/exhibitor_{num}.jpg", name=name,
                           surname=surname)
    elif role == "organizer":
        usr = md.Organizer(email=f"{name.lower()}@email.com", password=f"{name}1234",
                           image=f"/assets/organizer_{num}.jpg", name=name,
                           surname=surname)
    print(f"email: {usr.email}, password: {usr.password}")
    usr.make_password_hash()
    return usr


users = {
    "organizer_1": create_user("organizer", "Marek", "Mostowiak", 1),
    "organizer_2": create_user("organizer", "Hanna", "Mostowiak", 2),
    "organizer_3": create_user("organizer", "Lucjan", "Mostowiak", 3),
    "organizer_4": create_user("organizer", "Natalia", "Mostowiak", 4),
    "organizer_5": create_user("organizer", "Barbara", "Mostowiak", 5),
    "exhibitor_6": create_user("exhibitor", "Gordon", "Ramsey", 6),
    "exhibitor_7": create_user("exhibitor", "Dave", "Brandt", 7),
    "exhibitor_8": create_user("exhibitor", "Bob", "Kelso", 8),
    "exhibitor_9": create_user("exhibitor", "Michael", "Scott", 9),
    "exhibitor_10": create_user("exhibitor", "Ron", "Swanson", 10),
}

industries = {
    "tech":    md.Industry(name="Technologies & Software", icon="devices", color="blue"),
    "health":  md.Industry(name="Healthcare", icon="medication", color="red"),
    "finance": md.Industry(name="Financial Services", icon="monetization_on", color="amber-lighten-1"),
    "retail":  md.Industry(name="Retail & E-commerce", icon="storefront", color="black"),
    "energy":  md.Industry(name="Energy", icon="bolt", color="yellow"),
    "auto":    md.Industry(name="Automotive", icon="garage", color="grey-darken-1"),
    "aero":    md.Industry(name="Aerospace", icon="flight", color="blue-lighten-3"),
    "food":    md.Industry(name="Food & Beverage", icon="restaurant", color="red"),
    "media":   md.Industry(name="Entertainment & Media", icon="live_tv", color="purple"),
    "trans":   md.Industry(name="Transportation & Logistics", icon="local_shipping", color="grey-darken-1"),
    "edu":     md.Industry(name="Education & E-learning", icon="school", color="blue"),
    "agric":   md.Industry(name="Agriculture & Agribusiness", icon="agriculture", color="green"),
    "legal":   md.Industry(name="Legal Services", icon="gavel", color="brown-darken-1"),
    "sport":   md.Industry(name="Sports & Recreation", icon="fitness_center", color="red-lighten-1"),
    "biotech": md.Industry(name="Biotechnology", icon="biotech", color="green"),
    "gaming":  md.Industry(name="Gaming & Entertainment", icon="sports_esports", color="red"),
    "archi":   md.Industry(name="Architecture", icon="architecture", color="green"),
    "fashi":   md.Industry(name="Fashion", icon="diamond", color="pink-lighten-2"),
    "envir":   md.Industry(name="Environmental Services", icon="water_drop", color="blue"),
    "estate":  md.Industry(name="Real Estate", icon="apartment", color="grey-darken-1")
}

halls = {
    "hala_B": md.Hall(parking=True, internet=True, dissability=True, pets=False,
                      price=200000, size=20535, public=True, city="Nadarzyn", street="Al. Katowicka 62",
                      zipcode="05-830", name="Hala B", description="Hala o łącznej powierzchni do wynajęcia (bez powierzchni wspólnych) 20 535 m2, podzielona na 3 strefy dwoma ścianami dźwiękoszczelnymi – możliwość przeprowadzenia 3 niezależnych imprez jednocześnie. W zależności od potrzeb imprezy, hala może być doświetlona światłem dziennym (świetliki w połaci dachu) lub całkowicie wyciemniona. Istnieje możliwość podwieszenia do konstrukcji dachu elementów dekoracji, oświetlenia czy elementów reklamowych. Wykaz miejsc i nośność punktów podwieszeń jest dostępna w Dziale Technicznym."),
    "hala_C": md.Hall(parking=True, internet=True, dissability=True, pets=False,
                      price=220000, size=20588, public=True, city="Nadarzyn", street="Al. Katowicka 62",
                      zipcode="05-830", name="Hala C", description="Hala o łącznej powierzchni do wynajęcia 20 588 m2, podzielona na 3 strefy dwoma ścianami dźwiękoszczelnymi – możliwość przeprowadzenia 3 niezależnych imprez jednocześnie. W zależności od potrzeb imprezy, hala może być doświetlona światłem dziennym (świetliki w połaci dachu) lub całkowicie wyciemniona. Istnieje możliwość podwieszenia do konstrukcji dachu elementów dekoracji, oświetlenia czy elementów reklamowych. Wykaz miejsc i nośność punktów podwieszeń jest dostępna w Dziale Technicznym."),
    "hala_D": md.Hall(parking=True, internet=True, dissability=True, pets=False,
                      price=180000, size=20288, public=True, city="Nadarzyn", street="Al. Katowicka 62",
                      zipcode="05-830", name="Hala D", description="Hala o łącznej powierzchni do wynajęcia 20 288 m2, podzielona na 3 strefy dwoma ścianami dźwiękoszczelnymi – możliwość przeprowadzenia 3 niezależnych imprez jednocześnie. W zależności od potrzeb imprezy, hala może być doświetlona światłem dziennym (świetliki w połaci dachu) lub całkowicie wyciemniona. Istnieje możliwość podwieszenia do konstrukcji dachu elementów dekoracji, oświetlenia czy elementów reklamowych. Wykaz miejsc i nośność punktów podwieszeń jest dostępna w Dziale Technicznym."),
    "mck": md.Hall(parking=True, internet=True, dissability=False, pets=True,
                      price=18000, size=2839, public=True, city="Katowice", street="Plac Sławika i Antalla 1",
                      zipcode="40-163", name="Międzynarodowe Centrum Kongresowe", description="Hala o łącznej powierzchni do wynajęcia 20 288 m2, podzielona na 3 strefy dwoma ścianami dźwiękoszczelnymi – możliwość przeprowadzenia 3 niezależnych imprez jednocześnie. W zależności od potrzeb imprezy, hala może być doświetlona światłem dziennym (świetliki w połaci dachu) lub całkowicie wyciemniona. Istnieje możliwość podwieszenia do konstrukcji dachu elementów dekoracji, oświetlenia czy elementów reklamowych. Wykaz miejsc i nośność punktów podwieszeń jest dostępna w Dziale Technicznym."),
    "hs": md.Hall(parking=True, internet=True, dissability=False, pets=True,
                      price=18000, size=2839, public=True, city="Wrocław", street="Wystawowa 1",
                      zipcode="51-618", name="Hala Stulecia", description="Hala Stulecia jest symbolem. Trwa, mimo dziejowych przetasowań, tworząc most między pokoleniami, ustrojami, nacjami. Choć wolimy mówić – między ludźmi. Ponadczasowa bryła wraz z otaczającymi ją terenami zielonymi stanowi wyjątkowe miejsce spotkań, gdzie każdy znajdzie coś dla siebie. Wszystkie potrzeby naszych gości traktujemy z taką samą wagą. Wierzymy, że właśnie o tak rozumianej równości myślał Max Berg, architekt budynku, definiując go jako Katedrę Demokracji. Nazywamy ją „perłą wrocławskiego modernizmu”, a przecież w momencie powstania, na początku XX wieku, nie miała sobie równych w świecie. O całe lata wyprzedzała manifesty Le Corbusiera i poręczne sentencje Miesa van der Rohe (Less is more, tłumaczone jako: Mniej znaczy więcej), apostołów nowego kierunku. To, co inni postulowali, w Breslau wrastało już w ziemię swoimi mocarnymi, betonowymi korzeniami. Hala Stulecia modelowo realizowała założenia ruchu nowoczesnego w architekturze (synonimiczne określenie modernizmu), nadrzędną rolę przyznając funkcjonalności w miejsce ornamentyki. Jak powiedział Louis Sullivan: Form follows function (Forma wynika z funkcji). Prostota. Otwartość. Utylitaryzm. Dziś Hala Stulecia jest miejscem chętnie odwiedzanym przez mieszkańców miasta, turystów, sympatyków architektury i urbanistyki. Organizatorzy największych wydarzeń kulturalnych, sportowych oraz biznesowych z całego świata zabiegają o wynajem unikalnych przestrzeni. Wpisanie kompleksu na Listę Światowego Dziedzictwa UNESCO w 2006 potwierdziło szczególny status obiektów i przestrzeni, które są wizytówką współczesnego Dolnego Śląska i Wrocławia.  Jesteśmy dumni, że możemy zaprosić Cię do tego miejsca. Czuj się jak u siebie."),
    "tauron": md.Hall(parking=True, internet=True, dissability=False, pets=False,
                      price=320000, size=58442, public=True, city="Kraków", street="Stanisława Lema 7",
                      zipcode="31-571", name="Tauron Arena", description="Kompleks TAURON Areny Kraków składa się Areny Głównej i Małej Hali. Wielofunkcyjny charakter obiektu, możliwość dowolnej konfiguracji widowni, wygodne zaplecze dla sportowców i wykonawców, rozbudowane systemy multimedialne i sceniczne, a także bardzo dobre warunki akustyczne to cechy, które spełniają warunki organizacji imprez każdej skali. W TAURON Arenie Kraków organizowane są koncerty, festiwale, pokazy filmowe, musicale, show na lodzie; pokazy akrobatyczne, gale, kongresy, bankiety, imprezy branżowe i plenerowe. W obiekcie można też rozgrywać zawody w 18 dyscyplinach rangi mistrzostw świata, m.in. w siatkówce, piłce ręcznej, koszykówce, halowej piłce nożnej, hokeju, jeździectwie, gimnastyce, tenisie i sportach walki. Projekt TAURON Areny Kraków został wyłoniony w konkursie ogłoszonym przez Gminę Miejska Kraków. Nagrodę przyznano za jednoznaczną formę architektoniczną tworzącą żywą ikonę miasta, umiejętne wykorzystanie środków technicznych światła oraz za przejrzysty schemat konstrukcyjny i funkcjonalny. Obiekt wyróżnia się charakterystyczną bryłą zbliżoną do spłaszczonej elipsoidy obrotowej. Zadaszenie areny jest wykonane na planie okręgu. Natomiast widownia, otoczona szerokimi galeriami komunikacyjnymi, umieszczonymi na trzech poziomach, ma kształt owalny. Wykonawcą projektu i dokumentacji projektowej było PERBO-Projekt Sp. z o.o. Obiekt zaprojektowali: Piotr Łabowicz-Sajkiewicz, Marcin Kulpa i Wojciech Ryżyński. Generalnym wykonawcą inwestycji było konsorcjum firm w składzie: Mostostal Warszawa S.A. (lider), Acciona Infraestructuras S.A., Mostostal Puławy S.A. i Asseco Poland S.A."),
    "mtp": md.Hall(parking=True, internet=True, dissability=True, pets=False,
                      price=500000, size=150000, public=True, city="Poznań", street="Głogowska 14",
                      zipcode="60-734", name="Międzynarodowe Targi Poznańskie", description="Napawa nas dumą, że Poznań to od ponad 100 lat targowa stolica Polski, a Międzynarodowe Targi Poznańskie to niekwestionowany lider wśród ośrodków targowych w Polsce i Europie Środkowej Wschodniej. W połowie drogi z Warszawy do Berlina i w zasięgu 7 aglomeracji, w samym centrum Poznania, zlokalizowane są najnowocześniejsze, profesjonalnie przygotowane tereny targowe o powierzchni 212,5 ha, w tym teren wystawowy z obiektami i terenami administracyjnymi o wielkości 22,9 ha. Tu odbywają się topowe wydarzenia branżowe, tu pokazywane są nowości i premiery. To właśnie tu spotykają się liderzy biznesowi, by podejmować kluczowe decyzje o przyszłości swoich przedsiębiorstw. Międzynarodowe Targi Poznańskie. Ośrodek targowy nr 1 w Polsce i Europie Środkowo – Wschodniej. Do dyspozycji naszych klientów oddajemy 150 000 m2 powierzchni wystawienniczej w zróżnicowanych pod względem wielkości i charakteru pawilonach. Wśród europejskich ośrodków Międzynarodowe Targi Poznańskie są na 25. miejscu pod względem wielkości posiadanej infrastruktury. Targi dysponują 15. przestrzennymi, klimatyzowanymi pawilonami, wieloma przestrzeniami do rozmów i spotkań biznesowych, zapleczem bankietowym, a także terenem otwartym z możliwością parkowania 2 000 samochodów."),
}

images = {
        "hala_B": [
            md.Image(path="/assets/hall_B_image01.jpg", description="Opis zdjęcia", hall=halls["hala_B"]),
        ],
        "hala_C": [
            md.Image(path="/assets/hall_C_image01.jpg", description="Opis zdjęcia", hall=halls["hala_C"]),
        ],
        "hala_D": [
            md.Image(path="/assets/hall_D_image01.jpg", description="Opis zdjęcia", hall=halls["hala_D"]),
        ],
        "mck": [
            md.Image(path="/assets/hall_mck_image01.jpg", description="Opis zdjęcia", hall=halls["mck"]),
            md.Image(path="/assets/hall_mck_image02.jpg", description="Opis zdjęcia", hall=halls["mck"]),
            md.Image(path="/assets/hall_mck_image03.jpg", description="Opis zdjęcia", hall=halls["mck"]),
        ],
        "hs": [
            md.Image(path="/assets/hall_hs_image01.webp", description="Opis zdjęcia", hall=halls["hs"]),
            md.Image(path="/assets/hall_hs_image02.webp", description="Opis zdjęcia", hall=halls["hs"]),
            md.Image(path="/assets/hall_hs_image03.webp", description="Opis zdjęcia", hall=halls["hs"]),
        ],
        "tauron": [
            md.Image(path="/assets/hall_tauron_image01.jpg", description="Opis zdjęcia", hall=halls["tauron"]),
            md.Image(path="/assets/hall_tauron_image02.jpg", description="Opis zdjęcia", hall=halls["tauron"]),
        ],
        "mtp": [
            md.Image(path="/assets/hall_mtp_image01.jpg", description="Opis zdjęcia", hall=halls["mtp"]),
        ],
}


stalls = {
    "hala_B": md.Stall(size=20, electricity=True, network=True, support=True, image="/assets/stall_hall_B.png", max_amount=500, hall=halls["hala_B"]),
    "hala_C": md.Stall(size=20, electricity=True, network=True, support=True, image="/assets/stall_hall_C.jpg", max_amount=400, hall=halls["hala_C"]),
    "hala_D": md.Stall(size=20, electricity=True, network=True, support=True, image="/assets/stall_hall_D.webp", max_amount=400, hall=halls["hala_D"]),
    "mck": md.Stall(size=20, electricity=True, network=True, support=False, image="/assets/stall_hall_mck.jpg", max_amount=200, hall=halls["mck"]),
    "hs": md.Stall(size=20, electricity=True, network=False, support=True, image="/assets/stall_hall_hs.jpg", max_amount=100, hall=halls["hs"]),
    "tauron": md.Stall(size=20, electricity=False, network=True, support=True, image="/assets/stall_hall_tauron.webp", max_amount=50, hall=halls["tauron"]),
    "mtp": md.Stall(size=20, electricity=True, network=True, support=True, image="/assets/stall_hall_mtp.webp", max_amount=5, hall=halls["mtp"]),
}

fairs = {
    "eurogastro": md.Fair(hall=halls["hala_B"], published=True,
                          organizer=users["organizer_1"], image="/assets/fair_eurogastro.jpg", name="Eurogastro",
                          description="Międzynarodowy charakter, gromadzi tysiące odwiedzających, setki wystawców, profesjonalistów z branży, osobowości kulinarnych, najznamienitszych szefów kuchni, światowej sławy barmanów i baristów czy cukierników. Wydarzenie kierujemy do restauratorów, cukierników, kawiarni, piekarni i lodziarni, producentów i dystrybutorów sprzętu oraz usług dla gastronomii. W Ptak Warsaw Expo tworzymy bezkonkurencyjną platformę do dyskusji o branży, poszerzania wiedzy o rynku i pojawiających się na nim nowościach i trendach. Targi to idealna okazja na nawiązanie współpracy biznesowej, opartej na wzajemnej korzyści w modelu B2B. EuroGastro to branżowe specjalistyczne wydarzenie odbywające się w Ptak Warsaw Expo, Największym Centrum Targowo – Kongresowym w Europie Środkowej. Mające na celu skupienie wszystkich gałęzi branży i stworzenie dogodnych warunków do profesjonalnych kontaktów biznesowych. Międzynarodowe Targi Rozwiązań dla Branży HoReCa pozwolą na znalezienie potencjalnych partnerów biznesowych dla twojej firmy. EuroGastro to doskonała okazja byś mógł porównać i dokładnie przeanalizować wszystkie dostępne na polskim rynku oferty dedykowane branży. Wydarzenie to stanowi również doskonałą okazję do uczestnictwa w konferencjach, warsztatach oraz kongresach branży rozwijających znajomość rynku oraz pokazujących działanie najnowszych technologii. Zarejestruj się i otrzymaj zaproszenie na targi."),
    "foodtech": md.Fair(hall=halls["hala_C"], published=True,
                        organizer=users["organizer_1"], image="/assets/fair_foodtech.jpg", name="Food Tech Expo",
                        description="Targi Food Tech to prezentacja kompleksowej oferty producentów i dystrybutorów maszyn do przetwórstwa i produkcji spożywczej, technologii zwiększających bezpieczeństwo żywności oraz prezentacja dodatków i komponentów które zagwarantują stworzenie idealnie smacznego produktu dla wymagającego konsumenta. Wystawcy zaprezentują rozwiązania w mieszaniu, napowietrzaniu, porcjowaniu, chłodzeniu, nalewaniu, dozowaniu, zmrażaniu i wielu innych technikach potrzebnych do wytworzenia żywności najlepszej jakości. Wydarzenie to dedykujemy przedstawicielom branży producentów żywności. Oferta z jaką zapoznają się Państwo na targach pozwoli wprowadzić w produkcji automatyzację gwarantując optymalizację kosztów i zwiększenie konkurencyjności na rynku branży spożywczej. Na wydarzeniu spotkamy się z Państwem na dwóch strefach: Strefie maszyn i urządzeń do przetwórstwa spożywczego oraz w strefie komponentów i dodatków do żywności. Zaprosimy Państwa na konferencję dla przemysłu przetwórstwa oraz do strefy spotkań biznesowych. Food Tech Expo to branżowe specjalistyczne wydarzenie odbywające się w Ptak Warsaw Expo, Największym Centrum Targowo – Kongresowym w Europie Środkowej. Mające na celu skupienie wszystkich gałęzi branży technologii spożywczych i stworzenie dogodnych warunków do profesjonalnych kontaktów biznesowych. Międzynarodowe Targi Technologii Spożywczych pozwolą na znalezienie potencjalnych partnerów biznesowych dla twojej firmy. Food Tech Expo to doskonała okazja byś mógł porównać i dokładnie przeanalizować wszystkie dostępne na polskim rynku oferty dedykowane branży. Wydarzenie to stanowi również doskonałą okazję do uczestnictwa w konferencjach, warsztatach oraz kongresach branży technologii spożywczych rozwijających znajomość rynku oraz pokazujących działanie najnowszych technologii."),
    "ctr": md.Fair(hall=halls["hala_D"], published=True,
                        organizer=users["organizer_1"], image="/assets/fair_ctr.png", name="Centralne Targi Rolnicze",
                        description="Centralne Targi Rolnicze to nie tylko wystawa maszyn, urządzeń rolniczych oraz środków do produkcji rolnej. Celem Targów, jest budowa płaszczyzny dla rozwoju kontaktów biznesowych dla naszych klientów oraz stworzenie dogodnej przestrzeni do umacniania współpracy. Centralne Targi Rolnicze, jako platforma spotkań biznesowych, z sukcesem rozwijają program Hosted Buyers. Jako pierwsi w Polsce dla naszych klientów wyszukujemy partnerów z zagranicy o ściśle określonym profilu działalności oraz zajmujemy się organizacją sesji matchmakingowych. Podczas poprzednich edycji CTR odbyło się kilka tysięcy spotkań z partnerami zagranicznymi. Celem Targów, poza aranżacją strefy wystawienniczej jest także stworzenie płaszczyzny dla organizacji debat, seminariów i paneli branżowych podnoszących najistotniejsze problemy sektora rolno – spożywczego, które identyfikowane są zarówno przez środowisko naukowo – akademickie jak i przedstawicieli organizacji branżowych, biznes oraz rolników indywidualnych. Nasze doskonałe zaplecze techniczne umożliwia organizację spotkań z kluczowymi klientami, organizację szkoleń i seminariów ściśle dopasowanych do potrzeb naszych partnerów oraz klientów."),
    "wme": md.Fair(hall=halls["hala_B"], published=True,
                        organizer=users["organizer_1"], image="/assets/fair_wme.png", name="Warsaw Medical Expo",
                        description="Warsaw Medical Expo to Międzynarodowe Targi Sprzętu i Wyposażenia Placówek Medycznych organizowane w Ptak Warsaw Expo. To miejsce spotkania producentów oraz dystrybutorów kompleksowego wyposażenia placówek medycznych, zarówno najmniejszych jak i największych wielospecjalistycznych klinik. Warsaw Medical Expo to promocja i dostęp do szerokiej informacji ze świata przemysłu, medycyny i biznesu. To platforma prezentacji nowości rynkowych i szybkiego postępu technologicznego. Ogromna przestrzeń i szerokie spektrum tematyczne pozwala poznać nowości i rozwiązania z wszystkich kluczowych sektorów przemysłu medycznego."),
    "hb": md.Fair(hall=halls["mck"], published=True,
                        organizer=users["organizer_2"], image="/assets/fair_hb.jpg", name="Hair & Beauty Festival",
                        description="Festival Hair&Beauty, to miejsce spotkań z liderami branży oraz nowymi markami, które prężnie wchodzą na rynek profesjonalistów. Zapraszamy na potężną dawkę wiedzy, inspiracji, spotkań branżowych, wykładów, konferencji, promocji, pokazów i szkoleń. H&B FESTIWAL inspiruje i otwiera możliwości na prezentacje marki, na odwiedzających czekają liczne pokazy i szkolenia!. Nasz Festiwal skierowany jest do profesjonalistów, ale nie zapominamy także o osobach spoza branży —  tutaj znajda się dla nich produktu i inspiracje do stylizacji włosów z wykorzystaniem profesjonalnych produktów"),
    "wtdk": md.Fair(hall=halls["hs"], published=True,
                        organizer=users["organizer_3"], image="/assets/fair_wtdk.png", name="Wrocławskie Targi Dobrych Książek",
                        description="Wrocławskie Targi Dobrych Książek odbywają się od 1992 roku – najpierw jako Spotkania Wydawców Dobrej Książki – które odbywały się w kilku miastach, m.in. w Gdańsku, Krakowie czy Warszawie. Początkowo organizacją imprezy we Wrocławiu zajmowało się Wydawnictwo Zakładu Narodowego im. Ossolińskich, następnie Wydawnictwo Dolnośląskie. Zmieniali się organizatorzy, ale i lokalizacje wydarzenia; najpierw był to budynek Opery Wrocławskiej, później Ratusz. Spotkania przetrwały jedynie w stolicy Dolnego Śląska, zmieniając nazwę najpierw na Wrocławskie Promocje Dobrych Książek, a w 2013 roku – na Wrocławskie Targi Dobrych Książek. Do 2015 roku organizatorem Targów była Miejska Biblioteka Publiczna, w roku 2016 pieczę nad tym wydarzeniem (jak również Targami Książki dla Dzieci i Młodzieży Dobre Strony) przejął Wrocławski Dom Literatury. W 2019 roku WTDK połączyły się z Targami Dobre Strony, tworząc jedno grudniowe wydarzenie. Od 2022 operatorem WTDK jest Fundacja Halo Targi. W roku 2022r Wrocławskie Targi Książki było 225 wystawców oraz 50 000 odwiedzających."),
    "ts": md.Fair(hall=halls["tauron"], published=True,
                        organizer=users["organizer_4"], image="/assets/fair_ts.jpg", name="Małopolskie Targi Ślubne",
                        description="Nasza firma istnieje od 1990 roku. Jesteśmy pierwszym i największym organizatorem Targów Ślubnych w Polsce. Pierwsze Targi Ślubne zorganizowaliśmy w 1998 roku i w ciągu tych  lat odbyło sie już ponad 150 imprez w kilkunastu miastach. Targi ślubne od początku cieszą się bardzo dużym zainteresowaniem. Współpracuje z nami kilka tysięcy firm ślubno - weselnych. W ciągu jednego sezonu nasze imprezy odwiedza kilkanaście tysięcy przyszłych par młodych. Organizowane przez nas Targi Ślubne odbywają się w okresie od listopada do lutego - tuż przed rozpoczęciem sezonu ślubno - weselnego. Jest to doskonała okazja do zapoznania się z nową ofertą ślubną dla przyszłych nowożeńców, a dla firm oferujących swoje usługi w branży ślubnej do przedstawienia oferty swoim potencjalnym klientom. Targi dają możliwość załatwienia wielu spraw w jednym miejscu, zapoznania się z najnowszymi trendami i podpatrzenia pomysłów na własny ślub i wesele, a także skorzystania z rad ekspertów. Firmy przygotowują specjalne rabaty i promocje na swoich stoiskach reklamowych. Na dużej scenie odbywają się pokazy mody ślubnej i wizytowej, prezentacje fryzur, makijażu, pokazy florystyczne, występy artystyczne ale i również konkursy z atrakcyjnymi nagrodami dla narzeczonych w których można wygrać suknie ślubne, sesje fotograficzne czy inne usługi. Do prowadzenia imprez zatrudniamy sprawdzonych prezenterów. Pojawiają się u nas również celebryci i gwiazdy tv. W poprzednich latach gościliśmy min Krzyztofa Ibisza, Tomasza Kammela, Kubę Wesołowskiego, Grzegorza Stasiaka, Sebastiana Wątrobą, uczestników i zwycięzców znanych programów telewizyjnych, takich wykonawców jak Bayer Full, aktorów spektaklu 'Romeo i Julia' i wielu innych. Na stałe współpracujemy z Biurem MIss Polski. Wielokrotnie gościliśmy aktualne MISS Polski. To na naszej scenie pierwszy raz w historii spotkały się Miss Polski i Miss Polonia. Zapraszamy do odwiedzania naszych imprez. Sprawdzony od lat organizator nie pozwoli sobie na to aby Państwa niedziela została zmarnowana :)"),
    "mt": md.Fair(hall=halls["hala_B"], published=True,
                        organizer=users["organizer_1"], image="/assets/fair_mt.jpg", name="WARSAW METALTECH",
                        description="Innowacyjne technologie obróbki plastycznej metali, zaawansowane technicznie maszyny, precyzyjne rozwiązania narzędziowe oraz usługi służące procesom związanym z przemysłową obróbką metali – tylko w Ptak Warsaw Expo. WARSAW METALTECH to specjalistyczne targi branżowe, zlokalizowane w biznesowej stolicy środkowo-wschodniej Europy. To nasza odpowiedź na potrzeby szybko rozwijającego się polskiego sektora obróbki. Jako organizator Warsaw Industry Week – Międzynarodowych Targów Innowacyjnych Rozwiązań Przemysłowych organizowanych od pięciu lat w Ptak Warsaw Expo, będących jednocześnie najszybciej rozwijającym się wydarzeniem przeznaczonym dla kluczowych sektorów przemysłu, obserwujemy zapotrzebowanie na imprezę dedykowaną w całości branży obróbki metali. WARSAW METALTECH to branżowe specjalistyczne wydarzenie odbywające się w Ptak Warsaw Expo, Największym Centrum Targowo – Kongresowym w Europie Środkowej. Mające na celu skupienie wszystkich gałęzi branży maszyn i narzędzi do obróbki metalu i stworzenie dogodnych warunków do profesjonalnych kontaktów biznesowych. Targi Technologii, Maszyn i Narzędzi do Obróbki Metalu pozwolą na znalezienie potencjalnych partnerów biznesowych dla twojej firmy. WARSAW METALTECH to doskonała okazja byś mógł porównać i dokładnie przeanalizować wszystkie dostępne na polskim rynku oferty dedykowane branży. Wydarzenie to stanowi również doskonałą okazję do uczestnictwa w konferencjach, warsztatach oraz kongresach branży maszyn i narzędzi do obróbki metalu rozwijających znajomość rynku oraz pokazujących działanie najnowszych technologii. Zarejestruj się i otrzymaj zaproszenie na targi."),
    "bud": md.Fair(hall=halls["mtp"], published=True,
                        organizer=users["organizer_5"], image="/assets/fair_budma.svg", name="BUDMA",
                        description="Targi BUDMA należą do czołówki branżowych wydarzeń na arenie międzynarodowej i przyciągają przedsiębiorców z całego świata. Kluczową rolę w zdobywaniu klientów odgrywają Program Hosted Buyers oraz Międzynarodowa Strefa Spotkań. W ich ramach pomagamy uczestnikom znaleźć potencjalnych partnerów biznesowych z zagranicy i zapewniamy dostęp do kompleksowej wiedzy, jak globalnie kierować rozwojem firmy. Targi BUDMA to wydarzenie skupiające całą branżę budowlaną. To czas premier rynkowych, nowości technologicznych, zdobywania nowych kontaktów biznesowych i kontraktów warunkujących rozwój. Skorzystaj już dzisiaj z wyjątkowej oferty udziału w targach BUDMA! Targi BUDMA to czas biznesowych spotkań, prezentacji innowacyjnych rozwiązań, nowości rynkowych, zdobycia cennej wiedzy. To wyjątkowa okazja na nawiązanie globalnych relacji handlowych oraz miejsce na debatę o wyzwaniach i trendach. Cieszę się, że cała branża mogła spotkać się w Poznaniu podczas jednego z najważniejszych wydarzeń sektora budowlanego i już dziś serdecznie zapraszam na BUDMĘ 2024!"),
    "ms": md.Fair(hall=halls["hala_D"], published=True,
                        organizer=users["organizer_1"], image="/assets/fair_ms.png", name="Warsaw Motorcycle Show",
                        description="Największe targi motocyklowe w Polsce – Warsaw Motorcycle Show, to świetne miejsce by zapoznać się z aktualną ofertą motocykli producentów z całego świata. Setki premier, dziesiątki specjalnie przygotowanych stref, to tylko część atrakcji, która czeka na odwiedzających – to właśnie dlatego nie może Cię tam zabraknąć! Zapraszamy na niepowtarzalne wydarzenie dla branży motocyklowej w największym centrum targowo-kongresowym w Europie Środkowej. Atrakcje dla miłośników motocykli, kilkadziesiąt tysięcy zwiedzających, show dla fanów motoryzacyjnych wrażeń. A wszystko zaledwie 15 minut jazdy od centrum Warszawy. Spotkaj się z największymi producentami z Polski i z zagranicy. Zobacz innowacje z branży cukierniczej, lodziarskiej i kawiarnianej. Odkryj najnowsze rozwiązania w zakresie technologii i produkcji. Warsaw Motorcycle Show to doskonała okazja byś mógł porównać i dokładnie przeanalizować wszystkie dostępne na polskim rynku oferty dedykowane branży. Zarejestruj się i otrzymaj zaproszenie na targi."),
}

fairs["eurogastro"].industries.append(industries["food"])
fairs["foodtech"].industries.append(industries["food"])
fairs["ctr"].industries.append(industries["agric"])
fairs["wme"].industries.append(industries["health"])
fairs["hb"].industries.append(industries["fashi"])
fairs["wtdk"].industries.append(industries["retail"])
fairs["ts"].industries.append(industries["retail"])
fairs["ts"].industries.append(industries["fashi"])
fairs["mt"].industries.append(industries["tech"])
fairs["mt"].industries.append(industries["auto"])
fairs["mt"].industries.append(industries["edu"])
fairs["bud"].industries.append(industries["archi"])
fairs["bud"].industries.append(industries["estate"])
fairs["ms"].industries.append(industries["auto"])
fairs["ms"].industries.append(industries["tech"])


companies = {
    "mextra":    md.Company(exhibitor=users["exhibitor_9"], image="/assets/company_mextra.png", name="Mextra", description="To, co najlepsze, powstaje z potrzeby. Mextra wpisuje się w tę regułę. Od lat obserwujemy funkcjonowanie branży hotelarskiej i gastronomicznej. Dostrzegamy, jak ważną rolę pełni tu wyposażenie. Dla dobrych wrażeń klientów, dla komfortu ich pracowników, dla oszczędności czasu i pieniędzy – tworzymy meble na miarę potrzeb. Produkcja i dystrybucja produktów dla sektora HoReCa to nasza specjalność. Członków naszego zespołu wyróżnia doświadczenie oraz ekspercka wiedza o meblach i oczekiwaniach klientów. Nasza obsługa jest na najwyższym poziomie, tak samo jak jakość naszych produktów. Trzon naszej oferty stanowią trzy marki, każda wyspecjalizowana w swojej dziedzinie."),
    "loftlight": md.Company(exhibitor=users["exhibitor_9"], image="/assets/company_loftlight.webp", name="Loftlight", description="LOFTLIGHT to polski producent lamp, tworzący wysokiej jakości oświetlenie, idealnie wpisujące się w obecne trendy designu. Nasze produkty to lampy betonowe, lampy z malowanego proszkowo aluminium oraz naturalnych materiałów jak drewno, stal nierdzewna czy mosiądz. Oferujemy produkt w 100% wyprodukowany w Polsce, ręcznie robione, za którymi stoją najwyższa jakość, solidność wykonania oraz oryginalne projekty. Jeżeli pragniesz oświetlić swój dom to hurtownia oświetlenia LOFTLIGHT jest dokładnie tym, czego szukasz. Od początku istnienia działalności staramy się codzienną pracą udowadniać, że lampy polskich producentów są doskonałą alternatywą dla europejskiego designu. Dowodem na to jest przyznana w 2022 r. prestiżowa międzynarodowa nagroda Red dot dla projektu lampy ConTeak. Jako doświadczony producent oświetlenia doskonale zdajemy sobie sprawę, jak ważnym elementem są lampy. Dzięki oferowanym produktom stworzysz przestrzeń, w której będziesz czuł się swobodnie i naturalnie. Nasza hurtownia lamp ma wiele lamp przeznaczonych do unikatowych i designerskich wnętrz. Oryginalne formy, loftowa stylistyka oraz przemyślany design to nasz znak rozpoznawczy. Oryginalność i ponadczasowość to cechy, których w aranżacji wnętrz szuka coraz większa liczba osób. Do produkcji oświetlenie wykorzystujemy żarówki i moduły LED. Nasze produkty cechuje prostota wykonania, modne, nieszablonowe kształty, które odpowiadają aktualnym trendom, wykorzystanie innowacyjnych struktur i materiałów wykończeniowych oraz przyciągająca wzrok kolorystyka i stylistyka. Wszystko to sprawia, że polskie lampy LOFTLIGHT są nie tylko praktyczne, ale przede wszystkim posiadają walory dekoracyjne. Nasza oferta ma nieograniczony potencjał aranżacyjny, co doceniają projektanci, architekci wnętrz oraz miłośnicy aktualnych trendów."),
    "tarsmak":   md.Company(exhibitor=users["exhibitor_6"], image="/assets/company_tarsmak.png", name="Tarsmak", description="Jesteśmy polską, rodzinną spółką, założoną w 1991 roku przez małżeństwo Teresę i Józefa Gondków. Wszystkie nasze produkty powstają w malowniczej Małopolsce – w Radgoszczy koło Tarnowa, gdzie mamy swoją siedzibę. Specjalizujemy się w produkcji różnorodnych sosów majonezowych i pomidorowych, majonezów, ketchupów, musztard i dresingów. Nasza oferta obejmuje gamę ponad 200 produktów, dostępnych także w opakowaniach gastronomicznych. Jesteśmy obecni we wszystkich segmentach rynku, począwszy od tradycyjnego, przez nowoczesny (sieciowy), po rozwijające się systematycznie rynki eksportowe.Współpracujemy z licznymi hurtowniami, sieciami hiper i supermarketów, sieciami gastronomicznymi, przetwórstwami rybnymi i garmażeryjnymi. Wśród naszych klientów są również firmy z branży cukierniczo-piekarniczej, dystrybutorzy i detaliści. Współpracujemy ze stałymi i sprawdzonymi dostawcami. Produkcja przebiega w surowo przestrzeganych warunkach, przy stałej i ścisłej kontroli na wszystkich etapach powstawania produktów. Tak dbamy o ich najwyższą jakość. Dbając o dobrostan zwierząt i szanując oczekiwania naszych Klientów, deklarujemy rezygnację  z używania jaj pochodzących z chowu klatkowego w formie masy jajowej, proszku jajecznego, jaj całych i wszelkich innych form przy wytwarzaniu produktów firmy TARSMAK do 2025 roku."),
    "foodmate":  md.Company(exhibitor=users["exhibitor_6"], image="/assets/company_foodmate.png", name="Foodmate", description="Foodmate jest firmą produkującą maszyny z siedzibą w Holandii. Założona w 2006 roku, skupia się przede wszystkim na przetwórstwie drobiu. Po udanym otwarciu firm Foodmate US i Foodmate Brasil, które poszerzyły naszą globalną dystrybucję na Amerykę, uruchomiliśmy niedawno Foodmate Polska i Foodmate UK, poszerzając naszą wiedzę i rozwijając rynek. Kierując się badaniami, w połączeniu z niezrównaną wiedzą i wieloletnim doświadczeniem, naszą misją jest wprowadzanie innowacji, automatyzacja i wprowadzanie efektywnych kosztowo rozwiązań w branży. Nasz zespół reprezentuje dziesiątki lat wiedzy i doświadczenia w branży, czego efektem jest projektowanie, opracowywanie i wdrażanie nowych projektów dla naszych klientów i ich ciągle zmieniających się potrzeb. Chociaż systemy trybowania mięsa, ciemnego i białego są głównym celem firmy, linia produktów Foodmate obejmuje szeroki asortyment urządzeń do przetwórstwa drobiu, przeznaczonych do obsługi żywych ptaków, zabijania, patroszenia, schładzania, ważenia, sortowania i wiele innych. Oprócz produkcji urządzeń, Foodmate oferuje szeroki zakres części zamiennych oraz wsparcie serwisowe"),
    "agroserwis":  md.Company(exhibitor=users["exhibitor_7"], image="/assets/company_agroserwis.png", name="Agro-Serwis", description="Specjalizujemy się w sprzedaży i serwisie maszyn do produkcji rolnej. Posiadamy pełną ofertę maszyn firm: STEYR, CASE IH, MANITOU, LEMKEN, ITALMIX, STRAUTMANN, MASCHIO GASPARDO, HARDI i wielu innych. Oferujemy maszyny nowe jak i używane z obsługą finansowania i z możliwością skorzystania z pakietu ubezpieczeń. W sprzedaży posiadamy szeroką gamę części zamiennych oraz kompleksowy serwis podparty fachowym doradztwem techniczym. Dodatkowo świadczymy usługi rolnicze z możliwością wynajmu maszyn. Zdajemy sobie sprawę z tego, jak cenny jest dziś czas, dlatego naszym klientom oferujemy wszystkie niezbędne usługi w jednym miejscu. Nasza działalność obejmuje głównie teren centralnej i północno – wschodniej Polski. Siedziba główna naszej firmy znajduje się w Zambrowie (woj. podlaskie). Nasze oddziały zlokalizowane są w: Przasnysz, Stare Opole k. Siedlec, Ostrołęka i Grójec."),
    "grunner":  md.Company(exhibitor=users["exhibitor_7"], image="/assets/company_grunner.svg", name="Grunner", description="Kombajn marki Grunner to polski produkt stworzony z myślą o sadownikach, którzy niejednokrotnie muszą borykać się z wieloma problemami - awariami maszyn czy brakiem pracowników. Dzięki połączeniu sił doświadczonego sadownika oraz inżyniera konstruktora, właściciele sadów mogą zacząć pracować znacznie szybciej i wydajniej. Misją naszej firmy jest usprawnienie pracy w sadach, by w krótkim czasie można było zebrać jak największą ilość jabłek z zachowaniem wysokiej jakości plonów. Konstrukcja kombajnu Grunner została bardzo dokładnie przemyślana, dzięki czemu ryzyko powstawania obić na owocach znacznie się zmniejsza."),
    "orimed":  md.Company(exhibitor=users["exhibitor_8"], image="/assets/company_orimed.png", name="Orimed", description="Orimed to innowacyjne rozwiązania w zakresie uszlachetniania i dystrybucji instrumentów medycznych, wykonanych z wysokiej jakości stali chirurgicznej. Nasz Zespół tworzą specjaliści z branży medycznej, projektowej i marketingowej. Są to ludzie z wieloletnim doświadczeniem, którzy – nieprzerwanie od wielu lat – podejmują starania, aby tworzyć najlepsze produkty i usługi. Firma Orimed cyklicznie uczestniczy w krajowych i zagranicznych targach, systematycznie obserwując dynamicznie rozwijający się rynek branży medycznej."),
    "tahe":  md.Company(exhibitor=users["exhibitor_10"], image="/assets/company_tahe.png", name="Tahe", description="Kiedy pod koniec ubiegłej dekady Polska rozpoczynała współprace z hiszpańską marką TAHE, byliśmy dwudziestym siódmym krajem posiadającym dystrybucję tych kosmetyków. W ciągu kilku niespełna lat ta liczba wzrosła do ponad pięćdziesięciu. W tym czasie Laboratorium TAHE opracowało dziesięć nowych linii produktów do pielęgnacji, stylizacji, koloryzacji i specjalistycznych zabiegów fryzjerskich. Podczas procesu tworzenia kosmetyków Laboratorium Tahe kładzie szczególny nacisk na skuteczny i innowacyjny skład kosmetyków, dbałość o szczegóły i wysoką ich jakość. Produkty TAHE posiadają bardzo bogate i starannie dobrane kompozycje witamin, białek i aminokwasów. Zawartość amoniaku w farbach obniżona została do niezbędnego minimum. Wykluczono wiele substancji szkodliwych i obciążających włosy. Zastosowano naturalne i ekologiczne składniki takie jak : olej arganowy, woski roślinne z candelli, carnauby, jojoby, otrębów ryżowych, masła karotenowego, co czyni kosmetyki bardzo naturalnymi i przyjaznymi dla włosów. Nowe serie kosmetyków Tahe wykorzystują w swoim składzie keratynę, olej arganowy, komórki macierzyste roślinnego pochodzenia, ekstrakty z bambusa, naturalny kolagen i kwas hialuronowy.Ich formuły nie zawierają szkodliwych parabenów oraz mocnych konserwantów. Tam gdzie jest to możliwe szkodliwe związki chemiczne zastępuje Natura. Właśnie dlatego zdecydowaliśmy się wprowadzić kosmetyki Tahe na polski rynek. Wierzymy że każdy kto choć raz spróbuje jakości kosmetyków Tahe , przekona się o ich wysokiej jakości.Z przyjemnością prezentujemy Państwu nowości Tahe, skuteczne i profesjonalne kosmetyki do włosów."),
    "szarlatan":  md.Company(exhibitor=users["exhibitor_9"], image="/assets/company_szarlatan.png", name="Antykwariat Szarlatan", description="Codziennie spotykamy fascynujące historie przynoszone do nas przez ludzi i antykwaryczne obiekty. Jednak ludzie odchodzą, artefakty sprzedajemy a czas zaciera pamięć. Postanowiliśmy część z tych historii zachować, uratować przed zapomnieniem i pokazać je światu, bowiem całe sedno antykwarycznej magii mieści się w tych spotkaniach. Tak powstał nasz zupełnie amatorski serial: NA SOFIE SZARLATANA, którego emisję rozpoczęliśmy 24.012014r. Na naszej sofie zasiedli m.in: Anna Pawlowska-Koziar – poetka i bizneswoman, Jolanta Maria Kaleta – pisarka, dr Grzegorz Nieć – bibliolog, Katarzyna Georgiou – poetka. "),
    "sturmer":  md.Company(exhibitor=users["exhibitor_9"], image="/assets/company_sturmer.png", name="Stürmer", description="Spółka Stürmer Maszyny powstała z myślą o klientach, którzy cenią sobie fachowość obsługi, wysoką jakość oferowanych produktów (maszyn do drewna i metalu) i w razie potrzeby rzetelny i szybki serwis. Nasz zespół to ludzie z wieloletnim doświadczeniem zdobytym głównie w firmach niemieckich. Dzięki temu macie Państwo gwarancję, że jakość oferowanych przez nas produktów jak i usług stoi na najwyższym europejskim poziomie. Jesteśmy jedynym przedstawicielem na Polskę niemieckiej firmy Stürmer Maschinen GmbH, która za naszą zachodnią granicą ceniona jest głównie za produkty najwyższej jakości jak i perfekcyjny serwis gwarancyjny i pogwarancyjny. W skład firmy Stürmer wchodzą następujące marki: OPTIMUM, METALLKRAFT, HOLZKRAFT, HOLZSTAR, AIRCRAFT, UNICRAFT, CLEANCRAFT. Dzięki temu wszyscy nasi klienci mają pewność, że nawet po kilku latach będą mieli dostęp do wszystkich części zamiennych. Na naszej hali wystawowej w Kostrzynie, można obejrzeć produkty oferowane przez naszą firmę. Na początku kwietnia 2014 r. rozpoczęło działalność nowe Centrum Logistyczne. Na liczącym ok. 50 000 m² terenie zakładu w Pettstadt koło Bambergu (15 km od głównej siedziby) powstało nowe Centrum Logistyczne w hali o powierzchni 20 000 m². Był to kolejny kamień milowy w historii koncernu STÜRMER."),
}



companies["mextra"].industries.append(industries["retail"])
companies["loftlight"].industries.append(industries["retail"])
companies["tarsmak"].industries.append(industries["food"])
companies["foodmate"].industries.append(industries["food"])
companies["agroserwis"].industries.append(industries["auto"])
companies["agroserwis"].industries.append(industries["agric"])
companies["grunner"].industries.append(industries["auto"])
companies["grunner"].industries.append(industries["agric"])
companies["orimed"].industries.append(industries["health"])
companies["tahe"].industries.append(industries["fashi"])
companies["szarlatan"].industries.append(industries["retail"])
companies["szarlatan"].industries.append(industries["media"])
companies["szarlatan"].industries.append(industries["edu"])
companies["sturmer"].industries.append(industries["retail"])

companies["mextra"].addresses.append(md.Address(city="Kędzierzyn Koźle", street="Szkolna 15", zipcode="47-225"))
companies["loftlight"].addresses.append(md.Address(city="Wrocław", street="Robotnicza 64", zipcode="53-608"))
companies["tarsmak"].addresses.append(md.Address(city="Radgoszcz", street="Witosa 40", zipcode="33-207"))
companies["foodmate"].addresses.append(md.Address(city="Lublin", street="Głęboka 10", zipcode="20-612"))
companies["agroserwis"].addresses.append(md.Address(city="Warszawa", street="Aleja Wilanowska 67", zipcode="02-765"))
companies["grunner"].addresses.append(md.Address(city="Koszajec", street="Koszajec 18", zipcode="96-514"))
companies["orimed"].addresses.append(md.Address(city="Osieck", street="Króla Zygmunta Augusta 9", zipcode="08-445"))
companies["tahe"].addresses.append(md.Address(city="Płock", street="Józefa Kaczmarskiego 2/3", zipcode="09-400"))
companies["szarlatan"].addresses.append(md.Address(city="Wrocław", street="Szczytnicka 51", zipcode="50-382"))
companies["sturmer"].addresses.append(md.Address(city="Kostrzyn", street="Zbożowa 1", zipcode="60-025"))

invites = [
    md.FairProxy(company=companies["mextra"], fair=fairs["eurogastro"], status=md.FairProxyStatus.ACCEPTED, stall=stalls["hala_B"]),
    md.FairProxy(company=companies["loftlight"], fair=fairs["eurogastro"], status=md.FairProxyStatus.ACCEPTED, stall=stalls["hala_B"]),
    md.FairProxy(company=companies["tarsmak"], fair=fairs["eurogastro"], status=md.FairProxyStatus.ACCEPTED, stall=stalls["hala_B"]),
    md.FairProxy(company=companies["foodmate"], fair=fairs["foodtech"], status=md.FairProxyStatus.ACCEPTED, stall=stalls["hala_B"]),
    md.FairProxy(company=companies["agroserwis"], fair=fairs["ctr"], status=md.FairProxyStatus.ACCEPTED, stall=stalls["hala_B"]),
    md.FairProxy(company=companies["grunner"], fair=fairs["ctr"], status=md.FairProxyStatus.ACCEPTED, stall=stalls["hala_B"]),
    md.FairProxy(company=companies["orimed"], fair=fairs["wme"], status=md.FairProxyStatus.ACCEPTED, stall=stalls["hala_B"]),
    md.FairProxy(company=companies["tahe"], fair=fairs["hb"], status=md.FairProxyStatus.ACCEPTED, stall=stalls["hala_B"]),
 ]


@click.command('seed')
def seed():
    base = datetime.date.today() + datetime.timedelta(days=35)
    frs = list(fairs.values())
    for i in range(len(frs)):
        frs[i].start = base + datetime.timedelta(days=i*5)
        frs[i].end = frs[i].start + datetime.timedelta(days=3)

    with current_app.app_context():
        meta = md.db.metadata
        for table in reversed(meta.sorted_tables):
            md.db.session.execute(table.delete())
        md.db.session.commit()

        md.db.session.add_all(halls.values())
        md.db.session.add_all(halls.values())
        md.db.session.add_all(stalls.values())
        md.db.session.add_all(companies.values())
        md.db.session.add_all(invites)
        for ilist in images.values():
            md.db.session.add_all(ilist)
        md.db.session.add_all(frs)
        md.db.session.commit()
