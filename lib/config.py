import os

DATASET_ROOT = "dataset"
TRAIN_ROOT = os.path.join(DATASET_ROOT, "train")
VALID_ROOT = os.path.join(DATASET_ROOT, "valid")
TEST_ROOT = os.path.join(DATASET_ROOT, "test")

CATEGORIES_PATH = "resources/categories.json"
CLASSES_PATH = "resources/classes.json"
TRAIN_METADATA_PATH = "resources/kinetics_train.json"
VAL_METADATA_PATH = "resources/kinetics_val.json"
TEST_METADATA_PATH = "resources/kinetics_test.json"