# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 19:28:39 2013

@author: Stardrad
"""

import numpy as np
import matplotlib.pyplot as plt

def getData(fName):
    bitsTable = []
    yPSNRTable = []
    uPSNRTable = []
    vPSNRTable = []
    with open(fName, 'rb') as fSrc:
        for line in fSrc:
            bits, yPSNR, uPSNR, vPSNR = line.split(' ', 4)
            bitsTable.append(int(bits))
            yPSNRTable.append(float(yPSNR))
            uPSNRTable.append(float(uPSNR))
            vPSNRTable.append(float(vPSNR))
    return bitsTable, yPSNRTable, uPSNRTable, vPSNRTable
    
def mergeA(dataArray, factor = 8):
    firstRg = dataArray[len(dataArray) - 1][0] - dataArray[0][0]
    step = firstRg / factor
    retArray = []
    i = 0
    for low in xrange(dataArray[0][0], dataArray[len(dataArray) - 1][0], step):
        bsum,psum = 0,0.0
        sumNum = 0
        while True:
            if i == len(dataArray):
                break
            bitrate, PSNR = dataArray[i]            
            if low <= bitrate <= (low + step):
                bsum += bitrate
                psum += PSNR
                i += 1
                sumNum += 1
            else:
                break
        if sumNum > 0:
            retArray.append([bsum/sumNum, psum/sumNum])
    return retArray

video_name = 'Johnny'  
properties = ['1280x720', 60]
#typeStr = '_intra_'
#typeStr = '_lowdelay_'
#typeStr = '_lowdelayP_'
for i, typeStr in enumerate(['_intra_', '_lowdelay_', '_lowdelayP_', '_random_']):
    AVC_Name =  video_name + '_AVC' + typeStr + 'data.txt'
    HEVC_Name = video_name + '_HEVC' + typeStr + 'data.txt'
    
    AVC_Bits, AVC_YPSNR, AVC_UPSNR, AVC_VPSNR = getData(AVC_Name)
    HEVC_Bits, HEVC_YPSNR, HEVC_UPSNR, HEVC_VPSNR = getData(HEVC_Name)
    
    frames = np.arange(0, len(AVC_YPSNR))
  
    fig = plt.figure(i+1, figsize=(16,8))
    graphY = plt.subplot(221)
    graphU = plt.subplot(222)
    graphV = plt.subplot(223)
    graphBits = plt.subplot(224)
    
    lineJM, = graphY.plot(frames, AVC_YPSNR, 'r-')
    lineHM, = graphY.plot(frames, HEVC_YPSNR, 'b-')
    graphY.set_xlabel('Frame')
    graphY.set_ylabel('YPSNR')
    graphY.grid()
    
    
    graphU.plot(frames, AVC_UPSNR, 'r-')
    graphU.plot(frames, HEVC_UPSNR, 'b-')
    graphU.set_xlabel('Frame')
    graphU.set_ylabel('UPSNR')
    graphU.grid()
    
    graphV.plot(frames, AVC_VPSNR, 'r-')
    graphV.plot(frames, HEVC_VPSNR, 'b-')
    graphV.set_xlabel('Frame')
    graphV.set_ylabel('VPSNR')
    graphV.grid()
    
    

    AVC_BitRate = np.multiply(AVC_Bits, properties[1]) / 1000
    HEVC_BitRate = np.multiply(HEVC_Bits, properties[1]) / 1000
    graphBits.plot(frames, AVC_BitRate, 'r-')
    graphBits.plot(frames, HEVC_BitRate, 'b-')
    graphBits.set_xlabel('Frame')
    graphBits.set_ylabel('KBits/s')
    graphBits.grid()
    
    
    fig.legend((lineJM, lineHM), ('JM 18.5', 'HM 10.1'), loc='upper left')
    fig.suptitle('%s_%s_%dHz_%s' % (video_name, \
                properties[0], properties[1], typeStr[1:-1]), \
                fontsize = 22, weight = 'bold')
    #plt.figure(1)
    #plt.legend()
    
    #plt.show()
    plt.savefig(video_name + typeStr[:-1]+'.emf',transparent=True)
    print 'Output %s' % (video_name + typeStr[:-1]+'.emf')
    
AVC_Name =  video_name + '_AVC_' + 'Bitrate.txt'
HEVC_Name = video_name + '_HEVC_' + 'Bitrate.txt'
AVC_Bits, AVC_YPSNR, AVC_UPSNR, AVC_VPSNR = getData(AVC_Name)
HEVC_Bits, HEVC_YPSNR, HEVC_UPSNR, HEVC_VPSNR = getData(HEVC_Name)


AVC_BitRate = np.array(AVC_Bits) * 60/ 1024
HEVC_BitRate = np.array(HEVC_Bits) * 60/1024


AVC_AVGPSNR = (np.multiply(AVC_YPSNR, 6) + np.array(AVC_UPSNR) + np.array(AVC_VPSNR) ) / 8
HEVC_AVGPSNR = (np.multiply(HEVC_YPSNR, 6) + np.array(HEVC_UPSNR) + np.array(HEVC_VPSNR) ) / 8
#AVC_AVGPSNR = np.array(AVC_YPSNR)
#HEVC_AVGPSNR = np.array(HEVC_YPSNR)
fig = plt.figure(5, figsize=(12,6))
graph = fig.gca()

mDtype = [('Bitrate', 'i'),('PSNR', 'f')]
AVCArray = np.sort(np.array(zip(AVC_BitRate, AVC_AVGPSNR), dtype=mDtype), order='Bitrate')
HEVCArray = np.sort(np.array(zip(HEVC_BitRate, HEVC_AVGPSNR), dtype=mDtype), order='Bitrate')
AVCArray=mergeA(AVCArray, 8)
HEVCArray=mergeA(HEVCArray, 8)
AVC_BitRate, AVC_AVGPSNR = zip(*AVCArray)
HEVC_BitRate, HEVC_AVGPSNR = zip(*HEVCArray)

AVC_Coeff = np.polyfit(AVC_BitRate, AVC_AVGPSNR, 12)
HEVC_Coeff = np.polyfit(HEVC_BitRate, HEVC_AVGPSNR, 12)
AVC_Poly = np.poly1d(AVC_Coeff)
HEVC_Poly = np.poly1d(HEVC_Coeff)

#AVC_BitRate[len(AVC_BitRate) - 1]
AVC_Bits = np.linspace(0, 25000, 100)
HEVC_Bits = np.linspace(0, 25000, 100)

#graph.plot(AVC_BitRate, AVC_AVGPSNR, 'k-')
graph.plot(AVC_Bits, AVC_Poly(AVC_Bits), 'r-', label = 'JM 18.5')
#graph.plot(HEVC_BitRate, HEVC_AVGPSNR, 'k-')
graph.plot(HEVC_Bits, HEVC_Poly(HEVC_Bits), 'b-', label = 'HM 10.1')
graph.set_xlim(xmax=25000)
graph.set_xlabel('KBits/s')
graph.set_ylabel('$PSNR_{avg}$')
graph.grid()
graph.legend()
fig.suptitle('%s_%s_%dHz_%s' % (video_name, \
                properties[0], properties[1], 'random'), \
                fontsize = 22, weight = 'bold')
plt.savefig(video_name + '_Bitrate'+'.emf',transparent=True)
print 'Output %s' % (video_name + '_Bitrate'+'.emf')
