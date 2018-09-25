from scope_binding.scope_enum import ScopeEnum


class ScopeBindingMethods(object):

    DECORATED = {}

    def scope_binding_decorator(self, dependency_graph, dependency_obj, inner_obj):
        if dependency_obj.scope == ScopeEnum.INSTANCE and not self.is_decorated(inner_obj):
            self.decorate_instance_obj(dependency_graph, dependency_obj.dependency_obj)

    @staticmethod
    def decorate_instance_obj(dependency_graph, obj):
        try:
            obj_instance = obj.__self__
        except AttributeError:
            raise ValueError("{} is not bound to class instance, and can not be defined with instance scope")
        def new_del(self_ref):
            if hasattr(obj, "__del__"):
                obj_instance.__del__()
            if self_ref is obj_instance:
                dependency_graph[obj.__name__].delete_entry_from_service_locator(str(obj_instance.__self__))
        obj_instance.__class__.__del__ = new_del

    @classmethod
    def is_decorated(cls, obj):
        cls.DECORATED[obj] = True

