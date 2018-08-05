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
    def getApiList(self, recPerPage=25, search=None, filter={}, page=1, order={}):
        if hasattr(self, '__view__'):
            me = db.table(self.__view__)
            table = self.__view__
        else:
            me = self
            table = me.__table__

        # Filter
        if len(filter):
            for k, v in filter.items():
                me = me.where(k, v)

        # Search
        if search is not None and search != '':
            me = me.where_raw(search)

        # Order
        if order is not None and len(order):
            for k, v in order.items():
                if schema.has_column(table, k) and (v.lower() == 'asc' or v.lower() == 'desc'):
                    me = me.order_by(k, v)

        paged = me.paginate(recPerPage, page)
        result = {
            "total": paged.total,
            "per_page": paged.per_page,
            "current_page": paged.current_page,
            "last_page": paged.last_page,
            "prev_page": paged.previous_page,
            "next_page": paged.next_page,
            "data": paged.serialize()
        }
        return result

    @classmethod
    def getWebList(self, search, args):
        if hasattr(self, '__view__'):
            me = db.table(self.__view__)
            table = self.__view__
        else:
            me = self
            table = me.__table__
        
        recPerPage=10
        page=1

        if 'p' in args:
            page=int(args['p'])
        else:
            args['p']=page

        if 'rp' in args:
            recPerPage=int(args['rp'])
        else:
            args['rp']=recPerPage

        if search is not None and search != '':
            me = me.where_raw(search)

        result = {
            'args':args
        }         
        
        #use simple_paginate to just use next and prev paging
        result['data'] = me.simple_paginate(recPerPage, page)
            
        result['next']=page+1
        if len(result['data'])<recPerPage:
            result['next']=page

        result['prev']=page-1
        if page==1:
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
