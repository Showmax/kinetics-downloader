# Python
import sys

# Django
from django.conf import settings

sys.path.append(str(settings.DOWNLOADER_DIR.resolve()))

import download


def download_data(data, save_root, failed_path):
  download.download_missing(
    data, save_root, 8, failed_path,
    None, None, None, None
  )