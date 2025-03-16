import functools
import importlib
import json
import xml.etree.ElementTree as ET
from configparser import ConfigParser

import toml
import yaml


class Data:
    def __init__(self, path):
        self.path = path

    def __getattr__(self, name):
        return self.load(name)

    def all(self):
        return [self.load(x.name) for x in self.path.glob("*")]

    @functools.cache
    def load(self, name):
        path = self.path.glob(name + ".*")
        path = next(path, None)
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
                return ET.fromstring(f.read())
        raise ValueError(f"Unknown file type: {path}")
