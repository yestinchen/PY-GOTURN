# Date: Friday 02 June 2017 05:50:20 PM IST
# Email: nrupatunga@whodat.com
# Name: Nrupatunga
# Description: Test file for showing the tracker output

import argparse
import setproctitle
from ..logger.logger import setup_logger
from ..network.regressor import regressor
from ..loader.loader_single import loader_single
from ..tracker.tracker import tracker
from ..tracker.tracker_manager import tracker_manager

setproctitle.setproctitle('SHOW_TRACKER_VOT')
logger = setup_logger(logfile=None)

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="Path to the prototxt")
ap.add_argument("-m", "--model", required=True, help="Path to the model")
ap.add_argument("-v", "--input", required=True, help="Path to the vot directory")
ap.add_argument("-g", "--gpuID", required=False, default=-1, help="gpu to use, omit to use cpu only")
args = vars(ap.parse_args())
gpuId = args['gpuID'] if int(args['gpuID']) >= 0 else -1

do_train = False
objRegressor = regressor(args['prototxt'], args['model'], gpuId, 1, do_train, logger)
objTracker = tracker(False, logger)  # Currently no idea why this class is needed, eventually we shall figure it out
objLoaderVot = loader_single(args['input'], logger)
videos = objLoaderVot.get_video()
objTrackerVis = tracker_manager(videos, objRegressor, objTracker, logger)
objTrackerVis.trackDemo()
