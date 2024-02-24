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

camera_config = picam2.create_still_configuration(main = {"size":(1280,720)})
picam2.configure(camera_config)

picam2.start()
picam2.set_controls({"LensPosition": 5.7})
time.sleep(4)

count = 0


def mail_admin(cwd,foldername):
	
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
	attachment = open(os.path.join(cwd,foldername+"/Myfile.txt"),"rb") 
	p = MIMEBase('application', 'octet-stream') 

	# To change the payload into encoded form 
	p.set_payload((attachment).read()) 

	# encode into base64 
	encoders.encode_base64(p) 

	p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

	# attach the instance 'p' to instance 'msg' 
	msg.attach(p) 
	ImgFileName = os.path.join(cwd,foldername+"/capture1.jpg")
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


detectionCount=1
with KLD7("/dev/serial0") as radar:
	radar.set_param('RSPI', 2)
	radar.set_param('RRAI', 3)
	radar.set_param('MISP', 0)
	radar.set_param('SPTH', 100)

	vel_ls = []
	readings_ls = []

	while True:
		
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
			
			
			#saving latest data from the radar and the latest image from the camera
			if abs(sum(vel_ls))/3.0 >=40:
				now = datetime.now()
				
				foldername = now.strftime("%H%M%S")
				os.mkdir(foldername)
				file1 = open(foldername +"/Myfile.txt","w")
				for i in range(len(vel_ls)):
					file1.write("Detection number: " + str(i) + "\n")
					file1.write("distance: " + str(readings_ls[i].distance) + 
					"      speed: " + str(readings_ls[i].speed) +
					"          angle: " + str(readings_ls[i].angle) + 
					"           magnitude:  " + str(target_info.magnitude) + "\n")
				picam2.capture_file(foldername + "/capture1" + ".jpg")
				vel_ls.clear()
				readings_ls.clear()
				file1.close()	
				cwd = os.getcwd()
				mail_admin(cwd,foldername)

