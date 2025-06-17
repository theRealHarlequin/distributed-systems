# Lab Task 4: Monitoring Operating Parameters in a Production Facility

## Task Description

The operating parameters of machines in a production environment are to be monitored. To achieve this, various sensors are mounted on the machines that cyclically measure:

- Temperature  
- Pressure  
- Vibration behavior  

These values are transmitted to a **central monitoring unit**.

Sensors must be **hot-swappable** — meaning they can be added or removed during runtime.

## System Requirements

- The **monitoring unit** records the incoming data.
- It performs **frequency analysis** on vibration data.
- It determines the **operating state** of each machine based on configurable **threshold values**.
- The frequency analysis must be **scalable** in terms of computational power.
- Configurable interfaces must be provided to:
  - Set threshold values
  - Output **aggregated measurement data**
  - Output **status messages** for visualization

## Assignment

Design a solution concept for the task described above.

### Deliverables

- ✅ Design documentation using **block diagrams** and **sequence diagrams**  
- ✅ Message format documentation using **Protocol Buffers (Protobuf-IDL)**  
- ✅ Implementation of your concept  
- ✅ Demonstration of its functionality  
