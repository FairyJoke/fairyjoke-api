import functools
import importlib
import json
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from pathlib import Path

import toml
import yaml


class Element(ET.Element):
    @property
    def value(self):
        coerce = str
        if type := self.get("__type"):
            if type[0] in ("s", "u"):
                coerce = int
        return coerce(self.text)

    def parse(self, accessor):
        return self.find(accessor).value

    def parse_all(self, **accessors):
        return {k: self.parse(v) for k, v in accessors.items()}

    def __str__(self):
        return self.value


tree_builder = ET.TreeBuilder(element_factory=Element)


class Data:
    def __init__(self, path):
        self.path = path

    def __getattr__(self, name):
        return self.load(name)

    def all(self):
        return [self.load(x.name) for x in self.path.glob("*")]

    @functools.cache
    def load(self, name):
        if isinstance(name, str):
            path = self.path.glob(name + ".*")
            path = next(path, None)
        elif isinstance(name, Path):
            path = name
        else:
            raise ValueError(f"Invalid name type: {name}")
        if not path:
            raise FileNotFoundError(f"File not found: {name}")
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if path.suffix == ".json":
            return json.loads(path.read_text())
        if path.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(path.read_text())
        if path.suffix == ".toml":
            return toml.loads(path.read_text())
        if path.suffix == ".ini":
            config = ConfigParser()
            config.read(path)
            return config
        if path.suffix == "*.py":
            module = importlib.import_module(path.stem)
            return module.main()
        if path.suffix == ".xml":
            with path.open(encoding="cp932", errors="ignore") as f:
                return ET.fromstring(
                    f.read(), parser=ET.XMLParser(target=tree_builder)
                )
        raise ValueError(f"Unknown file type: {path}")
