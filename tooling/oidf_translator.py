class OIDFTranslator:
    def __init__(self, registry):
        self.registry = registry

    def translate(self, provider, raw_payload):
        translated = {}
        for key, value in raw_payload.items():
            canonical_key = self.registry.get_canonical(provider, key)
            if canonical_key:
                translated[canonical_key] = value
            else:
                translated[key] = value
        return translated
