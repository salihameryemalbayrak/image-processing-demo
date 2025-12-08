import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

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

        self.mode = self.request.get_param("ConfigEnhanceType")
        self.value = self.request.get_param(f"{self.mode}Value")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def enhance(self, img):
        img = np.asarray(img).astype(np.float32)

        if self.mode == "EnhanceBrightness":
            img = img * self.value

        elif self.mode == "EnhanceContrast":
            img = img * self.value + (128 * (1 - self.value))

        return np.clip(img, 0, 255).astype(np.uint8)

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.enhance(img.value)

        self.outputEnhanced = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

        return build_response_enhance(self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
