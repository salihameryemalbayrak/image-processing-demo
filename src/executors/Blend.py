import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageProcessingDemo.src.utils.response import build_response_blend
from components.ImageProcessingDemo.src.models.PackageModel import PackageModel


class Blend(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        self.imageA = self.request.get_param("inputImageA")
        self.imageB = self.request.get_param("inputImageB")

        self.mode = self.request.get_param("ConfigBlendMode")

        if self.mode == "BlendAlpha":
            self.strength = self.request.get_param("ConfigBlendStrength")

        elif self.mode == "BlendMask":
            self.smooth = self.request.get_param("ConfigUseSmoothMask")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def resize_to_match(self, A, B):
        if A.shape[:2] != B.shape[:2]:
            B = cv2.resize(B, (A.shape[1], A.shape[0]))
        return A, B

    def run(self):
        imgA = Image.get_frame(self.imageA, self.redis_db)
        imgB = Image.get_frame(self.imageB, self.redis_db)

        A = np.asarray(imgA.value, dtype=np.uint8)
        B = np.asarray(imgB.value, dtype=np.uint8)

        A, B = self.resize_to_match(A, B)

        if self.mode == "BlendAlpha":
            alpha = float(self.strength)
            blended = cv2.addWeighted(A, alpha, B, 1 - alpha, 0)
            mask = cv2.absdiff(A, B)

        else:
            diff = cv2.absdiff(A, B)
            mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            if bool(self.smooth):
                mask = cv2.GaussianBlur(mask, (7, 7), 0)

            mask3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            mask_f = mask3.astype(np.float32) / 255.0

            blended = (A * mask_f + B * (1 - mask_f)).astype(np.uint8)
            mask = mask3

        imgA.value = blended
        self.outputBlendedImage = Image.set_frame(imgA, self.uID, self.redis_db)

        imgB.value = mask
        self.outputMaskImage = Image.set_frame(imgB, self.uID, self.redis_db)

        return build_response_blend(self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
