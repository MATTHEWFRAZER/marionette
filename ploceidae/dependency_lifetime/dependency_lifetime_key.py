from inspect import getsourcefile

import six

from ploceidae.dependency_lifetime.dependency_lifetime_enum import DependencyLifetimeEnum

class DependencyLifetimeKey(object):
    def __init__(self, dependency_object):
        self.dependency_object = dependency_object
        self.alt_key = None

    def init_dependency_lifetime(self, dependency_lifetime):
        """resolves dependency_lifetime here because we don't get dependency_lifetime until wiring up dependencies"""
        self.dependency_lifetime = dependency_lifetime

    def init_alt_key(self, time_stamp):
        self.alt_key_format = "alt::" + "{}::" + str(self.dependency_object) + "::" + str(time_stamp)

    def __repr__(self):
        if self.dependency_lifetime == DependencyLifetimeEnum.SESSION:
            return "session"
        elif self.dependency_lifetime == DependencyLifetimeEnum.MODULE:
            return "{0}".format(getsourcefile(self.dependency_object))
        elif self.dependency_lifetime == DependencyLifetimeEnum.CLASS:
            return self.handle_class_dependency_lifetime()
        elif self.dependency_lifetime == DependencyLifetimeEnum.INSTANCE:
            return self.handle_instance_dependency_lifetime()
        elif self.dependency_lifetime == DependencyLifetimeEnum.FUNCTION:
            return self.handle_function_dependency_lifetime()
        else:
            raise NotImplementedError("{0} not a valid dependency_lifetime".format(self.dependency_lifetime))

    def handle_class_dependency_lifetime(self):
        try:
            return "{0}".format(self.dependency_object.__self__.__class__)
        except AttributeError: # TODO PLOCEIDAE 11: if dependency_object is for some reason not bound correctly (i.e. dynamically set method like a lambda)
            raise ValueError("{0} does not have a __self__.__class__ reference to resolve class dependency_lifetime for".format(self.dependency_object))

    def handle_instance_dependency_lifetime(self):
        if isinstance(self.dependency_object, six.class_types):
            return self.alt_key_format.format(self.dependency_lifetime)
        if hasattr(self.dependency_object, "__name__") and self.dependency_object.__name__ == "__init__":
            return self.alt_key_format.format(self.dependency_lifetime)
        if hasattr(self.dependency_object, "__self__"):
            return "{0}".format(self.dependency_object.__self__)
        return "{0}".format(self.dependency_object)

    def handle_function_dependency_lifetime(self):
        try:
            instance_binding = self.dependency_object.__self__
        except AttributeError:
            instance_binding = "null"
        try:
            used_name = self.dependency_object.__qualname__
        except:
            used_name = str(self.dependency_object)
        return "{0}::{1}".format(instance_binding, used_name)

    @staticmethod
    def generate_alt_dependency_lifetime_key(obj, dependency_lifetime, time_stamp):
        return "alt::{}::{}::{}".format(dependency_lifetime, obj, time_stamp)

    @staticmethod
    def has_function_dependency_lifetime(dependency_lifetime_key):
        return "::" in dependency_lifetime_key.dependency_lifetime