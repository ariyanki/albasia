import logging
import hashlib
from var_dump import var_dump

from app import db
from app import dbmongo_history
from orator import Model, Schema
from datetime import datetime
from app.variable_constant import VariableConstant
from bson.objectid import ObjectId

db.connection().enable_query_log()

Model.set_connection_resolver(db)
schema = Schema(db)


class CrudBase(Model):

    __timestamps__ = False

    @classmethod
    def getList(self, args, qraw=None):
        if hasattr(self, '__view__'):
            me = db.table(self.__view__)
        elif hasattr(self, 'use_raw_view'):
            if self.use_raw_view:
                me = self.vw()
            else:
                me = self
        else:
            me = self
        
        #Page Number
        if 'p' in args:
            args['p']=int(args['p'])
        else:
            args['p']=1

        # Record Per Page
        if 'rp' in args:
            args['rp']=int(args['rp'])
        else:
            args['rp']=25

        # Search Raw
        if qraw is not None:
            me = me.where_raw(qraw)

        # Filter
        if 'f' in args:
            if len(args['f']):
                for k, v in args['f'].items():
                    me = me.where(k, v)
        # Order
        if 'o' in args:
            if args['o'] is not None and len(args['o']):
                for k, v in args['o'].items():
                    if (v.lower() == 'asc' or v.lower() == 'desc'):
                        me = me.order_by(k, v)
        result = {
            'args':args
        }   
        result['data'] = me.simple_paginate(args['rp'], args['p']).serialize()

        result['next']=args['p']+1
        if len(result['data'])<args['rp']:
            result['next']=args['p']

        result['prev']=args['p']-1
        if args['p']==1:
            result['prev']=1

        return result

    @classmethod
    def getById(self, id):
        result = self.find(id)
        return result

    @classmethod
    def addNew(self, data):
        result = self.first()
        me = self()
        for v in me.__add_new_fillable__:
            try:
                setattr(me, v, data[v])
            except Exception as e:
                pass
        setattr(me, 'created_at', datetime.now())
        setattr(me, 'updated_at', datetime.now())
        me.save()
        savedId = getattr(me, me.__primary_key__)
        return me.getById(savedId)

    @classmethod
    def doUpdate(self, id, data):
        me = self.find(id)
        if(me is None):
            raise Exception(VariableConstant.DATA_NOT_FOUND_MESSAGE)
        for v in self.__update_fillable__:
            try:
                setattr(me, v, data[v])
            except Exception as e:
                pass
        setattr(me, 'updated_at', datetime.now())
        me.save()
        savedId = getattr(me, self.__primary_key__)
        return self.getById(savedId)

    @classmethod
    def doDelete(self, id):
        me = self.find(id).delete()


    @classmethod
    def getAll(self):
        result = self.get()
        return result

    @classmethod
    def is_exists(cls, filter_data: dict):
        me = cls.where(filter_data)
        count = me.get().count()
        return bool(count)

class CrudBaseMongoDB():

    @classmethod
    def addNew(self, data):
        data['created_at']=datetime.now()
        data['updated_at']=datetime.now()
        _id = self.__collection__.insert(data)
        result=self.__collection__.find_one({"_id":_id})
        return result

    @classmethod
    def getById(self, id):
        result = None
        if ObjectId.is_valid(id):
            result=self.__collection__.find_one({"_id":ObjectId(id)})
        return result

    @classmethod
    def getCount(self, args):
        result=self.__collection__.count_documents(args)
        return result

    @classmethod
    def getByCustom(self, args):
        result=self.__collection__.find_one(args)
        return result

    @classmethod
    def getAggregate(self, args):
        result=self.__collection__.aggregate(args)
        return result

    @classmethod
    def getAll(self,args=None):
        if args is not None:
            result=self.__collection__.find(args)
        else:
            result=self.__collection__.find()
        return result

    @classmethod
    def doUpdate(self, id, data):
        result=self.__collection__.find_one({"_id":ObjectId(id)})
        if(result is None):
            return None
        # #save old data
        # hist = result.copy()
        # hist['id']=hist['_id']
        # del hist['_id']
        # dbmongo_history[self.__collection__.name].insert(hist)
        
        data['updated_at']=datetime.now()
        self.__collection__.update({"_id":ObjectId(id)}, {'$set':data})
        return self.getById(id)

    @classmethod
    def doUpdateWithHistory(self, id, data):
        result=self.__collection__.find_one({"_id":ObjectId(id)})
        if(result is None):
            return None
        #save old data
        hist = result.copy()
        hist['id']=hist['_id']
        del hist['_id']
        dbmongo_history[self.__collection__.name].insert(hist)
        
        data['updated_at']=datetime.now()
        self.__collection__.update({"_id":ObjectId(id)}, {'$set':data})
        return self.getById(id)

    @classmethod
    def doDelete(self, id):
        result=self.__collection__.find_one({"_id":ObjectId(id)})
        if(result is None):
            return None
        #save old data
        hist = result.copy()
        hist['id']=hist['_id']
        del hist['_id']
        dbmongo_history[self.__collection__.name].insert(hist)
        
        self.__collection__.remove({"_id":ObjectId(id)})
        return "Deleted"

    @classmethod
    def getList(self, args):

        # Filter
        if 'f' not in args:
            args['f']={}
        
        result=self.__collection__.find(args['f'])

        # Order
        if 'o' in args:
            if args['o'] is not None and len(args['o']):
                sortList = []
                for k, v in args['o'].items():
                    if (v == 1 or v == -1):
                        sortBy=(k,v)
                        sortList.append(sortBy)
                result=result.sort(sortList)

        if 'p' in args:
            args['p']=int(args['p'])
        else:
            args['p']=1

        # Record Per Page
        if 'rp' in args:
            args['rp']=int(args['rp'])
        else:
            args['rp']=25

        skips = args['rp'] * (args['p'] - 1)
        data=result.skip(skips).limit(args['rp'])

        result = {
            'args':args,
            'data':list(data),
            'next':args['p']+1,
            'prev':args['p']-1
        }   
        if len(result['data'])<args['rp']:
            result['next']=args['p']

        if result['prev']==0:
            result['prev']=1

        return result