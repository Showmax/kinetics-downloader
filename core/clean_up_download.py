import os, subprocess

import lib.config as config

print("files to delete:")
for root in [config.TRAIN_ROOT, config.VALID_ROOT, config.TEST_ROOT]:
  if os.path.isdir(root):
    subprocess.call(["find", root, "(",
                     "-name", "*.ytdl", "-o",
                     "-name", "*.part", "-o",
                     "-name", "*_raw*", ")",
                     "-exec", "echo", "{}", ";"])

input("Are you sure? (press enter to continue)")
for root in [config.TRAIN_ROOT, config.VALID_ROOT, config.TEST_ROOT]:
  if os.path.isdir(root):
    subprocess.call(["find", root, "(",
                     "-name", "*.ytdl", "-o",
                     "-name", "*.part", "-o",
                     "-name", "*_raw*", ")",
                     "-exec", "rm", "{}", ";"])