import cv2, os

def video_to_jpgs(video_path, save_path, do_resize=True, shorter_side=256):

  cap = cv2.VideoCapture(video_path)

  if not cap.isOpened():
    return False

  i = 0
  res, frame = cap.read()

  while res:
    if do_resize:
      frame = resize(frame, shorter_side=shorter_side)

    cv2.imwrite(os.path.join(save_path, "frame{:d}.jpg".format(i)), frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
    res, frame = cap.read()
    i += 1

  num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  num_images = len(os.listdir(save_path))

  return num_frames == num_images

def resize(frame, shorter_side=256):
  if frame.shape[0] > frame.shape[1]:
    long = frame.shape[0]
    short = frame.shape[1]
  else:
    short = frame.shape[0]
    long = frame.shape[1]

  fract = shorter_side / short
  target_long = int(long * fract)

  if frame.shape[0] > frame.shape[1]:
    return cv2.resize(frame, (shorter_side, target_long))
  else:
    return cv2.resize(frame, (target_long, shorter_side))

