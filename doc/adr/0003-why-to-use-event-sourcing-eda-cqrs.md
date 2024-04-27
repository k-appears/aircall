# 3. why to use Event Sourcing + EDA + CQRS

Date: 2024-04-27

## Status

Accepted

## Context
Our organization is developing an alert system to monitor and respond to incidents in our infrastructure. The system must be capable of detecting anomalies, generating alerts, and notifying relevant stakeholders or triggering automated actions. We need to decide on the architectural approach to design a scalable, resilient, and responsive alert system.

## Decision
We will adopt Event Sourcing and Event-Driven Architecture (EDA) with Command Query Responsibility Segregation (CQRS) for our alert system.

## Rationale
1. **Traceability and Auditability**: Event Sourcing captures every change to the system's state as immutable events, providing a complete audit trail of all actions taken within the system, including the generation, handling, and resolution of alerts. This ensures traceability and accountability, essential for compliance and incident investigation.

2. **Temporal Queries and Replayability**: Event Sourcing enables us to reconstruct the system's state at any point in time by replaying events from the event log. This capability facilitates temporal queries, allowing us to analyze past states and behaviors for debugging, performance assessment, and trend analysis.

3. **Resilience and Scalability**: Event-Driven Architecture decouples system components using asynchronous communication through events, improving system resilience and scalability. Components can process events independently at their own pace and scale, ensuring timely alert processing and handling under varying loads and failures.

4. **Real-time Responsiveness**: Event-Driven Architecture enables real-time alert processing as events are generated, ensuring prompt reactions to changes in monitored services or conditions. This responsiveness minimizes response times and ensures timely notifications or automated actions in response to alerts.

5. **Scalable Data Storage**: Event Sourcing stores the system's state as a sequence of events, providing flexibility and scalability in data storage. Events can be distributed across multiple event stores or databases, allowing horizontal scaling to accommodate growing volumes of alerts and event data.

6. **Separation of Concerns**: Command Query Responsibility Segregation (CQRS) separates the command (write) and query (read) responsibilities of the system. This separation optimizes each side independently, tailoring data storage, processing, and retrieval mechanisms to the specific needs of each use case.

7. **Flexibility and Extensibility**: Event-Driven Architecture and CQRS promote loose coupling between system components, facilitating the introduction of new features, integration with external systems, or evolution of the system over time. Clear boundaries between commands, events, and queries allow for refactoring, extension, or replacement of individual components without impacting the overall system architecture.

## Consequences
- **Complexity**: Event Sourcing and EDA+CQRS introduce additional complexity compared to traditional architectures. Developers need to understand and adhere to event-driven patterns, and the system must manage event processing, consistency, and eventual consistency challenges.
- **Learning Curve**: Adoption of Event Sourcing and EDA+CQRS may require a learning curve for the development team, particularly if they are unfamiliar with these architectural patterns.
- **Infrastructure Requirements**: Event Sourcing may require specialized infrastructure for storing and processing event logs, potentially adding operational overhead and costs.

## References
- Martin Fowler. [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- Martin Fowler. [CQRS](https://martinfowler.com/bliki/CQRS.html)
- Vaughn Vernon. "Implementing Domain-Driven Design." Addison-Wesley Professional, 2013.
