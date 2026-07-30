import json
import yaml

class OIDFRegistry:
    def __init__(self, schema_path="../core_schemas/canonical/dictionary.yaml"):
        self.schema_path = schema_path
        self.mappings = {}
        self._load_schemas()

    def _load_schemas(self):
        # Loads from the canonical dictionary YAML
        with open(self.schema_path, 'r') as f:
            data = yaml.safe_load(f)
            self.mappings = data.get('oidf_registry', {}).get('domains', {})

    def get_canonical(self, provider, native_key):
        # Traversal logic for mapped dictionary
        for domain, items in self.mappings.items():
            if native_key in items:
                return f"{domain}.{native_key}"
        return None
