## Download DeepMind's Kinetics

Download all videos from DeepMind's [Kinetics dataset](https://deepmind.com/research/open-source/open-source-datasets/kinetics/).
Moreover, you can use this library to extract **frames** and **sound track** from videos, generate metadata for training
and pack all sound tracks into a single **tfrecords** file for faster reading.

#### Requirements

* Python >= 3.4
* youtube-dl
* ffmpeg
* gzip

Required Python packages are listed in **requirements.txt**.

#### Usage

**Download all videos**:
```
python download.py --all
```

**Download specific classes**:
```
python download.py --classes 'pole vault' 'blowing glass'
```

List all classes:
```
python list_classes.py
```

**Download specific categories**:

Categories are defined as described in **[1]**. However, 14 classes were not present
in any category, therefore, I added them under the category "custom".

```
python download.py --categories 'arts and crafts' cooking
```

List all categories and classes that belong to them:
```
python list_categories.py
```

**Extract frames from videos**:

```
python videos_to_frames.py --all
```

**Extract sound tracks from videos**:

```
python videos_to_sound.py --all
```

**Create metadata**:

Although it would be ideal to have the whole dataset available, a fraction of videos has been delete from
YouTube since Kinetics was released. Furthermore, not all videos contain a sound track and frame extraction might fail for some videos.
For this reason, it is convenient to generate metadata that keep track of all successfully downloaded videos.

You can generate metadata for videos (.mp4 files), video frames or sound tracks. You will need to generate
metadata for sound tracks if you want to pack them into a tfrecords file (see below).

Generate metadata for videos:

```
python create_meta.py videos --sets 400 --save resources/kinetics_videos
```

Generate metadata for video frames:

```
python create_meta.py frames --sets 400 --save resources/kinetics_video_frames
```

Generate metadata for sound tracks:

```
python create_meta.py sound --sets 400 --save resources/kinetics_sound
```

**Convert sound tracks into a tfrecords file**:

Loading mp3 files in Tensorflow (as of version 1.3.0) creates a severe bottleneck for the training speed.
It is convenient to pack all mp3 files into a single tfrecords file and load the tfrecords file during training.

Example:

```
python sound_to_tfrecords.py train resources/kinetics_sound_400_train.json resources/kinetics_sound_400_classes.json dataset/kinetics_400_train_sound.tfrecords
```

Note:
First, you will need to generate metadata for sound tracks.

#### Download structure

The training and validation videos are downloaded into their individual directories.
Furthermore, a directory is created for each class.

Example:
```
dataset/train/blowing_glass
dataset/valid/blowing_glass
```

Test videos are all downloaded into a single directory because their classes are not known.

Example"
```
dataset/test
```

#### File names and video format

The videos are all download in mp4. If a video isn't available in mp4, it's downloaded in
 the next best format and converted into mp4. All videos are downloaded with sound.

Videos' file names correspond to their YouTube IDs. All spaces in directory names are replaced with
underscores (e.g. blowing glass => blowing_glass).

#### References

[[1] The Kinetics Human Action Video Dataset - W.Kay et al. (2017)](https://arxiv.org/abs/1705.06950)
