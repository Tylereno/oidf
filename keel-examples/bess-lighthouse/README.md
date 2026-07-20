# BESS Lighthouse Example (RFC 0021)

End-to-end **machine Evidence** commissioning path.

```bash
pip install -e 'keel-core[dev]'
python keel-examples/bess-lighthouse/run_e2e.py /tmp/keel-bess-lighthouse
```

Happy path Evidence types are machine-sourced (`CellVoltageInBand`, `InsulationResistanceOk`, `ThermalStable`) via `keel-telemetry` → `keel-evidence`. No click-to-advance.
