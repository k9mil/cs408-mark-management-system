from typing import Any, Dict, Callable


def singleton(class_: Any) -> Callable:
    instances: Dict = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return getinstance
