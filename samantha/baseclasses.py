
import abc

class ModuleBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, preprocessed_sentence):
        pass

    @abc.abstractmethod
    def evaluate_with_context(self, preprocessed_sentence):
        pass

    @property
    def name(self):
        return self.__class__.__name__


class SpeakerBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def speak(self):
        pass


class ListenerBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def listen(self):
        pass
