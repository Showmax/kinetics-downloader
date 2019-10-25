# Python
import json
import subprocess
import shutil
from pathlib import Path
import tqdm
from collections import defaultdict

# Django
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

# App
from core.models import DownloadStatus

DOWNLOAD_PATH = settings.WORK_DIR / 'downloaded.json'
ALL_PATH = settings.WORK_DIR / 'all.json'
MISSING_PATH = settings.WORK_DIR / 'missing.json'
ERROR_PATH = settings.WORK_DIR / 'error.json'

CATEGORIES_PATH = settings.RESOURCES_DIR / "categories.json"
CLASSES_PATH = settings.RESOURCES_DIR / "classes.json"

TRAIN_METADATA_PATH = settings.RESOURCES_DIR / "700/train/kinetics_700_train.json"
VAL_METADATA_PATH = settings.RESOURCES_DIR / "700/val/kinetics_700_val.json"
TEST_METADATA_PATH = settings.RESOURCES_DIR / "700/json/kinetics_test.json"


class Command(BaseCommand):
    def save_downloaded(self, subset='train'):
        data = defaultdict(dict)

        DATASET_ROOT = Path("/media/gitumarkk/Seagate Backup Plus Drive//Dancelogue/DATASETS/Kinetics/")

        for subset in ['train', 'val', 'test']:
            print('subset :', subset)
            for folder in tqdm.tqdm((DATASET_ROOT / subset).iterdir()):
                for video in folder.iterdir():
                    if video.suffix in ['.mp4', '.mkv']:
                        data[video.stem] = {
                            'path': str(video.resolve()),
                            'subset': subset
                        }

        print(len(data.keys()))

        with DOWNLOAD_PATH.open(mode='w') as f:
            json.dump(data, f, indent=2)

    def load_and_save(self):
        data = defaultdict(dict)

        for path in [TRAIN_METADATA_PATH, VAL_METADATA_PATH]:
            with path.open(mode='r') as f:
                annotations = json.load(f)

            for key, value in tqdm.tqdm(annotations.items()):
                data[key] = {
                    'url': value.get('url'),
                    'subset': value.get('subset')
                }

        with ALL_PATH.open(mode='w') as f:
            json.dump(data, f, indent=2)

        print(len(data.keys()))

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

        print(keys_diff)

        for key, value in full.items():
            if not downloaded.get(key):
                diff[key] = value

        diff_keys = len(list(diff.keys()))

        print(keys_diff, diff_keys, " difference", keys_diff - diff_keys)

        with MISSING_PATH.open(mode='w') as f:
            json.dump(diff, f, indent=2)


    def handle(self, *args, **options):
        self.save_downloaded()
        self.load_and_save()
        self.get_diff()

        # self.load_and_save(VAL_METADATA_PATH)
        # self.load_and_save(TEST_METADATA_PATH)

        #

        # raw_path = settings.WORK_DIR / "dancelogue_dataset.json"

        # origin = process_labels(raw_path)

        # for folder in detections_path.iterdir():
        #     origin_data = origin.get(folder.stem)

        #     if not origin_data:
        #         print(str(folder))
        #         continue

        #     json_file = folder / 'detections.json'

        #     mp4_file = self.convert_mp4(folder)

        #     if json_file.exists():
        #         with json_file.open(mode='r', encoding='utf-8') as f:
        #             detections = json.load(f)

        #         if isinstance(detections, list):
        #             detections = {
        #                 'data': detections,
        #                 'duration': -1
        #             }
        #     else:
        #         print("{} does not exist".format(str(json_file)))

        #     inference = Inference.objects.filter(uuid=origin_data['uuid']).first()

        #     if not inference:
        #         print("{} does not exist".format(origin_data['uuid']))

        #     elif inference.status == Inference.PREDICTED:
        #         inference.return_results()

        #     elif inference.status == Inference.INITIALIZED:
        #         print("{} - migrated".format(inference.id))
        #         inference.result = detections
        #         inference.video_url = origin_data['media']
        #         inference.processed_at = timezone.now()
        #         inference.local_path = str(mp4_file.resolve())
        #         inference.status = Inference.PREDICTED
        #         inference.save()
