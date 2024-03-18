from typing import Any, Dict, Callable

# https://stackoverflow.com/questions/6760685/what-is-the-best-way-of-implementing-singleton-in-python
def singleton(class_: Any) -> Callable:
    instances: Dict = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return getinstance
