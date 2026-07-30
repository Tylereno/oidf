
import json

class OIDFRegistry:
    def __init__(self, schema_dir="schemas"):
        self.schema_dir = schema_dir
        self.mappings = {}
        self._load_schemas()

    def _load_schemas(self):
        # Mocking registry structure
        self.mappings = {
            "jira": {"status": "workflow.status.current", "assignee": "actors.user.id"},
            "github": {"state": "workflow.status.current", "author": "actors.user.id"}
        }

    def get_canonical(self, provider, native_key):
        return self.mappings.get(provider, {}).get(native_key)
