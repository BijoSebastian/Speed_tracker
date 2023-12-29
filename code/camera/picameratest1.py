from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from libcamera import controls

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
#camera_config = picam2.create_still_configuration(main = {"size":(4624,3472), "format":("YUV420")})
camera_config = picam2.create_still_configuration(main = {"size":(4624,3472)})

picam2.configure(camera_config)
print(picam2.sensor_resolution)
#picam2.configure(camera_config)
picam2.start()
#picam2.switch_mode_and_capture_file(camera_config, "test_full.jpg")


ctrls =Controls(picam2)
ctrls.AnalogueGain = 2.71
ctrls.ExposureTime = 29999
#ctrls.DigitalGain = 1.0
#picam2.set_controls(ctrls) 
#picam2.set_controls({"AwbEnable": 0, "AeEnable": 0})
#picam2.set_controls({"AfMode": 2 ,"AfTrigger": 0})
#print(picam2.get_libcamera_controls)

#encoder = H264Encoder(10000000)
#output = FfmpegOutput('test.mp4', audio=True)

#picam2.start_recording(encoder, output)

#picam2.set_controls({"LensPosition": 5})
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
job = picam2.autofocus_cycle(wait=False)

#success = picam2.wait(job)



time.sleep(4)

print(picam2.capture_metadata())
picam2.capture_file("test.jpg")
