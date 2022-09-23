from .models import HappyHour , Product
from datetime import datetime ,timedelta

def update_happyhour():
    happy_h = HappyHour.objects.get(pk = 1)
    print(happy_h.modified_at.strftime("%Y-%m-%d %H:%M"))
    print(happy_h.discount_percentage)
    print(datetime.now().strftime("%Y-%m-%d %H:%M"))
    if happy_h.is_active :
        after_hour = happy_h.modified_at + timedelta(minutes=60)
        if datetime.now().strftime("%Y-%m-%d %H:%M")== after_hour.strftime("%Y-%m-%d %H:%M") :
            happy_h.is_active = False
            products = Product.objects.filter(boutique__in= happy_h.boutiques.all())
            for product in  products :
                product.discount_percentage -= happy_h.discount_percentage
                product.save()

