from sdks.novavision.src.helper.package import PackageHelper
from components.ImageProcessingDemo.src.models.PackageModel import (
    PackageConfigs,
    ConfigExecutor,
    PackageModel,
    OutputEnhancedImage,
    EnhanceOutputs,
    EnhanceExecutor,
    EnhanceResponse,
    OutputBlendedImage,
    OutputMaskImage,
    BlendOutputs,
    BlendExecutor,
    BlendResponse
)


def build_response_enhance(context):
    outputEnhancedImage = OutputEnhancedImage(value=context.enhanced_image)
    enhanceOutputs = EnhanceOutputs(outputEnhancedImage=outputEnhancedImage)
    enhanceResponse = EnhanceResponse(outputs=enhanceOutputs)
    enhanceExecutor = EnhanceExecutor(value=enhanceResponse)
    executor = ConfigExecutor(value=enhanceExecutor)
    packageConfigs = PackageConfigs(configExecutor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_blend(context):
    outputBlendedImage = OutputBlendedImage(value=context.blended_image)
    outputMaskImage = OutputMaskImage(value=context.mask_image)
    blendOutputs = BlendOutputs(outputBlendedImage=outputBlendedImage, outputMaskImage=outputMaskImage)
    blendResponse = BlendResponse(outputs=blendOutputs)
    blendExecutor = BlendExecutor(value=blendResponse)
    executor = ConfigExecutor(value=blendExecutor)
    packageConfigs = PackageConfigs(configExecutor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
