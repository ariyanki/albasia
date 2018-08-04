import logging
import hashlib
from var_dump import var_dump

from app import db
from orator import Model, Schema
from app.variable_constant import VariableConstant as VariableConstant
from datetime import datetime

db.connection().enable_query_log()

Model.set_connection_resolver(db)
schema = Schema(db)


class CrudBase(Model):

    __timestamps__ = False

    srcRawQry = ""
    srcQryBind = []

    @classmethod
    def setSrcRawQry(self, strSearch):
        self.srcRawQry = "%s = %s"
        self.srcQryBind = [strSearch, strSearch]

    @classmethod
    def getList(self, recPerPage=25, search=None, filter={}, page=1, order={}):
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
                # if schema.has_column(table, k) and (v is not None and v != ''):
                #     me = me.where(k, v)

        # Search
        if search is not None and search != '':
            self.setSrcRawQry(search)
            me = me.where_raw(search)
            # me = me.where(
            #     me.where_raw(self.srcRawQry, self.srcQryBind)
            # )
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
            return self.response(
                {},
                VariableConstant.DATA_NOT_FOUND_RESCODE,
                VariableConstant.DATA_NOT_FOUND_TITLE,
                VariableConstant.DATA_NOT_FOUND_MESSAGE,
                VariableConstant.DATA_NOT_FOUND_STATUS_CODE)
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
    def getAll(self):
        result = self.get()
        return result

    @classmethod
    def getPagingData(self, raw_query, limit, offset):
        result = self.where_raw(raw_query).simple_paginate(limit, offset)
        return result
