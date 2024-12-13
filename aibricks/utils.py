import xml.etree.ElementTree as ET


def dict_from_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
        return {child.tag.lower(): child.text for child in root}
    except Exception as e:
        print(xml_string)
        raise e


def list_from_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
        return [dict_from_xml(ET.tostring(child)) for child in root]
    except Exception as e:
        print(xml_string)
        raise e


def lookup(data, key, default=...):
    """Look up a value in nested data structures using dot notation."""
    current = data

    for part in key.split('.'):
        try:
            # Handle both positive and negative indices
            if part.lstrip('-').isdigit():
                current = current[int(part)]
            elif hasattr(current, '__getitem__'):
                current = current[part]
            else:
                current = getattr(current, part)
        except (KeyError, IndexError, AttributeError):
            if default is ...:
                raise KeyError(key)
            return default

    return current


class DatabaseFactory:
    _instances = {}

    @classmethod
    def get_connection(cls, path):
        if path not in cls._instances:
            import sqlite3
            from pathlib import Path
            if path != ':memory:':
                Path(path).parent.mkdir(parents=True, exist_ok=True)
            cls._instances[path] = sqlite3.connect(path)
        return cls._instances[path]
