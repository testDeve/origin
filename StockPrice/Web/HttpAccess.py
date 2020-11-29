from abc import ABCMeta, abstractmethod

class HttpAccess(metaclass=ABCMeta):

    @abstractmethod
    def set_url(url):
        pass

    @abstractmethod
    def set_params(param):
        pass

    @abstractmethod
    def send_request(self):
        pass

    @abstractmethod
    def set_headers(header):
        pass

    @abstractmethod
    def reset_headers(self):
        pass

    @abstractmethod
    def create_headers(self):
        pass
