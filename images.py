import cv2

img = cv2.imread('C:\Users\alazarevic\Desktop\lseg_junk.png')
cv2.imshow('Shows Texture', img)
print(img.shape)
cv2.waitKey(0)
cv2.destroyAllWindows()
