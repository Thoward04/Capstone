import matplotlib.pylab as plt
from skimage.morphology import skeletonize 
import numpy as np
import cv2

# Load image
im = cv2.imread('maze.jpg')

# Define the colour we want to find - remember OpenCV uses BGR ordering
blue = [254,0,0]
# green = [0,255,0]
# red = [0,0,255]
purple = [125,0,86]

# Get X and Y coordinates of all x(color) pixels
YB, XB = np.where(np.all(im==blue,axis=2))
#formerly green, changed to purple, too lazy to change variables
YG, XG = np.where(np.all(im==purple,axis=2))
# YR, XR = np.where(np.all(im==red,axis=2))

# print(XB,YB)
# print(XG,YG)
# print(XR,YR)

midBX = (len(XB) )//2
finishX = (XB[midBX])
midBY = (len(YB) )//2
finishY = (YB[midBY])

midGX = (len(XG) )//2
startX = (XG[midGX])
midGY = (len(YG) )//2
startY = (YG[midGY])

# print(startX, startY)
# print(finishX, finishY)

originalImage = cv2.imread('maze.jpg')
grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
  
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
 
# cv2.imshow('BW', blackAndWhiteImage)
# cv2.imshow('Original image',originalImage)
# cv2.imshow('Gray image', grayImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.imwrite('maze-1.jpg', blackAndWhiteImage)

img_name = 'maze-1.jpg'
rgb_img = plt.imread(img_name)

# plt.figure(figsize=(14,14))
plt.imshow(rgb_img)

# plt.figure(figsize=(14,14))
plt.imshow(rgb_img)

x0,y0 = startX, startY #start x,y point
x1,y1 = finishX, finishY #finish x,y point

plt.plot(x0,y0, 'gx', markersize = 7)
plt.plot(x1,y1, 'rx', markersize = 7)
# #plt.show()

if rgb_img.shape.__len__()>2:
    thr_img = rgb_img[:,:,0] > np.max(rgb_img[:,:,0])/2
else:
    thr_img = rgb_img > np.max(rgb_img)/2
skeleton = skeletonize(thr_img)
# plt.figure(figsize=(14,14))
plt.imshow(skeleton)
#map of routes.
mapT = ~skeleton
plt.imshow(mapT)
plt.plot(x0,x0, 'gx', markersize=7)
plt.plot(x1,y1, 'rx', markersize=7)

_mapt = np.copy(mapT)

#searching for our end point and connect to the path.
boxr = 50

#Just a little safety check, if the points are too near the edge, it will error.
if y1 < boxr: y1 = boxr
if x1 < boxr: x1 = boxr

cpys, cpxs = np.where(_mapt[y1-boxr:y1+boxr, x1-boxr:x1+boxr]==0)
#calibrate points to main scale.
cpys += y1-boxr
cpxs += x1-boxr
#find clooset point of possible path end points
idx = np.argmin(np.sqrt((cpys-y1)**2 + (cpxs-x1)**2))
y, x = cpys[idx], cpxs[idx]

pts_x = [x]
pts_y = [y]
pts_c = [0]

#mesh of displacements.
xmesh, ymesh = np.meshgrid(np.arange(-1,2),np.arange(-1,2))
ymesh = ymesh.reshape(-1)
xmesh = xmesh.reshape(-1)

dst = np.zeros((thr_img.shape))
               
#Breath first algorithm exploring a tree
while(True):
    #update distance.
    idc = np.argmin(pts_c)
    ct = pts_c.pop(idc)
    x = pts_x.pop(idc)
    y = pts_y.pop(idc)
    #Search 3x3 neighbourhood for possible
    ys,xs = np.where(_mapt[y-1:y+2,x-1:x+2] == 0)
    #Invalidate these point from future searchers.
    _mapt[ys+y-1, xs+x-1] = ct
    _mapt[y,x] = 9999999
    #set the distance in the distance image.
    dst[ys+y-1,xs+x-1] = ct+1
    #extend our list.s
    pts_x.extend(xs+x-1)
    pts_y.extend(ys+y-1)
    pts_c.extend([ct+1]*xs.shape[0])
    #If we run of points.
    if pts_x == []:
        break
    if np.sqrt((x-x0)**2 + (y-y0)**2) <boxr:
        edx = x
        edy = y
        break
# plt.figure(figsize=(14,14))
plt.imshow(dst)

path_x = []
path_y = []

y = edy
x = edx
#Traces best path
while(True):
    nbh = dst[y-1:y+2,x-1:x+2]
    nbh[1,1] = 9999999
    nbh[nbh==0] = 9999999
    #If we reach a deadend
    if np.min(nbh) == 9999999:
        break
    idx = np.argmin(nbh)
    #find direction
    y += ymesh[idx]
    x += xmesh[idx]
    
    if np.sqrt((x-x1)**2 + (y-y1)**2) < boxr:
        print('Optimum route found.')
        break
    path_y.append(y)
    path_x.append(x)

    plt.figure(figsize=(14,14))
    plt.imshow(rgb_img)
    plt.plot(path_x,path_y, 'r-', linewidth=5)
plt.show()
    
