The dataset is composed of three splits with corresponding CSV / JSON files:

Training set (14.1 MB zip file)
Validation set (1.1 MB zip file)
Test set (1.7 MB zip file, with annotations held out for the purpose of the
  ActivityNet challenge. Once the challenge is over, we plan to release the
  annotations.)

In the CSV files, each row describes one video and the columns are organized as
follows:

label - (string) a human-readable name for the action class. Characters used
  are lowercase letters, spaces, and single quotation ('). (Held out for the
  test set.)
youtube_id - (string) the YouTube identifier of the video the segment was
  extracted from. One may view the selected video at
  http://youtu.be/${youtube_id}.
time_start - (integer) the starting time of the action snippet in the video, in
  seconds.
time_end - (integer) the ending time of the action snippet in the video, in
  seconds. 
split - (string) "train", "val", or "test".

The JSON files contain the same data as the CSV files, but formatted
differently. Check the ActivityNet website for details at:
http://activity-net.org/.

The validation and test sets each contain a maximum of 50 and 100 videos per
class, respectively. However some classes may have less than the maximum, and
over time YouTube videos may be deleted or taken down from public viewing by
the uploading user. For the ActivityNet challenge, scoring will consider only
those videos available after the submission deadline.

In some cases the video may end before time_end, but we always provide a
10-second window from time_start to time_end, so as much of the clip should be
used as possible.
