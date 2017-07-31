import lib.config as config
import lib.parallel_to_frames as parallel

pool = parallel.Pool(["jogging"], config.TRAIN_ROOT, config.TRAIN_FRAMES_ROOT, 1, "dataset/failed_frames.txt")
pool.start_workers()
pool.feed_videos()
pool.stop_workers()