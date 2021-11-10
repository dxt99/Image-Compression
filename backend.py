import numpy as np
from PIL import Image
import math
import sys
import time

def imageToMatRGB(ar):
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

def matToImageRGB(matR,matG,matB,compressed):
    tempMatRGB=[[[0,0,0] for j in range(np.shape(matR)[1])] for i in range(np.shape(matR)[0])]
    for i in range(np.shape(matR)[0]):
        for j in range(np.shape(matR)[1]):
            tempMatRGB[i][j]=[matR[i,j],matG[i,j],matB[i,j]]
    matRGB=np.array(tempMatRGB)
    im = Image.fromarray(matRGB)
    im.save(compressed) #filename probably needs to change
    
def sumPol(m1,m2): #Penjumlahan Polinom
    lenM1 = len(m1)
    lenM2 = len(m2)
    if (lenM1 > lenM2) :
        m3  = [0 for i in range(lenM1)]
        for i in range(lenM2):
            m3[i] = m1[i] + m2[i]
        for i in range(lenM1-lenM2):
            i += lenM2
            m3[i] = m1[i]
        return m3
    elif (lenM1 < lenM2) :
        m3 = [0 for i in range(lenM2)]
        for i in range(lenM1):
            m3[i] = m1[i] + m2[i]
        for i in range(lenM2-lenM1):
            i += lenM1
            m3[i] = m2[i]
        return m3
    else:
        m3 = [0 for i in range(lenM1)]
        for i in range(lenM1):
            m3[i] = m1[i] + m2[i]
        return m3
    
def subsPol(m1, m2): #Pengurangan Polinom
    lenM1 = len(m1)
    lenM2 = len(m2)
    if (lenM1 > lenM2) :
        m3  = [0 for i in range(lenM1)]
        for i in range(lenM2):
            m3[i] = m1[i] - m2[i]
        for i in range(lenM1-lenM2):
            i += lenM2
            m3[i] = m1[i]
        return m3
    elif (lenM1 < lenM2) :
        m3 = [0 for i in range(lenM2)]
        for i in range(lenM1):
            m3[i] = m1[i] - m2[i]
        for i in range(lenM2-lenM1):
            i += lenM1
            m3[i] = -m2[i]
        return m3
    else:
        m3 = [0 for i in range(lenM1)]
        for i in range(lenM1):
            m3[i] = m1[i] - m2[i]
        return m3

def mulPol(m1, m2): #Perkalian Polinom
    lenM1 = len(m1)
    lenM2 = len(m2)
    lenM3 = lenM1 + lenM2 - 1
    m3 = [0 for i in range(lenM3)]
    for i in range(lenM1):
        for j in range(lenM2):
            m3[i+j] += m1[i]*m2[j]
    return m3

def subMatrix(mat,row, col):
    subMat = [[[0,0] for j in range(len(mat)-1)] for i in range(len(mat)-1)]
    subRow = 0
    subCol = 0
    for i in range(len(mat)):
        for j in range(len(mat)):
            if(i != row) and (j!= col):
                subMat[subRow][subCol] = mat[i][j]
                subCol+=1
                if(subCol == len(subMat)):
                    subRow+=1
                    subCol=0

    return subMat

def detMatrixPol(m): #Mendapatkan Determinan dalam bentuk Polinom (array), dengan masukan m = lambda(I) - A
    det = [0 for i in range(len(m) + 1)]
    if (len(m) == 2):
        return (subsPol(mulPol(m[0][0], m[1][1]), mulPol(m[0][1], m[1][0])))
    else :
        for i in range(len(m)):
            if(i % 2 == 0):
                temp = mulPol(m[i][0],detMatrixPol(subMatrix(m, i, 0)))
                det = sumPol(det, temp)
            else:
                temp = mulPol(m[i][0],detMatrixPol(subMatrix(m, i, 0)))
                det = subsPol(det, temp) 
    return det

def invMatDet(m): #Memutar posisi matriks determinan agar pangkat terbesar di posisi indeks 1 agar dapat np.roots
    idxTemp = len(m)-1
    matRes = [0 for i in range(len(m))]
    for i in range(len(m)):
        matRes[i] = m[idxTemp]
        idxTemp -=1
    return matRes

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

'''
mat = [[[-5, 1], [-4], [3]], #contoh
        [[-4], [-5, 1], [3]], 
        [[3], [3], [-2, 1]]]
print((invMatDet(detMatrixPol(mat))))
'''

if __name__ == '__main__':
    #Image to matrix
    t_start=time.time()
    filename=sys.argv[1]
    im=Image.open(filename)
    ar=np.array(im)
    if (len(np.shape(ar))==3): #RGB
        mats=imageToMatRGB(ar)
    else: #BW
        mats=ar
    sv_used=sys.argv[3]
 
    #matrix calculation here
    #Case 1: RGB, mats: array of 3 matrices, each n*m.
    #        Just SVD each array seperately
    #Case 2: BW, mats: a matrix, size n*m, normal SVD
    #Number of singular value used: sv_used (MAY NOT BE INTEGER)
    if (len(np.shape(ar))==3):
        #Case 1
        for i in range(3):
            mat=mats[i]
            #SVD mat
            mats[i]=mat
    else:
        #Case 2
        mat=mats
        #SVD mat
        mats=mat
    
    #Outputs
    compressed=sys.argv[2]
    if (len(np.shape(ar))==3): #RGB
        matToImageRGB(mats[0],mats[1],mats[2],compressed)
    else:
        im = Image.fromarray(mats)
        im.save(compressed)    
    t_end=time.time()
    print(t_end-t_start)
