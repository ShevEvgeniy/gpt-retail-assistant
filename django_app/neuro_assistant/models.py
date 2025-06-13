from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class Chunk(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.category.name
    
    class Meta:
        verbose_name = 'Чанк'
        verbose_name_plural = 'Чанки'

