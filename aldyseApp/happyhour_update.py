from .models import HappyHour , Product
from datetime import datetime ,timedelta

def update_happyhour():
    happy_h = HappyHour.objects.get(pk = 1)
    print(happy_h.modified_at.strftime("%Y-%m-%d %H:%M"))
    print(happy_h.discount_percentage)
    print(datetime.now().strftime("%Y-%m-%d %H:%M"))
    if happy_h.is_active and (happy_h.modified_at.strftime("%Y-%m-%d %H:%M") == datetime.now().strftime("%Y-%m-%d %H:%M")) :
        products = Product.objects.filter(boutique__in= happy_h.boutiques.all() , discount_percentage = 0.00)
        for product in products :
                product.discount_percentage += happy_h.discount_percentage
                product.happyhour_discount = True
                product.save()
    after_hour = happy_h.modified_at + timedelta(minutes=60)
    print(after_hour.strftime("%Y-%m-%d %H:%M"))
    if datetime.now().strftime("%Y-%m-%d %H:%M")== after_hour.strftime("%Y-%m-%d %H:%M") :
        happy_h.is_active = False
        happy_h.save()
        products = Product.objects.filter(boutique__in= happy_h.boutiques.all(), happyhour_discount = True)
        for product in  products :
            product.discount_percentage -= happy_h.discount_percentage
            product.happyhour_discount = False
            product.save()

