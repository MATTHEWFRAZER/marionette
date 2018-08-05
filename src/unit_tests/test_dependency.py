from functools import partial

import pytest


class TestDependency:

    def test_dependency_application_with_runtime_syntax(self, dependency_decorator):
        application_callback = lambda: dependency_decorator(lambda: None)
        self.dependency_application("runtime", application_callback)

    def test_dependency_application_with_decorator_syntax(self, dependency_decorator):
        application_callback = partial(self.decorator_dependency_application, dependency_decorator)
        self.dependency_application("decorator", application_callback)

    @pytest.mark.xfail(raises=ValueError)
    def test_dependency_application_to_obj_that_depends_on_itself(self, dependency_decorator):
        @dependency_decorator
        def a(a): pass

    @pytest.mark.xfail(raises=ValueError)
    def test_dependency_application_to_obj_that_is_missing_name_attribute(self, dependency_decorator):
        # assumes partial object will not have __name__ attribute
        dependency_decorator(partial(lambda: None))

    @pytest.mark.xfail(raises=ValueError)
    def test_dependency_application_to_obj_that_is_not_callable(self, dependency_decorator):
        dependency_decorator("invalid")

    @pytest.mark.skip(reason="support for decorator means that this check will not be done until wiring")
    @pytest.mark.xfail(raises=BaseException)
    def test_dependency_application_to_obj_that_has_missing_dependency_at_time_of_application(self, dependency_decorator):
        def a(b): pass
        dependency_decorator(a)

    def test_dependency_application_with_decorator_syntax_with_a_second_decorator(self, dependency_decorator, separate_decorator):
        try:
            @dependency_decorator
            @separate_decorator
            def a(b): pass
        except Exception as ex:
            pytest.fail("could not decorate previously decorated function. Ex: {0}".format(ex))

    def test_dependency_application_with_scope_passed_as_argument(self, dependency_decorator):
        try:
            @dependency_decorator(scope="function")
            def a(): pass
        except Exception as ex:
            pytest.fail("could not decorate function. Ex: {0}".format(ex))

    @pytest.mark.skip(reason="as of now, invalid. will trick control_initialization into thinking no decoration needs to be called")
    def test_dependency_application_with_no_arguments(self, dependency_decorator):
        try:
            @dependency_decorator()
            def a(): pass
        except Exception as ex:
            pytest.fail("could not decorate function while calling dependency_decorator with no arguments. Ex: {0}".format(ex))

    @staticmethod
    def dependency_application(syntax, application_callback):
        try:
            application_callback()
        except Exception as ex:
            pytest.fail("could not decorate simple function with {0} syntax. Ex: {1}".format(syntax, ex))

    @staticmethod
    def decorator_dependency_application(dependency_decorator):
        @dependency_decorator
        def a(): pass