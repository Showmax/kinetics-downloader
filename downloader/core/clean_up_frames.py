import subprocess

failed_frames_path = "dataset/failed_frames.txt"

with open(failed_frames_path, "r") as file:
  failed_frames = file.readlines()

failed_frames = [x.strip() for x in failed_frames]

for video_id in failed_frames:
  subprocess.call(["find", "dataset/train_frames", "-maxdepth", "2",
                   "-name", "*{:s}*".format(video_id),
                   "-exec", "rmdir", "{}", ";"])

  subprocess.call(["find", "dataset/valid_frames", "-maxdepth", "2",
                   "-name", "*{:s}*".format(video_id),
                   "-exec", "rmdir", "{}", ";"])