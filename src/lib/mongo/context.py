import importlib
import logging
import os
import re


def memoize_single_argument(f):
    ''' Memoization decorator for a function taking a single argument
    http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/'''
    class Memodict(dict):

        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return Memodict().__getitem__


@memoize_single_argument
def load_class_by_path(path):
    return getattr(
        importlib.import_module(
            re.sub(
                r"\.[^.]+$",
                "",
                path)),
        re.sub(
            r"^.*\.",
            "",
            path))


class LazyObject(object):

    ''' Lazy-connection class. Connections will only be initialized when first used. '''

    def __init__(self):
        self._factories = []
        self._attributes_via_factories = []

    def add_factory(self, factory):
        self._factories.append(factory)

    # This will be called only once, when the attribute is still missing
    def __getattr__(self, attr):

        for factory in self._factories:
            value = factory(attr)
            if value is not None:
                self._attributes_via_factories.append(attr)
                self.__dict__[attr] = value
                return value

    def reset(self):
        # TODO proper connection close?
        for attr in self._attributes_via_factories:
            del self.__dict__[attr]
        self._attributes_via_factories = []


CLUSTER_TO_VAR = {
    "mongodb_jobs": ("MRQ_MONGODB_JOBS", "mrq")
}


def _connections_factory(attr):

    logging.info("connection factory")
    if attr not in CLUSTER_TO_VAR:
        raise Exception("[MONGODB] cluster %s not registered in cluster_to_var" % attr)

    cluster_var, database_name = CLUSTER_TO_VAR[attr]

    config_line = os.environ.get(cluster_var)
    if config_line is None:
        raise Exception("[MONGODB] missing %s environ -- cannot connect!" % cluster_var)

    if attr.startswith("mongodb"):
        if isinstance(config_line, str):
            import pymongo

            logging.debug("[MONGODB] Connecting to %s..." % config_line)
            mongo_parsed = pymongo.uri_parser.parse_uri(config_line)

            kwargs = {}
            kwargs.update(mongo_parsed["options"])
            db = pymongo.MongoClient(config_line, **kwargs)[database_name]

            logging.debug("[MONGODB] %s: ... connected. (readPreference=%s)" % (attr, db.read_preference))
            return db

connections = LazyObject()
connections.add_factory(_connections_factory)
