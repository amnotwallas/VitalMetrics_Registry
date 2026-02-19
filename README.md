# Vital Metrics Registry API

`vital_metrics_registry` is the backend API for a digital health dashboard. Its design prioritizes architectural clarity, data integrity, and a clear separation between raw data and derived insights.

## Core Design Philosophy

The system is built on a single, fundamental principle: **the backend's single source of truth is raw, granular metric data.** All aggregate views, such as daily KPIs or weekly activity charts, are **derived on-the-fly** from this raw data at request time.

This approach offers several key advantages:
1. **Data Integrity:** It eliminates data duplication and the risk of synchronization issues between raw and pre-computed data.
2. **Flexibility:** The logic for calculating aggregates can be changed or corrected at any time, and the updates will immediately apply to all historical data. New types of aggregates can be added without data migration.
3. **Simplicity:** The persistence layer remains incredibly simple and stable, with a single, well-defined `Metric` table at its core.

##System Behavior

### Data Persistence (The Source of Truth)

- All incoming data points are stored in the `Metric` table.
- Each row contains a `user_id`, `type` (e.g., `steps`, `sleep`), `value`, `unit`, and a precise `timestamp`.
- This table is optimized for writes and for efficient time-series queries via database indexes on `(user_id, type, timestamp)`.

### Data Derivation (The API Response)

- The API **does not** store pre-computed JSON responses for dashboards.
- When a client requests KPIs (e.g., `GET /api/metrics/kpis`), the backend performs the following steps: 
1. Queries the `Metric` table for the user's raw data within the relevant time frame (e.g., the last 24 hours). 
2. Performs aggregations (SUM, AVG, etc.) on this data in memory. 
3. Assembles the final JSON response based on the computed values.
- This ensures that every API response reflects the most current and accurately calculated view of the raw data.