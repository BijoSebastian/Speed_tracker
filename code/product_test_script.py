from picamera2 import Picamera2, Preview
from kld7 import KLD7
from kld7 import RadarParamProxy
import time
import os
from datetime import datetime
import uuid

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email.mime.image import MIMEImage
import os
from email import encoders 

picam2 = Picamera2()

camera_config = picam2.create_still_configuration(main = {"size":(4624,3472)})
picam2.configure(camera_config)

picam2.start()
picam2.set_controls({"LensPosition": 5})
time.sleep(4)

count = 0
now = datetime.now()


detectionCount=1
with KLD7("/dev/serial0") as radar:
	radar.set_param('RSPI', 2)
	radar.set_param('RRAI', 3)
	radar.set_param('MISP', 0)
	radar.set_param('SPTH', 100)

	print(radar._param_dict['RSPI'])
	vel_ls = []
	readings_ls = []
	past = time.time()
	while True:
		now = time.time()
		if now-past >=1.0:
			past = now
			print("1second has elapsed")
		print(vel_ls)
		target_info = next(radar.stream_TDAT())
		if target_info == None:
			vel_ls.clear()
			readings_ls.clear()
			
		if target_info != None:
			if len(vel_ls) <3:
				vel_ls.append(target_info.speed)
				readings_ls.append(target_info)
			else:
				vel_ls.pop(0)
				readings_ls.pop(0)
				vel_ls.append(target_info.speed)
				readings_ls.append(target_info)
				
			if abs(sum(vel_ls))/3.0 >=40:
				foldername = str(uuid.uuid4())
				os.mkdir(foldername)
				file1 = open(foldername +"/Myfile.txt","w")
				for i in range(len(vel_ls)):
					file1.write("Detection number: " + str(detectionCount) + "\n")
					file1.write("distance: " + str(readings_ls[i].distance) + 
					"      speed: " + str(readings_ls[i].speed) +
					"          angle: " + str(readings_ls[i].angle) + 
					"           magnitude:  " + str(target_info.magnitude) + "\n")
				picam2.capture_file(foldername + "/capture" + str(detectionCount) + ".jpg")
				vel_ls.clear()
				readings_ls.clear()
				file1.close()
				
				fromaddr = "veladmi070224@gmail.com"
				toaddr = fromaddr
				msg = MIMEMultipart() 

				# storing the senders email address 
				msg['From'] = fromaddr 

				# storing the receivers email address 
				msg['To'] = toaddr 

				# storing the subject 
				msg['Subject'] = "testing smtp with attachments"

				# string to store the body of the mail 
				body = "hello, speed limit violations detected"

				# attach the body with the msg instance 
				msg.attach(MIMEText(body, 'plain')) 

				# open the file to be sent 
				filename = "speed_detections.txt"
				attachment = open(os.path.join(os.getcwd(),foldername+"/Myfile.txt"),"rb") 
				p = MIMEBase('application', 'octet-stream') 

				# To change the payload into encoded form 
				p.set_payload((attachment).read()) 

				# encode into base64 
				encoders.encode_base64(p) 

				p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

				# attach the instance 'p' to instance 'msg' 
				msg.attach(p) 
				ImgFileName = os.path.join(os.getcwd(),foldername+"/capture1.jpg")
				with open(ImgFileName, 'rb') as f:
						img_data = f.read()
				image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
				msg.attach(image)
				# creates SMTP session 
				s = smtplib.SMTP('smtp.gmail.com', 587) 

				# start TLS for security 
				s.starttls() 

				# Authentication 
				s.login(fromaddr, "qbuk jgsb brsp ahjm") 

				# Converts the Multipart msg into a string 
				text = msg.as_string() 

				# sending the mail 
				s.sendmail(fromaddr, toaddr, text) 

				# terminating the session 
				s.quit() 
