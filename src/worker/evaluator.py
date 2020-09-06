#!/usr/bin/env python3
import abc

class Evaluator(abc.ABC):
    @abc.abstractclassmethod
    @abc.abstractmethod
    def add_new_task():
        pass

    @abc.abstractclassmethod
    @abc.abstractmethod
    def get_one_task():
        pass

    @abc.abstractclassmethod
    @abc.abstractmethod
    def score():
        pass

class EasyEvaluator(Evaluator):
    def __init__(self):
        pass

    def add_new_task(self):
        pass

    def get_one_task(self):
        pass

    def score(self):
        pass

if __name__ == "__main__":
    x = EasyEvaluator()
