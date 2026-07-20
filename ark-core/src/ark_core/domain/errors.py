"""Core domain errors — no I/O."""


class ArkCoreError(Exception):
    """Base error for ark-core."""


class UnauthorizedError(ArkCoreError):
    pass


class InvalidTransitionError(ArkCoreError):
    pass


class SchemaValidationError(ArkCoreError):
    pass


class QuarantineError(ArkCoreError):
    pass


class PluginAllowlistError(ArkCoreError):
    pass
