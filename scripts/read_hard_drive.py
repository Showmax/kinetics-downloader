from pathlib import Path
from collections import defaultdict
import json

DATASET_ROOT = Path("/media/gitumarkk/Seagate Backup Plus Drive//Dancelogue/DATASETS/Kinetics/")


def read_files():
  file_dict = defaultdict(dict)
  for f1 in DATASET_ROOT.iterdir():
    if f1.stem in ['train', 'val', 'test']:
      for f2 in f1.iterdir():
        if f2.is_dir():
          for f3 in f2.iterdir():
            file_dict[f3.name]['folder'] = f1.stem
            file_dict[f3.name]['class'] = f2.stem
            file_dict[f3.name]['size'] = f3.stat().st_size

        else:
          file_dict[f2.name]['folder'] = f1.stem
          file_dict[f2.name]['size'] = f2.stat().st_size
  return file_dict

def run():
  result = read_files()
  with open(Path('result.json'), "w") as f:
      json.dump(result, f, indent=4)

run()
