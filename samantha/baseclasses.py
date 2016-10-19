
import abc

class ModuleBase(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def evaluate(self, preprocessed_sentence):
        pass

    @abc.abstractmethod
    def evaluate_with_context(self, preprocessed_sentence):
        pass

    @abc.abstractmethod
    def act(self, preprocessed_sentence):
        pass


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

