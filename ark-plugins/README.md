# ark-plugins

Official Plugins.

## ark-evidence (v0.1)

Out-of-process Evidence validator (ADR-0016).

```bash
# exercised via ark-core SubprocessPluginRuntime tests
pytest ark-core/tests/test_plugin_runtime.py -q
```

Rules (initial): accepts `InspectionPass`, `TorqueReport`, `Permit` with non-empty `evidence_id`.
