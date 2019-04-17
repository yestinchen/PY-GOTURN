# Date: Wednesday 07 June 2017 11:28:11 AM IST
# Email: nrupatunga@whodat.com
# Name: Nrupatunga
# Description: tracker manager

import cv2
import time
from ..helper.BoundingBox import BoundingBox

opencv_version = cv2.__version__.split('.')[0]


class tracker_manager:

    """Docstring for tracker_manager. """

    def __init__(self, videos, regressor, tracker, logger):
        """This is

        :videos: list of video frames and annotations
        :regressor: regressor object
        :tracker: tracker object
        :logger: logger object
        :returns: list of video sub directories
        """

        self.videos = videos
        self.regressor = regressor
        self.tracker = tracker
        self.logger = logger

    def trackAll(self, start_video_num, pause_val):
        """Track the objects in the video
        """

        videos = self.videos
        objRegressor = self.regressor
        objTracker = self.tracker

        video_keys = list(videos.keys())
        count =0
        start=time.time()
        for i in range(start_video_num, len(videos)):
            video_frames = videos[video_keys[i]][0]
            annot_frames = videos[video_keys[i]][1]

            num_frames = min(len(video_frames), len(annot_frames))

            # Get the first frame of this video with the intial ground-truth bounding box
            frame_0 = video_frames[0]
            bbox_0 = annot_frames[0]
            sMatImage = cv2.imread(frame_0)
            objTracker.init(sMatImage, bbox_0, objRegressor)
            for i in range(1, num_frames):
                frame = video_frames[i]
                sMatImage = cv2.imread(frame)
                sMatImageDraw = sMatImage.copy()
                bbox = annot_frames[i]

                if opencv_version == '2':
                    cv2.rectangle(sMatImageDraw, (int(bbox.x1), int(bbox.y1)), (int(bbox.x2), int(bbox.y2)), (255, 255, 255), 2)
                else:
                    sMatImageDraw = cv2.rectangle(sMatImageDraw, (int(bbox.x1), int(bbox.y1)), (int(bbox.x2), int(bbox.y2)), (255, 255, 255), 2)

                bbox = objTracker.track(sMatImage, objRegressor)
                if opencv_version == '2':
                    cv2.rectangle(sMatImageDraw, (int(bbox.x1), int(bbox.y1)), (int(bbox.x2), int(bbox.y2)), (255, 0, 0), 2)
                else:
                    sMatImageDraw = cv2.rectangle(sMatImageDraw, (int(bbox.x1), int(bbox.y1)), (int(bbox.x2), int(bbox.y2)), (255, 0, 0), 2)

                count+=1
                timeUsed = time.time()-start

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(sMatImageDraw,'{:0.2f}fps[#{}]'.format(count/timeUsed, i),(0,50), font, 0.5,(255,255,255),1,cv2.LINE_AA)

                cv2.imshow('Results', sMatImageDraw)
                cv2.waitKey(10)

    def trackDemo(self):
        video = self.videos # a list of images.
        objRegressor = self.regressor
        objTracker = self.tracker

        cv2.namedWindow("Demo", cv2.WND_PROP_FULLSCREEN)
        ims = [cv2.imread(imf) for imf in video]
        initBox = None
        try:
            init_rect = cv2.selectROI('Demo', ims[0], False, False)
            x, y, w, h = init_rect
            initBox = BoundingBox(x, y, w+x, h+y)
        except:
            exit()
        
        count =0
        start=time.time()
        for f, im in enumerate(ims):
            tic = cv2.getTickCount()
            if f == 0:  # init
                # init
                objTracker.init(im, initBox, objRegressor)
            elif f > 0:  # tracking
                sMatImageDraw = im.copy()
                bbox = objTracker.track(im, objRegressor)
                if opencv_version == '2':
                    cv2.rectangle(sMatImageDraw, (int(bbox.x1), int(bbox.y1)), (int(bbox.x2), int(bbox.y2)), (255, 0, 0), 2)
                else:
                    sMatImageDraw = cv2.rectangle(sMatImageDraw, (int(bbox.x1), int(bbox.y1)), (int(bbox.x2), int(bbox.y2)), (255, 0, 0), 2)

                count+=1
                timeUsed = time.time()-start

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(sMatImageDraw,'{:0.2f}fps[#{}]'.format(count/timeUsed, f),(0,50), font, 0.5,(255,255,255),1,cv2.LINE_AA)

                cv2.imshow('Demo', sMatImageDraw)
                key = cv2.waitKey(10)
                if key > 0:
                    break

