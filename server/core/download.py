# Python
import sys
import multiprocessing

# Django
from django.conf import settings

sys.path.append(str(settings.DOWNLOADER_DIR.resolve()))

import download


def download_data(data, save_root, failed_path):
  print('starting with {} workers'.format(multiprocessing.cpu_count() + 1))
  download.download_missing(
    data, save_root, multiprocessing.cpu_count() + 1, failed_path,
    None, None, None, None
  )
