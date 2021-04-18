# encoding: utf-8

"""
This module can only be used to read CELEBA dataset

Author: Jie Lyu
E-mail: jiejielyu@outlook.com
Date: 2017.12.01
"""

import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
# from scipy import misc
import skimage.io

def readSubsetPartition(path):
	"""
	Function: Read indexes to part subsets: trainset, valset, testset
	Input:
		path,
	Date: 2017.12.01
	"""
	if not os.path.isfile(path):
		raise ValueError('error: not exist file: ' + path)
	with open(path) as fid:
		imgNameList = []
		indexList = []
		for line in fid:
			line = line.strip()
			tmp = line.split()
			if len(tmp) != 2:
				raise ValueError('error: not partition file: ' + path)
			imgNameList.append(tmp[0])
			indexList.append(int(tmp[1]))
	# Return
	# print(len(imgNameList))
	return imgNameList, indexList
	
def readAttr(path):
	"""
	Function: Read attribution labels, 40 binary categories
	Input:
		path,
	Date: 2017.12.01
	"""
	if not os.path.isfile(path):
		raise ValueError('error: not exist file: ' + path)
	with open(path) as fid:
		imgNameList = []
		attrList = []
		cnt = 0
		for line in fid:
			cnt += 1
			if cnt <= 2:
				continue
			line = line.strip()
			tmp = line.split()
			if len(tmp) != 41:
				print('parse string: {0}'.format(tmp))
				raise ValueError('not attrition file: ' + path)
			imgNameList.append(tmp[0])
			attrList.append(tmp[1:])
	# Return
	# print(len(attrList))
	# print(type(attrList[0]))
	return imgNameList, attrList
	
def readLandmark(path):
	"""
	Function: Read landmark points, 5 key-points [x, y], \
			  2 eyes center, nose, and mouth corner
	Input:
		path,
	Date: 2017.12.01
	"""
	if not os.path.isfile(path):
		raise ValueError('error: not exist file: ' + path)
	with open(path) as fid:
		imgNameList = []
		landmarkList = []
		cnt = 0
		for line in fid:
			cnt += 1
			if cnt <= 2:
				continue
			tmp = line.split()
			if len(tmp) != 11:
				print('parse string: {0}'.format(tmp))
				raise ValueError('not landmark file: ' + path)
			imgNameList.append(tmp[0])
			landmarkList.append(tmp[1:])
	
	# Return
	# print(len(landmarkList))
	# print(len(landmarkList[0]))
	return imgNameList, landmarkList
	
def readBbox(path):
	"""
	Function: Read bbox of face, [x, y, w, h]
	Input:
		path,
	Date: 2017.12.01
	"""
	if not os.path.isfile(path):
		raise ValueError('error: not exist file: ' + path)
	with open(path) as fid:
		imgNameList = []
		bboxList = []
		cnt = 0
		for line in fid:
			cnt += 1
			if cnt <= 2:
					continue
			tmp = line.split()
			if len(tmp) != 5:
				print('parse string: {0}'.format(tmp))
				raise ValueError('not bbox file: ' + path)
			imgNameList.append(tmp[0])
			bboxList.append(tmp[1:])
	# Return
	# print(len(bboxList))
	# print(len(bboxList[0]))
	return imgNameList, bboxList
	
def dispSample(img, attr, lpts, bboxes=None):
	plt.clf()
	h, w, ch = img.shape
	# Draw image
	plt.imshow(img)
	# Draw attributions
	numAttr = attr.shape[0]
	step = h/218*15
	for j in range(numAttr):
		if attr[j] > 0:
			plt.text(step*(j%4), step*(j//4+1), 
					 s=str(attr[j])+',', color='red')
		else:
			plt.text(step*(j%4), step*(j//4+1), 
					 s=str(attr[j])+',', color='green')
	# Draw key points
	numPts = lpts.shape[0]
	for j in range(numPts):
		plt.plot(lpts[j, 0], lpts[j, 1], 'ro', color='red')
		plt.text(lpts[j, 0], lpts[j, 1], s=str(j), color='red')
		
	# draw bboxes	
	if bboxes is not None:
		if len(bboxes.shape) == 1:
			bboxes = np.expand_dims(bboxes, axis=0)
		numBboxes = bboxes.shape[0]
		for i in range(numBboxes):
			b = bboxes[i]
			b[2] += b[0]
			b[3] += b[1]
			plt.plot([b[0], b[2], b[2], b[0], b[0]], 
					 [b[1], b[1], b[3], b[3], b[1]], '-b')
	
	
def dispSamples(imgs, attrs, landmarks):
	"""
	Function: Display a group of samples
	Input:
		imgs, 4d, [n, h, w. channel] 
		attrs, 2d, [n, 40]
		landmarks, 3d, [n, 5, 2]
	Date: 2017.12.01
	"""
	numImgs = imgs.shape[0]
	for i in range(numImgs):
		img = imgs[i]
		attr = attrs[i]
		lpts = landmarks[i]
		dispSample(img, attr, lpts)
		plt.show()

		
class Dataset(object):

	def __init__(self, isRandomBatch=False, batchSize=64, isOri=False):
		self.isRandomBatch = isRandomBatch  # set random batch
		self.isOri = isOri                  # set original flag
		self.imgSize = [218, 178, 3]
		# Buffer of subset
		self.imgPathList = []               # buffer for img paths
		self.attrList = []                  # attr for imgs
		self.landmarkList = []              # landmarks for imgs
		self.bboxList = None                # bbox for original imgs
		
		# Counter
		self.batchSize = batchSize  # size of a batch
		self.batchCount = 0         # batch counter
		self.epochCount = 0         # epoch counter
		self.randomIndex = 0        # random indexes of all samples
		
	def setSubsetBuffers(self, imgPathList, attrList, landmarkList, bboxList):
		"""
		Function: Set subset buffers: img path, attributions, landmarks, bbox
		Input:
			imgPathList, 
			attrList, 
			landmarkList, 
			bboxList
		Date: 2017.12.01
		"""
		numImgs = len(imgPathList)
		numAttrs = len(attrList)
		numLandmarks = len(landmarkList)
		# Check number of samples
		if numImgs == numAttrs and numAttrs == numLandmarks:
			if bboxList is not None and len(bboxList) != numImgs:
				raise ValueError('error: length of bboxes disagrees \
				with imgs, img={0}, bbox={1}'.format(numImgs, len(bboxList)))
			else:
				self.imgPathList = imgPathList
				self.attrList = attrList
				self.landmarkList = landmarkList
				self.bboxList = bboxList
		else:
			raise ValueError('error: lengths disagree: img={0}, \
			attr={1}, landmark={2}'.format(numImgs, numAttrs, numLandmarks))
	
	def getNextBatchIndexes(self):
		if self.isOri:
			raise ValueError(
				'error: cannot create a batch from original images')
			
		if self.batchSize < 1:
			raise ValueError('Batch size is less than one')

		# Set batch size
		num = self.getSampleNum()
		if num < self.batchSize:
			raise ValueError('Batch size is more than samples')

		# Create random index
		if self.batchCount == 0:
			if self.isRandomBatch:
				self.randomIndex = \
					np.random.randint(0, num, num, dtype=np.int32)
			else:
				self.randomIndex = \
					np.arange(0, num, dtype=np.int32)

		# Compute start and end index
		startIndex = self.batchCount * self.batchSize
		endIndex = (self.batchCount + 1) * self.batchSize
		if endIndex > num:
			endIndex = num
			startIndex = num - self.batchSize
			self.batchCount = 0
			self.epochCount += 1
		else:
			self.batchCount += 1
		# Return    
		return startIndex, endIndex
	
	def getNextBatch(self):
		# Get head and tail indexes of the current batch
		startIndex, endIndex = self.getNextBatchIndexes()
		print('startIndex={0}, endIndex={1}'.format(startIndex, endIndex))
		
		# Allocate memories for the batch
		shape = [self.batchSize, self.imgSize[0], 
				 self.imgSize[1], self.imgSize[2]]
		imgs = np.zeros(shape=shape, dtype=np.uint8)
		shape = [self.batchSize, self.attrList.shape[1]]
		attrs = np.zeros(shape=shape, dtype=np.int32)
		shape = [self.batchSize, self.landmarkList.shape[1]//2, 2]
		landmarks = np.zeros(shape=shape, dtype=np.float32)
		# Read images and arrange samples
		cnt = 0
		for i in self.randomIndex[startIndex:endIndex]:
			cnt += 1
			img_path = self.imgPathList[i]
			timg = skimage.io.imread(img_path)
			# Convert gray image into 3 channels
			if len(timg.shape) < 3:
				timg = np.expand_dims(timg, axis=-1)
			if timg.shape[2] == 1:
				timg = np.tile(timg, [1, 1, 3])
			# Transfer to buffer
			imgs[cnt-1] = timg
			attrs[cnt-1] = self.attrList[i]
			lpts = self.landmarkList[i]
			lpts = np.reshape(lpts, newshape=[lpts.shape[0]//2, 2])
			landmarks[cnt-1] = lpts
		# Return
		return imgs, attrs, landmarks
		
	def show(self, maxNum=-1, saveDir=None):
		numSam = self.getSampleNum()
		if maxNum==-1 or maxNum>numSam:
			maxNum = maxSam
		for i in range(maxNum):
			img_path = self.imgPathList[i]
			img = skimage.io.imread(img_path)
			# Convert gray image into 3 channels
			if len(img.shape) < 3:
				img = np.expand_dims(img, axis=-1)
			if img.shape[2] == 1:
				img = np.tile(img, [1, 1, 3])
			# Get attr and lpts
			attr = self.attrList[i]
			lpts = self.landmarkList[i]
			lpts = np.reshape(lpts, newshape=[lpts.shape[0]//2, 2])
			if self.bboxList is not None:
				bbox = self.bboxList[i]
			else:
				bbox = None
			# Draw and show
			dispSample(img, attr, lpts, bbox)
			if saveDir is None:
				plt.show()
			else:
				if not os.path.isdir(saveDir):
					os.makedirs(saveDir)
				tmp = img_path.split('/')
				name, ext = tmp[-1].split('.')
				# save_name = '%0*d.png'%(6, i)
				save_name = name + '.png'
				save_path = os.path.join(saveDir, save_name)
				print('I[{0}]:saving sample to '.format(i+1) + save_path)
				plt.savefig(save_path, format='png', \
							dpi=64, bbox_inches='tight')
			
	def getSampleNum(self):
		return len(self.imgPathList)
		
			
class CELEBADataset(object):
	
	def __init__(self,
				 dataHomeDir='.',
				 dataType='origin_jpg',   # origin_jpg, align_jpg, align_png
				 batchSize=64,
				 isRandomBatch=True):
		if not os.path.isdir(dataHomeDir):
			raise ValueError('error: not exist dir: ' + dataHomeDir)
		self.dataHomeDir = dataHomeDir
		self.batchSize = batchSize
		self.isRandomBatch = isRandomBatch
		# Set path
		# path of subset partition
		self.subsetPartPath = os.path.join(
			dataHomeDir, 'Eval/list_eval_partition.txt')
		# path of attributions
		self.attrPath = os.path.join(dataHomeDir,
									 'Anno/list_attr_celeba.txt')
		# path of bbox and landmark
		self.bboxPath = None
		self.landmarkPath = os.path.join(
			dataHomeDir, 'Anno/list_landmarks_align_celeba.txt')
		# dir of images
		self.imgExt = 'jpg'
		self.isOri = False
		if dataType == 'origin_jpg':
			# dir of origin images
			self.imgRelDir = 'Img/img_celeba'   
			self.landmarkPath = os.path.join(dataHomeDir,
										 'Anno/list_landmarks_celeba.txt')
			self.bboxPath = os.path.join(dataHomeDir,
										 'Anno/list_bbox_celeba.txt')
			self.isOri = True
		elif dataType == 'align_jpg':
			# dir of aligned images with jpg
			self.imgRelDir = 'Img/img_align_celeba' 
		else:
			# dir of aligned images with png
			self.imgExt = 'png'
			self.imgRelDir = 'Img/img_align_celeba_png'
		self.imgDir = os.path.join(dataHomeDir, 
									self.imgRelDir)
									
		self.trainset = Dataset(isRandomBatch=isRandomBatch, 
								batchSize=batchSize,
								isOri=self.isOri)
		self.valset = Dataset(isRandomBatch=False, 
							  batchSize=batchSize,
								isOri=self.isOri)
		self.testset = Dataset(isRandomBatch=False, 
							   batchSize=batchSize,
								isOri=self.isOri)
		
	def readDataset(self):
		"""
		Function: Read img paths and annotations
		Input:
			
		Date: 2017.12.01
		"""
		start = time.clock()
		# Read data from files
		imgNameList, indexList = readSubsetPartition(self.subsetPartPath)
		_, attrList = readAttr(self.attrPath)
		_, landmarkList = readLandmark(self.landmarkPath)
		if self.bboxPath is not None:
			_, bboxList = readBbox(self.bboxPath)
		else:
			bboxList = None
			
		# Parse subset indexes
		trainIndexList = []
		valIndexList = []
		testIndexList = []
		numImgs = len(imgNameList)
		imgPathList = []
		for i in range(numImgs):
			name, ext = imgNameList[i].split('.')
			tmp = os.path.join(self.imgDir, name + '.' + self.imgExt)
			tmp = tmp.replace('\\', '/')
			imgPathList.append(tmp)
			if indexList[i] == 0:
				trainIndexList.append(i)
			elif indexList[i] == 1:
				valIndexList.append(i)
			elif indexList[i] == 2:
				testIndexList.append(i)
			else:
				raise ValueError('error: not celeba dataset, \
								  more than 3 subsets')
		
		# Convert to np.ndarray, and set subset buffers
		imgPathList = np.array(imgPathList)
		attrList = np.array(attrList, dtype=np.int32)
		landmarkList = np.array(landmarkList, dtype=np.float32)
		trainIndexList = np.array(trainIndexList, dtype=np.int32)
		valIndexList = np.array(valIndexList, dtype=np.int32)
		testIndexList = np.array(testIndexList, dtype=np.int32)
		if bboxList is None:
			self.trainset.setSubsetBuffers(
				imgPathList=imgPathList[trainIndexList], 
				attrList=attrList[trainIndexList[:]], 
				landmarkList=landmarkList[trainIndexList], 
				bboxList=None)
			self.valset.setSubsetBuffers(
				imgPathList=imgPathList[valIndexList], 
				attrList=attrList[valIndexList], 
				landmarkList=landmarkList[valIndexList], 
				bboxList=None)
			self.testset.setSubsetBuffers(
				imgPathList=imgPathList[testIndexList], 
				attrList=attrList[testIndexList], 
				landmarkList=landmarkList[testIndexList], 
				bboxList=None)
		else:
			bboxList = np.array(bboxList, dtype=np.float32)
			self.trainset.setSubsetBuffers(
				imgPathList=imgPathList[trainIndexList], 
				attrList=attrList[trainIndexList], 
				landmarkList=landmarkList[trainIndexList], 
				bboxList=bboxList[trainIndexList])
			self.valset.setSubsetBuffers(
				imgPathList=imgPathList[valIndexList], 
				attrList=attrList[valIndexList], 
				landmarkList=landmarkList[valIndexList], 
				bboxList=bboxList[valIndexList])
			self.testset.setSubsetBuffers(
				imgPathList=imgPathList[testIndexList], 
				attrList=attrList[testIndexList], 
				landmarkList=landmarkList[testIndexList], 
				bboxList=bboxList[testIndexList])
		print('number of samples on trainset: {0}'.\
			format(self.trainset.getSampleNum()))
		print('number of samples on valset: {0}'.\
			format(self.valset.getSampleNum()))
		print('number of samples on testset: {0}'.\
			format(self.testset.getSampleNum()))
		
		end = time.clock()
		print('Read CELEBA-dataset completely, cost time %3.2f seconds' \
			  % (end - start))
		
def main():
	print(sys.argv)
	# path = 'J:\\Dataset\\celebA-dataset\\Eval\\list_eval_partition.txt'
	# readSubsetPartition(path)
	
	# path = 'J:\\Dataset\\celebA-dataset\\Anno\\list_attr_celeba.txt'
	# readAttr(path)
	
	# path = 'J:\\Dataset\\celebA-dataset\\Anno\\list_landmarks_celeba.txt'
	# readLandmark(path)
	
	# path = 'J:\\Dataset\\celebA-dataset\\Anno\\list_landmarks_align_celeba.txt'
	# readLandmark(path)
	
	# path = 'J:\\Dataset\\celebA-dataset\\Anno\\list_bbox_celeba.txt'
	# readBbox(path)
	
	# Create dataset object
	celeba = CELEBADataset(dataType='align_jpg')
	celeba.readDataset()
	# celeba.trainset.show(maxNum=1000, saveDir='./output/trainset')
	# celeba.valset.show(maxNum=1000, saveDir='./output/valset')
	# celeba.testset.show(maxNum=1000, saveDir='./output/testset')
	
	# Get a batch of samples
	imgs, attrs, landmarks = celeba.trainset.getNextBatch()
	print('imgs.shape={0}, attrs.shape={1}, landmarks.shape={2}'.\
		format(imgs.shape, attrs.shape, landmarks.shape))
	dispSamples(imgs, attrs, landmarks)
	
	
if __name__ == '__main__':
	main()
