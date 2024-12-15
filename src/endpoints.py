from enum import StrEnum


class BASE(StrEnum):
    
    ROOT = r"https://api.streak.com/api"
    V1 = r"https://api.streak.com/api/v1"
    V2 = r"https://api.streak.com/api/v2"    
    
class USER(StrEnum):
    
    ME = r"/v1/users/me"
    GET = r"/v1/users/{user_key}"
    
class TEAM(StrEnum):
    
    MY = r"/v2/users/me/teams"
    
class PIPELINE(StrEnum):
    
    GET = r"/v1/pipelines/{pipeline_key}"
    LIST = r"/v1/pipelines?sortBy=creationTimestamp%20"
    
class BOX(StrEnum):
    
    GET_BY_KEY = r"/v1/boxes/{box_key}"
    GET_BY_NAME = r"/v1/search?"
    LIST = r"/v1/pipelines/{pipeline_key}/boxes?sortBy=creationTimestamp"
    FIELD_NEWVAL = r"/v1/boxes/{box_key}/fields/{field_key}"
    FILE = r"/v1/boxes/{box_key}/files"
    
class THREAD(StrEnum):
    
    GET = r"/v1/threads/{thread_key}"
    LIST = r"/v1/boxes/{box_key}/threads"
    
    
class FIELD(StrEnum):
    
    GET = r"/v1/pipelines/{pipeline_key}/fields/{field_key}"
    UPDATE_NAME = ""
    LIST = r"/v1/pipelines/{pipeline_key}/fields"
    
    
class FILE(StrEnum):
    
    GET = r"/v1/files/{file_key}"
    CONTENT = r"/v1/files/{file_key}/contents"
    


def jformat(blocks: list, base: str = None, **kargs):
    """
    Join strings and formatting them.
    """
    base = base if base is not None else BASE.ROOT
    blocks = [base] + blocks
    endpoint = "".join(blocks).format(**kargs)
    return endpoint
