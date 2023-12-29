from picamera2 import Picamera2, Preview
import time
picam2 = Picamera2()
#camera_config = picam2.create_preview_configuration()
#picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
#time.sleep(1)
#picam2.set_controls({"AfMode": 0, "LensPosition": 425})
#picam2.set_controls({"AfMode": 1 ,"AfTrigger": 0})
#camera_config = picam2.create_still_configuration(main={"size": (1920,1080)}, lores={"size": (640, 480)}, display="lores")
#picam2.create_still_configuration({"size":(4056, 3040)})

#camera_config = picam2.create_preview_configuration(raw={})
preview_config = picam2.create_preview_configuration(main = {"size":(4056, 3040)})
#preview_config = picam2.create_preview_configuration(main={"size": (1920,1080)})
camera_config = picam2.create_still_configuration(main = {"size":(4624,3472), "format"})

picam2.configure(camera_config)
print(picam2.sensor_resolution)
#picam2.configure(camera_config)
picam2.start()
#picam2.switch_mode_and_capture_file(camera_config, "test_full.jpg")
print(picam2.capture_metadata())

picam2.set_controls({"AwbEnable": 0, "AeEnable": 0})
#picam2.set_controls({"AfMode": 2 ,"AfTrigger": 0})
#print(picam2.get_libcamera_controls)
print(picam2.create_preview_configuration.sensor)
picam2.capture_file("test.jpg")
