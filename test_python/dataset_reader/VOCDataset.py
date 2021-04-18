# encoding: utf-8

# Import standard libraries
import os
import sys
import time
from xml.dom import minidom
import re

# Import 3rd-part libraries
import skimage.io
import numpy as np
from matplotlib import pyplot as plt

# Import self-define libraries
from src.SuperClass.SuperDataset import SuperDatasetManager
from src.SuperClass.SuperDataset import SuperDataset


def createVOCCategoryDict():
    t_list = ['aeroplane', 'bicycle', 'bird', 'boat',
              'bottle', 'bus', 'car', 'cat', 'chair',
              'cow', 'diningtable', 'dog', 'horse',
              'motorbike', 'person', 'pottedplant',
              'sheep', 'sofa', 'train', 'tvmonitor']
    t_dict = {}
    cnt = 0
    for key in t_list:
        t_dict[key] = cnt
        cnt += 1
    return t_dict


class VOCManager(SuperDatasetManager):

    def __init__(self,
                 enableMemSave=False,
                 isRandomBatch=True,
                 batchSize=64,
                 bboxMaxNum=1,
                 maxSampleNum=100000,
                 isTheLargestObj=True,
                 specificClassName='aeroplane'):
        super(VOCManager, self).__init__()

        # Enable memory saved mode
        self.enableMemSave = enableMemSave
        self.isRandomBatch = isRandomBatch

        self.images = 0
        self.imagesPosition = 0
        self.bbox = 0
        self.labels = 0
        self.imagePathList = []
        self.gtPathList = []
        #
        self.bboxMaxNum = bboxMaxNum
        self.specificClassName = specificClassName
        self.isTheLargestObj = isTheLargestObj
        self.maxImageSize = 0
        self.numCate = 0
        self.VOCCateDict = createVOCCategoryDict()

        # Counter
        self.batchSize = batchSize
        self.maxSampleNum = maxSampleNum
        self.batchCount = 0
        self.epochCount = 0
        self.randomIndex = 0

    def readDataset(self, txtPath):
        """
        Function: Read dataset
        :param txtPath: the path of path list file
        :return: None
        """
        VOCCateDict = self.VOCCateDict
        numCate = len(VOCCateDict)
        self.numCate = numCate
        # Obtain the directions of images and annotations
        fdir = txtPath
        setName = 'xxx'
        while re.match(r'VOC.{4}', setName) is None:
            fdir, setName = os.path.split(fdir)
        datasetDir = os.path.join(fdir, setName)
        imageDir = os.path.join(datasetDir, 'JPEGImages')
        annotationDir = os.path.join(datasetDir, 'Annotations')
        # print imageDir
        # print annotationDir
        # Read fileNames
        fileNameList = []
        isPosList = []
        with open(txtPath, 'r') as fid:
            line = fid.readline()
            while line:
                fileName, isPos = line.split()
                fileNameList.append(fileName)
                isPosList.append(int(isPos))
                line = fid.readline()
        # Read all annoations and choose the max image size
        antList = []
        imageSize = []
        for fileName in fileNameList:
            t_filePath = os.path.join(annotationDir, fileName+'.xml')
            # print t_filePath
            antList.append(self.readAnnotation(t_filePath))
            imageSize.append(antList[-1]['size'])
        imageSize = np.array(imageSize)
        maxImageSize = np.max(imageSize, axis=0)
        self.maxImageSize = maxImageSize
        # if self.maxImageSize[0] > self.maxImageSize[1]:
        #     self.maxImageSize[1] = self.maxImageSize[0]
        # else:
        #     self.maxImageSize[0] = self.maxImageSize[1]

        # Limit max number of samples
        num = len(fileNameList)
        if self.maxSampleNum != 0 and num > self.maxSampleNum:
            num = self.maxSampleNum

        if self.enableMemSave:
            for i in range(0, num):
                t_path = os.path.join(imageDir, fileNameList[i] + '.jpg')
                self.imagePathList.append(t_path)
                t_path = os.path.join(annotationDir, fileNameList[i] + '.xml')
                self.gtPathList.append(t_path)
                # self.labels
        else:

            imgsShape = [num, maxImageSize[0], maxImageSize[1], maxImageSize[2]]
            self.images = np.zeros(shape=imgsShape,
                                   dtype=np.uint8)
            self.imagesPosition = np.zeros(shape=[num, 4],
                                           dtype=np.int32)
            self.bbox = np.zeros(shape=[num, self.bboxMaxNum, 4],
                                 dtype=np.float32)
            self.labels = np.zeros(shape=[num, self.bboxMaxNum, numCate],
                                   dtype=np.float32)

            for i in range(0, num):
                t_imgPath = os.path.join(imageDir, fileNameList[i] + '.jpg')
                t_antPath = os.path.join(annotationDir, fileNameList[i] + '.xml')
                # print t_imgPath
                img, imgPos, bbox, labels = \
                    self.readOneDataPoint(t_imgPath, t_antPath, VOCCateDict)
                self.images[i, :] = img
                self.imagesPosition[i, :] = imgPos
                self.bbox[i, :] = bbox
                self.labels[i, :] = labels

                # print self.labels[i, :]
                # plt.clf()
                # plt.imshow(self.images[i, :])
                # plt.show()

    def readOneDataPoint(self, t_imgPath, t_antPath, VOCCateDict):
        """
        Function: Read a data point (image, annotation)
        :param t_imgPath: the path of image
        :param t_antPath:  the path of annotation
        :param VOCCateDict: the dictionary of categoties
        :return: image, imagePosition, bboxes, labels
        """
        # Create memory
        maxImageSize = self.maxImageSize
        image = np.zeros(shape=maxImageSize,
                         dtype=np.uint8)
        imagePosition = np.zeros(shape=[4],
                                 dtype=np.int32)
        bboxes = np.zeros(shape=[self.bboxMaxNum, 4],
                          dtype=np.float32)
        labels = np.zeros(shape=[self.bboxMaxNum, self.numCate],
                          dtype=np.float32)
        # Read and restore image data
        img = self.readImage(t_imgPath)
        annotation = self.readAnnotation(t_antPath)
        size = annotation['size']  # w-h-d
        lux = maxImageSize[1] / 2 - size[1] / 2
        luy = maxImageSize[0] / 2 - size[0] / 2
        rdx = lux + size[1]
        rdy = luy + size[0]
        image[luy:rdy, lux:rdx, :] = img
        imagePosition[:] = [lux, luy, rdx, rdy]
        # Store annotation
        objs = annotation['object']
        objsUsedFlag = [False] * len(objs)
        # Search positive category
        posIndex = []
        areaList = []
        for j in range(0, len(objs)):
            obj = objs[j]
            name = obj['name']
            if name == self.specificClassName:
                posIndex.append(j)
            t_area = (obj['xmax']-obj['xmin'])*(obj['ymax']-obj['ymin'])
            areaList.append(t_area)

        # Select the largest object or the specific category
        if self.isTheLargestObj:
            posIndex = list(np.argsort(-np.array(areaList)))

        # Store positive category at first
        minNum = np.minimum(len(posIndex), self.bboxMaxNum)
        if len(posIndex) > 0:
            for j in range(0, minNum):
                lux = objs[posIndex[j]]['xmin']
                luy = objs[posIndex[j]]['ymin']
                w = objs[posIndex[j]]['xmax'] - lux
                h = objs[posIndex[j]]['ymax'] - luy
                lux += imagePosition[0]
                luy += imagePosition[1]
                bboxes[j, :] = [lux, luy, w, h]
                cateIndex = VOCCateDict[objs[posIndex[j]]['name']]
                labels[j, cateIndex] = 1.0
                objsUsedFlag[posIndex[j]] = True
        # Store negative category
        if minNum < self.bboxMaxNum:
            # The index of the first empty bbox
            bboxIndex = minNum
            for j in range(0, len(objs)):
                # print 'bboxIndex = ', bboxIndex
                if not objsUsedFlag[j]:
                    lux = objs[j]['xmin']
                    luy = objs[j]['ymin']
                    w = objs[j]['xmax'] - lux
                    h = objs[j]['ymax'] - luy
                    lux += imagePosition[0]
                    luy += imagePosition[1]
                    bboxes[bboxIndex, :] = [lux, luy, w, h]
                    cateIndex = VOCCateDict[objs[j]['name']]
                    labels[bboxIndex, cateIndex] = 1.0
                    objsUsedFlag[j] = True
                    bboxIndex += 1
                if bboxIndex >= self.bboxMaxNum:
                    break
        return image, imagePosition, bboxes, labels

    def readBatchDataset(self, index):
        """
        Function: Read a batch of samples
        :param index: 
        :return: images, bbox, labels
        """
        VOCCateDict = self.VOCCateDict
        num = index.shape[0]
        maxImageSize = self.maxImageSize
        imgsShape = [num, maxImageSize[0], maxImageSize[1], maxImageSize[2]]
        images = np.zeros(shape=imgsShape,
                          dtype=np.uint8)
        imagesPosition = np.zeros(shape=[num, 4],
                                  dtype=np.int32)
        bboxes = np.zeros(shape=[num, self.bboxMaxNum, 4],
                          dtype=np.float32)
        labels = np.zeros(shape=[num, self.bboxMaxNum, self.numCate],
                          dtype=np.float32)

        for i in range(0, num):
            t_imgPath = self.imagePathList[index[i]]
            t_antPath = self.gtPathList[index[i]]

            img, imgPos, bbox, labs = \
                self.readOneDataPoint(t_imgPath, t_antPath, VOCCateDict)
            images[i, :] = img
            imagesPosition[i, :] = imgPos
            bboxes[i, :] = bbox
            labels[i, :] = labs

        return images, bboxes, labels

    def getNextBatch(self, batchSize=0):

        images, bbox, labels = \
            self.getNextBatchWithLabels(batchSize=batchSize)

        return images, bbox

    def getNextBatchWithLabels(self, batchSize=0):
        """
        Function: Get a batch of samples
        :param batchSize: batch, int
        :return: images, bbox, labels
        """
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
        # print 'hello'
        if self.enableMemSave:

            images, bbox, labels = \
                self.readBatchDataset(self.randomIndex[startIndex:endIndex])
        else:

            # Fetch images and bboxes
            if isinstance(self.images, int) or isinstance(self.bbox, int):
                raise ValueError('Empty Dataset')
            images = self.images[self.randomIndex[startIndex:endIndex], :]
            bbox = self.bbox[self.randomIndex[startIndex:endIndex], :]
            labels = self.labels[self.randomIndex[startIndex:endIndex], :]

        # labels = labels[:, 0, :]
        labels = np.squeeze(labels)
        # Return images and bboxes
        return images, bbox, labels

    def getSampleNum(self):
        """
        Function: Get the number of dataset
        :return: num, int
        """
        # Check memory and return number of samples
        if isinstance(self.images, np.ndarray):
            return self.images.shape[0]
        elif len(self.imagePathList) > 0:
            return len(self.imagePathList)
        else:
            return 0

    @staticmethod
    def showBbox(images, bbox, index=0, isSave=False, savePath=''):
        """
        Function: Show or save image with bbox
        :param images: ndarray, [n, h, w, ch], uint8
        :param bbox:  ndarray, [n, m, 4], float32
        :param index:  ndarray, [k], int32
        :param isSave: True(for save), False(for show)
        :param savePath: the path to save
        :return: None
        """
        plt.clf()
        plt.imshow(images[index, :])
        bbox = bbox[index, :]
        # Plot five points
        plt.plot([bbox[0, 0], bbox[0, 0] + bbox[0, 2],
                  bbox[0, 0] + bbox[0, 2], bbox[0, 0], bbox[0, 0]],
                 [bbox[0, 1], bbox[0, 1], bbox[0, 1] + bbox[0, 3],
                  bbox[0, 1] + bbox[0, 3], bbox[0, 1]], color='red', lw=3)
        # Limit coordinates range
        plt.axis([0, images.shape[2], images.shape[1], 0])
        # Save or show
        if isSave:
            foo_fig = plt.gcf()  # 'get current figure
            foo_fig.savefig(savePath,
                            format='png',
                            dpi=128,
                            bbox_inches='tight')
        else:
            plt.show()

    @staticmethod
    def readImage(path):
        """
        Function: Read image from the specific path
        :param path: The path of an image
        :return:
        """
        if not os.path.isfile(path):
            raise ValueError('Not Exist')
        return skimage.io.imread(fname=path)

    @staticmethod
    def readAnnotation(path):
        """
        Function: Read annotation xml file
        :param path: The path of a xml file
        :return: dict{}
        """
        if not os.path.isfile(path):
            raise ValueError('Not Exist')
        annotation = {}
        # Create DOM
        dom = minidom.parse(path)
        root = dom.documentElement
        # folder
        nodes = root.getElementsByTagName('folder')
        if len(nodes) != 0:
            folder = nodes[0].childNodes[0].data
            annotation['folder'] = folder
        # filename
        nodes = root.getElementsByTagName('filename')
        if len(nodes) != 0:
            filename = nodes[0].childNodes[0].data
            annotation['filename'] = filename
        # size
        nodes = root.getElementsByTagName('size')
        if len(nodes) != 0:
            # width
            t_nodes = nodes[0].getElementsByTagName('width')
            if len(t_nodes) == 0:
                raise ValueError('')
            width = int(t_nodes[0].childNodes[0].data)
            # height
            t_nodes = nodes[0].getElementsByTagName('height')
            if len(t_nodes) == 0:
                raise ValueError('')
            height = int(t_nodes[0].childNodes[0].data)
            # depth
            t_nodes = nodes[0].getElementsByTagName('depth')
            if len(t_nodes) == 0:
                raise ValueError('')
            depth = int(t_nodes[0].childNodes[0].data)
            annotation['size'] = [height, width, depth]
        # segmented
        nodes = root.getElementsByTagName('segmented')
        if len(nodes) != 0:
            segmented = nodes[0].childNodes[0].data
            annotation['segmented'] = segmented
        # object
        nodes = root.getElementsByTagName('object')
        objs = []
        for node in nodes:
            obj = {}
            # name
            t_nodes = node.getElementsByTagName('name')
            if len(t_nodes) != 0:
                name = t_nodes[0].childNodes[0].data
                obj['name'] = name
            # pose
            t_nodes = node.getElementsByTagName('pose')
            if len(t_nodes) != 0:
                pose = t_nodes[0].childNodes[0].data
                obj['pose'] = pose
            # truncated
            t_nodes = node.getElementsByTagName('truncated')
            if len(t_nodes) != 0:
                truncated = t_nodes[0].childNodes[0].data
                obj['truncated'] = truncated
            # difficult
            t_nodes = node.getElementsByTagName('difficult')
            if len(t_nodes) != 0:
                difficult = t_nodes[0].childNodes[0].data
                obj['difficult'] = difficult
            # bndbox
            t_nodes = node.getElementsByTagName('bndbox')
            if len(t_nodes) != 0:
                tt_nodes = t_nodes[0].getElementsByTagName('xmin')
                xmin = float(tt_nodes[0].childNodes[0].data)
                tt_nodes = t_nodes[0].getElementsByTagName('ymin')
                ymin = float(tt_nodes[0].childNodes[0].data)
                tt_nodes = t_nodes[0].getElementsByTagName('xmax')
                xmax = float(tt_nodes[0].childNodes[0].data)
                tt_nodes = t_nodes[0].getElementsByTagName('ymax')
                ymax = float(tt_nodes[0].childNodes[0].data)
                # print xmin, ymin, xmax, ymax
                obj['xmin'] = xmin
                obj['ymin'] = ymin
                obj['xmax'] = xmax
                obj['ymax'] = ymax
            # part
            t_nodes = node.getElementsByTagName('part')
            parts = []
            for t_node in t_nodes:
                part = {}
                # name
                tt_nodes = t_node.getElementsByTagName('name')
                name = tt_nodes[0].childNodes[0].data
                part['name'] = name
                # bndbox
                tt_nodes = t_node.getElementsByTagName('bndbox')
                if len(tt_nodes) != 0:
                    ttt_nodes = tt_nodes[0].getElementsByTagName('xmin')
                    xmin = float(ttt_nodes[0].childNodes[0].data)
                    ttt_nodes = tt_nodes[0].getElementsByTagName('ymin')
                    ymin = float(ttt_nodes[0].childNodes[0].data)
                    ttt_nodes = tt_nodes[0].getElementsByTagName('xmax')
                    xmax = float(ttt_nodes[0].childNodes[0].data)
                    ttt_nodes = tt_nodes[0].getElementsByTagName('ymax')
                    ymax = float(ttt_nodes[0].childNodes[0].data)
                    # print xmin, ymin, xmax, ymax
                    part['xmin'] = xmin
                    part['ymin'] = ymin
                    part['xmax'] = xmax
                    part['ymax'] = ymax
                parts.append(part)
            obj['part'] = parts
            objs.append(obj)
        annotation['object'] = objs
        # Return
        return annotation


class Config(object):

    def __init__(self,
                 enableMemSave=False,
                 batchSize=64,
                 bboxMaxNum=1,
                 maxSampleNum=100000,
                 testingSampleRatio=0.3,
                 isUseAllData=True,
                 isTheLargestObj=True,
                 specificClassName='aeroplane',
                 datasetDir='/home/share/Dataset/VOC-dataset/VOC2012'):
        """
        Function: Initialize the parameters of configuration
        :param enableMemSave: flag to enable memory-saved mode
        :param batchSize: size of a batch
        :param bboxMaxNum: the maximum number of bboxes
        :param maxSampleNum: the maximum number of samples
        :param testingSampleRatio: the ratio of testset and trainset
        :param isUseAllData:  flag to use all data
        :param isTheLargestObj: flag to the largest object
        :param specificClassName: the name of specific category
        :param dataHomeDir: the home direction of dataset
        """

        self.dataHomeDir = datasetDir
        self.enableMemSave = enableMemSave
        self.batchSize = batchSize
        self.bboxMaxNum = bboxMaxNum
        # The number of samples
        self.maxSampleNum = maxSampleNum
        self.testingSampleRatio = testingSampleRatio
        # Load the largest object or specific class
        self.isTheLargestObj = isTheLargestObj
        self.specificClassName = specificClassName
        if isTheLargestObj:
            self.specificClassName = ''

        # Used all data
        self.isUseAllData = isUseAllData
        if self.isUseAllData:
            self.dataListRelativeDir = 'ImageSets'
            self.teTrName = ['testset', 'trainset']

        # Use partial data
        else:
            self.dataListRelativeDir = 'ImageSets/Main'
            if len(self.specificClassName) == 0:
                self.teTrName = ['val', 'train']
            else:
                self.teTrName = [self.specificClassName+'_train',
                                 self.specificClassName+'_val']


class VOCDataset(SuperDataset):

    def __init__(self, config=Config()):
        super(VOCDataset, self).__init__()

        # Configuration
        self.config = config

        # Dataset
        maxNum = np.int(config.maxSampleNum * config.testingSampleRatio)
        self.testset = VOCManager(
            enableMemSave=config.enableMemSave,
            isRandomBatch=False,
            batchSize=config.batchSize,
            bboxMaxNum=config.bboxMaxNum,
            maxSampleNum=maxNum,
            isTheLargestObj=config.isTheLargestObj,
            specificClassName=config.specificClassName)
        maxNum = np.int(config.maxSampleNum * (1 - config.testingSampleRatio))
        self.trainset = VOCManager(
            enableMemSave=config.enableMemSave,
            batchSize=config.batchSize,
            bboxMaxNum=config.bboxMaxNum,
            maxSampleNum=maxNum,
            isTheLargestObj=config.isTheLargestObj,
            specificClassName=config.specificClassName)

    def readDataset(self, isTrain=True, isTest=True):
        """
        Function: Read the whole dataset
        :param isTrain: enable flag to load trainset
        :param isTest:  enable flag to load testset
        :return: None
        """

        testListPath = os.path.join(self.config.dataHomeDir,
                                    self.config.dataListRelativeDir,
                                    self.config.teTrName[0]+'.txt')
        trainListPath = os.path.join(self.config.dataHomeDir,
                                     self.config.dataListRelativeDir,
                                     self.config.teTrName[1]+'.txt')

        # Check Path
        if not os.path.isfile(testListPath):
            raise ValueError('Not testset:\r\n\t%s' % (testListPath))
        if not os.path.isfile(trainListPath):
            raise ValueError('Not trainset:\r\n\t%s' % (trainListPath))

        start = time.clock()
        if isTest:
            print 'Reading VOC-dataset testset ...'
            self.testset.readDataset(testListPath)
        if isTrain:
            print 'Reading VOC-dataset trainset ...'
            self.trainset.readDataset(trainListPath)
        end = time.clock()
        print 'Read VOC-dataset completely, cost time %f seconds' \
              % (end - start)

    def createDataList(self):
        """
        Function: the create the list file of image path
        :return: None
        """
        testListPath = os.path.join(self.config.dataHomeDir,
                                    'ImageSets/testset.txt')
        trainListPath = os.path.join(self.config.dataHomeDir,
                                     'ImageSets/trainset.txt')

        imgDir = os.path.join(self.config.dataHomeDir, 'JPEGImages')
        fileNameList = os.listdir(imgDir)
        num = len(fileNameList)
        numTest = int(num*self.config.testingSampleRatio)
        numTrain = num - numTest
        randIndex = np.random.randint(0, num, num)
        with open(testListPath, 'w') as fid:
            for i in range(0, numTest):
                # print fileNameList[randIndex[i]]
                name, ext = fileNameList[randIndex[i]].split('.')
                t_str = name + ' ' + str(1) + '\r\n'
                fid.write(t_str)
        with open(trainListPath, 'w') as fid:
            for i in range(numTest, num):
                name, ext = fileNameList[randIndex[i]].split('.')
                t_str = name + ' ' + str(1) + '\r\n'
                fid.write(t_str)


def main():
    print sys.argv
    datapath = 'F:/Dataset/VOC-dataset/VOC2012/ImageSets/Main/aeroplane_train.txt'
    # mng = VOCManager(enableMemSave=True)
    # mng.readDataset(datapath)
    # # print mng.images.shape
    # # print mng.bbox.shape
    # # print mng.labels.shape
    #
    # images, bbox, labels = mng.getNextBatch()
    # print images.shape
    # print bbox.shape
    # print labels.shape
    # for i in range(0, images.shape[0]):
    #     # plt.clf()
    #     # plt.imshow(images[i, :])
    #     # plt.show()
    #     mng.showBbox(images, bbox, i)

    config = Config(
        enableMemSave=True,
        batchSize=64,
        bboxMaxNum=1,
        maxSampleNum=100000,
        testingSampleRatio=0.3,
        isUseAllData=True,
        isTheLargestObj=True,
        specificClassName='aeroplane',
        datasetDir='/home/share/Dataset/VOC-dataset/VOC2012')
    voc = VOCDataset(config=config)
    voc.readDataset()

    print 'trainingSampleNum = ', voc.trainset.getSampleNum()
    print 'testingSampleNum = ', voc.testset.getSampleNum()
    for i in range(0, 1000):
        images, bbox, labels = voc.trainset.getNextBatchWithLabels()
        print voc.trainset.epochCount
        print images.shape
        print bbox.shape
        print labels.shape
        # for i in range(0, images.shape[0]):
        #     voc.trainset.showBbox(images, bbox, i)

    # Save the image with object bbox
    # saveHomeDir = './marked/trainset/'
    # if not os.path.isdir(saveHomeDir):
    #     os.makedirs(saveHomeDir)
    # for i in range(0, voc.trainset.getSampleNum()):
    #     t_str = '%0*d'%(6, i) + '.jpg'
    #     t_path = os.path.join(saveHomeDir, t_str)
    #     voc.trainset.showBbox(voc.trainset.images, voc.trainset.bbox, i,
    #                           isSave=True, savePath=t_path)
    # saveHomeDir = './marked/testset/'
    # if not os.path.isdir(saveHomeDir):
    #     os.makedirs(saveHomeDir)
    # for i in range(0, voc.testset.getSampleNum()):
    #     t_str = '%0*d' % (6, i) + '.jpg'
    #     t_path = os.path.join(saveHomeDir, t_str)
    #     voc.testset.showBbox(voc.testset.images, voc.testset.bbox, i,
    #                          isSave=True, savePath=t_path)
    # voc.createDataList()


if __name__ == '__main__':
    main()
