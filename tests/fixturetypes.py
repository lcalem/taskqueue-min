import json
import requests


class ApiFixture(object):

    def __init__(self, host, port=8000, stop_signal=15):
        self.process = None
        self.stopped = False
        self.started = False
        self.stop_signal = stop_signal

        self.wait_port = port
        self.host = host
        self.url = "http://%s:%s" % (self.host, self.wait_port)

    def _request(self, method, path, assert_200=True, **kwargs):

        # if not self.started:
        #     self.start()

        res = getattr(requests, method)(self.url + path, **kwargs)

        if assert_200 and res.status_code != 200:
            raise Exception("%s: %s" % (res.status_code, res.text))

        try:
            js = json.loads(res.text)
        except:
            print("Couldn't json parse", repr(res.text)[0:100])
            js = None

        return js, res

    def GET(self, *args, **kwargs):
        return self._request("get", *args, **kwargs)

    def POST(self, *args, **kwargs):
        return self._request("post", *args, **kwargs)

    def DELETE(self, *args, **kwargs):
        return self._request("delete", *args, **kwargs)


# class MongoFixture(object):
#     # TODO: indexes

#     def __init__(self):
#         from lib.context import connections
#         self.db = connections.mongodb_main

#     # def build_indexes(self):
#     #     for collection, indexes in self.indexes.items():
#     #         for index_data in indexes:
#     #             key = index_data[0]
#     #             kwargs = index_data[1]
#     #             try:
#     #                 self.db[collection].create_index(key, **kwargs)
#     #             except Exception as e:
#     #                 print(e)
#     #                 print("***** INDEX CREATION ERROR : %s" % str([collection, key, e]))

#     def flush(self):

#         from lib.context import connections

#         print("Flushing MongoDB")
#         for mongodb in (connections.mongodb_main, ):
#             if mongodb:
#                 for c in mongodb.collection_names():
#                     if not c.startswith("system."):
#                         mongodb.drop_collection(c)
