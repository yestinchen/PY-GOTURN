from __future__ import print_function

import os
import glob
from .video import video

class loader_single:
  def __init__(self, folder, logger):
    self.logger = logger
    self.folder = folder
    self.videos = []
    if not os.path.isdir(folder):
      logger.error('{} is not a valid directory'.format(folder))

  def get_video(self):
    logger = self.logger
    folder = self.folder
    video_path = glob.glob(os.path.join(folder, '*.jpg'))
    objVid = video(video_path)
    list_of_frames = sorted(video_path)
    if not list_of_frames:
        logger.error('image folders should contain only .jpg images')

    self.videos = list_of_frames
    return self.videos