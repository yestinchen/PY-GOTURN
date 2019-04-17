@echo OFF
set pwd=%cd%
set DEPLOY_PROTO=./nets/tracker.prototxt		 
set CAFFE_MODEL=./nets/tracker.caffemodel
REM set TEST_DATA_PATH=../../dataset/VOT2014/car/
set TEST_DATA_PATH=../../dataset/tennis/

python -m goturn.test.track_demo ^
	--p %DEPLOY_PROTO% ^
	--m %CAFFE_MODEL% ^
	--i %TEST_DATA_PATH% ^
	--g -1
