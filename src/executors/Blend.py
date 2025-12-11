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

        self.blend_mode_cfg = self.request.get_param("configBlendMode")
        self.mode = self.blend_mode_cfg.get("value")

        if self.mode == "alphaBlend":
            self.strength = self.blend_mode_cfg.get("configBlendStrength")

        elif self.mode == "maskBlend":
            smooth_cfg = self.blend_mode_cfg.get("configUseSmoothMask", {})
            self.smooth = smooth_cfg.get("value", False)

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def resize_to_match(A, B):
        if A.shape[:2] != B.shape[:2]:
            B = cv2.resize(B, (A.shape[1], A.shape[0]))
        return A, B

    def run(self):
        imgA = Image.get_frame(self.imageA, self.redis_db)
        imgB = Image.get_frame(self.imageB, self.redis_db)

        A = np.asarray(imgA.value, dtype=np.uint8)
        B = np.asarray(imgB.value, dtype=np.uint8)

        A, B = self.resize_to_match(A, B)

        if self.mode == "alphaBlend":
            alpha = float(self.strength)
            blended = cv2.addWeighted(A, alpha, B, 1 - alpha, 0)
            mask = cv2.absdiff(A, B)

        elif self.mode == "maskBlend":
            diff = cv2.absdiff(A, B)
            mask_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            if bool(self.smooth):
                mask_gray = cv2.GaussianBlur(mask_gray, (7, 7), 0)

            mask3 = cv2.cvtColor(mask_gray, cv2.COLOR_GRAY2BGR)
            mask_f = mask3.astype(np.float32) / 255.0

            blended = (A * mask_f + B * (1.0 - mask_f)).astype(np.uint8)
            mask = mask3

        else:
            blended = A
            mask = np.zeros_like(A)
        imgA.value = blended
        self.outputBlendedImage = Image.set_frame(imgA, self.uID, self.redis_db)

        imgB.value = mask
        self.outputMaskImage = Image.set_frame(imgB, self.uID, self.redis_db)

        return build_response_blend(self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
