import numpy as np
from PIL import Image
import math

def imageToMat(filename):
    im=Image.open(filename)
    ar=np.array(im)
    tempMatR=[[0 for j in range(np.shape(ar)[1])] for i in range(np.shape(ar)[0])]
    tempMatG=[[0 for j in range(np.shape(ar)[1])] for i in range(np.shape(ar)[0])]
    tempMatB=[[0 for j in range(np.shape(ar)[1])] for i in range(np.shape(ar)[0])]
    for i in range(np.shape(ar)[0]):
        for j in range(np.shape(ar)[1]):
            tempMatR[i][j]=ar[i,j,0]
    for i in range(np.shape(ar)[0]):
        for j in range(np.shape(ar)[1]):
            tempMatG[i][j]=ar[i,j,1]
    for i in range(np.shape(ar)[0]):
        for j in range(np.shape(ar)[1]):
            tempMatB[i][j]=ar[i,j,2]
    matR=np.array(tempMatR)
    matG=np.array(tempMatG)
    matB=np.array(tempMatB)
    return [matR,matG,matB]

def matToImage(matR,matG,matB):
    tempMatRGB=[[[0,0,0] for j in range(np.shape(matR)[1])] for i in range(np.shape(matR)[0])]
    for i in range(np.shape(matR)[0]):
        for j in range(np.shape(matR)[1]):
            tempMatRGB[i][j]=[matR[i,j],matG[i,j],matB[i,j]]
    matRGB=np.array(tempMatRGB)
    im = Image.fromarray(matRGB)
    im.save("compressed.jpg") #filename probably needs to change

def sqrt(m):
    square = 0
    for i in range(len(m)):
        square += math.pow(m[i],2)
    root = math.sqrt(square)
    return root

def U(m):
    A = np.copy(m)
    AT = np.transpose(A)
    AAT = np.dot(A,AT)
    """
    Mencari nilai eigen dari AAT, lalu di-assign ke nilai_eigen
    Mencari vektor eigen dari nilai eigen, lalu di-assign ke vektor_eigen
    """
    normal = np.copy(vektor_eigen)
    for i in range(len(normal)):
        normal[i] = np.divide(vektor_eigen[i],sqrt(vektor_eigen[i]))
    combine = normal[0]
    for j in range(1,len(normal)):
        combine = np.column_stack((combine,normal[j]))
    return combine

def sigma(m):
    A = np.copy(m)
    AT = np.transpose(A)
    ATA = np.dot(AT,A)
    """
    Mencari nilai eigen yang tidak nol dari ATA, lalu di-assign ke nilai_eigen
    """
    singular = np.copy(nilai_eigen)
    for i in range(len(singular)):
        singular[i] = math.sqrt(nilai_eigen[i])
    result = np.zeros(np.shape(A))
    row = np.shape(result)[0]
    col = np.shape(result)[1]
    i = 0
    for j in range(row):
        for k in range(col):
            if (j == k):
                result[j][k] = nilai_eigen[i]
                i += 1
    return result

def VT(m):
    A = np.copy(m)
    AT = np.transpose(A)
    ATA = np.dot(AT,A)
    """
    Mencari nilai eigen dari ATA, lalu di-assign ke nilai_eigen
    Mencari vektor eigen dari nilai eigen, lalu di-assign ke vektor_eigen
    """
    normal = np.copy(vektor_eigen)
    for i in range(len(normal)):
        normal[i] = np.divide(vektor_eigen[i],sqrt(vektor_eigen[i]))
    combine = normal[0]
    for j in range(1,len(normal)):
        combine = np.column_stack((combine,normal[j]))
    combineT = np.transpose(combine)
    return combineT