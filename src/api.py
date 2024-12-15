import requests as rqs
import base64
from enum import Enum

import endpoints as endp
from endpoints import jformat

# Insert your api key here.

class Auth:
    

    DOCS = r"https://streak.readme.io/reference/get-current-user"
    ENDP = r"https://api.streak.com/api"

    def __init__(self, auth64: bytes) -> object:
        self.auth64: bytes = auth64
        
    @property
    def key(self):
        return self._auth64
    
        
    @classmethod
    def connect(cls, key_filepath: str = ""):
        key64 = cls.fromfile(key_filepath)
        return cls(key64)

    def get(self, url: str) -> rqs.models.Response:        
        query = {"authorization": f"Basic {self.auth64.decode()}",
                 "accept": "application/json",
                 "Content-Type": "application/json"}
        response = rqs.get(url, headers = query)
        return response
    
    def post(self, url, payload: dict = None):
        query = {"authorization": f"Basic {self.auth64.decode()}",
                 "accept": "application/json",
                 "Content-Type": "application/json"}
        response = rqs.post(url, headers = query, json = payload)
        return response
    
    @staticmethod
    def fromfile(key_filepath: str = ""):
        with open(key_filepath, "r") as file:
            key = file.read()
        encrypted_key = base64.b64encode(key.encode())
        return encrypted_key

            

    
    
class User:
    
    
    def me(self) -> object:
        RESOURCE = r"/v1/users/me"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response

    def get_user(self, user_key: str) -> rqs.models.Response:
        RESOURCE = fr"/v1/users/{user_key}"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response

    def get_my_team(self) -> rqs.models.Response:
        RESOURCE = r"/v2/users/me/teams"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response


class PipelineQuery:    

    base = endp.BASE.ROOT
    connect = Auth.connect
    resources = endp.PIPELINE
    
    def __init__(self, auth: object, pipeline_key: str):
        data = self.get_pipeline(auth, pipeline_key)
        if data.status_code == 200:
            self.auth = auth
            self.key = pipeline_key
            self.data = data.json()
    
    @classmethod
    def list_pipelines(cls, auth: object) -> object:
        blocks = [cls.base, cls.resources.LIST]
        
        end_point = jformat(blocks)
        response = auth.get(end_point)
        return response

    @classmethod
    def get_pipeline(cls, auth: object, pipeline_key: str):
        blocks = [cls.base, cls.resources.GET]
        kargs = {"pipeline_key": pipeline_key}
        
        end_point = jformat(blocks, **kargs)
        response = auth.get(end_point)
        return response

    
    def is_pipeline_key(self, key: str):
        return True if self.get_pipeline(key).status_code == 200 else False


class Box:
    
    LIST_BOXES = r"/v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp"
    GET_BOX = r"/v1/boxes/{box_key}"
    
    
    def get_box(self, auth: object, box_key: str):
        RESOURCE = fr"/v1/boxes/{box_key}"
        end_point = auth.ENDP + RESOURCE
        response = auth.get(end_point)
        return response
    
    def get_box_by_name(self, box_name: str, stage_key: str = None, pipeline_key: str = None):
        RESOURCE = r"/v1/search?"
        
        end_point = self.ENDP + RESOURCE
        end_point += "" if pipeline_key is None else fr"pipelineKey={pipeline_key}&"
        end_point += "" if stage_key is None else fr"stageKey={stage_key}&"
        end_point = end_point + fr"name={box_name}"
        
        response = self.get(end_point)
        return response


    def list_boxes(self, pipeline_key: str, page: int = None, 
                   stage_key: str = None, limit: int = None):
        RESOURCE = fr"/v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp"
        
        end_point = self.ENDP + RESOURCE
        end_point += fr"&page={page}" if page is not None else ""
        end_point += fr"&stageKey={stage_key}" if stage_key is not None else ""
        end_point += fr"&limit={limit}" if limit is not None else ""
        
        response = self.get(end_point)
        return response
    
    def get_box_files(self, box_key: str):
        RESOURCE = fr"/v1/boxes/{box_key}/files"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response
    
    def is_box_key(self, key: str):
        return True if self.get_box(key).status_code == 200 else False
    

class Thread:
    
    def list_threads(self, box_key: str):
        end_point = self.ENDP + fr"/v1/boxes/{box_key}/threads"
        response = self.get(end_point)
        return response


    def get_thread(self, thread_key: str):
        end_point = self.ENDP + fr"/v1/threads/{thread_key}"
        response = self.get(end_point)
        return response
        

class Field:
    
    auth = Auth
    resources = endp.FIELD
    
    def __init__(self, auth: object, key: str):
        pass
    
            
    def get_field(self, pipeline_key: str, field_key: str):
        RESOURCE = fr"/v1/pipelines/{pipeline_key}/fields/{field_key}"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response
    
    def update_field_value(self, box_key: str, field_key: str, new_value: str):
        RESOURCE = fr"/v1/boxes/{box_key}/fields/{field_key}"
        end_point = self.ENDP + RESOURCE
        response = self.post(end_point, payload = {"value": new_value})
        return response
    
    def list_fields(self, pipeline_key: str):
        end_point = self.ENDP + fr"/v1/pipelines/{pipeline_key}/fields"
        response = self.get(end_point)
        return response

    def is_field_key(self, key: str):
        return True if self.get_box(key).status_code == 200 else False



class FileQuery:
    
    connect = Auth.connect
    resources = endp.FILE
    base = endp.BASE.ROOT
    
    def __init__(self, auth: object, file_key: str):
        self.auth = auth
        self.key = file_key
        self.data = self.request(self.auth, self.key).json()
    
    @classmethod
    def request(cls, auth: object, file_key: str):
        blocks = [cls.base, cls.resources.GET]
        input_keys = {"file_key": file_key}
        
        end_point = jformat(blocks, **input_keys)
        response = auth.get(end_point)
        return response
    
    @classmethod
    def content(cls, auth: object, file_key: str):        
        blocks = [cls.base, cls.resources.CONTENT]
        input_keys = {"file_key": file_key}
        
        end_point = jformat(blocks, **input_keys)
        response = auth.get(end_point)
        return response
    
        
        
        
            
        












