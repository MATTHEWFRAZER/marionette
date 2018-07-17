from framework_primivites.primitive_marker import MarionettePrimitive
from dependency_graph.dependency_graph_manager import DependencyGraphManager
from framework_primivites.dependency_validation_methods import DependencyValidationMethods

__all__ = ["dependency"]


class Dependency(MarionettePrimitive):
    """decorator is a class object because that will make it easier to hook into later"""

    def __init__(self, **kwargs):
        DependencyValidationMethods.input_validation_to_init(kwargs)
        self.scope = kwargs.get("scope", "function")

    def __call__(self, decorated_obj):
        # we need to take this algorithm into somne place else, question do we want the end caller to be in the dependency graph
        # do I need to do classmethod check here? Maybe because the class method itself (unbounded will not be callable). If a user does class
        # introspection and decides to decorate a classmethod accessed via __dict__ yeah
        DependencyValidationMethods.input_validation_for_dependency_obj(decorated_obj)

        DependencyGraphManager.add_dependency(decorated_obj)
        resolved_dependencies = DependencyGraphManager.resolve_dependencies(decorated_obj)

        def inner(*unresolved_dependencies):
            dependencies = unresolved_dependencies + resolved_dependencies
            return decorated_obj(*dependencies)

        return inner


dependency = Dependency
