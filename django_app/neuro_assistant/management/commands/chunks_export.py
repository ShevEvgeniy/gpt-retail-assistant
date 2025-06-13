from django.core.management.base import BaseCommand
from neuro_assistant.models import Category, Chunk
from shop.models import Product

class Command(BaseCommand):
    help = 'Export all chunks to a text file'

    def handle(self, *args, **options):
        relative_path = '../fastapi_sushi/chunks_export.md'  # путь до FastAPI-папки

        with open(relative_path, 'w', encoding="utf-8") as file:
            # ===== 🔥 Блок акционных товаров =====
            on_sale_products = Product.objects.filter(on_sale=True)
            if on_sale_products.exists():
                file.write("# 🔥 Товары по акции\n\n")
                for product in on_sale_products:
                    file.write(f'## Позиция каталога – {product.name}\n')
                    clean_description = product.description.replace('\r', '')
                    file.write(f"Описание: {clean_description}\n")
                    file.write(f'Цена по акции: {int(product.price)} рублей\n')
                    file.write(f'Ссылка на товар: [{product.name}](http://127.0.0.1:8000{product.get_absolute_url()})\n\n')

            # ===== 🛍️ Все товары =====
            file.write("# 🛍️ Все товары\n\n")
            products = Product.objects.all()
            for product in products:
                file.write(f'## Позиция каталога – {product.name}\n')
                clean_description = product.description.replace('\r', '')
                file.write(f"Описание: {clean_description}\n")
                file.write(f'Цена: {int(product.price)} рублей\n')
                file.write(f'Ссылка на товар: [{product.name}](http://127.0.0.1:8000{product.get_absolute_url()})\n\n')

            # ===== 📚 Чанки из базы =====
            for category in Category.objects.all():
                chunks = Chunk.objects.filter(category=category)
                for chunk in chunks:
                    file.write(f'## {category.name}\n')
                    file.write(f'{chunk.text}\n')
