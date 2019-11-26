import cv2 as cv

img = cv.imread(r"orgin_images/arrow_up", 0)
# cv.imshow(" ", img)

if cv.waitKey(100) & 0xff == ord('q'):
    cv.destroyAllWindows()

cv.destroyAllWindows()
