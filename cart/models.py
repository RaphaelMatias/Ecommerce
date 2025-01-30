from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def clear_cart(self):
        if self.is_paid:
            raise ValueError('Não é possivel limpar um carrinho que já foi pago')
        self.items.all().delete()

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f'Carrinho de {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_selected = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.final_price * self.quantity

    def save(self, *args, **kwargs):
        try:
            existing_item = CartItem.objects.get(cart=self.cart, product=self.product)
            new_quantity = existing_item.quantity + self.quantity
            
            if new_quantity > self.product.stock:
                new_quantity = self.product.stock
            existing_item.quantity = new_quantity
            existing_item.save()
        except CartItem.DoesNotExist:
                if self.quantity > self.product.stock:
                    self.quantity = self.product.stock
                super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
