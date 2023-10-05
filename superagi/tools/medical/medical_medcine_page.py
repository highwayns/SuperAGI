import requests
import json

from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from helper.medical_helper import MedicalHelper

class MedicalMedcinePageSchema(BaseModel):
    content_list:  list = Field( 
        ...,
        description='Be very clear about the content_list format.Here is an array of different medical blocks that you can use in Medical Medcine page API:["paragraph","code","heading_1","heading_2","heading_3","bulleted_list_item","numbered_list_item","to_do","quote","toggle"].content_list should be a list of dictionaries containing content,type of the content and language of the content, example: content_list=[{"type":"based on content, if no such block type exists choose it from the list provided above","content":some text,"language":"which coding language is used"}]. Strictly follow the given example and include the keys type,content and language in the dictionary',
    )
    title: str = Field(
        ...,
        description="Title of the page to be created",
    )                      
    tags: list = Field(
        ...,
        description="list of tags to be added to the page based on the content",
    )

class MedicalMedcinePageTool(BaseTool):
    """
    Medical Medcine Page tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "MedicalMedcinePage"
    description = (
        "A tool for creating a page on medical."
    )
    args_schema: Type[MedicalMedcinePageSchema] = MedicalMedcinePageSchema

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, question) -> str:
        """
        Execute the Medical Medcine answer tool.

        Args:
            question: The content of the question to be entered.
            
        Returns:
            The answer to the question to be entered. or error message.
        """

        try:
            filename = "loadmedicine.json"
            filepath = "./langflow"
            medical_token=self.get_tool_config("MEDICAL_TOKEN")
            medical_helper=MedicalHelper(medical_token)
            response=medical_helper.answer_question_usef_low(filename, filepath, question)
            return response.text
        except Exception as err:
            return f"Error: Unable to answer {err}"