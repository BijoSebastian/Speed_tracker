from picamera2 import Picamera2, Preview
from kld7 import KLD7
from kld7 import RadarParamProxy
import time

picam2 = Picamera2()

camera_config = picam2.create_still_configuration(main = {"size":(4624,3472)})
picam2.configure(camera_config)

picam2.start()
picam2.set_controls({"LensPosition": 5})
time.sleep(4)

count = 0

with KLD7("/dev/serial0") as radar:
	file1 = open("MyFile1.txt","w")
	while True:
		tmpvar = 1
		detectionCount = 0

		user_input = input("Enter SPACE to print 'hello' or 0 to exit: ")
		if user_input == ' ':
			print("Received space input")
			for i in range(5):
				target_info = next(radar.stream_TDAT())
				if target_info != None:
					print("Detection number: " + str(detectionCount))
					detectionCount += 1
					file1.write("Detection number: " + str(detectionCount) + "\n")
					print(target_info.distance)
					file1.write("distance: " + str(target_info.distance) + "      speed: " + str(target_info.speed) + "          angle: " + str(target_info.angle) + "           magnitude:  " + str(target_info.magnitude) + "\n")
					picam2.capture_file("capture" + str(detectionCount) + ".jpg")
		elif user_input == '0':
			file1.close()
			print("Exiting program.")
			break
		else:
			print("Invalid input. Please enter 1 to print 'hello' or 0 to exit.")

