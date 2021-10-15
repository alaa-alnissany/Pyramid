import cv2
import numpy as np


class Pyramids:
    status = True  # down
    numOfPyr = 3
    method = ["Gaussian Pyramids", "bilateral filter", "Guided filter"]
    methodNum = 0
    pyrS = []
    # guided filter param
    r = 3
    eps = 100

    def __init__(self, image, _status=True, num_of_pyr=3, method_num=0):
        self.img = image
        self.status = _status
        self.numOfPyr = num_of_pyr
        self.methodNum = method_num

    def __set__(self, _status=True, num_of_pyr=3, method_num=0):
        self.status = _status
        self.numOfPyr = num_of_pyr
        self.methodNum = method_num

    def __get__(self):
        print("Statue is Down") if self.status else print("Statue is Up")
        print("Number of pyramids is " + str(self.numOfPyr))
        print("Used kernel is "+self.method[self.methodNum])

    def downSamble(self, image):
        dc = image[:, range(0, image.shape[1], 2)]
        destination = dc[range(0, image.shape[0], 2), :]
        return destination

    def upSamble(self, image):
        sp = 2
        width = int(image.shape[1]*sp)
        height = int(image.shape[0]*sp)
        dim = (width, height)
        destination = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return destination

    def guided_Fitler(self, I, p, r, eps):
        """
        This is a guided filter implementation depends on opencv
        For more info about guided filter, please refer to
        https://en.wikipedia.org/wiki/Guided_filter
        :parms
        I: guided image
        p: filtering input image
        r: window radius
        eps: regularization
        :return
        filtering output q
        """
        k_size = 2 * r + 1
        I = I.astype(np.float32)
        P = p.astype(np.float32)

        mean_i = cv2.blur(I, (k_size, k_size), borderType=cv2.BORDER_REFLECT_101)
        mean_p = cv2.blur(P, (k_size, k_size), borderType=cv2.BORDER_REFLECT_101)
        corr_i = cv2.blur(I * I, (k_size, k_size), borderType=cv2.BORDER_REFLECT_101)
        corr_ip = cv2.blur(I * P, (k_size, k_size), borderType=cv2.BORDER_REFLECT_101)

        var_i = corr_i - mean_i * mean_i
        cov_ip = corr_ip - mean_i * mean_p

        a = cov_ip / (var_i + eps)
        b = mean_p - a * mean_i

        a = cv2.blur(a, (k_size, k_size), borderType=cv2.BORDER_REFLECT_101)
        b = cv2.blur(b, (k_size, k_size), borderType=cv2.BORDER_REFLECT_101)

        q = a * I + b
        return q.astype(np.uint8)

    def pyr(self):
        layer: object = self.img.copy()
        if self.methodNum == 0:
            for i in range(self.numOfPyr):
                if self.status:
                    # using pyrDown() function
                    layer = cv2.pyrDown(layer)
                    self.pyrS.append(layer)
                else:
                    # using pyrUp() function
                    layer = cv2.pyrUp(layer)
                    self.pyrS.append(layer)
        elif self.methodNum == 1:
            for i in range(self.numOfPyr):
                layer = cv2.bilateralFilter(layer, 11, 75, 75)
                if self.status:
                    # using pyrDown() function
                    layer = self.downSamble(layer)
                    self.pyrS.append(layer)
                else:
                    # using pyrUp() function
                    layer = self.upSamble(layer)
                    self.pyrS.append(layer)
        elif self.methodNum == 2:
            for i in range(self.numOfPyr):
                layer = self.guided_Fitler(layer, layer, r=3, eps=100)
                print('alaa')
                if self.status:
                    # using pyrDown() function
                    layer = self.downSamble(layer)
                    self.pyrS.append(layer)
                else:
                    # using pyrUp() function
                    layer = self.upSamble(layer)
                    self.pyrS.append(layer)
        else:
            pass