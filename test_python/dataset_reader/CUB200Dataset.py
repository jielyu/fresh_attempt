#encoding: utf-8

import os, sys, time, math
import numpy as np
import skimage.io
import matplotlib.pyplot as plt
from scipy import misc

def showSample(img, label, bbox):
    plt.clf()
    plt.imshow(img)
    plt.plot([bbox[0], bbox[0] + bbox[2],
          bbox[0] + bbox[2], bbox[0], bbox[0]],
         [bbox[1], bbox[1], bbox[1] + bbox[3],
          bbox[1] + bbox[3], bbox[1]], color='red', lw=3)
    plt.text(bbox[0], bbox[1], s=str(label), color='blue')
    plt.show()

class Dataset(object):

    def __init__(self, isRandomBatch=True, batchSize=64, maxSampleNum=100000, imgSize=[448, 448, 3], numCate=200):
        # Store annotation and image path
        self.imgPathList = []
        self.bboxList = []
        self.labelList = []
        # Set uniform image size
        self.imgSize = imgSize
        self.numCate = numCate
        # Counter
        self.isRandomBatch = isRandomBatch
        self.batchSize = batchSize
        self.maxSampleNum = maxSampleNum
        self.batchCount = 0
        self.epochCount = 0
        self.randomIndex = 0
        
    def readDataset(self, dataDir, isTrain):
        # Construct the txt paths of all annotations  
        labelTxtPath = os.path.join(dataDir, 'image_class_labels.txt')
        bboxTxtPath = os.path.join(dataDir, 'bounding_boxes.txt')
        imgTxtPath = os.path.join(dataDir, 'images.txt')
        splitTxtPath = os.path.join(dataDir, 'train_test_split.txt')
        
        fspt = open(splitTxtPath)
        flbl = open(labelTxtPath)
        fbbx = open(bboxTxtPath)
        fimgp = open(imgTxtPath)
        # Read annotaiton and image path
        line=fspt.readline()
        imgSize = []
        while line:
            lbl = flbl.readline()
            bbx = fbbx.readline()
            imgp = fimgp.readline()
            
            # Parse text read from files
            # split flag
            id, flag = line.split()
            id, flag = int(id), int(flag)
            # label
            id, label = lbl.split()
            id, label = int(id), int(label)
            # bbox
            id, x, y, w, h = bbx.split()
            id, x, y, w, h = int(id), float(x), float(y), float(w), float(h)
            # image path
            id, img_path = imgp.split()
            id, img_path = int(id), img_path.strip()
            
            # Add to specific subset
            if bool(flag) == isTrain:
                img_path = os.path.join(dataDir, 'images', img_path)
                self.imgPathList.append(img_path)
                self.labelList.append(label-1)
                self.bboxList.append(np.array([x, y, w, h], dtype=np.float32))
                #img = skimage.io.imread(self.imgPathList[-1])
                #if len(img.shape) < 3:
                #    img = np.expand_dims(img, axis=-1)
                #    img = np.tile(img, [1, 1, 3])
                #imgSize.append([img.shape[0], img.shape[1], img.shape[2]])
                # print('id = %d'%(id))
                # print('label = %d'%(self.labelList[-1]))
                # print('bbox = %s'%(str(self.bboxList[-1])))
                # print('imgpath = %s'%(self.imgPathList[-1]))
            # raise ValueError('Test')
            line = fspt.readline()  
        fspt.close()
        flbl.close()
        fbbx.close()
        fimgp.close()
        
        #imgSize = np.array(imgSize)
        #maxSize = np.max(imgSize, axis=0)
        #minSize = np.min(imgSize, axis=0)
        #print('maxSize = %s'%(str(maxSize)))
        #print('minSize = %s'%(str(minSize)))

    def getSampleNum(self):
        return len(self.imgPathList)
        
    def getNextBatch(self, batchSize=0):
        # Check parameters
        if batchSize != 0 and self.batchSize != batchSize:
            self.batchSize = batchSize
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
            
        # Get a batch of samples
        spSize = self.imgSize  # specific image size
        shape = [self.batchSize, spSize[0], spSize[1], spSize[2]]
        img = np.zeros(shape=shape, dtype=np.uint8)
        bbox = np.zeros(shape=[self.batchSize, 4], dtype=np.float32)
        label = np.zeros(shape=[self.batchSize, self.numCate], dtype=np.float32)
        img_bbox = np.zeros(shape=[self.batchSize, 4], dtype=np.float32)
        img_size = np.zeros(shape=[self.batchSize, 2], dtype=np.int32)
        cnt = 0
        for ind in self.randomIndex[startIndex:endIndex]:
            # Read original data
            img_path = self.imgPathList[ind]
            timg = skimage.io.imread(img_path)
            if len(timg.shape) < 3 or timg.shape[2] == 1:
                timg = np.expand_dims(timg, axis=-1)
                timg = np.tile(timg, [1, 1, 3])
            tlbl = self.labelList[ind]
            tbbox = self.bboxList[ind]
            # 
            # Resize image and adjust bbox
            ti_size = [timg.shape[0], timg.shape[1]]
            ui_size = [self.imgSize[0], self.imgSize[1]]
            if ti_size[0] > ti_size[1]:
                scale = ui_size[0]/float(ti_size[0])
                tg_size = [ui_size[0], int(ti_size[1]*scale)]
                
            else:
                scale = ui_size[1]/float(ti_size[1])
                tg_size = [int(ti_size[0]*scale), ui_size[1]]
            # print 'scale =', scale
            rs_img = misc.imresize(timg, tg_size)
            # image bbox
            ibbox = [ui_size[1]/2-tg_size[1]/2, ui_size[0]/2-tg_size[0]/2, tg_size[1], tg_size[0]]
            img[cnt, ibbox[1]:(ibbox[1]+ibbox[3]), ibbox[0]:(ibbox[0]+ibbox[2]), :] = rs_img
            # new bbox of object
            obbox = tbbox*scale
            obbox[0] += ibbox[0]
            obbox[1] += ibbox[1]
            # Store annotattion information
            bbox[cnt, :] = obbox
            label[cnt, tlbl] = 1.0
            img_bbox[cnt, :] = ibbox
            img_size[cnt, :] = ti_size
            # showSample(timg, tlbl, tbbox)
            # showSample(img[cnt, :], tlbl, obbox)
            cnt +=1
        bbox = np.expand_dims(bbox, axis=1)
        return img, bbox, label #  ,img_bbox, img_size

    def getNextBatchWithLabels(self, batchSize=0):
        return self.getNextBatch(batchSize=batchSize)


class Config(object):
    def __init__(self, dataHomeDir='.', batchSize=64, 
                 imgSize=[448, 448, 3], subsetName='CUB_200_2011'):
        self.dataHomeDir = dataHomeDir
        self.batchSize = batchSize
        self.subsetName = subsetName
        self.imgSize = imgSize
        self.maxSampleNum = 100000
        self.numCate = 200

class CUB200Dataset(object):

    def __init__(self, config=Config()):
        self.config = config
        self.trainset = Dataset(
            isRandomBatch=True, 
            batchSize=config.batchSize, 
            maxSampleNum=config.maxSampleNum, 
            imgSize=config.imgSize, 
            numCate=config.numCate)
        self.testset = Dataset(
            isRandomBatch=False, 
            batchSize=config.batchSize, 
            maxSampleNum=config.maxSampleNum, 
            imgSize=config.imgSize, 
            numCate=config.numCate)

    def readDataset(self, isTrain=True, isTest=True):
        start = time.clock()
        dataDir = os.path.join(self.config.dataHomeDir, self.config.subsetName)
        if isTrain:
            print('Reading trainset on CUB200 dataset ...')
            self.trainset.readDataset(dataDir=dataDir, isTrain=True)
        if isTest:
            print('Reading testset on CUB200 dataset ...')
            self.testset.readDataset(dataDir=dataDir, isTrain=False)
        end = time.clock()
        print('Read CUB200 dataset completely, cost time: %2.2f secs'%(end-start))
        
        
def main():
    print(sys.argv)
    dataHomeDir = '/media/home_bak/jielyu/Database/CUB200-dataset'
    config = Config(dataHomeDir=dataHomeDir)
    cub200 = CUB200Dataset(config=config)
    cub200.readDataset()
    images, bboxes, labels = cub200.trainset.getNextBatch()
    images, bboxes, labels = cub200.testset.getNextBatch()
    print images.shape, images.dtype
    print bboxes.shape, bboxes.dtype
    print labels.shape, labels.dtype
    #dataHomeDir = './CUB_200_2011'
    #dataset = Dataset()
    #dataset.readDataset(dataDir=dataHomeDir, isTrain=False)
    #print('num_sam = %d'%(dataset.getSampleNum()))
    #images, bboxes, labels = dataset.getNextBatch()
    #print images.shape, images.dtype
    #print bboxes.shape, bboxes.dtype
    #print labels.shape, labels.dtype
    #for i in range(images.shape[0]):
    #    showSample(images[i, :], np.argmax(labels[i, :]), bboxes[i, :])
    
if __name__ == '__main__':
    main()
