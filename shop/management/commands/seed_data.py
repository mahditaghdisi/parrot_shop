from django.core.management.base import BaseCommand
from shop.models import Category, Bird


CATEGORIES = [
    ("عروس هلندی", "🦜"),
    ("مرغ عشق", "💚"),
    ("کاسکو (طوطی خاکستری)", "🦚"),
    ("قناری", "🐤"),
    ("طوطی آمازون", "🌴"),
    ("فنچ", "🐦"),
    ("طوطی سان کانیور", "☀️"),
    ("لوازم و اکسسوری", "🏠"),
]

BIRDS = [
    ("عروس هلندی پرل", "عروس هلندی", "Cockatiel", "M", 6, "پرل خاکستری", "easy", False, 950000, 0, 12, True,
     "پرنده‌ای آرام و اجتماعی، مناسب مبتدیان و خانواده‌ها."),
    ("مرغ عشق رنگی یاسی", "مرغ عشق", "Budgerigar", "F", 4, "یاسی", "easy", True, 480000, 10, 20, True,
     "بازیگوش و کم‌هزینه، امکان یادگیری چند کلمه ساده."),
    ("کاسکو آفریقایی اصیل", "کاسکو (طوطی خاکستری)", "African Grey", "M", 18, "خاکستری", "pro", True, 45000000, 5, 2, True,
     "باهوش‌ترین طوطی جهان، توانایی یادگیری صدها کلمه — نیاز به نگهدارنده باتجربه."),
    ("قناری ملودی وایت", "قناری", "Canary", "M", 8, "سفید", "medium", False, 1800000, 0, 6, False,
     "قناری آوازخوان با صدای دلنشین، مناسب فضای آرام خانه."),
    ("طوطی آمازون سرزرد", "طوطی آمازون", "Yellow-headed Amazon", "U", 24, "سبز-زرد", "pro", True, 28000000, 0, 1, False,
     "طوطی بزرگ و باهوش با قدرت تقلید صدا بسیار بالا."),
    ("فنچ زبرا جفت", "فنچ", "Zebra Finch", "U", 3, "خاکستری-سفید", "easy", False, 650000, 15, 15, False,
     "زوج فنچ کوچک و پرانرژی، مناسب قفس‌های اجتماعی."),
    "سان کانیور رنگین‌کمانی",
]

SUN_CONURE = ("سان کانیور رنگین‌کمانی", "طوطی سان کانیور", "Sun Conure", "F", 10, "نارنجی-زرد", "medium", True,
              6200000, 20, 4, True, "طوطی رنگارنگ و پرسروصدا با شخصیت بازیگوش و اجتماعی.")


class Command(BaseCommand):
    help = "داده‌های نمونه برای فروشگاه پرندگان را ایجاد می‌کند"

    def handle(self, *args, **options):
        cat_objs = {}
        for name, icon in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"icon": icon})
            cat_objs[name] = cat
        self.stdout.write(self.style.SUCCESS(f"{len(cat_objs)} دسته‌بندی آماده شد."))

        rows = [b for b in BIRDS if isinstance(b, tuple)]
        rows.append(SUN_CONURE)

        created = 0
        for (name, cat_name, species, gender, age, color, level, can_talk,
             price, discount, stock, featured, desc) in rows:
            if Bird.objects.filter(name=name).exists():
                continue
            Bird.objects.create(
                category=cat_objs[cat_name],
                name=name,
                species=species,
                gender=gender,
                age_months=age,
                color=color,
                care_level=level,
                can_talk=can_talk,
                price=price,
                discount_percent=discount,
                stock=stock,
                is_featured=featured,
                short_description=desc,
                description=desc + "\n\nشامل مشاوره رایگان تغذیه و نگهداری پس از خرید.",
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"{created} پرنده جدید اضافه شد."))
