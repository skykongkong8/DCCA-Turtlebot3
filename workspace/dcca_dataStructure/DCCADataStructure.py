import numpy as np
from dataclasses import dataclass

@dataclass
class DCCA_DataStructure:
    label : str = label
    cautionLevel : int = None
    distance : float = None
    position = None

    def __str__(self):
        info = f"Object : {self.label}\nid : {str(id(self))}"
        return info

    