from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MinValueValidator
from users.models import CustomUser


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name="variants"
    )
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    price_override = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)],
    )

    def __str__(self):
        return f"{self.product.name} - {self.color or 'Sem cor'} - {self.size or 'Tamanho único'}"

class Review(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE_STAR = 1, "1 estrela"
        TWO_STARS = 2, "2 estrelas"
        THREE_STARS = 3, "3 estrelas"
        FOUR_STARS = 4, "4 estrelas"
        FIVE_STARS = 5, "5 estrelas"

    product = models.ForeignKey(
        "Product", related_name="reviews", on_delete=models.CASCADE
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RatingChoices.choices)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} avaliou {self.product.name} com {self.rating} estrelas"

    def clean(self):
        if Review.objects.filter(product=self.product, user=self.user).exists():
            raise ValidationError("Você já avaliou este produto.")


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        Brand, related_name="products", on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    related_products = models.ManyToManyField("self", blank=True)
    default_variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_for_product",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.name)
            unique_slug = original_slug
            num = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def clean(self):
        if self.discount_price and self.discount_price > self.price:
            raise ValidationError(
                "O preço com desconto não pode ser maior que o preço original."
            )

    @property
    def is_available(self):
        return self.variants.filter(stock__gt=0).exists() and self.is_active

    @property
    def final_price(self):
        if self.default_variant and self.default_variant.price_override:
            return self.default_variant.price_override
        return self.discount_price or self.price



