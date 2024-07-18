import os
import csv
import zipfile
import requests

from tqdm import tqdm
from typing import Any
from django.core.management.base import BaseCommand

from ...models import City


class Command(BaseCommand):
    help = 'Загружает данные о городах в базу данных.'

    def handle(self, *args: Any, **options: Any) -> None:
        url = 'http://download.geonames.org/export/dump/cities500.zip'
        zip_file_path = url.rsplit('/')[-1]
        extract_to = '.'

        self.stdout.write(f'Загрузка файла {url}...')
        try:
            self.download_file(url, zip_file_path)
        except requests.RequestException as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке файла: {error}'))

        self.stdout.write(f'Распаковка файла "{zip_file_path}"...')
        try:
            self.unzip_file(zip_file_path, extract_to)
        except zipfile.BadZipFile as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при распаковке файла: {error}'))

        txt_file_path = zip_file_path.split('.')[0] + '.txt'
        self.stdout.write(f'Загрузка данных в БД из файла "{txt_file_path}"...')
        try:
            self.load_cities_from_file(txt_file_path)
        except Exception as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных в БД: {error}'))

        self.stdout.write('Очистка ненужных файлов...')
        try:
            self.cleanup(zip_file_path, txt_file_path)
        except OSError as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при удалении файлов: {error}'))

        self.stdout.write(self.style.SUCCESS('Готово!'))

    def download_file(self, url: str, local_filename: str) -> None:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        return local_filename
    
    def unzip_file(self, zip_file_path: str, extract_to: str) -> None:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            zip_file.extractall(extract_to)

    def load_cities_from_file(self, file_path: str) -> None:
        cities_to_create = []

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            for _, _, name_en, alternate_names, latitude, longitude, _, _, country_code, *_ in tqdm(reader):
                if not name_en:
                    continue
                name_ru = None
                for name in alternate_names.split(','):
                    name = name.strip()
                    if all(char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for char in name.strip().lower()):
                        name_ru = name
                        break
                
                city = City(
                    name_en=name_en.strip(),
                    name_ru=name_ru,
                    country_code=country_code,
                    latitude=latitude,
                    longitude=longitude,
                )
                cities_to_create.append(city)
        
        City.objects.bulk_create(
            cities_to_create,
            update_conflicts=False,
            unique_fields=['name_en', 'country_code', 'latitude', 'longitude'],
        )
    
    def cleanup(self, *files: tuple[str]) -> None:
        for file in files:
            os.remove(file)

                

    