from httpx import URL

# TODO
class BASE(URL):

    def __init__(self):
        super().__init__(r"https://api.streak.com")
        self.address = str(self)

    @property
    def complete(self):
        return str(self)

    def __add__(self, item):
        return str(self) + str(item)

    def joins(self, *items):
        new_url = self.complete
        for item in items:
            new_url += item
        return URL(new_url)

class USER:

    BASE = BASE()

    ME = BASE + r"/api/v1/users/me"
    GET = BASE + r"/api/v1/users/{user_key}"

class TEAM:

    BASE = BASE()

    MY = BASE + r"/api/v2/users/me/teams"

class PIPELINE:

    BASE = BASE()

    GET = BASE + r"/api/v1/pipelines/{pipeline_key}"
    LIST = BASE + r"/api/v1/pipelines?sortBy=creationTimestamp%20"

class BOX:

    BASE = BASE()

    GET_BY_KEY = BASE + r"/api/v1/boxes/{box_key}"

    # 'get by name' endpoint parts
    _GBN_HEAD = BASE + r"/api/v1/search?"
    _GBN_TAIL = r"name={box_name}"
    _GBN_IN_PIP = r"pipelineKey={pipeline_key}&"
    _GBN_AT_STG = r"stageKey={stage_key}&"
    GET_BY_NAME_IN_PIPELINE = _GBN_HEAD + _GBN_IN_PIP + _GBN_TAIL
    GET_BY_NAME_AT_STAGE = _GBN_HEAD + _GBN_AT_STG + _GBN_TAIL
    GET_BY_NAME_IN_PIP_AT_STAGE = (_GBN_HEAD + _GBN_IN_PIP +
                                   _GBN_AT_STG + _GBN_TAIL)

    # 'list box' endpoint
    _LIST_IN_PIP = r"/api/v1/pipelines/{pipeline_key}"
    _LIST_SORT = r"/boxes?sortBy=creationTimestamp"
    _LIST_HEAD = BASE + _LIST_IN_PIP + _LIST_SORT

    _LST_OPT_PAGE = r"&page={page}"
    _LST_OPT_STAGE = r"&stageKey={stage_key}"
    _LST_OPT_LIMIT = r"&limit={limit}"

    FILES = BASE + r"/api/v1/boxes/{box_key}/files"



class THREAD:

    BASE = BASE()

    GET = BASE + r"/api/v1/threads/{thread_key}"
    LIST = BASE + r"/api/v1/boxes/{box_key}/threads"


class FIELD:

    BASE = BASE()

    GET = BASE + r"/api/v1/pipelines/{pipeline_key}/fields/{field_key}"
    LIST = BASE + r"/api/v1/pipelines/{pipeline_key}/fields"
    UPDATE = BASE + r"/api/v1/boxes/{box_key}/fields/{field_key}"


class FILE:

    BASE = BASE()

    GET = BASE + r"/api/v1/files/{file_key}"
    CONTENT = BASE + r"/api/v1/files/{file_key}/contents"

class EVENT:

    BASE = BASE()

    NEW_BOX_CREATE = r""
