from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    on_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.pk)])