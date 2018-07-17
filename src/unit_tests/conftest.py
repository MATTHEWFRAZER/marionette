import sys

import pytest

sys.path.append("..")
from dependency_graph.dependency_graph import DependencyGraphNode
from dependency_graph.dependency_graph_manager import DependencyGraphManager
from framework_primivites.container import Container
from framework_primivites.dependency import dependency


@pytest.fixture
def dependency_graph_manager():
    yield DependencyGraphManager
    DependencyGraphManager.DEPENDENCY_GRAPH.clear()


@pytest.fixture
def dependency_graph_with_cycle():
    # permute these
    def a(b): pass
    def b(c): pass
    def c(a): pass

    return a, b, c


@pytest.fixture
def dependency_graph():
    def a(b): return "a" + b
    def b(c): return "b" + c
    def c(): return "c"

    return a, b, c


@pytest.fixture
def dependency_graph2():
    def d(e): return "d" + e
    def e(f): return "e" + f
    def f(): return "f"

    return d, e, f


@pytest.fixture
def dependency_graph_with_obj_that_depends_on_all_other_nodes(dependency_graph):
    def x(a, b, c): return "x" + a + b + c
    return (x,) + dependency_graph


@pytest.fixture
def dependency_graph_node_with_in_edges():
    return DependencyGraphNode(lambda _: _, "a", "b", "c")


@pytest.fixture
def dependency_graph_node_with_no_in_edges():
    return DependencyGraphNode(lambda _: _)


@pytest.fixture
def container(dependency_graph_with_obj_that_depends_on_all_other_nodes, dependency_graph_manager):
    for dependency in dependency_graph_with_obj_that_depends_on_all_other_nodes:
        dependency_graph_manager.add_dependency(dependency)
    return Container


@pytest.fixture
def container2(dependency_graph2, dependency_graph_manager, container):
    for dependency in dependency_graph2:
        dependency_graph_manager.add_dependency(dependency)
    return container


@pytest.fixture
def obj_to_wire_up(dependency_graph_with_obj_that_depends_on_all_other_nodes):
    return dependency_graph_with_obj_that_depends_on_all_other_nodes[0]


@pytest.fixture
def obj_to_wire_up2(dependency_graph2):
    return dependency_graph2[0]


@pytest.fixture
def dependency_graph_node():
    return DependencyGraphNode


@pytest.fixture
def dependency_decorator():
    yield dependency
    DependencyGraphManager.DEPENDENCY_GRAPH.clear()


@pytest.fixture(params=[(("a",), ("abc",)), (("b",), ("bc",)), (("a", "b"), ("abc", "bc"))])
def partial_dependency_fixture(request, container):
    attributes = {"ignored_dependencies": request.param[0], "left_over_dependencies": request.param[1], "container": container}
    return type("PartialDependencyFixture", (), attributes)