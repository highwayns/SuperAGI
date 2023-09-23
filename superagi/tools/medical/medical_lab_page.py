import requests
import json

from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from helper.medical_helper import MedicalHelper



class MedicalLabPageSchema(BaseModel):
    title: str = Field(
        ...,
        description="title of the medical lab page",
    )

class MedicalLabPageTool(BaseTool):
    """
    Medical Lab Page tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "MedicalLabPage"
    description = (
        "A tool for fetching medical lab."
    )
    args_schema: Type[MedicalLabPageSchema] = MedicalLabPageSchema

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, title:str):
        """
        Execute the Medical Lab Page tool.

        Args:
            title: The title of the medical lab.

        Returns:
            Pages fetched successfully. or No such page exists. or error message.
        """
        try:
            medical_token=self.get_tool_config("MEDICAL_TOKEN")
            medical_helper=MedicalHelper(medical_token)
            page_ids=medical_helper.get_page_ids(title,"page")
            if len(page_ids)==0:
                return "No such page exists."
            try:
                final_result="" 
                for index in range(0,len(page_ids)):
                    helper_content_str=medical_helper.get_page_content(page_ids[index])
                    page_content=f"page {index+1}:\n\n{helper_content_str}"
                    final_result+=(f"\n{page_content}")
                    if medical_helper.count_text_tokens(final_result) > 6000:
                        break

                return f"Pages fetched successfully:{final_result}"
            except Exception as err:
                return f"Error: Unable to fetch page {err}"
        except Exception as err:
            return f"Error: Unable to fetch page {err}"