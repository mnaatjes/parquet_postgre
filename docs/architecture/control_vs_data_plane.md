# Control Plane vs. Data Plane Architecture

This document defines the core architectural split for the Elite Dangerous Parquet Pipeline. To handle 200GB+ of data with high reliability and human oversight, we use a "Control vs. Data Plane" separation.

## 1. The Core Philosophy
The pipeline is split into two distinct, decoupled environments:

*   **The Control Plane (SIP):** The "Lawmaker." Responsible for discovery, schema inference, normalization design, and human sign-off. It defines *what* the data should look like.
*   **The Data Plane (ETL):** The "Law Enforcer." Responsible for high-speed validation, transformation, and loading. It executes the *work* based on the rules set by the Control Plane.

## 2. Why This Split?
1.  **Safety:** The 200GB ETL process is "dumb" and never runs "blind." It only processes data that has been explicitly "signed off" by a human in the Control Plane.
2.  **Scalability:** The Control Plane (SIP) runs on small samples (the "Lab"), making it fast and interactive. The Data Plane (ETL) is optimized for massive batch processing (the "Factory").
3.  **Decoupling:** You can change the discovery logic (e.g., using different inference tools) without ever touching the stable, high-performance ETL code.

## 3. The Handshake: Data Contracts
The two planes never share memory or complex code. They communicate exclusively through **Data Contracts**—JSON files that define the source, the schema, and the normalization rules.

| Feature | Control Plane (SIP) | Data Plane (ETL) |
| :--- | :--- | :--- |
| **Role** | Brain / Lawmaker | Muscle / Enforcer |
| **Data Scope** | 5KB - 10MB Samples | 200GB+ Full Files |
| **Interface** | Interactive CLI | Automated Batch |
| **Artifact** | Generates Contracts | Consumes Contracts |
| **Speed** | Human-speed (Low) | Machine-speed (High) |
