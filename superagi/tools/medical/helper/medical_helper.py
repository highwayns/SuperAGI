import requests
import json
import tiktoken
import os
from langflow import load_flow_from_json

class MedicalHelper:
    def __init__(self, medical_token):
        """
        Initializes the NotionHelper with the provided notion token.

        Args:
            medical_token (str): Personal Notion token.
        """
        self.medical_token = medical_token
        self.headers = {
            "Authorization": f"Bearer {medical_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def answer_question_usef_low(self, filename, filepath, question):
        combined_path = os.path.join(filepath, filename)
        flow = load_flow_from_json(combined_path)
        return flow(question)

    def get_page_ids(self,title,filter_type):
        payload={"query": title,"sort": {"direction": "ascending","timestamp": "last_edited_time"},"filter": {"value": filter_type,"property": "object"},}
        response = requests.post("https://api.notion.com/v1/search", headers=self.headers, json=payload)
        ids=[]
        if "results" in response.json():
            for res in response.json()["results"]:
                if title.lower() in res['properties']['Title']['title'][0]['plain_text'].lower():
                    ids.append(res['id'].replace('-',''))

        return ids

    def get_page_content(self,page_id):
        res = requests.request("GET", f"https://api.notion.com/v1/blocks/{page_id}/children", headers=self.headers)
        content_str=""
        for block in res.json()["results"]:
            if 'text' in block[block['type']]:
                if block[block['type']]['text'] and ('plain_text' in block[block['type']]['text'][0]):
                    content_str+=(f"{block[block['type']]['text'][0]['plain_text']}\n")
            elif 'rich_text' in block[block['type']]:
                if block[block['type']]['rich_text'] and ('plain_text' in block[block['type']]['rich_text'][0]):
                    content_str+=(f"{block[block['type']]['rich_text'][0]['plain_text']}\n")
        return content_str
    
    def create_page_children(self,content):
        children = []
        for index in range(0,len(content)):
            content_type=content[index]['type'].lower()
            children.append({
                "object": "block",
                "type":content_type ,
                content_type: {
                    **({"language": content[index]['language'].lower()} if content_type=="code" else {}),
                    "rich_text": [{"text": {"content": content[index]['content'][:1900]}}]
                },
            })
        return children
    
    def create_page(self,content,title,database_id,tags=None):
        data = {
            "parent": {"database_id": database_id},
            "properties": {"title": {"title": [{"text": {"content": title}}]},"Tags": {"multi_select": [{"name": tag} for tag in tags]},},
            "children":self.create_page_children(content),
        }
        return requests.post("https://api.notion.com/v1/pages", headers=self.headers, data=json.dumps(data))
    
    @staticmethod
    def count_text_tokens(message: str) -> int:
        """
        Function to count the number of tokens in a text.

        Args:
            message (str): The text to count the tokens for.

        Returns:
            int: The number of tokens in the text.
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(message)) + 4
        return num_tokens
