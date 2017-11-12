# coding:utf-8
import os
import mongokit.connection
from bson.objectid import ObjectId
from mongokit import Document, Connection
from mongokit.document import DocumentProperties
from yajl import dumps


class CallableMixin(object):
    """
    brings the callable method to a Document. usefull for the connection's
    register method
    """

    def __call__(self, doc=None, gen_skel=False,
                 lang='en', fallback_lang='en'):
        return self._obj_class(
            doc=doc,
            gen_skel=gen_skel,
            collection=self.collection,
            lang=lang,
            fallback_lang=fallback_lang
        )


mongokit.connection.CallableMixin = CallableMixin
_iterables = (list, tuple, set, frozenset)
MONGO_CONFIG = dict(host=os.getenv("MONGO_HOST", "mongodb://127.0.0.1:27017/"))
MONGO_DB = os.getenv("MONGO_DB", "gateway")
mongo = Connection(**MONGO_CONFIG)


class JsOb(object):

    def __init__(self, *args, **kwds):
        for i in args:
            self.__dict__.update(args)
        self.__dict__.update(kwds)

    def __getattr__(self, name):
        return self.__dict__.get(name, '')

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            del self.__dict__[name]

    def __repr__(self):
        return self.__dict__.__repr__()

    __getitem__ = __getattr__
    __delitem__ = __delattr__
    __setitem__ = __setattr__

    def __len__(self):
        return self.__dict__.__len__()

    def __iter__(self):
        return self.__dict__.iteritems()

    def __contains__(self, name):
        return self.__dict__.__contains__(name)

    def __str__(self):
        return dumps(self.__dict__)


class StripJsOb(JsOb):

    def __init__(self, *args, **kwds):
        super(StripJsOb, self).__init__(*args, **kwds)
        d = self.__dict__
        for k, v in d.items():
            if isinstance(v, basestring):
                if "\n" not in v:
                    _v = v.strip()
                    if _v != v:
                        d[k] = _v


class MetaDoc(DocumentProperties):

    def __new__(cls, name, bases, attrs):
        new_cls = super(MetaDoc, cls).__new__(cls, name, bases, attrs)
        if bases[0] is not Document:

            new_cls.__mongo__ = mongo
            if not new_cls.__name__.startswith('Callable'):
                new_cls.__collection__ = (name[0].lower() + name[1:])
                new_cls = mongo.register(new_cls)
                new_cls = getattr(mongo, name)
            else:
                new_cls._protected_field_names.append("_collection")
                _ = getattr(new_cls.__mongo__, new_cls.__database__)
                _ = getattr(_, new_cls.__collection__)
                new_cls._collection = _

        return new_cls


class Doc(Document):
    __metaclass__ = MetaDoc
    __database__ = MONGO_DB
    use_dot_notation = True
    use_autorefs = False
    skip_validation = True

    def __init__(self, doc={}, gen_skel=None, *args, **kwds):
        '''
        gen_skel为True的时候设置default value, 否则不设置
        '''
        if doc is None:
            doc = {}
        else:
            if isinstance(doc, JsOb):
                doc = doc.__dict__
        super(Doc, self).__init__(doc, *args, **kwds)
        for i in self.structure:
            if i not in doc:
                self[i] = None

        if gen_skel:
            if self.default_values:
                self._set_default_fields(self, self.structure)

    def upsert(self, spec, multi=False):
        if isinstance(spec, basestring):
            spec = {'_id': ObjectId(spec)}
        update = dict((k, v) for k, v in self.iteritems() if v is not None)
        update.update(spec)
        self.collection.update(
            spec,
            {'$set': update},
            upsert=True,
            multi=multi
        )

        return self

    def save(self, *args, **kwds):
        if "_id" in self:
            _id = self['_id']
            if isinstance(_id, basestring):
                self['_id'] = ObjectId(_id)
        super(Doc, self).save(*args, **kwds)
        return self

    @classmethod
    def count(cls, *args, **kwds):
        return cls._collection.find(*args, **kwds).count()

    @classmethod
    def find(cls, *args, **kwds):
        result = []
        for i in cls._collection.find(*args, **kwds):
            i['_id'] = str(i['_id'])
            result.append(i)
        return map(lambda doc: cls(doc, collection=cls._collection), result)

    @classmethod
    def find_one(cls, spec_or_id=None, *args, **kwds):
        if isinstance(spec_or_id, basestring):
            spec_or_id = ObjectId(spec_or_id)
        o = cls._collection.find_one(spec_or_id, *args, **kwds)
        if o:
            return cls(o, collection=cls._collection)

    @classmethod
    def find_and_modify(cls, spec_or_id, update, *args, **kwargs):
        if isinstance(spec_or_id, basestring):
            spec_or_id = ObjectId(spec_or_id)
        o = cls._collection.find_and_modify(spec_or_id, update,
                                            *args, **kwargs)
        if o:
            return cls(o, collection=cls._collection)

    def delete(self):
        if self._collection:
            self._collection.remove({'_id': ObjectId(self['_id'])})

    @classmethod
    def remove(cls, spec_or_id, safe=None, multi=True, **kwargs):
        if isinstance(spec_or_id, basestring):
            spec_or_id = ObjectId(spec_or_id)
        if spec_or_id:
            cls._collection.remove(spec_or_id=spec_or_id,
                                   safe=safe, multi=multi, **kwargs)

    @classmethod
    def iterdoc(cls, *args, **kwargs):
        skip = 0
        limit = 100
        while True:
            kwargs.update(dict(skip=skip, limit=limit))
            result = cls.find(*args, **kwargs)
            if not result:
                break
            for doc in result:
                yield doc
            skip += limit
