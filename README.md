## Download DeepMind's Kinetics

Download all videos from DeepMind's [Kinetics dataset](https://deepmind.com/research/open-source/open-source-datasets/kinetics/).

Work in progress ...

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

**Download specific classes (labels)**:
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

#### Download structure

The training, validation and test videos are downloaded into their individual directories.
Furthermore, a directory is created for each class.

Example:
```
dataset/train/blowing_glass
dataset/valid/blowing_glass
```

#### File names and video format

The videos are all download in mp4. If a video isn't available in mp3, it's downloaded in
 the next best format and converted into mp4. All videos are downloaded with sound.
 
Videos' file names correspond to their YouTube IDs. All spaces in directory names are replaced with
underscores (e.g. blowing glass => blowing_glass).

#### TODO

* download test set
* make sure videos that are not download in the mp4 format are correctly converted
* enable video format selection

#### References

[[1] The Kinetics Human Action Video Dataset - W.Kay et al. (2017)](https://arxiv.org/abs/1705.06950)