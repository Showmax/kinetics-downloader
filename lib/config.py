import os

DATASET_ROOT = "dataset"
TRAIN_ROOT = os.path.join(DATASET_ROOT, "train")
VALID_ROOT = os.path.join(DATASET_ROOT, "valid")
TEST_ROOT = os.path.join(DATASET_ROOT, "test")

CATEGORIES_PATH = "resources/categories.json"
KINETICS_TRAIN_PATH = "resources/kinetics_train.json"
KINETICS_VAL_PATH = "resources/kinetics_val.json"
KINETICS_TEST_PATH = "resources/kinetics_test.json"