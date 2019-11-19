from abc import ABCMeta, abstractmethod
import boto3

class DynamoDB(metaclass=ABCMeta):

    def aws_DynamoDB(self):
        self.dynamo_db = boto3.client('dynamodb')

    @abstractmethod
    def initialize(**kwargs):
        pass

    @abstractmethod
    def insert(**kwargs):
        pass

    @abstractmethod
    def select(**kwargs):
        pass