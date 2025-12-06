import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageProcessingDemo.src.utils.response import build_response_blend
from components.ImageProcessingDemo.src.models.PackageModel import PackageModel


class Blend(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        self.img1 = self.request.get_param("inputImageOne")
        self.img2 = self.request.get_param("inputImageTwo")

        self.mode = self.request.get_param("ConfigBlendType")
        self.value = self.request.get_param(f"{self.mode}Value")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def blend_images(self, a, b):
        a = np.asarray(a).astype(np.float32)
        b = np.asarray(b).astype(np.float32)

        mask = cv2.absdiff(a, b).astype(np.uint8)

        blended = cv2.addWeighted(a, 0.5, b, 0.5, 0)

        return blended.astype(np.uint8), mask

    def run(self):
        img1 = Image.get_frame(img=self.img1, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.img2, redis_db=self.redis_db)

        blended, mask = self.blend_images(img1.value, img2.value)

        img1.value = blended
        img2.value = mask

        self.outputBlended = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.outputMask = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        return build_response_blend(self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
