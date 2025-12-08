
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


class ConfigEnhanceType(Config):
    """
    Which enhancement method to apply
    """
    name: Literal["enhanceType"] = "enhanceType"
    value: Literal["brightness", "contrast", "sharpen", "blur"]
    type: Literal["string"] = "string"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Enhancement Method"


class ConfigEnhanceAmount(Config):
    """
    Strength of enhancement
    """
    name: Literal["enhanceAmount"] = "enhanceAmount"
    value: int = Field(default=20, ge=1, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Enhancement Amount"

class EnhanceInputs(Inputs):
    inputImage: InputImage


class EnhanceConfigs(Configs):
    enhanceType: ConfigEnhanceType
    enhanceAmount: ConfigEnhanceAmount


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
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigBlendAlpha(Config):
    name: Literal["blendAlpha"] = "blendAlpha"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Alpha"


class ConfigBlendBeta(Config):
    name: Literal["blendBeta"] = "blendBeta"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Beta"


class BlendInputs(Inputs):
    inputImageA: InputImageA
    inputImageB: InputImageB


class BlendConfigs(Configs):
    blendAlpha: ConfigBlendAlpha
    blendBeta: ConfigBlendBeta


class BlendOutputs(Outputs):
    outputBlendedImage: OutputBlendedImage   ###iki output nasıl koyacağım
    outputMaskImage: OutputMaskImage


class BlendRequest(Request):
    inputs: Optional[BlendInputs]     #optional nsıl kullanılıcak???
    configs: BlendConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class BlendResponse(Response):
    outputs: BlendOutputs


class BlendExecutor(Config):
    name: Literal["Blend"] = "Blend"
    value: Union[BlendRequest, BlendResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blend"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[EnhanceExecutor, BlendExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True      #bu olmalı mı emin değilim

    class Config:
        title = "Type"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    name: Literal["ImageProcessingDemo"] = "ImageProcessingDemo"
    configs: PackageConfigs
    type: Literal["component"] = "component"