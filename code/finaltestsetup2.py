from picamera2 import Picamera2, Preview
from kld7 import KLD7
from kld7 import RadarParamProxy
import time
import os
from datetime import datetime

picam2 = Picamera2()

camera_config = picam2.create_still_configuration(main = {"size":(4624,3472)})
picam2.configure(camera_config)

picam2.start()
picam2.set_controls({"LensPosition": 5})
time.sleep(4)

count = 0
now = datetime.now()
foldername = now.strftime("%H%M%S")
os.mkdir(foldername)

with KLD7("/dev/serial0") as radar:
	radar.set_param('RSPI', 2)
	radar.set_param('RRAI', 3)
	radar.set_param('MISP', 0)
	radar.set_param('SPTH', 100)

	print(radar._param_dict['RSPI'])

	file1 = open(foldername +"/Myfile.txt","w")
	while True:
		tmpvar = 1
		detectionCount = 0
		count = 0

		user_input = input("Enter SPACE to print 'hello' or 0 to exit: ")
		if user_input == ' ':
			print("Received space input")
			while count <= 3:
				target_info = next(radar.stream_TDAT())
				#print("came till here")
				if target_info != None:
					print("Detection number: " + str(detectionCount))
					detectionCount += 1
					file1.write("Detection number: " + str(detectionCount) + "\n")
					print(target_info)
					file1.write("distance: " + str(target_info.distance) + "      speed: " + str(target_info.speed) + "          angle: " + str(target_info.angle) + "           magnitude:  " + str(target_info.magnitude) + "\n")
					picam2.capture_file(foldername + "/capture" + str(detectionCount) + ".jpg")
					count += 1
		elif user_input == '0':
			file1.close()
			print("Exiting program.")
			break
		else:
			print("Invalid input. Please enter 1 to print 'hello' or 0 to exit.")

