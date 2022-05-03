import numpy as np
from dataclasses import dataclass

@dataclass
class DCCA_DataStructure:
    def __init__(self, label):
        self.label = label
        self.cautionLevel = None
        self.distance = None
        self.position = None

    def __str__(self):
        info = f"Object : {self.label}\nid : {str(id(self))}"
        return info

    