import json
from typing import Dict, Any, List, Union

class JsonToClassConverter:
    @staticmethod
    def _to_python_class_name(key: str) -> str:
        parts = key.split('_')
        return ''.join(part.capitalize() for part in parts)

    @staticmethod
    def _singularize(key: str) -> str:
        if key.endswith('s'):
            return key[:-1]
        return key

    @classmethod
    def convert(cls, class_name: str, json_data: Union[Dict[str, Any], List[Any]], parent_class: type = None) -> type:
        if isinstance(json_data, list):
            result = []
            for item in json_data:
                if isinstance(item, (dict, list)):
                    singular_name = cls._singularize(class_name)
                    converted_item = cls.convert(singular_name, item)
                    if isinstance(converted_item, type):
                        setattr(converted_item, 'json', item)
                    result.append(converted_item)
                else:
                    result.append(item)
            return result
        
        bases = (parent_class,) if parent_class else ()
        new_class = type(class_name, bases, {})
        
        setattr(new_class, 'json', json_data)
        
        for key, value in json_data.items():
            if isinstance(value, dict):
                nested_class_name = cls._to_python_class_name(key)
                nested_class = cls.convert(nested_class_name, value)
                setattr(new_class, key, nested_class)
                setattr(nested_class, 'json', value)
            elif isinstance(value, list):
                singular_key = cls._singularize(key)
                list_items = cls.convert(singular_key, value)
                setattr(new_class, key, list_items)
            else:
                setattr(new_class, key, value)
        
        return new_class