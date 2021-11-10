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
 
def U(m):
    A = np.copy(m)
    AT = np.transpose(A)
    AAT = np.dot(A,AT)
    
    #eigen values
    mat=[]
    for i in range(np.shape(AAT)[0]):
        mat.append([])
        for j in range(np.shape(AAT)[1]):
            mat[i].append([])
            mat[i][j].append(AAT[i,j])
    for i in range(np.shape(AAT)[0]):
        mat[i][i].append(-1)
    poly=invMatDet(detMatrixPol(mat))
    poly=np.array(poly)
    roots=np.roots(poly)
    #eigen vectors
    vektor_eigen=[]
    for root in roots:
        mat=[]
        for i in range(np.shape(AAT)[0]):
            mat.append([])
            for j in range(np.shape(AAT)[1]):
                mat[i].append(AAT[i,j])
        for i in range(np.shape(AAT)[0]):
            mat[i][i]-=root
        mat=np.array(mat)
        pl, u = lu(mat, permute_l=True)
        vecs=gaussJordan(u)
        for i in range(len(vecs)):
            vektor_eigen.append(vecs[i])
     
    normal = np.copy(vektor_eigen)
    for i in range(len(normal)):
        normal[i] = np.divide(vektor_eigen[i],sqrt(vektor_eigen[i]))
    combine = normal[0]
    for j in range(1,len(normal)):
        combine = np.column_stack((combine,normal[j]))
    return combine

def sigma(m,sv_used):
    A = np.copy(m)
    AT = np.transpose(A)
    ATA = np.dot(AT,A)
    
    #eigen values
    mat=[]
    for i in range(np.shape(ATA)[0]):
        mat.append([])
        for j in range(np.shape(ATA)[1]):
            mat[i].append([])
            mat[i][j].append(ATA[i,j])
    for i in range(np.shape(ATA)[0]):
        mat[i][i].append(-1)
    poly=invMatDet(detMatrixPol(mat))
    poly=np.array(poly)
    nilai_eigen=np.roots(poly)
    
    singular = np.copy(nilai_eigen)
    n=len(singular)
    if (isinstance(sv_used) and sv_used>0 and sv_used<n):
        n=sv_used
    for i in range(n):
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
    
    #eigen values
    mat=[]
    for i in range(np.shape(ATA)[0]):
        mat.append([])
        for j in range(np.shape(ATA)[1]):
            mat[i].append([])
            mat[i][j].append(ATA[i,j])
    for i in range(np.shape(ATA)[0]):
        mat[i][i].append(-1)
    poly=invMatDet(detMatrixPol(mat))
    poly=np.array(poly)
    roots=np.roots(poly)
    #eigen vectors
    vektor_eigen=[]
    for root in roots:
        mat=[]
        for i in range(np.shape(ATA)[0]):
            mat.append([])
            for j in range(np.shape(ATA)[1]):
                mat[i].append(ATA[i,j])
        for i in range(np.shape(ATA)[0]):
            mat[i][i]-=root
        mat=np.array(mat)
        pl, u = lu(mat, permute_l=True)
        vecs=gaussJordan(u)
        for i in range(len(vecs)):
            vektor_eigen.append(vecs[i])
     
    normal = np.copy(vektor_eigen)
    for i in range(len(normal)):
        normal[i] = np.divide(vektor_eigen[i],sqrt(vektor_eigen[i]))
    combine = normal[0]
    for j in range(1,len(normal)):
        combine = np.column_stack((combine,normal[j]))
    combineT = np.transpose(combine)
    return combineT
    
def SVD(m,sv_used):
    matU=U(m)
    matS=sigma(m,sv_used)
    matV=VT(m)
    ret=np.dot(matU,matS)
    ret=np.dot(ret,matV)
    return ret
    

'''
mat = [[[-5, 1], [-4], [3]], #contoh
        [[-4], [-5, 1], [3]], 
        [[3], [3], [-2, 1]]]
print((invMatDet(detMatrixPol(mat))))
'''

if __name__ == '__main__':
    #Args handling
    filename=sys.argv[1]
    compressed=sys.argv[2]
    sv_used=sys.argv[3]
    
    #Image to matrix
    t_start=time.time()
    im=Image.open(filename)
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
            mats[i]=SVD(mat,sv_used)
    else:
        #Case 2
        mat=mats
        #SVD mat
        mats=SVD(mat,sv_used)
    
    #Outputs
    if (len(np.shape(ar))==3): #RGB
        matToImageRGB(mats[0],mats[1],mats[2],compressed)
    else:
        im = Image.fromarray(mats)
        im.save(compressed)    
    t_end=time.time()
    print(t_end-t_start)


'''
mat=[[2.,4.,4.,4.],[0.,2.,1.,2.],[0.,0.,1.,1.],[0.,0.,0.,0.]]
mat=np.array(mat)

a=(U(mat))
'''