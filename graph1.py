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

video_name = 'Johnny'  
properties = ['1280x720', '60Hz']
#typeStr = '_intra_'
#typeStr = '_lowdelay_'
#typeStr = '_lowdelayP_'
typeStr = '_random_'
AVC_Name =  video_name + '_AVC' + typeStr + 'data.txt'
HEVC_Name = video_name + '_HEVC' + typeStr + 'data.txt'



AVC_Bits, AVC_YPSNR, AVC_UPSNR, AVC_VPSNR = getData(AVC_Name)
HEVC_Bits, HEVC_YPSNR, HEVC_UPSNR, HEVC_VPSNR = getData(HEVC_Name)

frames = np.linspace(1, len(AVC_YPSNR), len(AVC_YPSNR))


fig = plt.figure(1, figsize=(16,8))
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


graphBits.plot(frames[1:], AVC_Bits[1:], 'r-')
graphBits.plot(frames[1:], HEVC_Bits[1:], 'b-')
graphBits.set_xlabel('Frame')
graphBits.set_ylabel('Bits')
graphBits.grid()

fig.legend((lineJM, lineHM), ('JM 18.5', 'HM 10.1'), loc='best')
fig.suptitle(video_name + '_' +'_'.join(properties), fontsize = 22, weight = 'bold')
#plt.figure(1)
#plt.legend()

plt.show()
plt.savefig(video_name + typeStr+'.emf',transparent=True)
