from abc import abstractmethod
from dataclasses import dataclass
import typing
import requests

@NotImplemented
@dataclass
class PayloadMachine:
    url : str

    param_list : typing.List[str] = None
    body_list : typing.List[str] = None

    c_max_fail = 10
    c_max_log = 10
    c_use_log = False

    @abstractmethod
    def pre_send(self):
        pass
    
    @abstractmethod
    def post_send(self, res : requests.Response):
        pass

    def send(self,**kwargs):
        pass

    @abstractmethod
    def pre_loop(self):
        pass
    
    @abstractmethod
    def post_loop(self, res : requests.Response):
        pass

    def loop(self, interval : int = 10, timeout : int = 10, **kwargs):
        # verfication


        self.pre_loop()



    
