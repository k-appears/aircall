# 2. Use of Domain Model in Hexagonal Architecture

Date: 2024-04-27

## Context

In the development of our application, we need to decide how to structure the core business logic and entities within
the Hexagonal Architecture.

In the Hexagonal Architecture, the domain model represents the core business logic and entities. The domain model
consists of:

#### 1. Domain Entities:

- Domain entities are objects that represent real-world objects. They encapsulate the state and behavior related to
  those concepts.
- Entities often encapsulate the business logic.
- Contain state.

#### 2. Value Objects:

- Value objects are immutable and represents types of measurements.

#### 3. Domain Services:

- Encapsulate domain logic that do not fit to a domain entity.
- Operate on one or more domain entities or value objects.
- Stateless.

#### 4. Aggregates:

- Aggregates are clusters of domain objects that are treated as a single unit for data changes.
- If required in our system will `Number of events for an alert`.

## Decision

1. Use as __Domain Entities__ `Alert` and `Events`.
2. Use as __value objects__ `Escalation Policy`
3. User as __Domain Services__ `AlertService` and `EventService`

## Consequences

1. **Maintainability**

2. **Scalability**

3. **Testability**

4. **Isolation from Technical Concerns**

5. **Learning Curve**

## Status

Accepted

## Decision Log

- [2024-04-27] Decision made to adopt the use of Domain Model in the Hexagonal Architecture.
