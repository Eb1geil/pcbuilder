from django.core.management.base import BaseCommand
from pc_builder_core.models import CPU, GPU, RAM, Storage, Motherboard
import json
import os


class Command(BaseCommand):
    help = "Load components from JSON files into the database"

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_files = {
            'CPU': os.path.join(BASE_DIR, 'json', 'CPU.json'),
            'GPU': os.path.join(BASE_DIR, 'json', 'GPU.json'),
            'RAM': os.path.join(BASE_DIR, 'json', 'memory.json'),
            'Storage': os.path.join(BASE_DIR, 'json', 'SSD.json'),
            'Motherboard': os.path.join(BASE_DIR, 'json', 'motherboard.json'),
        }

        for model_name, file_path in json_files.items():
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"Файл {file_path} не найден. Пропускаем."))
                continue

            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            model = globals()[model_name]

            for entry in data:
                # Преобразование benchmark в целое число, если это возможно
                if 'benchmark' in entry:
                    try:
                        entry['benchmark'] = int(float(entry['benchmark']))
                    except ValueError:
                        entry['benchmark'] = None

                # Загрузка данных в модель
                model.objects.update_or_create(**entry)

            self.stdout.write(self.style.SUCCESS(f"{model_name}: успешно загружено {len(data)} записей из {file_path}"))
