import cv2 
import numpy as np
import copy
import math

# read position and gyro
# https://stackoverflow.com/questions/22881878/how-can-i-draw-half-circle-in-opencv
# https://stackoverflow.com/questions/31281235/anomaly-with-ellipse-fitting-when-using-cv2-ellipse-with-different-parameters

class draw_blank_radar():
	def __init__(self):
		self.height = 480
		self.width = 720
		self.blank_image = np.zeros((self.height,self.width,3), np.uint8)
		self.blank_image += 220
		self.line_thickness = 3

		self.images = []

		# read_txt
		self.listAngleIndex = []
		self.detectAngles = []
		pathAngle = './/ang.txt'
		with open(pathAngle, 'r') as f:
			content_list = f.read().splitlines()

			for angleIndex in range(len(content_list)):
				self.listAngleIndex.append(int(content_list[angleIndex]))
			self.angleBinNum = 128
			for  angleIndex in range(0, len(self.listAngleIndex)):
				self.theta_ =  2 * (self.listAngleIndex[angleIndex] - self.angleBinNum//2)/self.angleBinNum
				if self.theta_ > 0:
					self.theta_ -= 1
				else:
					self.theta_ += 1
				self.detectedAngle = self.theta_ * angular_ratio
				self.detectedAngle = int(self.detectedAngle)
				self.detectAngles.append(self.detectedAngle)



		
	def draw_line(self, x1, y1, x2, y2):
		cv2.line(self.blank_image, (x1, y1), (x2, y2), (100, 100, 100), thickness = self.line_thickness)
	
	def draw_line_t_r(self, x1, y1, x2, y2):
		cv2.line(self.blank_image, (x1, y1), (x2, y2), (0, 69, 255), thickness = 5)
	
	def draw_line_t_b(self, x1, y1, x2, y2):
		cv2.line(self.blank_image, (x1, y1), (x2, y2), (225, 105, 65), thickness = 5)
	
	def draw_line_l_r(self, x1, y1, x2, y2):
		cv2.line(self.blank_image, (x1, y1), (x2, y2), (0, 69, 255), thickness = 1)
	
	def draw_line_l_b(self, x1, y1, x2, y2):
		cv2.line(self.blank_image, (x1, y1), (x2, y2), (225, 105, 65), thickness = 1)

	def draw_half_circle_rounded(self):
		center_coordinates = (360, 400)
		axesLength = (250, 250)
		angle = 0
		startAngle = 180
		endAngle = 360
		color = (100, 100, 100)
		thickness = 5

		self.blank_image = cv2.ellipse(self.blank_image, center_coordinates, axesLength,
		           angle, startAngle, endAngle, color, thickness)

	def show_image(self):
		cv2.imshow('h',self.blank_image)
		cv2.waitKey(0) # waits until a key is pressed
		cv2.destroyAllWindows() # destroys the window showing image

	def copy_blank(self):
		self.copyBlank = copy.copy(self.blank_image)

	def return_image(self):
		return self.blank_image
		
	def returnAngle(self):
		return self.detectAngles

	def draw_line_r(self, x1, y1, x2, y2):
		cv2.line(self.blank_image, (x1, y1), (x2, y2), (0, 69, 255), thickness = 3)
	
	def draw_line_b(self, x1, y1, x2, y2):
		cv2.line(self.blank_image, (x1, y1), (x2, y2), (225, 105, 65), thickness = 3)

	def refresh(self):
		self.blank_image = []
		self.blank_image = self.copyBlank
	def outputimages(self):
		return self.images

	def writeVideo(self):
		for angleIndex in range(0,230):
			print(len(self.images))
			self.out.write(self.images[angleIndex])
		self.out.release()
		cv2.destroyAllWindows()


# size setting

height = 480
width = 720

# angle setting

set_angle_g0 = 55
set_angle_g1 = 55 + 35 * 2
half_fov = 55
g0_start_angle = set_angle_g0 - half_fov
g0_end_angle = set_angle_g0 + half_fov
g1_start_angle = set_angle_g1 - half_fov
g1_end_angle = set_angle_g1 + half_fov
angular_ratio = 180 / math.pi

blank_back = draw_blank_radar()
detected_Angle = blank_back.returnAngle()



# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 3.0
out = cv2.VideoWriter('output.avi',fourcc, fps, (width, height))

# drawing

for angleIndex in range(0,230):
	print(angleIndex)

	blank_back = draw_blank_radar()
	blank_back.draw_line(0, 400, width, 400)
	blank_back.draw_half_circle_rounded()
	blank_back.draw_line(width//2, 0, width//2, height)
	blank_back.draw_line_t_r(width//2, 400, width//2 + int(300*math.cos(set_angle_g0/angular_ratio)), 400 - int(300*math.sin(set_angle_g0/angular_ratio)))
	blank_back.draw_line_t_b(width//2, 400, width//2 + int(300*math.cos(set_angle_g1/angular_ratio)), 400 - int(300*math.sin(set_angle_g1/angular_ratio)))
	blank_back.draw_line_l_r(width//2, 400, width//2 + int(300*math.cos(g0_start_angle/angular_ratio)), 400 - int(300*math.sin(g0_start_angle/angular_ratio)))
	blank_back.draw_line_l_r(width//2, 400, width//2 + int(300*math.cos(g0_end_angle/angular_ratio)), 400 - int(300*math.sin(g0_end_angle/angular_ratio)))
	blank_back.draw_line_l_b(width//2, 400, width//2 + int(300*math.cos(g1_start_angle/angular_ratio)), 400 - int(300*math.sin(g1_start_angle/angular_ratio)))
	blank_back.draw_line_l_b(width//2, 400, width//2 + int(300*math.cos(g1_end_angle/angular_ratio)), 400 - int(300*math.sin(g1_end_angle/angular_ratio)))

	currentAngle = detected_Angle[angleIndex] + 90
	blank_back.draw_line_b(width//2, 400, width//2 + int(300*math.cos(currentAngle/angular_ratio)), 400 - int(300*math.sin(currentAngle/angular_ratio)))
	blank0 = blank_back.return_image()
	out.write(blank0)

out.release()
cv2.destroyAllWindows()

