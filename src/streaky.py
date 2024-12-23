import requests as rqs
import os

import io
# import pypdf as pp
import re

import client as cl





    # def list_boxes(self, pipeline_key: str, page: int = None, stage_key: str = None, limit: int = None):
    #     RESOURCE = fr"/v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp"
    #     end_point = self.ENDP + RESOURCE
        
    #     end_point = end_point if page is None else end_point + "&page={pages}"
    #     end_point = end_point if stage_key is None else end_point + fr"&stageKey={stage_key}"
    #     end_point = end_point if limit is None else end_point + fr"&limit={limit}"
    #     response = self.get(end_point)
    #     return response

    # def list_threads(self, box_key: str):
    #     end_point = self.ENDP + fr"/v1/boxes/{box_key}/threads"
    #     response = self.get(end_point)
    #     return response


    # def get_thread(self, thread_key: str):
    #     end_point = self.ENDP + fr"/v1/threads/{thread_key}"
    #     response = self.get(end_point)
    #     return response
    
    # def get_field(self, pipeline_key: str, field_key: str):
    #     RESOURCE = fr"/v1/pipelines/{pipeline_key}/fields/{field_key}"
    #     end_point = self.ENDP + RESOURCE
    #     response = self.get(end_point)
    #     return response
    
    # def update_field_value(self, box_key: str, field_key: str, new_value: str):
    #     RESOURCE = fr"/v1/boxes/{box_key}/fields/{field_key}"
    #     end_point = self.ENDP + RESOURCE
    #     response = self.post(end_point, payload = {"value": new_value})
    #     return response
        
    
    
    # def list_fields(self, pipeline_key: str):
    #     end_point = self.ENDP + fr"/v1/pipelines/{pipeline_key}/fields"
    #     response = self.get(end_point)
    #     return response

        
            
        



class User:
    
    api = cl.UserAPI

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
    def list(streak: object):
        response = streak.get_my_team()
        users = response.json()["results"][0]["members"]
        for user in users:
            yield user


class Pipeline:
    
    api = cl.PipelineAPI

    def __init__(self, pipeline_response: object):
        
        self.response = pipeline_response   
        
        self.auth = self.response.auth
        self.key = self.response.key
        self.name = self.response.name
        
        self.stages = self.response.data["stages"]
        self.fields = self.response.data["fields"]
        self.last_update = self.response.data["lastSavedTimestamp"]
        
    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Pipeline '{self.name}'>"
    
    def __getitem__(self, item: str):
        return self.response.get(item, None)
    
    def __len__(self):
        return self.response.data["boxCount"]
           
    def __contains__(self, box: str | object):
        pass
    

    @classmethod
    def request(cls, auth: object, name: str = None, key: str = None):
        
        if key is not None:
           pip_response = cls.api.get(auth, key)
           if pip_response is not None:
               return cls(pip_response)
        elif name is not None:
            for pip_response in cls.api.list(auth):
                if pip_response.name.lower() == name.lower():
                    return cls(pip_response)
        else:
            return None
    
    

class Box:
    
    api = cl.BoxAPI

    def __init__(self, box_response: object, pipeline: object = None):
        
        self.response = box_response   
        
        self.auth = self.response.auth
        self.key = self.response.key
        self.name = self.response.name
        
        
        # if self in pipeline:
        #     self.pipeline = pipeline
        # else:
        #     box_pipkey = self.response.data["pipelineKey"]
        #     self.pipeline = Pipeline.request(self.auth, key = box_pipkey)
            
        self.stage = self.response.data["stageKey"]
        self.fields = self.response.data["fields"]
        
        self.notes = self.response.data["notes"]
        self.last_update = self.response.data["lastSavedTimestamp"]


    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<Box '{self.name}'>"
    
    
    def __getitem__(self, item):
        return self._data.get(item, None)
    
    def __contains__(self, other: str | object):
        pass
    
    
    @classmethod
    def request(cls, pipeline: object, name: str = None, key: str = None):
        
        if key is not None:
           box_rep = cls.api.get(pipeline.auth, key)
           if box_rep is not None:
               return cls(box_rep, pipeline = pipeline)
        elif name is not None:
            for box_rep in cls.api.get_by_name(pipeline.auth, name,
                                               pipeline_key = pipeline.key):
                if box_rep.name.lower() == name.lower():
                    return cls(box_rep, pipeline = pipeline)
        else:
            return None
    


    



class Field:
    
    api = cl.FieldAPI
    
    def __init__(self, field_response: object, box: object = None):
        pass
        

    def __getitem__(self, item):
        return self._data.get(item, None)
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"<Field '{self.name}'>"



    @classmethod
    def request(cls, pipeline: object, name: str = None, key: str = None):
        
        if key is not None:
           field_rep = cls.api.get(pipeline.auth, key)
           if field_rep is not None:
               return cls(field_rep)
        elif name is not None:
            for field_rep in cls.api.list(pipeline.auth, 
                                          pipeline.key, limit=None):
                if field_rep.name.lower() == name.lower():
                    return cls(field_rep)
        else:
            return None
    



class File:
    
    api = cl.FileAPI
    
    def __init__(self, file: object):

        self._data = file_object
        self.key = file_object.key
        
    
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


# class InfoParser:
    
#     @staticmethod
#     def search(name: str, pipeline: str = None, box: str, )
    
        


# class Supervisor:
    
#     @staticmethod
#     def update_deal(box: object):
        
#         files = [f for f in box.files if f["fileName"].startswith("MKP-F")]
#         if files != []:
#             sorted_files = sorted(files, key = lambda x: x["lastSavedTimestamp"], reverse = True)[0]
#             filedata = streak.get_file_content(sorted_files["fileKey"]).content
#             filedata = io.BytesIO(filedata)
#             document = pp.PdfReader(filedata)
    
#             text = document.pages[0].extract_text()
    
#             pattern = re.compile(r"Signature\s€\s(?P<deal>.*)Impo", re.DOTALL)
#             found = float(pattern.search(text).groupdict()["deal"].replace(".", "_").replace(",", "."))
#             field = [fd for fd in Pipeline(box.auth, key = box["pipelineKey"]).fields if fd["name"] == "Deal"][0]
#             field_key = field["key"]
#             print(f"Inserting '{found}' in the field '{field['name']}")
#             response = box.auth.update_field_value(box.key, field_key, str(found))
            
#             return response

        



# key64 = Streak.get_key64_fromfile()
# streak = Streak.connect()

# pip = Pipeline(streak, name = "OFFERTE")
# box = Box(streak, pip, name = "0896")

# # aa = Supervisor.update_deal(box)

# ff = File(streak, key ="agxzfm1haWxmb29nYWVyOwsSDE9yZ2FuaXphdGlvbiIYaW5mby5tZWtwaXBpbmdAZ21haWwuY29tDAsSBEZpbGUYgICF6IzD1wsM")












