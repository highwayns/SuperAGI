import pytest
import requests
import json
from unittest.mock import patch
from helper.medical_helper import MedicalHelper
    
def test_create_page_children():
    medicalHelper = MedicalHelper("token")

    filename = "loadmedicine.json"
    filepath = "./langflow"
    question = "ペルジピンの相互に何にがありますか"

    print(medicalHelper.answer_question_usef_low(filename, filepath, question))
