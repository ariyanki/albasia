import logging
import hashlib
from var_dump import var_dump

from app import db
from orator import Model, Schema
from datetime import datetime
from app.variable_constant import VariableConstant

db.connection().enable_query_log()

Model.set_connection_resolver(db)
schema = Schema(db)


class CrudBase(Model):

    __timestamps__ = False

    @classmethod
    def getList(self, args):
        if hasattr(self, '__view__'):
            me = db.table(self.__view__)
            table = self.__view__
        else:
            me = self
            table = me.__table__

        
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

        # Filter
        if 'f' in args:
            if len(args['f']):
                for k, v in args['f'].items():
                    me = me.where(k, v)

        # Search Raw
        if 'q' in args:
            if args['q'] is not None and args['q'] != '':
                me = me.where_raw(args['q'])

        # Order
        if 'o' in args:
            if args['o'] is not None and len(args['o']):
                for k, v in args['o'].items():
                    if schema.has_column(table, k) and (v.lower() == 'asc' or v.lower() == 'desc'):
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
