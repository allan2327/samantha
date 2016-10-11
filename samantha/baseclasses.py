
import abc

class ModuleBase(abc.ABC):
    
    @abc.abstractmethod
    def evaluate(self, preprocessed_sentence):
        pass

    @abc.abstractmethod
    def evaluate_with_context(self, preprocessed_sentence):
        pass

    @abc.abstractmethod
    def act(self, preprocessed_sentence):
        pass


class SpeakerBase(abc.ABC):
    
    @abc.abstractmethod
    def speak(self):
        pass


class ListenerBase(abc.ABC):
    
    @abc.abstractmethod
    def listen(self):
        pass

