# Python
import sys
import multiprocessing

# Django
from django.conf import settings

sys.path.append(str(settings.DOWNLOADER_DIR.resolve()))

import download


def download_data(data, save_root, failed_path, stats_path):
  num_workers = (multiprocessing.cpu_count() * 2) + 1
  print('starting with {} workers'.format(num_workers))
  download.download_missing(
    data, save_root, num_workers, failed_path,
    None, None, None, None, stats_file=stats_path
  )
