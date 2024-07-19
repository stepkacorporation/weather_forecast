import os
import csv
import zipfile
import requests
import shutil

from tqdm import tqdm
from typing import Any
from django.core.management.base import BaseCommand

from ...models import City


class Command(BaseCommand):
    """Команда для загрузки данных о городах в базу данных."""

    help = 'Загружает данные о городах в базу данных.'

    def handle(self, *args: Any, **options: Any) -> None:
        url = 'https://gist.github.com/dnovik/694d106be3ff20eb0c73a0511c83b7f3/archive/056b7ece3b762723c02d3809ef77e2ae92a2bcd0.zip'
        zip_file_name = url.rsplit('/')[-1]
        tmp_folder = 'tmp'
        zip_file_path = os.path.join(tmp_folder, zip_file_name)
        extract_to = os.path.join(tmp_folder, 'extracted')

        os.makedirs(tmp_folder, exist_ok=True)

        self.stdout.write(f'Загрузка файла {url}...')
        try:
            self.download_file(url, zip_file_path)
        except requests.RequestException as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке файла: {error}'))
            return

        self.stdout.write(f'Распаковка файла "{zip_file_path}"...')
        try:
            self.unzip_file(zip_file_path, extract_to)
        except zipfile.BadZipFile as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при распаковке файла: {error}'))
            return

        txt_file_path = os.path.join(extract_to, 'cities.csv')
        self.stdout.write(f'Загрузка данных в БД из файла "{txt_file_path}"...')
        try:
            self.load_cities_from_file(txt_file_path)
        except Exception as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных в БД: {error}'))
            return

        self.stdout.write('Очистка временных файлов...')
        try:
            self.cleanup(tmp_folder)
        except OSError as error:
            self.stdout.write(self.style.ERROR(f'Ошибка при удалении файлов: {error}'))
            return

        self.stdout.write(self.style.SUCCESS('Готово!'))

    def download_file(self, url: str, local_filename: str) -> None:
        """
        Скачивает файл по заданному URL.

        Args:
            - url (str): URL для скачивания файла.
            - local_filename (str): Локальное имя файла для сохранения.

        Raises: 
            - requests.RequestException: Если возникла ошибка при запросе.
        """

        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        return local_filename
    
    def unzip_file(self, zip_file_path: str, extract_to: str) -> None:
        """
        Распаковывает ZIP-файл.

        Args:
            - zip_file_path (str): Путь к ZIP-файлу.
            - extract_to (str): Папка для извлечения содержимого.

        Raises:
            - zipfile.BadZipFile: Если ZIP-файл поврежден или не является ZIP-файлом.
        """
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            for file_info in zip_file.infolist():
                if file_info.filename.endswith('cities.csv'):
                    file_info.filename = os.path.basename(file_info.filename)
                    zip_file.extract(file_info, extract_to)
                    break

    def load_cities_from_file(self, file_path: str) -> None:
        """
        Загружает данные о городах из CSV-файла в базу данных.

        Args:
            - file_path (str): Путь к CSV-файлу.
        """

        cities_to_create = []

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in tqdm(reader):
                name_city = row['Город'].strip()
                locality = row['Н/п'].strip()
                region = row['Регион'].strip()
                if not name_city:
                    if locality:
                        name_city = locality
                    else:
                        name_city = region
                city = City(
                    name=name_city,
                    type_of_region=row['Тип региона'].strip(),
                    region=region,
                    timezone=row['Часовой пояс'].strip(),
                    latitude=row['Широта'].strip(),
                    longitude=row['Долгота'].strip(),
                )
                cities_to_create.append(city)
        
        City.objects.bulk_create(cities_to_create, ignore_conflicts=True)
    
    def cleanup(self, tmp_folder: str) -> None:
        """
        Удаляет временные файлы и папки.

        Args:
            - tmp_folder (str): Папка, содержащая временные файлы и папки.

        Raises:
            - OSError: Если возникла ошибка при удалении файлов.
        """
        
        shutil.rmtree(tmp_folder)
