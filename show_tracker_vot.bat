@echo OFF
set pwd=%cd%
set DEPLOY_PROTO=./nets/tracker.prototxt		 
set CAFFE_MODEL=./nets/tracker.caffemodel
set TEST_DATA_PATH=../../dataset/VOT2014/

python -m goturn.test.show_tracker_vot ^
	--p %DEPLOY_PROTO% ^
	--m %CAFFE_MODEL% ^
	--i %TEST_DATA_PATH% ^
	--g -1
