import cv2
import matplotlib.pyplot as plt
import numpy as np

# provide path where images are saved
path1 = 'C:/IACV project/image3.jpg'
path2 = 'C:/IACV project/image1.jpg'
N = 512

img1 = cv2.imread(path1)
img1 = cv2.resize(img1, (N, N))
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
plt.figure()
plt.imshow(img1, cmap='gray')

plt.figure()
plt.hist(img1.ravel(),256,[0,256])
plt.show()

img2 = cv2.imread(path2)
img2 = cv2.resize(img2, (N, N))
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
plt.figure()
plt.imshow(img2, cmap='gray')

plt.figure()
plt.hist(img2.ravel(),256,[0,256])
plt.show()

#ENCRYPTION

a = 5
b = 7
itr = 40
mu = 900
gamma = 400

def cat_transform(img, N, a, b):
    tx_img = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            tx_img[i][j] = img[(i+a*j)%N][(b*i+(a*b+1)*j)%N]
    return tx_img

def cat_tx_iter(img, itr, a, b):
    for i in range(itr):
        tx_img = cat_transform(img, N, a, b)
        img = tx_img
    return tx_img

scrambled_img = cat_tx_iter(img1, itr, a, b)
plt.figure()
plt.imshow(scrambled_img, cmap='gray')

plt.figure()
plt.hist(scrambled_img.ravel(),256,[0,256])
plt.show()

g1 = mu - scrambled_img
g2 = mu - img2

def plip_add(g1, g2, N, gamma):
    encrypt_img = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            encrypt_img[i][j] = g1[i][j] + g2[i][j] - (g1[i][j]*g2[i][j])//gamma
    return encrypt_img

encrypt_img = plip_add(g1, g2, N, gamma)
plt.figure()
plt.imshow(encrypt_img, cmap='gray')

plt.figure()
plt.hist(encrypt_img.ravel(),256,[0,256])
plt.show()

# DECRYPTION

k = gamma
mu = 900
a = 5
b = 7
itr = 40

def plip_sub(g1, g2, N, k):
    decrypt_img = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            decrypt_img[i][j] = k*(g1[i][j]-g2[i][j])//(k-g2[i][j])
    return decrypt_img

decrypt_img = plip_sub(encrypt_img, g2, N, k)

obtained_scrambled_img = mu - decrypt_img

plt.figure()
plt.imshow(obtained_scrambled_img, cmap='gray')

plt.figure()
plt.hist(obtained_scrambled_img.ravel(),256,[0,256])
plt.show()

def inv_cat_transform(img, N, a, b):
    inv_tx_img = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            inv_tx_img[(i+a*j)%N][(b*i+(a*b+1)*j)%N] = img[i][j]
    return inv_tx_img

def inv_cat_tx_iter(img, itr, a, b):
    for i in range(itr):
        tx_img = inv_cat_transform(img, N, a, b)
        img = tx_img
    return tx_img

final = inv_cat_tx_iter(obtained_scrambled_img, itr, a, b)
plt.figure()
plt.imshow(final, cmap='gray')

plt.figure()
plt.hist(final.ravel(),256,[0,256])
plt.show()