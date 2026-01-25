# Sensor Architecture - Bill of Materials (DRAFT)

**VOID-013: Sensor-Architektur (BOM & Protokoll)**
**Status:** DRAFT - Placeholder for sensor layer specification
**Created:** 2026-01-25
**Version:** 1.0

---

> **⚠️ SAFETY NOTICE**
>
> This is a **components-level overview only** for potential sensor layer implementation.
>
> **This document does NOT contain:**
> - Operational laboratory instructions
> - Risky assembly procedures
> - Medical device guidance
> - Human subject protocols
>
> Any hardware implementation requires:
> - Qualified supervision
> - Institutional review board (IRB) approval for human subjects
> - Compliance with local regulations
> - Professional safety assessment

---

## Overview

This document provides a **candidate component list** for potential biosignal and environmental sensing capabilities in the entaENGELment framework. This is a **component-level specification**, not an operational protocol.

**Scope:**
- Component specifications only
- Data interface definitions (see `spec/sensors.spec.json`)
- Traceability to framework requirements
- Safety boundaries and limitations

**Out of Scope:**
- Assembly instructions
- Medical diagnostics
- Human subject experimentation
- Certification/compliance claims

---

## Core Components (Candidate List)

### 1. Biosignal Acquisition

**Component ID:** `SENSOR-BIO-001`
**Type:** EEG/Biosignal Interface
**Candidate Example:** OpenBCI Cyton Board (8-channel)

**Specifications:**
- **Channels:** 8 differential inputs (example: Fp1, Fp2, C3, C4, P3, P4, O1, O2)
- **Sampling Rate:** 250 Hz (adjustable)
- **Resolution:** 24-bit ADC
- **Interface:** USB/Bluetooth
- **Power:** 3.3V-5V DC

**Rationale:**
- Open-source hardware platform
- Research-grade signal quality
- Community support and documentation
- Python SDK available

**Framework Integration:**
- Data format: See `spec/sensors.spec.json` → `biosignal_channels.eeg`
- Sample rate: 250 Hz baseline (spec/sensors.spec.json → `biosignal_channels.sampling_rate`)
- Traceability: Maps to entaENGELment resonance metrics (MI, PLV, phase coherence)

**Safety Notes:**
- Not a medical device
- Research use only
- Requires proper electrode placement training
- Signal quality depends on electrode-skin impedance

**Status:** DRAFT - Example component, not finalized selection

---

### 2. Environmental Sensors

**Component ID:** `SENSOR-ENV-001`
**Type:** Multi-Modal Environmental Sensor
**Candidate Example:** Bosch BME680

**Specifications:**
- **Temperature:** -40°C to +85°C (±0.5°C accuracy)
- **Humidity:** 0-100% RH (±3% accuracy)
- **Pressure:** 300-1100 hPa (±0.6 hPa accuracy)
- **Gas:** VOC sensor (air quality index)
- **Interface:** I2C/SPI
- **Power:** 1.8V-3.6V

**Rationale:**
- Single-chip multi-modal sensing
- Low power consumption
- Standard I2C interface
- Widely available and documented

**Framework Integration:**
- Data format: See `spec/sensors.spec.json` → `environmental`
- Units: Celsius, %, hPa (as per spec)
- Traceability: Environmental context for resonance state correlation

**Status:** DRAFT - Example component, not finalized selection

---

### 3. Processing Unit

**Component ID:** `SENSOR-PROC-001`
**Type:** Edge Processing Platform
**Candidate Example:** Raspberry Pi 4 Model B (4GB RAM)

**Specifications:**
- **CPU:** Quad-core ARM Cortex-A72 @ 1.5GHz
- **RAM:** 4GB LPDDR4
- **Storage:** microSD (32GB+ recommended)
- **I/O:** GPIO (40-pin), USB 3.0, Ethernet, Bluetooth, WiFi
- **Power:** 5V/3A USB-C

**Rationale:**
- Python 3.x support (entaENGELment framework requirement)
- GPIO for sensor interfacing
- Edge processing capability (real-time signal analysis)
- Well-documented ecosystem

**Framework Integration:**
- Runs entaENGELment sensor ingestion layer
- Real-time computation of MI, PLV metrics
- MQTT/HTTP client for data transmission (see spec/sensors.spec.json)

**Status:** DRAFT - Example component, not finalized selection

---

## Data Flow Architecture (High-Level)

```
┌─────────────────┐
│ Biosignal       │
│ Sensors         ├──────┐
│ (e.g. EEG)      │      │
└─────────────────┘      │
                         │
┌─────────────────┐      │      ┌─────────────────┐
│ Environmental   │      ├─────>│ Processing      │
│ Sensors         ├──────┘      │ Unit            │
│ (Temp/Hum/etc)  │             │ (Edge compute)  │
└─────────────────┘             └────────┬────────┘
                                         │
                                         │ MQTT/HTTP
                                         │ (JSON format)
                                         │
                                         ▼
                                ┌─────────────────┐
                                │ entaENGELment   │
                                │ Backend         │
                                │ (Analysis)      │
                                └─────────────────┘
```

**Protocol:** See `spec/sensors.spec.json` for data format and transport details.

---

## Traceability Matrix

Maps sensor components to entaENGELment framework requirements:

| Component ID       | Spec Reference                     | Framework Module          | Status  |
|--------------------|------------------------------------|---------------------------|---------|
| SENSOR-BIO-001     | spec/sensors.spec.json (biosignal) | Fractalsense (resonance)  | DRAFT   |
| SENSOR-ENV-001     | spec/sensors.spec.json (environmental) | Context layer         | DRAFT   |
| SENSOR-PROC-001    | spec/sensors.spec.json (protocol)  | Ingestion pipeline        | DRAFT   |

**TODO:** Validate traceability against actual framework requirements once sensor layer is implemented.

---

## Bill of Materials Table (Example)

| Item | Quantity | Candidate Part # | Est. Cost (USD) | Status  | Notes                  |
|------|----------|------------------|-----------------|---------|------------------------|
| EEG Interface | 1 | OpenBCI Cyton    | ~$500           | DRAFT   | 8-channel biosignal    |
| Environment Sensor | 1-4 | BME680 | ~$10 each | DRAFT | One per location |
| Processing Unit | 1 | Raspberry Pi 4B (4GB) | ~$55 | DRAFT | Edge compute |
| Power Supply | 1 | USB-C 5V/3A | ~$10 | DRAFT | Pi power |
| Storage | 1 | microSD 64GB | ~$15 | DRAFT | OS + data buffer |
| EEG Electrodes | 1 set | Gold-cup or Ag/AgCl | ~$50-200 | DRAFT | Depends on quality |
| **Total** | - | - | **~$640-900** | **DRAFT** | **Rough estimate** |

**Note:** Costs are approximate and vary by supplier, region, and procurement volume. This is NOT a procurement recommendation.

---

## Integration Protocol

For data format, communication protocol, and sampling specifications, see:

**📄 `spec/sensors.spec.json`**

Key integration points:
- **Transport:** MQTT or HTTP/REST (TBD based on deployment)
- **Encoding:** JSON
- **Baseline Rate:** 1 Hz (environmental), 250 Hz (biosignals)
- **Timestamp Format:** ISO8601 UTC
- **Sensor ID:** Unique identifier per physical sensor

---

## Safety & Compliance Boundaries

### What This BOM Is

✅ Component-level specification
✅ Data interface definition
✅ Framework integration overview
✅ Traceability to requirements

### What This BOM Is NOT

❌ Assembly instructions
❌ Medical device protocol
❌ Human subject research procedure
❌ Certification/approval claim
❌ Operational guidance

### Required Before Implementation

If you proceed with hardware implementation, you MUST:

1. **Institutional Review:** Obtain IRB/ethics committee approval for any human subjects research
2. **Qualified Supervision:** Work with qualified biomedical engineers or researchers
3. **Regulatory Compliance:** Verify compliance with local regulations (FDA, CE, etc. if applicable)
4. **Risk Assessment:** Conduct formal safety and risk assessment
5. **Training:** Ensure proper training for all personnel handling biosignals
6. **Informed Consent:** Obtain informed consent from any human subjects

**No claims are made about fitness for any medical, diagnostic, or therapeutic use.**

---

## References

- **VOIDMAP.yml:** VOID-013 (Sensor-Architektur)
- **Specification:** `spec/sensors.spec.json`
- **Framework:** entaENGELment resonance metrics (MI, PLV, FD)
- **OpenBCI Documentation:** https://docs.openbci.com
- **BME680 Datasheet:** https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme680/

---

## TODO for Full Implementation

- [ ] Validate component selection against actual framework requirements
- [ ] Benchmark candidate biosignal acquisition systems
- [ ] Define electrode placement protocol (reference standard: 10-20 system)
- [ ] Specify calibration procedures for environmental sensors
- [ ] Design power management and data buffering strategy
- [ ] Implement data ingestion layer in entaENGELment backend
- [ ] Create integration tests with mock sensor data
- [ ] Document deployment procedures (edge device setup)
- [ ] Define data retention and privacy policies
- [ ] Establish maintenance and calibration schedules

---

**Maintainer:** entaENGELment project
**Last Updated:** 2026-01-25
**Document Status:** DRAFT Placeholder (VOID-013 closure)
