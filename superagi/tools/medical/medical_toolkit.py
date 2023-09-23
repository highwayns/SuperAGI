from abc import ABC
from typing import List

from superagi.tools.base_tool import BaseToolkit, BaseTool
from medical_medcine_page import MedicalMedcinePageTool
from medical_lab_page import MedicalLabPageTool

class MedicalToolkit(BaseToolkit, ABC):
    name: str = "Medical Toolkit"
    description: str = "Toolkit containing tools for performing medical operations"

    def get_tools(self) -> List[BaseTool]:
        return [MedicalMedcinePageTool(),MedicalLabPageTool()]

    def get_env_keys(self) -> List[str]:
        return ["MEDICAL_TOKEN","MEDICAL_DATABASE_ID"]
