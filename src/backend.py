import numpy as np
from PIL import Image
import math
import sys
import time
from scipy.linalg import lu

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

def matToImageRGB(matR,matG,matB,compressed,testcompressed):
    tempMatRGB=[[[0,0,0] for j in range(np.shape(matR)[1])] for i in range(np.shape(matR)[0])]
    for i in range(np.shape(matR)[0]):
        for j in range(np.shape(matR)[1]):
            tempMatRGB[i][j]=[matR[i,j],matG[i,j],matB[i,j]]
    matRGB=np.array(tempMatRGB)
    matRGB=matRGB.astype(np.uint8)
    im = Image.fromarray(matRGB)
    im.save(compressed)
    im.save(testcompressed)
    
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

def gaussJordan(m):
    ranks=[]
    #divide
    for i in range(np.shape(m)[0]):
        f=0
        d=1
        for j in range(np.shape(m)[1]):
            if f==0 and m[i,j]>0.00001:
                f=1
                d=m[i,j]
                m[i,j]=1
                ranks.append(j)
            else:
                m[i,j]/=d
    #add
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i,j]==1:
                for k in range(i-1,-1,-1):
                    arr=m[i]
                    arr=arr*(-1*m[k,j])
                    m[k]=np.add(arr,m[k])
                break
    #conquer
    ret=[]
    for j in range(np.shape(m)[1]):
        if j in ranks:
            continue
        ans=[]
        for i in range(np.shape(m)[0]):
            ans.append(m[i,j])
        ans[j]=1
        ans=np.array(ans)
        ret.append(ans)
    return ret

def simultaneous_power_iteration(A, k):
    n, m = A.shape
    Q = np.random.rand(n, k)
    Q, _ = np.linalg.qr(Q)
    Q_prev = Q
 
    for i in range(1000):
        Z = A.dot(Q)
        Q, R = np.linalg.qr(Z)

        # can use other stopping criteria as well 
        err = ((Q - Q_prev) ** 2).sum()

        Q_prev = Q
        if err < 1e-3:
            break

    return np.diag(R), Q
 
def U(m):
    A = np.copy(m)
    AT = np.transpose(A)
    A = np.array(A, dtype=np.int64)
    AT = np.array(AT, dtype=np.int64)
    AAT = np.dot(A, AT)
    eigen = simultaneous_power_iteration(np.array(AAT), len(AAT))
    vectorEigen = eigen[1]
    norm = []
    for j in range(len(vectorEigen[0])):
        temp = 0
        for i in range(len(vectorEigen)):
            temp += vectorEigen[i][j]**2
        temp = temp**(0.5)
        norm.append(temp)
    for j in range(len(vectorEigen[0])):
        for i in range(len(vectorEigen)):
            vectorEigen[i][j] = vectorEigen[i][j]/norm[j]
    return(vectorEigen)

def sigma(m):
    A = np.copy(m)
    AT = np.transpose(A)
    A = np.array(A, dtype=np.int64)
    AT = np.array(AT, dtype=np.int64)
    ATA= np.dot(AT, A)
    nilai_eigen= simultaneous_power_iteration(np.array(ATA), len(ATA))[0]
    result = np.zeros(np.shape(A))
    singular = np.copy(nilai_eigen)
    n=len(singular)
    for i in range(n):
        if (singular[i] < (10**(-8))) :
            singular[i] = 0
        else :
            singular[i] = math.sqrt(nilai_eigen[i])
    col = len(result[0])
    row = len(result)
    for i in range(row):
        for j in range(col):
            if row >= col :
                if i == j :
                    result[i][j] = singular[j]
            else :
                if i == j :
                    result[i][j] = singular[i]
    return result

def VT(m):
    A = np.copy(m)
    AT = np.transpose(A)
    A = np.array(A, dtype=np.int64)
    AT = np.array(AT, dtype=np.int64)
    ATA = np.dot(AT, A)
    searchEigen = simultaneous_power_iteration(np.array(ATA), len(ATA))
    vectorEigen = searchEigen[1]
    norm = []
    for j in range(len(vectorEigen[0])):
        temp = 0
        for i in range(len(vectorEigen)):
            temp += vectorEigen[i][j]**2
        temp = temp**(0.5)
        norm.append(temp)
    for j in range(len(vectorEigen[0])):
        for i in range(len(vectorEigen)):
            vectorEigen[i][j] = vectorEigen[i][j]/norm[j]
    return np.transpose(vectorEigen)

def SVD(m,percentCompress):
    matU=U(m)
    matS=sigma(m)
    matV=VT(m)
    sv = 0
    if (len(matS) > len(matS[0])):
        sv = len(matS[0])
    else:
        sv = len(matS)
    sv_used = int(np.round((int(percentCompress)/100)*sv)) #Masukan precentCompress dari 1-100 (semakin kecil, maka semakin banyak sv yang dibuang)
    matUCompressed = np.delete(matU,[i for i in range(sv_used,np.shape(matU)[1])], 1)
    matVCompressed = np.delete(matV,[i for i in range(sv_used,np.shape(matV)[0])], 0)
    matSCompressed = np.delete(matS,[i for i in range(sv_used,np.shape(matS)[1])], 1)
    matSCompressed = np.delete(matSCompressed,[i for i in range(sv_used,np.shape(matSCompressed)[0])], 0)
    ret = np.dot(np.dot(matUCompressed, matSCompressed), matVCompressed)
    for i in range(len(ret)):
        for j in range(len(ret[0])):
            ret[i][j] = np.round(ret[i][j])
    return ret
    

if __name__ == '__main__':
    #Args handling
    filename=sys.argv[1]
    compressed=sys.argv[2]
    percentCompress=sys.argv[3]
    testpath=sys.argv[4]
    testcompressed=sys.argv[5]
    
    #Image to matrix
    t_start=time.time()
    im=Image.open(filename)
    im.save(testpath)
    ar=np.array(im)
    if (len(np.shape(ar))==3): #RGB
        mats=imageToMatRGB(ar)
    else: #BW
        mats=ar
 
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
            mats[i]=SVD(mat,percentCompress)
    else:
        #Case 2
        mat=mats
        #SVD mat
        mats=SVD(mat,percentCompress)
    
    #Outputs
    if (len(np.shape(ar))==3): #RGB
        matToImageRGB(mats[0],mats[1],mats[2],compressed,testcompressed)
    else:
        im = Image.fromarray(mats)
        im.save(compressed)
        im.save(testcompressed)
    t_end=time.time()
    print(t_end-t_start)
