import cv2


class Pyramids:
    status = True  # down
    numOfPyr = 3
    pyrS = []

    def __init__(self, image, _status=True, num_of_pyr=3):
        self.img = image
        self.statue = _status
        self.numOfPyr = num_of_pyr

    def __set__(self, _status, num_of_pyr):
        self.statue = _status
        self.numOfPyr = num_of_pyr

    def __get__(self):
        print("Statue is " + str(self.status))
        print("Number of pyramids is " + str(self.numOfPyr))

    def pyr(self):
        layer = self.img.copy()
        for i in range(self.numOfPyr):
            if self.status:
                # using pyrDown() function
                layer = cv2.pyrDown(layer)
                self.pyrS.append(layer)
            else:
                # using pyrUp() function
                layer = cv2.pyrUp(layer)
                self.pyrS.append(layer)

