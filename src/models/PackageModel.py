from pydantic import Field
from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Config, Inputs, Configs, Outputs, Response, Request, Output, Input, Image

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Image
    type: Literal["object"] = "object"

    class Config:
        title = "Input Image"


class InputImageA(Input):
    name: Literal["inputImageA"] = "inputImageA"
    value: Image
    type: Literal["object"] = "object"

    class Config:
        title = "Image A"


class InputImageB(Input):
    name: Literal["inputImageB"] = "inputImageB"
    value: Image
    type: Literal["object"] = "object"

    class Config:
        title = "Image B"


class OutputEnhancedImage(Output):
    name: Literal["outputEnhancedImage"] = "outputEnhancedImage"
    value: Image
    type: Literal["object"] = "object"

    class Config:
        title = "Enhanced Image"


class OutputBlendedImage(Output):
    name: Literal["outputBlendedImage"] = "outputBlendedImage"
    value: Image
    type: Literal["object"] = "object"

    class Config:
        title = "Blended Image"


class OutputMaskImage(Output):
    name: Literal["outputMaskImage"] = "outputMaskImage"
    value: Image
    type: Literal["object"] = "object"

    class Config:
        title = "Mask Image"


class ConfigBrightnessAmount(Config):
    """
    Controls how much brightness will be increased.
    """
    name: Literal["ConfigBrightnessAmount"] = "ConfigBrightnessAmount"
    value: int = Field(default=20, ge=1, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Brightness Amount"


class Brightness(Config):
    name: Literal["Brightness"] = "Brightness"
    value: Literal["Brightness"] = "Brightness"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configBrightnessAmount: ConfigBrightnessAmount

    class Config:
        title = "Brightness"


class Kernel3(Config):
    name: Literal["Kernel3"] = "Kernel3"
    value: Literal["Kernel3"] = "Kernel3"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"


class Kernel5(Config):
    name: Literal["Kernel5"] = "Kernel5"
    value: Literal["Kernel5"] = "Kernel5"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"


class ConfigSharpenKernel(Config):
    """
    Selects kernel size for sharpening.
    """
    name: Literal["ConfigSharpenKernel"] = "ConfigSharpenKernel"
    value: Union[Kernel3, Kernel5]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Sharpen Kernel"


class Sharpen(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configSharpenKernel: ConfigSharpenKernel

    class Config:
        title = "Sharpen"


class ConfigEnhanceType(Config):
    """
    Determines which enhancement method will be applied.
    """
    name: Literal["ConfigEnhanceType"] = "ConfigEnhanceType"
    value: Union[Brightness, Sharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Enhancement Method"


class ConfigBlendStrength(Config):
    """
    Defines the blending ratio for alpha-based image mixing.
    """
    name: Literal["ConfigBlendStrength"] = "ConfigBlendStrength"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Blend Strength"


class BlendAlpha(Config):
    name: Literal["BlendAlpha"] = "BlendAlpha"
    value: Literal["BlendAlpha"] = "BlendAlpha"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configBlendStrength: ConfigBlendStrength

    class Config:
        title = "Alpha Blend"


class MaskTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"


class MaskFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"


class ConfigUseSmoothMask(Config):
    """
      Enables or disables smoothing on the generated blend mask.
    """
    name: Literal["ConfigUseSmoothMask"] = "ConfigUseSmoothMask"
    value: Union[MaskTrue, MaskFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Smooth Mask"


class BlendMask(Config):
    name: Literal["BlendMask"] = "BlendMask"
    value: Literal["BlendMask"] = "BlendMask"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configUseSmoothMask: ConfigUseSmoothMask

    class Config:
        title = "Mask Blend"


class ConfigBlendMode(Config):
    """
    Selects the blending method.
    """
    name: Literal["ConfigBlendMode"] = "ConfigBlendMode"
    value: Union[BlendAlpha, BlendMask]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Blend Mode"


class EnhanceInputs(Inputs):
    inputImage: InputImage


class EnhanceConfigs(Configs):
    configEnhanceType: ConfigEnhanceType


class EnhanceOutputs(Outputs):
    outputEnhancedImage: OutputEnhancedImage


class EnhanceRequest(Request):
    inputs: EnhanceInputs
    configs: EnhanceConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class EnhanceResponse(Response):
    outputs: EnhanceOutputs


class EnhanceExecutor(Config):
    name: Literal["Enhance"] = "Enhance"
    value: Union[EnhanceRequest, EnhanceResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Enhance"
        json_schema_extra = {"target": {"value": 0}}


class BlendInputs(Inputs):
    inputImageA: InputImageA
    inputImageB: InputImageB


class BlendConfigs(Configs):
    configBlendMode: ConfigBlendMode


class BlendOutputs(Outputs):
    outputBlendedImage: OutputBlendedImage
    outputMaskImage: OutputMaskImage


class BlendRequest(Request):
    inputs: Optional[BlendInputs]
    configs: BlendConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class BlendResponse(Response):
    outputs: BlendOutputs


class BlendExecutor(Config):
    name: Literal["Blend"] = "Blend"
    value: Union[BlendRequest, BlendResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blend"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    """
    Determines which task will run.
    """
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[EnhanceExecutor, BlendExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True      #bu olmalı mı emin değilim

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    name: Literal["ImageProcessingDemo"] = "ImageProcessingDemo"
    configs: PackageConfigs
    type: Literal["component"] = "component"
