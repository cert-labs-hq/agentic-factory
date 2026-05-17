# Concepts

**Stream**: In OpenObserve, a "Stream" is essentially a database table. The fundamental building block of OpenObserve data storage. Each stream maps to a distinct dataset (e.g., application logs or telemetry) and enforces its own retention and indexing rules.
**Span**:  The individual "building blocks" of a trace. Each span records its own start/end time, operation name, nested relationships (parent/child), and key-value attributes like function parameters.
**Trace**: A trace tracks the complete journey of a request or workflow as it moves through multiple microservices
