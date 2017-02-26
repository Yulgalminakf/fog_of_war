from juc.timers import Timer
from juc import hardwareIO as io
from juc import file_stuff
from juc.box import *
from juc.vector_math import *
from juc.two_dimensional_list import *
from juc.misc import *
import PIL
from PIL import Image
import math
from enum import Enum
import random
import time
import PyQt5
import os
import numpy

"""
http://donjon.bin.sh/5e/dungeon/
Grid must be off.
Doesn't work with doors... yet.
Numbers must be gotten rid of (fuckin' deal with it)
"""
#print("\n{1:~^40}".format(" Starting FoW ", "other thing", "another thign"))
#TestBoundBoxIter()
"""
radius = 100
img = Image.new("RGB", (radius * 2 + 20, radius * 2 + 20), (255,255,255))
center = (int(img.size[0] / 2), int(img.size[1] / 2))
list = []
for xy in CircleCircumferenceIter(center, radius):
    img.putpixel(xy, (0,0,0))
    #print(xy)
    if FindInList(list, xy) is not None:
        print("Found duplicate xy: " + str(xy))
        #break
    else:
        list.append(xy)
img.save(file_stuff.GetUserDir() + "/Pictures/" + "testCircleIter.png")
input()
quit()
"""

random.seed(time.time)
shouldDebugPrint = True

def DebugPrint(str):
    if shouldDebugPrint:
        print(str)
        
#gridColor = (204,204,204,255)
wallColor = (0,0,0, 255)
freeSpaceColor = (255,255,255,255)
halfExposedColor = (128,128,128,255)

hasAlphaChannel = True
#hasAlphaChannel = False

def SetupGlobalColors(mode):
    #print("Color setup: " + str(mode))
    if mode == "RGB":
        print("Color setup: RGB")
        wallColor = (0,0,0)
        freeSpaceColor = (255,255,255)
        halfExposedColor = (128,128,128)
    elif mode == "RGBA":
        print("Color setup: RGBA")
        wallColor = (0,0,0, 255)
        freeSpaceColor = (255,255,255,255)
        halfExposedColor = (128,128,128,255)
    elif mode == "L":
        print("Color setup: Grayscale")
        wallColor = 0
        freeSpaceColor = 255
        halfExposedColor = 128
    else:
        print("\n{0:~>50}\nWARNING: Unrecognized color format: {1!s}\n{0:~>50}".format('', mode))

"""
img = Image.open(file_stuff.GetUserDir() + "/Pictures/grayscale.png")
#img = Image.open(file_stuff.GetUserDir() + "/Pictures/caverns_test/caverns_test.png")
print(img.getbands())
print(img.mode) 
SetupGlobalColors(img.mode)
print(img.getpixel((10,100)))
input()
exit()
"""

workingCopyFilenameAddition = "_WorkingCopy.png"

class StateTypes(Enum):
    hidden = 0
    fullyExposed = 1
    halfExposed = 2

def GetColorFromState(state:StateTypes):
    if state == StateTypes.hidden:
        return wallColor
    elif state == StateTypes.halfExposed:
        return halfExposedColor
    elif state == StateTypes.fullyExposed:
        return freeSpaceColor
    return None

#states = TwoDList(defaultImage.size, StateTypes.hidden)
#print(states.Get((0,0)))

#states = [HIDDEN] * defaultImage.size[0] * defaultImage.size[1]
#print("LKSdjfklsdfjls: " + str(len(states)))

#xSize = 200
#ySize = 100
#temp = Timer("Temp")
#blah = [[HIDDEN for i in range(ySize)] for j in range(xSize)]
#blah[199][99]

#print(defaultImage.size)
#workingImage = Image.new("RGB", defaultImage.size, wallColor)
#workingImage.putpixel((0,0),(255,255,255))
#workingImage.save(file_stuff.GetUserDir() + "/Pictures/testdatshizz.png")

def MultiplyColors(color1, color2):
    mult = [0,0,0]
    for i in range(0,3):
        mult[i] = int(((color1[i] / 255) * (color2[i] / 255)) * 255)
    return mult

#DebugPrint("Should be True: " + str(IsGridFullyExposed(GetGridOfPixel((104,46)))))
#DebugPrint("Should be False: " + str(IsGridFullyExposed(GetGridOfPixel((94,54)))))

#DebugPrint("Should be (255,128,0): " + str(MultiplyColors((255,255,255),(255,128,0))))
#DebugPrint("Should be (128,64,0): " + str(MultiplyColors((128,128,128),(255,128,0))))
def IsPixelFree(img, pos):
    return img.getpixel(pos) == freeSpaceColor
"""

def NumNonFree(img, pos, box):
    wallCheckBox = CreateBoxFromCenterAndSize(pos, (1,1))
    numNonFreeSpaces = 0
    for xy in BoundOfBoxIter(wallCheckBox, True):
        if box.IsPointInBox(xy) and not IsPixelFree(img, xy):
            #return True
            numNonFreeSpaces += 1
    return numNonFreeSpaces

def CrawlClockwiseTick(img, box, pos, lastPos):
    #up, right, down, left
    up = (pos[0], pos[1] - 1)
    right = (pos[0] + 1, pos[1])
    down = (pos[0], pos[1] + 1)
    left = (pos[0] - 1, pos[1])

    if up is not lastPos and box.IsPointInBox(up) and IsPixelFree(img,up):
        numNonFreeSpaces = NumNonFree(img, up, box)
        if numNonFreeSpaces > 0 and numNonFreeSpaces < 7:
            return up
    if box.IsPointInBox(down) and IsPixelFree(img,up):
        return down

def Crawler(img, states, center, box):
    startingPos = center
    clampBox = CreateBoxFromCorners((0,0),(img.size[0] - 1, img.size[1] - 1))
    box = ClampBox(box, clampBox)
    bSetPos = False
    #find the non-exposed pixel to the right
    for i in range(startingPos[0], box.right):
        if not IsPixelFree(img.getpixel((i,currPos[1])), freeSpaceColor):
            startingPos[0] = i - 1
            bSetPos = True
            break
    #if it couldn't find a non-fully exposed pixel in the box, then the right most one will be the starting pos
    if not bSetPos:
        startingPos[0] = box.right

    currPos = startingPos
    """

#This function sets all the hidden pixels that are within a radius of a fully exposed pixel.
#It's purely for looks, so people can more easily tell where hallways and such are.
def FindHalfExposedPixels(img, states, box):
    imgBox = Box(0, img.size[1] - 1, 0, img.size[0] - 1)
    box = ClampBox(box, imgBox)
    radius = 5
    radiusSqr = radius ** 2
    for xy in BoxIter(box):
        if states.Get(xy) is StateTypes.hidden and IsPixelFree(img, xy):
            checkBox = CreateBoxFromCenterAndSize(xy,(radius, radius))
            checkBox = ClampBox(checkBox, box)
            for checkXY in BoxIter(checkBox):
                #pixel = img.getpixel(checkXY)
                #if pixel == wallColor:
                #    continue
                state = states.Get(checkXY)
                if state is not StateTypes.fullyExposed:
                    continue
                if not IsInCircle(xy, radiusSqr, checkXY):
                    continue
                states.Set(xy, StateTypes.halfExposed)
                break
        """
        if states.Get(xy) == StateTypes.fullyExposed:
            checkBox = CreateBoxFromCenterAndSize(xy,(radius, radius))
            checkBox = ClampBox(checkBox, box)
            for checkXY in BoxIter(checkBox):
                pixel = img.getpixel(checkXY)
                if pixel == wallColor:
                    continue
                state = states.Get(checkXY)
                if state == StateTypes.fullyExposed:
                    continue
                if not IsInCircle(xy, radiusSqr, checkXY):
                    continue
                states.Set(checkXY, StateTypes.halfExposed)
                """
def IsInLOS(point1, point2, img):
    #TODO - implement function

    return True

#using the current LoS method leaves behind artifacts in the hidden/exposed differentiating
#this just goes to every hidden pixel and asks if it has too few hidden neighbors
#if it has 0, or 1, then it's considered an artifact
def CleanupHiddenArtifacts(states:TwoDList, box:Box):
    statesBox = CreateBoxFromCorners((0,0), (states.sizeXY[0] - 1, states.sizeXY[1] - 1))
    for xy in BoxIter(box):
        if states.Get(xy) == StateTypes.fullyExposed:
            continue
        #count the number of non-exposed pixels directly neighboring the pixel
        neighborFilledCount = 0
        for point in UpDownLeftRightIter(xy):
            if statesBox.IsPointInBox(point):
                if states.Get(point) != StateTypes.fullyExposed:
                    neighborFilledCount += 1
        #if it has too few filled neighbors, then it's an artifact
        if neighborFilledCount < 2:
            #print("klsjdfklsdjf")
            states.Set(xy, StateTypes.fullyExposed)

def ExposeCircle(img:Image.Image, states:TwoDList, center:tuple, radius:float, considerLOS:bool = True):
    radiusSqr = radius ** 2
    imgBox = Box(0, img.size[1] - 1, 0, img.size[0] - 1)
    boxOfPixels = CreateBoxFromCenterAndSize(center, (radius, radius))
    boxOfPixels = ClampBox(boxOfPixels, imgBox)

    if considerLOS:
        #cast a ray from the center to each pixel in the circumference
        for xy in CircleCircumferenceIter(center, radius):
            dir = numpy.subtract(xy, center)
            norm = dir / numpy.linalg.norm(dir)
            for r in range(1, radius):
                ray = norm * r
                point = numpy.add(center, ray)
                point = (int(point[0]), int(point[1]))
                if not imgBox.IsPointInBox(point):
                    break
                #print(img.getpixel(point))
                if img.getpixel(point) == wallColor:
                    break
                states.Set(point, StateTypes.fullyExposed)
    else:
        for xy in BoxIter(boxOfPixels):
            #print(xy)
            if not IsInCircle(center, radiusSqr, xy):
                #print(str(xy) + " is not in the circle")
                continue
            pixel = img.getpixel(xy)
            if pixel == wallColor:
                continue
            if considerLOS and not IsInLOS(center, xy, img):
                continue
            states.Set(xy, StateTypes.fullyExposed)

#This function modifies the working copy image.
#It only modifies the potentially changed pixels (those that would be within the box)
def CreateExposedImage(img:Image.Image, states:TwoDList, changesBox:Box):
    box = Box(0, states.sizeXY[1] - 1, 0, states.sizeXY[0] - 1)
    changesBox = ClampBox(changesBox, box)
    for xy in BoxIter(changesBox):
        state = states.Get(xy)
        colorOfState = GetColorFromState(state)
        pixelColor = img.getpixel(xy)
        if pixelColor == freeSpaceColor:
            continue
        img.putpixel(xy, colorOfState)
        #print(xy)
        #colors.Set(xy, colorOfState)
    #print("Done")

#the entire fog of war function
def RunFogOfWarCalculator(dir, filename, pos, radius, considerLOS = True):
    fowTimer = Timer("Total Fog of War")
    print("\n{:~^40}".format(" Starting FoW "))
    #mapName = "caverns_test"
    #workingCopyName = "WorkingCopy"
    #defaultMapDirPath = file_stuff.GetUserDir() + "/Pictures/" + filename + "/"
    #defaultMapFilePath = defaultMapDirPath + filename + ".png"
    #workingCopyFilename = filename + 

    defaultMapFilePath = dir + "/" + filename + ".png"
    workingCopyFilename = filename + workingCopyFilenameAddition
    workingCopyFilePath = dir + "/" + workingCopyFilename
    statesFilename = filename + "_states"
    statesFilePath = dir + "/" + statesFilename

    #print(pos)
    #print(defaultMapFilePath)
    defaultImage = Image.open(defaultMapFilePath)
    if defaultImage is None:
        print("Couldn't open image.")
        return
    else:
        print("Opened it!")

    
    #print("default image mode: " + str(defaultImage.getbands()))
    #defaultImage.mode()
    #SetupGlobalColors(defaultImage.getbands())
    #bands = defaultImage.getbands()
    #SetupGlobalColors(bands)
    #print([b for b in bands])
    SetupGlobalColors(defaultImage.mode)

    states = None
    if FindInList(file_stuff.GetOnlyFilesInDirectory(dir), statesFilename) is not None:
        states = file_stuff.UnpickleObject(statesFilePath)
    else:
        print("Couldn't find states file. Creating new one.")
        states = TwoDList(defaultImage.size, StateTypes.hidden)
    #workingImg = Image.new("RGB", defaultImage.size)
    workingImg = None# = Image.open(defaultMapDirPath + workingCopyName +".png")
    if FindInList(file_stuff.GetOnlyFilesInDirectory(dir),workingCopyFilename) is not None:
        workingImg = Image.open(workingCopyFilePath)
    else:
        print("Couldn't find working copy, making a new one.")
        workingImg = Image.new("RGB", defaultImage.size)

    exposeTimer = Timer("Expose")
    ExposeCircle(defaultImage, states, pos, radius, considerLOS)
    exposeTimer.PrintTime()
    padding = 10
    imgBox = CreateBoxFromCorners((0,0), (defaultImage.size[0] - 1, defaultImage.size[1] - 1))
    changesBox = CreateBoxFromCenterAndSize(pos, (radius + padding, radius + padding))
    changesBox = ClampBox(changesBox, imgBox)

    halfExposedTimer = Timer("Half Exposed")
    FindHalfExposedPixels(defaultImage, states, changesBox)
    halfExposedTimer.PrintTime()

    clearArtifactsTimer = Timer("Clear Artifacts")
    CleanupHiddenArtifacts(states, changesBox)
    clearArtifactsTimer.PrintTime()

    createTimer = Timer("Create")
    CreateExposedImage(workingImg, states, changesBox)
    createTimer.PrintTime()

    file_stuff.PickleObject(states, statesFilePath)
    workingImg.save(workingCopyFilePath)
    fowTimer.PrintTime()
    print("{:~^40}\n".format(" FoW Finished "))
    
center = (104,195)
center = (139,373)
center = (272, 334)

#print(IsInCircle((100,100),100 ** 2, (10,10)))

#for xy in BoundOfBoxIter(Box(0,10,0,10), True):
#    print(xy)
"""
list = TwoDList((10,10), (0,0,0))

for i in range(0,len(list.list)):
    list.list[i] = (i,i,i)

filename = "C:/Users/Frank/Pictures/caverns_test/blah"
#list.ToFile(filename)
file_stuff.PickleObject(list, filename)
list2 = file_stuff.UnpickleObject(filename)
#list2.FromFile(filename)

print(list2.sizeXY)
for i in range(0,len(list2.list)):
    print(list2.list[i])
"""
#list = [(255,255,255),(255,255,255),(255,255,255)]
#byteList = bytearray(list)
#file = open("C:/Users/Frank/Pictures/caverns_test/blah", 'w')
#file.write(str(byteList))

#RunFogOfWarCalculator("C:/Users/Frank/Pictures/caverns_test", "caverns_test", (100,100), 100)

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

#this is the pyqt5 display stuffs
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.defaultTitle = 'Fog of War'
        self.title = self.defaultTitle
        self.left = 300
        self.top = 10
        self.width = 640
        self.height = 480
        self.topLeftPixelOffset = (8,31)
        self.initUI()

    def LoadWorkingCopy(self):

        if file_stuff.IsFileInDir(self.dir, self.workingCopyFilename):
            self.pixmap = QPixmap(self.workingCopyFilePath)
            self.image = self.pixmap.toImage()
            self.label.setPixmap(self.pixmap)
            self.resize(self.pixmap.width(),self.pixmap.height())
        else:
            print("Could not find working copy. Loading original map.\nChoose starting location.")
            self.pixmap = QPixmap(self.filepath)
            self.image = self.pixmap.toImage()
            self.label.setPixmap(self.pixmap)
            self.resize(self.pixmap.width(),self.pixmap.height())
           
        #print("Image format: " + str(self.image.format()))
        #print(self.image.format().Format_RGB888)
        #print(PyQt5.Qt.QImage.Format_RGB888)
        #PyQt5.Qt.QImage
        #PyQt5.Qt.QImage.format
        #Qt.
        self.show()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #print(file_stuff.GetUserDir())
        #opens the dialog to get the file
        self.filepath = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, "Open Original Map File", file_stuff.GetUserDir() + "/Pictures", "*.png")[0]

        #if the filepath isn't valid, then exit the program
        if self.filepath == "":
            #print("KLSJDFLKSJDFKLSDF")
            #QApplication.exit(0)
            #PyQt5.QtCore.QCoreApplication.exit(0)
            #quit()
            PyQt5.QtCore.QCoreApplication.exit(0)
            #quit()
            #sys.exit(0)
            #self.close()
            return

        #print(self.filepath)
        pair = os.path.split(self.filepath)
        self.dir = pair[0]
        pair = os.path.splitext(pair[1])
        self.mapFilename = pair[0]
        
        #if not file_stuff.IsFileInDir(self.dir, self.mapFilename):
        #    PyQt5.QtCore.QCoreApplication.exit(0)
        #    return

        if pair[1] is not ".png":
            print("WARNING: only works with pngs!")

        self.workingCopyFilename = self.mapFilename + workingCopyFilenameAddition
        self.workingCopyFilePath = self.dir + "/" + self.workingCopyFilename 
        self.label = QLabel(self)
        self.radius = 100
        self.considerLOS = True
        self.LoadWorkingCopy()
        #print(os.path.splitext( self.mapFilename))

        #self.mapFileDir = self.dir + "/" + self.mapFilename
        #self.workingCopyFileDir = self.dir + "/" + self.workingCopyFilename
        #print(self.dir)
        #print(self.mapFileName)
        #self.LoadWorkingCopy()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_R:
            text, ok = PyQt5.QtWidgets.QInputDialog.getText(self, 'Radius', 'Enter the desired radius. 5 = ~1x1 grid.')
            if ok:
                val = 0
                try:
                    val = int(text)
                except ValueError:
                    print("Do you not know what a number is?")
                    val = 100
                self.radius = val
                print("Setting radius: " + str(self.radius))
        elif QKeyEvent.key() == Qt.Key_L:
            self.considerLOS = not self.considerLOS
            print("Considering LoS is now " + str(self.considerLOS))
        elif QKeyEvent.key() == Qt.Key_Escape:
            PyQt5.QtCore.QCoreApplication.exit(0)
            #QCoreApplication.quit()
        return super().keyPressEvent(QKeyEvent)

    def mousePressEvent(self, QMouseEvent):
        self.pixmap
        if QMouseEvent.button() == Qt.LeftButton:
            print("Left mouse button pressed")
            mPos = QtGui.QCursor.pos() - self.pos()
            #8,31
            mPos.setX(mPos.x() - self.topLeftPixelOffset[0])
            mPos.setY(mPos.y() - self.topLeftPixelOffset[1])
            pixel = self.image.pixelColor(mPos).getRgb()
            #print("Pixel color: " + str(pixel))
            #print(freeSpaceColor)
            #print("Mouse pos in window: " + str((mPos.x(), mPos.y())))
            
            if pixel[0] == freeSpaceColor[0] and pixel[1] == freeSpaceColor[1] and pixel[2] == freeSpaceColor[2]:
                #RunFogOfWarCalculator(self.defaultMapFilename, (mPos.x(), mPos.y()), 100)
                #self.title = 'Working...
                self.setWindowTitle('Working...')
                #self.show()
                RunFogOfWarCalculator(self.dir, self.mapFilename, (mPos.x(), mPos.y()), self.radius, self.considerLOS)
                #self.title = defaultTitle
                self.setWindowTitle(self.defaultTitle)
                self.LoadWorkingCopy()
            else:
                print("Clicked on a non-white pixel. Can only be done from a white pixel.")
                
        return super().mousePressEvent(QMouseEvent)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


"""
print("Hit enter to end the program.")
input()
"""