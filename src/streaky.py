import requests as rqs
import base64
import os

import io
import pypdf as pp
import re

# Insert your api key here.
KEYPATH = r"../key.txt"



  

class Streak:
    

    DOCS = r"https://streak.readme.io/reference/get-current-user"
    ENDP = r"https://api.streak.com/api"

    def __init__(self, auth64: bytes) -> object:
        
        self.auth64: bytes = auth64
        
    @property
    def me(self) -> rqs.models.Response:
        """
        Get current user details.
        (https://streak.readme.io/reference/get-current-user)
        """
        RESOURCE = r"/v1/users/me"
        
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response
        
    def __getitem__(self, item):
        return self.get(item)
    
    @staticmethod
    def get_key64_fromfile(key_filepath: str = KEYPATH):
        with open(key_filepath, "r") as file:
            key = file.read()
        encrypted_key = base64.b64encode(key.encode())
        return encrypted_key

    def get(self, url: str) -> rqs.models.Response:        
        query = {"authorization": f"Basic {self.auth64.decode()}"}
        response = rqs.get(url, headers = query)
        return response
    
    def post(self, url, payload: dict = None):
        query = {"authorization": f"Basic {self.auth64.decode()}",
                 "accept": "application/json",
                 "Content-Type": "application/json"}
        response = rqs.post(url, json = payload, headers = query)
        return response


    def get_user(self, user_key: str) -> rqs.models.Response:
        """
        Get user details.
        (https://streak.readme.io/reference/get-user)
        """
        RESOURCE = fr"/v1/users/{user_key}"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response

    def get_my_team(self) -> rqs.models.Response:
        RESOURCE = r"/v2/users/me/teams"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response


    def list_pipelines(self) -> object:
        RESOURCE = r"/v1/pipelines?sortBy=creationTimestamp%20"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response


    def get_pipeline(self, pipeline_key: str):
        end_point = self.ENDP + fr"/v1/pipelines/{pipeline_key}"
        response = self.get(end_point)
        return response


    def get_box(self, box_key: str):
        end_point = self.ENDP + fr"/v1/boxes/{box_key}"
        response = self.get(end_point)
        return response
    
    def get_box_by_name(self, box_name: str, stage_key: str = None, pipeline_key: str = None):
        RESOURCE = r"/v1/search?"
        end_point = self.ENDP + RESOURCE
        
        end_point = end_point if pipeline_key is None else end_point + fr"pipelineKey={pipeline_key}&"
        end_point = end_point if stage_key is None else end_point + fr"stageKey={stage_key}&"
        end_point = end_point + fr"name={box_name}"
        response = self.get(end_point)
        return response


    def list_boxes(self, pipeline_key: str, page: int = None, stage_key: str = None, limit: int = None):
        RESOURCE = fr"/v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp"
        end_point = self.ENDP + RESOURCE
        
        end_point = end_point if page is None else end_point + "&page={pages}"
        end_point = end_point if stage_key is None else end_point + fr"&stageKey={stage_key}"
        end_point = end_point if limit is None else end_point + fr"&limit={limit}"
        response = self.get(end_point)
        return response

    def list_threads(self, box_key: str):
        end_point = self.ENDP + fr"/v1/boxes/{box_key}/threads"
        response = self.get(end_point)
        return response


    def get_thread(self, thread_key: str):
        end_point = self.ENDP + fr"/v1/threads/{thread_key}"
        response = self.get(end_point)
        return response
    
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
        
    

    def is_pipeline_key(self, key: str):
        return True if self.get_pipeline(key).status_code == 200 else False

    def is_box_key(self, key: str):
        return True if self.get_box(key).status_code == 200 else False
    
    def is_field_key(self, key: str):
        return True if self.get_box(key).status_code == 200 else False
    
    
    def get_box_files(self, box_key: str):
        RESOURCE = fr"/v1/boxes/{box_key}/files"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response
    
    def get_file(self, file_key: str):
        RESOURCE = fr"/v1/files/{file_key}"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response
    
    def get_file_content(self, file_key: str):        
        RESOURCE = fr"/v1/files/{file_key}/contents"
        end_point = self.ENDP + RESOURCE
        response = self.get(end_point)
        return response
    
        
        
        
            
        



class User:

    def __init__(self, data: dict) -> object:
        
        for k, v in data.items():
            setattr(self, k, v)


    def __str__(self):
        return f"{self.userKey}"

    def __repr__(self):
        return f"{self.givenName}"

    @classmethod
    def from_api(cls, user: str = None):
        found_user = dict()
        for u in User.list_users():
            name, key = u["fullName"], u["userKey"]
            if user.lower() in name.lower() or user == key:
                found_user = u
                break
        return cls(found_user)

    @staticmethod
    def list_users(streak: object):
        response = streak.get_my_team()
        users = response.json()["results"][0]["members"]
        for user in users:
            yield user


class Pipeline:
    
    API = Streak

    def __init__(self, auth: object, name: str = None, key: str = None, source: dict = None) -> object:
        
        self._auth = auth
        if source is not None:
            data = [source]
        elif name is key is source is None:
            raise ValueError("Pipeline 'name' or 'key' must be specified.")
        else:
            data = self._request(self._auth, name = name, key = key)
        if len(data) == 0:
            raise ValueError("Pipeline not found")
        else:
            self._data = data[0]
                
    @property
    def data(self):
        return self._data
        
    @property
    def name(self):
        return self["name"]
    
    @property
    def key(self):
        return self["pipelineKey"]
    
    @property
    def box_count(self):
        return self["boxCount"]
    
    @property
    def stages(self):
        return {s["name"]: s for k, s in self._data["stages"].items()}
    
    @property
    def fields(self):
        return self["fields"]
    
    @property
    def last_update(self):
        return self["lastSavedTimestamp"]

    
    def __getitem__(self, item: str):
        return self._data.get(item, None)
    

    def __len__(self):
        return self.box_count
    

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Pipeline '{self.name}'>"
    
    @staticmethod
    def get_name_from_key(key: str, auth: object):
        return auth.get_pipeline(key).json()["name"]
    
    @staticmethod
    def get_key_from_name(name: str, auth: object):
        pipeline_list  = auth.list_pipelines().json()
        for p in pipeline_list:
            if p["name"] == name:
                return p["pipelineKey"]

    @staticmethod
    def _request(auth: object, name: str = None, key: str = None) -> list:

        if key is not None:
            pipelines = [auth.get_pipeline(key).json()]
        elif name is not None:
            pipelines = auth.list_pipelines().json()
            pipelines = [pip for pip in pipelines if name == pip["name"]]
        else:
            pipelines = auth.list_pipelines().json()
            
        return pipelines
    
    @classmethod
    def listpipeline(cls, auth: object):
        for pip in cls._request(auth):
            yield cls(auth, source = pip)
    

    



class Box:

    def __init__(self, auth: object, pipeline: object, 
                 name: str = None, key: str = None, source: dict = None) -> object:
        
        self._auth = auth
        
        if source is not None:
            data = [source]
        elif name is key is source is None:
            raise ValueError("Box 'name' or 'key' must be specified.")
        else:
            data = self._request(self._auth, pipeline, name = name, key = key)
            
        if len(data) == 0:
            raise ValueError("Box not found")
        else:
            self._data = data[0]


    def __getitem__(self, item):
        return self._data.get(item, None)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Box '{self.name}'>"
    
    @property
    def auth(self):
        return self._auth
    
    @property
    def name(self):
        return self["name"]
    
    @property
    def key(self):
        return self._data["boxKey"]
    
    @property
    def linked_box(self):
        pass
    
    @property
    def pipeline(self):
        pipeline_key = box._data["pipelineKey"]
        data = self.auth.get_pipeline(pipeline_key).json()
        return Pipeline(data["data"])
    
    @property
    def fields(self):
        return self["fields"]
    
    @property
    def files(self):
        return self._auth.get_box_files(self.key).json()
    
    
    @property
    def keys(self):
        return {"boxKey": self["boxKey"], 
                "stageKey": self["stageKey"], 
                "pipelineKey": self["pipelineKey"],
                "linkedBoxKeys": self["linkedBoxKeys"],
                "followerKeys": self["followerKeys"]
                }
    
    
    
    @staticmethod
    def _request(auth: object, pipeline: object, name: str = None, key: str = None, ) -> list:

        if name is key is None:
            raise ValueError("A value for 'name' or 'key' must be specified.")
        elif key is not None:            
            boxes = [auth.get_box(key).json()]
        elif name is not None:
            boxes_result = auth.get_box_by_name(name, pipeline_key = pipeline.key).json()["results"]["boxes"]            
            boxes_keys = [bx["boxKey"] for bx in boxes_result]
            boxes = [auth.get_box(k).json() for k in boxes_keys]
        else:
            boxes = auth.list_boxes(pipeline.key).json()            
        return boxes
    
    @classmethod
    def listboxes(cls, auth: object):
        for bx in cls._request(auth):
            yield cls(auth, source = bx)
    
    # @classmethod
    # def _request(cls, name_or_key: str, auth: object, pipeline: str = None, stage: str = None) -> list:
        
    #     pipeline_key = None if pipeline is None else Pipeline(pipeline, auth).key
    #     # TODO stage()
    #     if auth.is_box_key(name_or_key):
    #         boxes = [auth.get_box(name_or_key).json()]
    #     else:
    #         response = auth.get_box_by_name(name_or_key).json()
    #         result_boxes = response["results"]["boxes"]
    #         boxes = [b["boxKey"] for b in result_boxes]
    #         boxes = [auth.get_box(b).json() for b in boxes]
            
    #     return boxes[0]
    
            


    # @staticmethod
    # def list_boxes(pipeline: str, auth: object):
    #     pipeline_key = Pipeline(pipeline, auth).key
    #     boxes = auth.list_boxes(pipeline_key).json()
    #     for box in boxes:
    #         yield box


class Field:
    
    API = Streak
    
    def __init__(self, name: str, pipeline: str, auth: object) -> object:
        
        self._auth = auth
        self._data = self._request(name, pipeline, self._auth)
        if self._data is None:
            raise ValueError("Field not Found.")
    
    def __getitem__(self, item):
        return self._data.get(item, None)
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"<Field '{self.name}'>"
    
    @property
    def name(self):
        return self["name"]
    
    @property
    def key(self):
        return self["key"]
    
    @property
    def types(self):
        return self["type"]
    
    
    
    @staticmethod
    def _request(name: str, pipeline: str, auth: object):
        for p in auth.list_pipelines().json():
            if p["name"] == pipeline:
                for f in p["fields"]:
                    if f["name"] == name:
                        return f
    
    
    @staticmethod
    def list_fields(auth: object, pipeline: str = None):
        for p in auth.list_pipelines().json():
            if p["name"] == pipeline or pipeline is None:
                for f in p["fields"]:
                    yield f
                    
    
    @staticmethod
    def get_name_from_key(key: str, auth: object):
        return auth.get_field(key).json()["name"]
    
    @staticmethod
    def get_key_from_name(name: str, auth: object):
        pipeline_list  = auth.list_pipelines().json()
        for p in pipeline_list:
            if p["name"] == name:
                return p["Key"]


class File:
    
    def __init__(self, auth: object, key: str):
        
        self._auth = auth
        self._data = auth.get_file(key).json()
        
    
    def __getitem__(self, item):
        return self._data.get(item, None)
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"<File '{self.name}'>"
    
    @property
    def key(self):
        return self["fileKey"]
    
    @property
    def name(self):
        return self["fileName"]
    
    @property
    def stem(self):
        return os.path.splitext(self.name)[0]
    
    @property
    def ext(self):
        return os.path.splitext(self.name)[1]
       
    @property
    def last_update(self):
        return self["lastUpdatedTimestamp"]
    
    @property
    def size(self):
        return self["size"]
    
    @property
    def content(self):
        content = io.BytesIO(self._auth.get_file_content(self.key).content)
        return content
    
    @property
    def offer_price(self):
        
        file = self.content
        document = pp.PdfReader(file)
        text = document.pages[0].extract_text()
        pattern = re.compile(r"Signature\s€\s(?P<deal>.*)Impo", re.DOTALL)
        found = float(pattern.search(text).groupdict()["deal"].replace(".", "_").replace(",", "."))
        return found
        
    
    
        


class Supervisor:
    
    @staticmethod
    def update_deal(box: object):
        
        files = [f for f in box.files if f["fileName"].startswith("MKP-F")]
        if files != []:
            sorted_files = sorted(files, key = lambda x: x["lastSavedTimestamp"], reverse = True)[0]
            filedata = streak.get_file_content(sorted_files["fileKey"]).content
            filedata = io.BytesIO(filedata)
            document = pp.PdfReader(filedata)
    
            text = document.pages[0].extract_text()
    
            pattern = re.compile(r"Signature\s€\s(?P<deal>.*)Impo", re.DOTALL)
            found = float(pattern.search(text).groupdict()["deal"].replace(".", "_").replace(",", "."))
            field = [fd for fd in Pipeline(box.auth, key = box["pipelineKey"]).fields if fd["name"] == "Deal"][0]
            field_key = field["key"]
            print(f"Inserting '{found}' in the field '{field['name']}")
            response = box.auth.update_field_value(box.key, field_key, str(found))
            
            return response

        



key64 = Streak.get_key64_fromfile()
streak = Streak(key64)

pip = Pipeline(streak, name = "OFFERTE")
box = Box(streak, pip, name = "0896")

# aa = Supervisor.update_deal(box)

ff = File(streak, key ="agxzfm1haWxmb29nYWVyOwsSDE9yZ2FuaXphdGlvbiIYaW5mby5tZWtwaXBpbmdAZ21haWwuY29tDAsSBEZpbGUYgICF6IzD1wsM")














