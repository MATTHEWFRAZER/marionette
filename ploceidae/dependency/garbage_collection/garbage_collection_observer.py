from threading import Lock

from six import with_metaclass

from ploceidae.utilities.singleton_implementer import SingletonImplementer
from ploceidae.constants import PHASE_STOP

class GarbageCollectionObserver(with_metaclass(SingletonImplementer)):
    """
    Handles freeing of dependencies to instances. We have the lapsed listener problem in the lcoators.
    This class is needed for the case where an instance depends on an object. Weak references here might be
    an obvious candidate for a solution, however, they will NOT work in the case where an instance's __init__
    depends on a dependency, does not immediately use that reference, and later depends on said dependency in a method
    """

    def __new__(cls, *args, **kwargs):
        instance = super(GarbageCollectionObserver, cls).__new__(cls, *args, **kwargs)
        #gc.callbacks.append(instance)
        return instance

    def __init__(self):
        self.garbage_lock = Lock()
        self.callbacks = []

    def register(self, callback):
        with self.garbage_lock:
            self.callbacks.append(callback)

    def __call__(self, phase, info):
        if phase == PHASE_STOP:
            # we remove filter callbacks that cleanup
            with self.garbage_lock:
                # TODO: probably make async
                self.callbacks = list(callback for callback in self.callbacks if not callback(phase, info))
