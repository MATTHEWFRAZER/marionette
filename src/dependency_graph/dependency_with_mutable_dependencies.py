# make primitive
class DependencyWithMutableDependencies(object):
    def __init__(self, dependency_obj):
        self.dependency_obj = dependency_obj.dependency_obj
        self.dependencies = dependency_obj.dependencies
        self.mutable_dependencies = dependency_obj.dependencies[:]