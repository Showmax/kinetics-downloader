from pathlib import Path
import json
import shutil


def move_files():
    categories_path = Path().cwd() / 'resources' / '700' / 'categories_motion.json'

    kinetics_ssd = Path("/media/gitumarkk/Extreme SSD/Dancelogue/DATASETS/Kinetics/")
    kinetics_ssd_train = kinetics_ssd / "train"
    kinetics_ssd_val = kinetics_ssd / "val"

    kinetics_hdd = Path("/media/gitumarkk/Seagate Backup Plus Drive/Dancelogue/DATASETS/Kinetics/")
    kinetics_hdd_train = kinetics_hdd / "train"

    with categories_path.open(mode='r') as f:
        categories = json.load(f)

    # print(sorted(categories))

    folder_array = []
    for fp in kinetics_ssd_train.iterdir():
        name = " ".join(str(fp.stem).lower().split("_"))

        if name not in categories:
            folder_array.append(name)
            print('COPYING :', name)
            shutil.move(str(fp), str(kinetics_hdd_train))
    
    
    # print(sorted(folder_array))
    # print(kinetics_hdd_train.exists())

    # for fp in kinetics_hdd_train.iterdir():
    #     print(fp.stem)

move_files()