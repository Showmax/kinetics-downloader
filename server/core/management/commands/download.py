# Python
import json
import subprocess
import shutil
from pathlib import Path
from collections import defaultdict
import csv

# Django
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

# App
from core.download import download_data

# Third party
import tqdm


DOWNLOAD_PATH = settings.WORK_DIR / 'downloaded.json'

class Command(BaseCommand):
    def add_arguments(self, parser):
      parser.add_argument('path', type=Path, help='folder of the path to download')

    def handle(self, *args, **options):
        for subset in ['train', 'val']:
          path = options['path'] / subset / 'missing.json'
          with path.open(mode='r') as f:
            data = json.load(f)

          download_path = settings.ROOT_DIR.parent / 'downloads' /  subset
          download_path.mkdir(parents=True, exist_ok=True)

          failed_path = settings.ROOT_DIR.parent / 'downloads' / 'failed.csv'
          download_data(data, download_path, failed_path)
