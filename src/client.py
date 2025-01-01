import requests as req
import httpx as hx

import base64
import time as tm
import pandas as pd
from io import BytesIO
import asyncio

# local libraries
import endpoints as enp



class Client:

    def __init__(self, auth_key_b64: bytes) -> object:

        self._auth_key_b64: bytes = auth_key_b64
        self._log = [(tm.time_ns(), "START", "", None)]


    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<Auth '{self.key.decode()}'>"

    @classmethod
    def _DEFAULT_HEADER(cls):
        header = hx.Headers({"accept": "application/json",
                             'Content-Type': 'application/json'})
        return header

    @classmethod
    def _DEFAULT_GET_HEADER(cls):
        data = cls._DEFAULT_HEADER()
        return data


    @property
    def client(self):

        key = self.key.decode()
        key_item = {"authorization_key": f"Basic {key}"}

        header = self._DEFAULT_HEADER()
        header.update(key_item)

        return hx.AsyncClient(headers = header)


    def _logger(self, *data):
        self._log.append(data)

    @property
    def log(self):
        log_columns = "Time", "Type", "Url", "Response"
        table = pd.DataFrame(data=self._log,columns=log_columns)
        return table


    @property
    def key(self):
        return self._auth_key_b64


    @classmethod
    def fromfile(cls, path: str = ""):

        with open(path, "r") as file:
            key = file.read()

        encoded = key.encode()
        encrypted = base64.b64encode(encoded)
        return cls(encrypted)


    async def _get_task(self, client: object, url: str, timeout = None):
        """
        DESCRIPTION:
            Creates an asynchronous task for retrieving data from a given URL.
            This coroutine prepares an asynchronous GET request to the
            specified URL using the provided client.

        ARGS:
            - client: The asynchronous HTTP client to use for the request.
            - url: The URL to retrieve data from.
            - timeout (optional): The timeout for the request, in seconds.
                Defaults to None (no timeout).

        RETURN:
            The task object from the GET request.
        """
        response = await client.get(url, timeout = timeout)
        self._logger(tm.time_ns(), "GET", url, response)
        return response


    async def _post_task(self, client: object, url: str, payload: dict = None,
                        timeout = None):
        """
        DESCRIPTION:
            Creates an asynchronous task for retrieving data from a given URL.
            This coroutine prepares an asynchronous POST request to the
            specified URL using the provided client.

        ARGS:
            - client: The asynchronous HTTP client to use for the request.
            - url: The URL to retrieve data from.
            - timeout (optional): The timeout for the request, in seconds.
                Defaults to None (no timeout).

        RETURN:
            The task object from the POST request.
        """
        response = await client.post(url, json = payload, timeout = timeout)
        self._logger(tm.time_ns(), "POST", url, response)
        return response


    async def _gather_get(self, *urls: str, timeout = None) -> object:

        async with self.client as client:
            tasks = [self._get_task(client, url, timeout = timeout)
                     for url in urls]

            responses = await asyncio.gather(*tasks)
            return responses

    async def _gather(self, *urls: str,
                      timeout = None) -> object:

        async with self.client as client:
            tasks = [self._post_task(client, url, payload = payload,
                                     timeout = timeout)
                     for url in urls]

            responses = await asyncio.gather(*tasks)
            return responses


    def get(self, *urls: str, timeout = None) -> list:

        requests = self._gather(*urls, timeout = timeout)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(requests)
        return result


    def post(self, *urls, payload: dict = None, timeout = None) -> object:

        requests = self._gather(*urls, timeout = timeout)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(requests)
        return result







class UserAPI:

    _resources = enp.USER

    def __init__(self, auth: object, user_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = user_data
        self.email = self.data["email"]
        self.key = self.data["key"]

    def __getitem__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<UserAPI '{self.email}'>"

    @classmethod
    def me(cls, auth):
        end_point = cls._resources.ME
        response = auth.get(end_point)
        if response.status_code == 200:
            return cls(auth, response.json())

    @classmethod
    def get(cls, auth, user_key: str):
        end_point = cls._resources.GET.format(
            **{"user_key": user_key})
        response = auth.get(end_point)
        if response.status_code == 200:
            return cls(auth, response.json())

    @staticmethod
    def team(auth):
        return TeamAPI.my(auth)


class TeamAPI:

    _resources = enp.TEAM

    def __init__(self, auth: object, team_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = team_data
        self.name = self.data["name"]
        self.key = self.data["key"]

    def __getitem__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<TeamAPI '{self.name}'>"

    @classmethod
    def my(cls, auth):
        end_point = cls._resources.MY
        response = auth.get(end_point)
        if response.status_code == 200:
            keys_to_keep = ("creationDate", "creator",
                            "name", "key", "members",
                            "lastSavedTimestamp")
            all_data = response.json()["results"][0]
            data = {k: v for k,v in all_data.items() if k in keys_to_keep}
            return cls(auth, data)



class PipelineAPI:

    _resources = enp.PIPELINE

    def __init__(self, auth: object, pipeline_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = pipeline_data
        self.name = self.data["name"]
        self.key = self.data["key"]

    def __getitem__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<PipelineAPI '{self.name}'>"


    @classmethod
    def list(cls, auth: object) -> object:
        end_point = cls._resources.LIST

        request_coru = auth.get(end_point)
        loop = asyncio.get_event_loop()
        result = loop.create_task(request_coru)

        if result[0].status_code == 200:
            data = result[0].json()
            for pip in data:
                yield cls(auth, pip)

    @classmethod
    def get(cls, auth: object, pipeline_key: str) -> object:
        end_point = cls._resources.GET.format(
            **{"pipeline_key": pipeline_key})
        response = auth.get(end_point)
        if response.status_code == 200:
            pip = response.json()
            return cls(auth, pip)

class FieldAPI:

    _resources = enp.FIELD

    def __init__(self, auth: object, field_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = field_data
        self.name = self.data["name"]
        self.key = self.data["key"]

    def __getitem__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<FieldAPI '{self.name}'>"

    @classmethod
    def get(cls, auth: object, pipeline_key: str, field_key: str):
        end_point = cls._resources.GET
        end_point = end_point.format(pipeline_key = pipeline_key,
                                     field_key = field_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            field_data = response.json()
            return cls(auth, field_data)

    @classmethod
    def update(cls, auth: object, box_key: str, field_key: str,
               new_value: str):
        end_point = cls._resources.UPDATE
        end_point = end_point.format(box_key = box_key, field_key = field_key)
        response = auth.post(end_point, payload = {"value": new_value})
        if response.status_code == 200:
            return response

    @classmethod
    def list(cls, auth: object, pipeline_key: str):
        end_point = cls._resources.LIST
        end_point = end_point.format(pipeline_key = pipeline_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            field_list = response.json()
            for field in field_list:
                yield cls(auth, field)

    @classmethod
    def all(cls, auth) -> list:
        fields = dict()
        for pip in PipelineAPI.list(auth):
            fields.update({pip.key: pip["fields"]})
        return fields





class BoxAPI:

    _resources = enp.BOX

    def __init__(self, auth: object, box_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = box_data

        self.name = self.data["name"]
        self.key = self.data["boxKey"]


    def __getitem__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<BoxAPI '{self.name}'>"


    @classmethod
    def get_by_key(cls, auth: object, box_key: str):
        end_point = cls._resources.GET_BY_KEY.format(box_key = box_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            return cls(auth, response.json())

    @classmethod
    def get_by_name(cls, auth, box_name: str,
                    stage_key: str = None, pipeline_key: str = None):
        end_point = cls._resources._GBN_HEAD
        end_point += "" if pipeline_key is None else cls._resources._GBN_IN_PIP
        end_point += "" if stage_key is None else cls._resources._GBN_AT_STG
        end_point += cls._resources._GBN_TAIL

        end_point = end_point.format(box_name = box_name,
                                     pipeline_key = pipeline_key,
                                     stage_key = stage_key)

        search_response = auth.get(end_point)
        if search_response.status_code == 200:
            boxlist = search_response.json()["results"]["boxes"]
            for box in boxlist:
                box_data = box["boxKey"]
                yield cls.get_by_key(auth, box_data)

    @classmethod
    def list(cls, auth: object, pipeline_key: str, page: int = None,
             stage_key: str = None, limit: int = 10):
        """
        To limit the response, 'limit' parameter need to be set.
        The 'page' parameter than can be used to move around the response.

        If no page is set while limiting, the complete response will be
        retrieved by the api. Same when 'page' is set but 'limit' is none.

        Note:
            no 'hasNextPage' attribute found as mentioned in the api docs.
        """

        raw_ep = cls._resources._LIST_HEAD
        raw_ep += "" if page is None else cls._resources._LST_OPT_PAGE
        raw_ep += "" if stage_key is None else cls._resources._LST_OPT_STAGE
        raw_ep += "" if limit is None else cls._resources._LST_OPT_LIMIT

        end_point = raw_ep.format(pipeline_key = pipeline_key,
                                  page = page, stage_key = stage_key,
                                  limit = limit)


        response = auth.get(end_point)
        if response.status_code == 200:
            boxlist = response.json()
            for box_data in boxlist:
                yield cls(auth, box_data)

    @classmethod
    def files(cls, auth: object, box_key: str):
        end_point = cls._resources.FILES
        end_point = end_point.format(box_key = box_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            filelist = response.json()
            for file in filelist:
                # BUG TODO -- Endpoint
                yield FileAPI.get(auth, file["fileKey"])

    def is_box_key(self, key: str):
        return True if self.get_box(key).status_code == 200 else False


class ThreadAPI:

    _resources = enp.THREAD

    def __init__(self, auth: object, thread_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = thread_data
        self.name = self.data["subject"]
        self.key = self.data["key"]

    def __getitem__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        subject = self.name
        if len(subject) > 20:
            subject = f"{self.name[:8]}...{self.name[-8:]}"
        return f"<ThreadAPI '{subject}'>"


    @classmethod
    def get(cls, auth: object, thread_key: str):
        end_point = cls._resources.GET
        end_point = end_point.format(thread_key = thread_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            thread_data = response.json()
            return cls(auth, thread_data)

    @classmethod
    def list(cls, auth:object, box_key: str):
        end_point = cls._resources.LIST
        end_point = end_point.format(box_key = box_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            threads = response.json()
            for thread in threads:
                yield cls(auth, thread)



class FileAPI:

    _resources = enp.FILE

    def __init__(self, auth: object, file_data: dict):
        self.timestamp_ns = tm.time_ns()
        self.auth = auth
        self.data = file_data
        self.name = self.data["fileName"]
        self.key = self.data["fileKey"]

    def __getitem__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"<FileAPI '{self.name}'>"

    def __bytes__(self):
        return self.content(self.auth, self.key)

    @classmethod
    def get(cls, auth: object, file_key: str):
        end_point = cls._resources.GET
        end_point = end_point.format(file_key = file_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            file_data = response.json()
            return cls(auth, file_data)

    @classmethod
    def list(cls, auth: object, box_key: str):
        # BUG TODO -- Endpoint
        # BoxAPI.files return different type of dict respect to what
        # returned by FileAPI.list endpoint. Than for the moment,
        # the additional data on BoxAPI.files object is omitted
        # and GET endpoint is called instead of use the first directly
        for file in BoxAPI.files(auth, box_key):
            yield cls.get(auth, file["fileKey"])

    @classmethod
    def content(cls, auth: object, file_key: str) -> bytes:
        end_point = cls._resources.CONTENT
        end_point = end_point.format(file_key = file_key)
        response = auth.get(end_point)
        if response.status_code == 200:
            filedata = BytesIO(response.content)
            return filedata


time1 = tm.time()
res = Client.connect(r"key.txt").get(enp.PIPELINE.LIST)
time1 = tm.time() - time1

time2 = tm.time()
res = Client.connect(r"key.txt").get(enp.PIPELINE.LIST, enp.PIPELINE.LIST,
                                     enp.PIPELINE.LIST, enp.PIPELINE.LIST,
                                     enp.PIPELINE.LIST, enp.PIPELINE.LIST,
                                     enp.PIPELINE.LIST, enp.PIPELINE.LIST)
time2 = tm.time() - time2

print(time1, time2)


