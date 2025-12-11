import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageProcessingDemo.src.utils.response import build_response_enhance
from components.ImageProcessingDemo.src.models.PackageModel import PackageModel


class Enhance(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        self.image = self.request.get_param("inputImage")

        self.enhance_type = self.request.get_param("configEnhanceType")

        self.method = self.enhance_type.get("value")

        if self.method == "brightness":
            self.amount = self.enhance_type.get("configBrightnessAmount")

        elif self.method == "sharpen":
            kernel_cfg = self.enhance_type.get("configSharpenKernel", {})
            self.kernel = kernel_cfg.get("value")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        img = Image.get_frame(self.image, self.redis_db)
        frame = np.asarray(img.value, dtype=np.uint8)

        if self.method == "brightness":
            result = cv2.convertScaleAbs(frame, alpha=1.0, beta=self.amount)

        elif self.method == "sharpen":
            if self.kernel == "kernel3":
                k = np.array([[0, -1, 0],
                              [-1, 5, -1],
                              [0, -1, 0]], np.float32)
            else:
                k = np.array([
                    [0, -1, -1, -1, 0],
                    [-1, 2, -4, 2, -1],
                    [-1, -4, 13, -4, -1],
                    [-1, 2, -4, 2, -1],
                    [0, -1, -1, -1, 0]
                ], np.float32)

            result = cv2.filter2D(frame, -1, k)

        else:
            result = frame

        img.value = result
        self.outputEnhancedImage = Image.set_frame(img, self.uID, self.redis_db)

        return build_response_enhance(self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
