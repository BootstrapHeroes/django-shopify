# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from shopify_app.utils.render import render, render_string
from shopify_app.utils.python import convert_to_bool


class BaseService(object):

    _repo = property(fget=lambda self: self.entity.objects)
    _page_size = 10

    default_query_params = {}

    def __getattr__(self, name):
        """
            Delegates automatically all undefined methods on the repository entity.            
        """

        def decorator(*args, **kwargs):

            method = getattr(self._repo, name)
            if method is None:
                raise AttributeError("'%s' has no attribute '%s'" % (self.__class__.__name__, name))

            if not kwargs.pop("without_filters", False):
                for key, value in self.default_query_params.iteritems():
                    kwargs.setdefault(key, value)

            return method(*args, **kwargs)

        return decorator

    def get_page(self, page=0, size=None, min_page=None, **kwargs):

        if size is None:
            size = self._page_size

        page = int(page)

        if min_page is not None:
            min_page = int(min_page)
            limit = (page + 1) * size
            offset = min_page * size
        else:
            limit = (page + 1) * size
            offset = size * page

        return self._get_objects(self._get_page_query(offset, limit, **kwargs))

    def _get_page_query(self, offset, limit, **kwargs):

        return self.all()[offset:limit]

    def list(self, start, size, **kwargs):
        page = int(start / size)
        return self.get_page(page=page, size=size, min_page=None, **kwargs)

    def _get_objects(self, objects):
        """ Override to add behaviour """

        return objects

    def get_one(self, *args, **kwargs):

        objects = self.filter(*args, **kwargs)
        return objects[0] if objects else None

    def new(self, *args, **kwargs):

        return self.entity(*args, **kwargs)

    def _get_or_new(self, *args, **kwargs):

        try:
            obj, created = self.get_or_create(*args, **kwargs)
        except:
            obj, created = self.entity(*args, **kwargs), True
        return obj, created

    def get_or_new(self, *args, **kwargs):

        obj, _ = self._get_or_new(*args, **kwargs)
        return obj

    def update_or_create(self, pre_create_function=None, pre_update_function=None, *args, **kwargs):

        entity_id = kwargs.pop("id", None)
        if entity_id:
            
            if pre_update_function is not None:
                pre_update_function(kwargs)

            entity = self.get(id=entity_id)
            for key, value in kwargs.iteritems():
                setattr(entity, key, value)
            
        else:
            if pre_create_function is not None:
                pre_create_function(kwargs)

            entity = self.new(**kwargs)

        entity.save()
        return entity

    def get_or_new_created(self, *args, **kwargs):

        return self._get_or_new(*args, **kwargs)

    def get_form(self):

        return None

    def _get_data(self, request, *args, **kwargs):

        data = dict([(key, value) for key, value in request.POST.iteritems() if key != "csrfmiddlewaretoken"])
        data.update(self._get_additional_data(request))
        return data

    def _get_additional_data(self, request, *args, **kwargs):

        return {}

    def _get_entity(self, request, *args, **kwargs):

        return self.get_or_new(**self._get_data(request))

    def _set_data(self, entity, request, *args, **kwargs):

        data = self._get_data(request)
        for key, value in data.iteritems():
            setattr(entity, key, value)
        return entity

    def set_attrs(self, entity, attrs):

        for key, value in attrs.iteritems():
            setattr(entity, key, value)

    def save_entity(self, entity, *args, **kwargs):

        entity.save()

    def save(self, request, *args, **kwargs):

        entity = self._get_entity(request, *args, **kwargs)

        self._set_data(entity, request, *args, **kwargs)
        self.save_entity(entity, *args, **kwargs)
        self._post_save(entity, request, *args, **kwargs)

        return entity

    def _post_save(self, entity, request, *args, **kwargs):

        pass

    def render(self, template, context):

        return render(template, context)

    def render_string(self, string, context):

        return render_string(string, context)

    def get_object_or_404(self, **kwargs):

        return get_object_or_404(self.entity, **kwargs)

    def delete(self, *args, **kwargs):

        logical_delete = kwargs.pop("logical", False)

        objs = self.filter(*args, **kwargs)

        if not objs:
            return False

        for obj in objs:
            if not logical_delete:
                obj.delete()
            else:
                obj.active = False
                obj.save()

        return True

    def get_formated_sum(self, value):

        if value is None:
            value = 0

        return "%.2f" % value

    def _render_row_value(self, row_data, render):

        if isinstance(render, basestring):
            if isinstance(row_data, dict):
                return unicode(row_data[render])
            else:
                return unicode(getattr(row_data, render))
        else:
            return unicode(render(row_data))

    def get_params(self, data, params):

        dict_params = {}
        for param in params:
            dict_params[param] = data.get(param)
        return dict_params

    def convert_to_bool(self, data, params):

        convert_to_bool(data, params)

    def to_bool(self, param):

        return bool(int(param))

    def get_action_params(self, request, params_names, prefix="", bar_action=True):

        complete_names = ["%s%s" % (prefix, param) for param in params_names]

        params = self.get_params(request.POST, complete_names)

        if bar_action:
            boolean_params = ["%s%s" % (prefix, param) for param in ["is_main_action", "is_side_action"]]
            self.convert_to_bool(params, boolean_params)

        final_params = {}
        for key, value in params.iteritems():
            new_key = key.replace(prefix, "")
            final_params[new_key] = value

        return final_params

    def check_nullables(self, data, params):

        for param in params:
            if not data.get(param):
                data[param] = None
