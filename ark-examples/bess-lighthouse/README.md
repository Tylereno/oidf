# BESS Lighthouse Example (RFC 0021)

End-to-end **machine Evidence** commissioning path.

```bash
pip install -e 'ark-core[dev]'
python ark-examples/bess-lighthouse/run_e2e.py /tmp/ark-bess-lighthouse
```

Happy path Evidence types are machine-sourced (`CellVoltageInBand`, `InsulationResistanceOk`, `ThermalStable`) via `ark-telemetry` → `ark-evidence`. No click-to-advance.
