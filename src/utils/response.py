from sdks.novavision.src.helper.package import PackageHelper
from components.ImageProcessingDemo.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,

    EnhanceExecutor,
    EnhanceResponse,
    EnhanceOutputs,
    OutputEnhancedImage,

    BlendExecutor,
    BlendResponse,
    BlendOutputs,
    OutputBlendedImage,
    OutputMaskImage
)


def build_response_enhance(context):
    """
    Response builder for Enhance executor
    """
    outputEnhanced = OutputEnhancedImage(value=context.outputEnhanced)

    outputs = EnhanceOutputs(
        outputEnhancedImage=outputEnhanced
    )

    response = EnhanceResponse(outputs=outputs)

    enhanceExecutor = EnhanceExecutor(value=response)
    executor = ConfigExecutor(value=enhanceExecutor)

    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)

    return package.build_model(context)


def build_response_blend(context):
    """
    Response builder for Blend executor
    """
    blended = OutputBlendedImage(value=context.outputBlended)
    mask = OutputMaskImage(value=context.outputMask)

    outputs = BlendOutputs(
        outputBlendedImage=blended,
        outputMaskImage=mask
    )

    response = BlendResponse(outputs=outputs)

    blendExecutor = BlendExecutor(value=response)
    executor = ConfigExecutor(value=blendExecutor)

    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)

    return package.build_model(context)
