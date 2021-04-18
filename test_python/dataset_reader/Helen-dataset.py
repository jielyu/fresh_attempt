#encode: utf-8

import os
import skimage.io
import matplotlib.pyplot as plt


def getImagePathsFromDir(imgDir):
    """
    Function: Get paths of all images from the input directory
    Input:
        imgDir: the input directory
    Output:
        path_list: a list of path
    Date: 2018.04.09
    Author: Jie Lyu
    """
    name_list = os.listdir(imgDir)
    path_list = []
    for name in name_list:
        _, ext = os.path.splitext(name)
        if ext == '.jpg' or ext == '.png':
            path_list.append(os.path.join(imgDir, name))
    return path_list

def getImagePath(dataHomeDir='.', trainDir='trainset', testDir='testset'):
    """
    Function: Get path of training and testing images respectively
    Input:
        dataHomeDir: home directory of a dataset
        trainDir: name of trainset
        testDir: name of testset
    Output:
        tr_path_list: a list of training images
        te_path_list: a list of testing images
    Date: 2018.04.09
    Author: Jie Lyu
    """
    tr_dir = os.path.join(dataHomeDir, trainDir)
    te_dir = os.path.join(dataHomeDir, testDir)
    tr_path_list = getImagePathsFromDir(tr_dir)
    te_path_list = getImagePathsFromDir(te_dir)
    return tr_path_list, te_path_list

def getAnnPathFromImagePath(imgPath):
    """
    Function: Get path of annotation file from the corresponding image path
    Input:
        imgPath: path of an image
    Output:
        annPath: path of an annotation
    Date: 2018.04.09
    Author: Jie Lyu
    """
    name, _ = os.path.splitext(imgPath)
    return name + '.pts'

def readImgFile(imgPath):
    """
    Function: Read image data from a path
    Input:
        imgPath: path of an image
    Output:
        img: image data, ndarray, uint8
    Date: 2018.04.09
    Author: Jie Lyu
    """
    return skimage.io.imread(fname=imgPath)

def readAnnFile(annPath):
    """
    Function: Read annotation data from a path
    Input: 
        annPath: path of an annotation
    Output:
        pts, list, [[x1,y1], [x2,y2]...]
    Date: 2018.04.09
    Author: Jie Lyu
    """
    pts = []
    with open(annPath, 'r') as fid:
        # Parse version
        line = fid.readline()
        _, version = line.split(':')
        version= int(version)
        # Parse n_points
        line = fid.readline()
        _, n_points = line.split(':')
        n_points = int(n_points)
        # Parse "{""
        _ = fid.readline()
        # Paese (x,y) of all points
        for i in range(n_points):
            line = fid.readline()
            line = line.strip()
            x, y = line.split(' ')
            x = float(x)
            y = float(y)
            pts.append([x, y])
    # Return [[x1,y1], [x2,y2]...]
    return pts


def plotPtsOnImage(img, pts, savePath=None):
    """
    Function: Plot points on an image
    Input:
        img: image data, ndarray, uint8
        pts: point list, [[x1,y1], [x2,y2]...]
        savePath: path of saved result
    Output:
        None
    Date: 2018.04.09
    Author: Jie Lyu
    """
    plt.clf()
    plt.imshow(img)
    plt.axis([0, img.shape[1], img.shape[0], 0])
    plt.axis('off')
    for idx,xy in enumerate(pts):
        plt.plot(xy[0], xy[1], 'r.', color='blue', markersize=10)
        plt.text(x=xy[0], y=xy[1], s=str(idx), fontsize=10)
    if savePath is None:
        plt.show()
    else:
        _, ext = os.path.splitext(savePath)
        ext = ext[1:]
        plt.savefig(savePath, format=ext, dpi=128, bbox_inches='tight')

def plotGtPtsOnImage(imgPath, savePath=None):
    """
    Function: Plot groundtruth points on an image
    Input:
        imgPath: path of an image
        savePath: path of saved result
    Output:
        None
    Date: 2018.04.09
    Author: Jie Lyu
    """
    img = readImgFile(imgPath=imgPath)
    annPath = getAnnPathFromImagePath(imgPath=imgPath)
    pts = readAnnFile(annPath=annPath)
    plotPtsOnImage(img, pts, savePath=savePath)

def plotGtPtsOnDir(imgDir, saveDir=None):
    """
    Function: Plot groundtruth points for images under a drectory
    Input:
        imgDir: directory of images
        saveDir: directory of saved result
    Output:
        None
    Date: 2018.04.09
    Author: Jie Lyu
    """
    img_path_list = getImagePathsFromDir(imgDir=imgDir)
    for idx,p in enumerate(img_path_list):
        print('Processing {0}-th img:{1}'.format(idx, p))
        if saveDir is not None:
            name, _ = os.path.splitext(p)
            name = os.path.basename(name)
            savePath = os.path.join(saveDir, name+'.png')
            plotGtPtsOnImage(imgPath=p, savePath=savePath)
        else:
            plotGtPtsOnImage(imgPath=p, savePath=None)

def plotGtPtsOnDataset(dataDir, saveDir=None, 
                       testset='testset', trainset='trainset'):
    """
    Function: Plot groundtruth points on a dataset
    Input:
        dataDir: directory of a dataset
        saveDir: directory of saved results
        testset: name of testset
        trainset: name of trainset
    Output:
        None
    Date: 2018.04.09
    Author: Jie Lyu
    """
    # Plot groundtruth points for all images on testset 
    te_dir = os.path.join(dataDir, testset)
    if not os.path.isdir(te_dir):
        raise ValueError('Not exist directory: ' + te_dir)
    if saveDir is not None:
        te_save_dir = os.path.join(saveDir, testset)
        if not os.path.isdir(te_save_dir):
            os.makedirs(te_save_dir)
    else:
        te_save_dir = None
    plotGtPtsOnDir(imgDir=te_dir, saveDir=te_save_dir)
    # Plot groundtruth points for all images on trainset 
    tr_dir = os.path.join(dataDir, trainset)
    if not os.path.isdir(tr_dir):
        raise ValueError('Not exist directory: ' + tr_dir)
    if saveDir is not None:
        tr_save_dir = os.path.join(saveDir, trainset)
        if not os.path.isdir(tr_save_dir):
            os.makedirs(tr_save_dir)
    else:
        tr_save_dir = None
    plotGtPtsOnDir(imgDir=tr_dir, saveDir=tr_save_dir)


def main_helen(isSave=False):
    """
    Function: Plot groundtruth points for Helen-dataset
    Input:
        isSave: bool, save to file or display on the screen
    Output:
        None
    Date: 2018.04.09
    Author: Jie Lyu
    """
    dataDir = 'F:\\Dataset\\Helen-dataset'
    isSave = isSave
    if isSave is True:
        plotGtPtsOnDataset(dataDir=dataDir, 
                           saveDir=os.path.join(dataDir, 'gt_plot'))
    else:
        plotGtPtsOnDataset(dataDir=file_dir)

def main_lfpw(isSave=False):
    """
    Function: Plot groundtruth points for LFPW-dataset
    Input:
        isSave: bool, save to file or display on the screen
    Output:
        None
    Date: 2018.04.09
    Author: Jie Lyu
    """
    dataDir = 'F:\\Dataset\\LFPW-dataset'
    isSave = isSave
    if isSave is True:
        plotGtPtsOnDataset(dataDir=dataDir, 
                           saveDir=os.path.join(dataDir, 'gt_plot'))
    else:
        plotGtPtsOnDataset(dataDir=file_dir)

def main_afw(isSave=False):
    """
    Function: Plot groundtruth points for AFW-dataset
    Input:
        isSave: bool, save to file or display on the screen
    Output:
        None
    Date: 2018.04.09
    Author: Jie Lyu
    """
    dataDir = 'F:\\Dataset\\AFW-dataset'
    # dataDir = 'F:\\Course\\outline_demo\\pts_68'
    isSave = isSave
    if isSave is True:
        saveDir = os.path.join(dataDir, 'gt_plot')
        if not os.path.isdir(saveDir):
            os.makedirs(saveDir)
        plotGtPtsOnDir(imgDir=dataDir, saveDir=saveDir)
    else:
        plotGtPtsOnDir(imgDir=file_dir)

def createImgPathForAllDataset(dstImagePathTxtPath='./Path_Images.txt'):
    helenDir = 'F:\\Dataset\\Helen-dataset'
    lfpwDir = 'F:\\Dataset\\LFPW-dataset'
    afwDir = 'F:\\Dataset\\AFW-dataset'

    htr, hte = getImagePath(dataHomeDir=helenDir)
    ltr, lte = getImagePath(dataHomeDir=lfpwDir)
    atr = getImagePathsFromDir(imgDir=afwDir)

    name, ext = os.path.splitext(dstImagePathTxtPath)
    trainTxtPath = name + '_train' + ext
    with open(trainTxtPath, 'w') as fid:
        path_list_list = [htr, ltr, atr]
        for path_list in path_list_list:
            for path in path_list:
                path = path.replace('\\', '/')
                fid.write(path + '\n')
    testTxtPath = name + '_test' + ext
    with open(testTxtPath, 'w') as fid:
        path_list_list = [hte, lte]
        for path_list in path_list_list:
            for path in path_list:
                path = path.replace('\\', '/')
                fid.write(path + '\n')


# The entry of the program
if __name__ == '__main__':
    # Get the path of this file
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    # Plot groundtruth points for all image on dataset
    isSave = True
    # main_helen(isSave=isSave)   # For Helen-dataset
    # main_lfpw(isSave=isSave)    # For LFPW-dataset
    main_afw(isSave=isSave)     # For AFW-dataset

    # plotGtPtsOnImage("F:\\Dataset\\LFPW-dataset\\trainset\\image_0492.png")
    # dstImagePathTxtPath = os.path.join(file_dir, 'Path_Images.txt')
    # createImgPathForAllDataset(dstImagePathTxtPath=dstImagePathTxtPath)
