import os

# DATASET_ROOT = "/media/gitumarkk/Extreme SSD/Dancelogue/DATASETS/Kinetics/"
DATASET_ROOT = "/media/gitumarkk/Seagate Backup Plus Drive//Dancelogue/DATASETS/Kinetics/"
TRAIN_ROOT = os.path.join(DATASET_ROOT, "train")
VALID_ROOT = os.path.join(DATASET_ROOT, "val")
TEST_ROOT = os.path.join(DATASET_ROOT, "test")

TRAIN_FRAMES_ROOT = os.path.join(DATASET_ROOT, "train_frames")
VALID_FRAMES_ROOT = os.path.join(DATASET_ROOT, "val_frames")
TEST_FRAMES_ROOT = os.path.join(DATASET_ROOT, "test_frames")

TRAIN_SOUND_ROOT = os.path.join(DATASET_ROOT, "train_sound")
VALID_SOUND_ROOT = os.path.join(DATASET_ROOT, "val_sound")
TEST_SOUND_ROOT = os.path.join(DATASET_ROOT, "test_sound")

CATEGORIES_PATH = "resources/categories.json"
CLASSES_PATH = "resources/classes.json"

TRAIN_METADATA_PATH = "resources/700/train/kinetics_700_train.json"
VAL_METADATA_PATH = "resources/700/val/kinetics_700_val.json"
TEST_METADATA_PATH = "resources/700/json/kinetics_test.json"

SUB_CLASS_PATH = "resources/700/categories.json"
