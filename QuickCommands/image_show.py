import cv2
# display an image stored in `img` until any key is pressed


def image_show(img, img_name="my image"):
    cv2.imshow(img_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return
