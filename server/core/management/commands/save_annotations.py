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
from core.models import DownloadStatus

# Third party
import tqdm


DOWNLOAD_PATH = settings.WORK_DIR / 'downloaded.json'
ALL_PATH = settings.WORK_DIR / 'all.json'
MISSING_PATH = settings.WORK_DIR / 'missing.json'
ERROR_PATH = settings.WORK_DIR / 'error.json'
TO_DOWNLOAD_FOLDER_PATH = settings.WORK_DIR / 'to-download'
MISSING_SUMMARY_PATH = settings.WORK_DIR / 'missing_summary.csv'

CATEGORIES_PATH = settings.RESOURCES_DIR / "categories.json"
CLASSES_PATH = settings.RESOURCES_DIR / "classes.json"

TRAIN_METADATA_PATH = settings.RESOURCES_DIR / "700/train/kinetics_700_train.json"
VAL_METADATA_PATH = settings.RESOURCES_DIR / "700/val/kinetics_700_val.json"
TEST_METADATA_PATH = settings.RESOURCES_DIR / "700/json/kinetics_test.json"

TO_DOWNLOAD_FOLDER_PATH.mkdir(parents=True, exist_ok=True)

class Command(BaseCommand):
    def save_downloaded(self, subset='train'):
        data = defaultdict(dict)

        DATASET_ROOT = Path("/media/gitumarkk/Seagate Backup Plus Drive//Dancelogue/DATASETS/Kinetics/")

        for subset in ['train', 'val', 'test']:
            print('subset :', subset)
            for folder in tqdm.tqdm((DATASET_ROOT / subset).iterdir()):
                for video in folder.iterdir():
                    if video.suffix in ['.mp4', '.mkv']:
                        # print(folder.stem)
                        data[video.stem] = {
                            'path': str(video.resolve()),
                            'subset': subset,
                            'label': folder.stem
                        }

        print("Total Downloaded: ", len(data.keys()))

        with DOWNLOAD_PATH.open(mode='w') as f:
            json.dump(data, f)

    def load_and_save(self):
        data = defaultdict(dict)

        for path in [TRAIN_METADATA_PATH, VAL_METADATA_PATH]:
            with path.open(mode='r') as f:
                annotations = json.load(f)
            for key, value in tqdm.tqdm(annotations.items()):
                data[key].update(value)

        with ALL_PATH.open(mode='w') as f:
            json.dump(data, f)

        print("Total All", len(data.keys()))

            # ds, _ = DownloadStatus.objects.get_or_create(youtube_id=key)
            # ds.subset = value.get('subset')
            # ds.url = value.get('url')
            # ds.label = value.get('annotations', {}).get('label')
            # ds.save()

    def get_diff(self):
        diff = defaultdict(dict)

        with ALL_PATH.open(mode='r') as f:
            full = json.load(f)

        with DOWNLOAD_PATH.open(mode='r') as f:
            downloaded = json.load(f)

        keys_diff = len(list(full.keys())) - len(list(downloaded.keys()))

        print("Total Missing: ", keys_diff)

        for key, value in full.items():
            if not downloaded.get(key):
                diff[key] = value

        diff_keys = len(list(diff.keys()))

        print(keys_diff, diff_keys, " difference", keys_diff - diff_keys)

        with MISSING_PATH.open(mode='w') as f:
            json.dump(diff, f)

    def save_to_folders(self):
        """
        Conducted so that each folder can upload a category.
        """
        to_download = defaultdict(lambda: defaultdict(dict))
        summary = defaultdict(lambda: defaultdict(int))

        with MISSING_PATH.open(mode='r') as f:
            missing = json.load(f)

        for key, value in missing.items():
            to_download[value.get('annotations').get('label')][value.get('subset')].update({ key: value })

        for key, value in tqdm.tqdm(to_download.items()):
            for subset, data in value.items():
                label_path = TO_DOWNLOAD_FOLDER_PATH / key / subset
                label_path.mkdir(parents=True, exist_ok=True)

                summary[key][subset] = len(data.keys())
                with (label_path / 'missing.json').open(mode='w') as f:
                    json.dump(data, f)

        with MISSING_SUMMARY_PATH.open(mode="w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['label', 'train', 'val'])

            rows = [[key, value.get('train'), value.get('val')] for key, value in summary.items()]
            for row in sorted(rows, key=lambda x: x[0], reverse=True):
                writer.writerow(row)

    def handle(self, *args, **options):
        self.save_downloaded()
        self.load_and_save()
        self.get_diff()
        self.save_to_folders()
