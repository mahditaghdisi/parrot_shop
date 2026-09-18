from decimal import Decimal
from shop.models import Bird

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, bird, quantity=1, override_quantity=False):
        bird_id = str(bird.id)
        if bird_id not in self.cart:
            self.cart[bird_id] = {"quantity": 0}
        if override_quantity:
            self.cart[bird_id]["quantity"] = quantity
        else:
            self.cart[bird_id]["quantity"] += quantity
        if self.cart[bird_id]["quantity"] < 1:
            self.cart[bird_id]["quantity"] = 1
        if self.cart[bird_id]["quantity"] > bird.stock:
            self.cart[bird_id]["quantity"] = bird.stock
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, bird):
        bird_id = str(bird.id)
        if bird_id in self.cart:
            del self.cart[bird_id]
            self.save()

    def __iter__(self):
        bird_ids = self.cart.keys()
        birds = Bird.objects.filter(id__in=bird_ids)
        cart = self.cart.copy()
        for bird in birds:
            cart[str(bird.id)]["bird"] = bird

        for item in cart.values():
            item["price"] = Decimal(item["bird"].final_price)
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum((item["total_price"] for item in self), Decimal(0))

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
