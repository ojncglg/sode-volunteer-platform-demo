# SODE Volunteer Platform Demo v1 Workflows

This document describes the implemented demo workflows and likely future production flows. It is intended to help a future team create Figma or FigJam workflow charts.

## 1. Officer Account / Entry

### Current Demo Behavior

```mermaid
flowchart TD
    A[Officer opens app] --> B[Login page]
    B --> C{Existing demo user?}
    C -->|Login with any credentials| D[Demo authentication]
    D --> E[Opportunities]
    C -->|Create account| F[Account creation form]
    F --> G[Verification email sent state]
    G --> H[Demo verify shortcut]
    H --> B
```

Notes:

- Login is simulated.
- Account creation stores pending account data in session.
- Verification is simulated through `/demo/verify`.
- No production identity provider exists.

### Future Production Flow

Production needs real identity, agency verification, role assignment, and secure account lifecycle behavior.

## 2. Officer Opportunity Flow

### Current Demo Behavior

```mermaid
flowchart TD
    A[Opportunities] --> B[Filter events]
    B --> C[Select Fall Festival]
    C --> D[Event Detail]
    D --> E[Choose preferred assignment]
    E --> F[Confirm signup]
    F --> G[Session-backed registration]
    G --> H[Provisional assignment]
    H --> I[My Events]
```

Notes:

- The selected preference becomes the provisional assignment in the demo.
- Fall Festival is the full event-detail workflow.
- Bowling Classic is mocked as an already signed-up event.

## 3. Assignment Change Flow

### Current Demo Behavior

```mermaid
flowchart TD
    A[Officer has provisional assignment] --> B[Coordinator changes assignment]
    B --> C[Session assignment state updates]
    C --> D[Officer notification appears]
    D --> E[My Events shows Assignment Updated]
    E --> F[Previous assignment: Bocce Awards]
    E --> G[New assignment: Sports Arena]
    G --> H[Officer acknowledges update]
    H --> I[My Events shows Current Assignment]
    H --> J[Coordinator sees Acknowledged]
```

Important:

- Acknowledgment means seen.
- Acknowledgment does not mean accepted or approved.
- No real email, SMS, push, or notification backend exists.

## 4. Coordinator Event Operations Flow

### Current Demo Behavior

```mermaid
flowchart TD
    A[Coordinator Dashboard] --> B[Event Operations]
    B --> C[View upcoming events]
    C --> D[Open Fall Festival]
    D --> E[Staffing Coverage]
    E --> F[Officer Roster]
    F --> G[Assignment Management]
    G --> H[Reassign Alex]
    H --> I[Staffing counts update]
    I --> J[Officer notification state updates]
    F --> K[Assign available demo volunteer]
    K --> L[Staffing counts update]
    F --> M[Message Volunteers demo panel]
    M --> N[Demo success toast]
```

Fall Festival initial staffing:

| Area | Initial state |
| --- | --- |
| Bocce Awards | 3 / 3, filled |
| Sports Arena | 2 / 4, 2 officers needed |
| Main Awards | 3 / 3, filled |
| LDR Awards | 2 / 2, filled |
| Cafeteria | 2 / 4, 2 officers needed |
| Overall | 12 / 16, 4 officers needed |

After Alex is reassigned from Bocce Awards to Sports Arena:

| Area | Updated state |
| --- | --- |
| Bocce Awards | 2 / 3, 1 officer needed |
| Sports Arena | 3 / 4, 1 officer needed |
| Overall | 12 / 16, 4 officers needed |

The assignment distribution changes. The number of volunteers does not.

## 5. Volunteer Hours Flow

### Current Demo Behavior

```mermaid
flowchart TD
    A[Completed historical event records] --> B[Credited volunteer hours]
    B --> C[My Events total]
    B --> D[Officer Leaderboard]
    B --> E[Department Leaderboard]
    B --> F[Coordinator Reports]
```

Current data behavior:

- Alex Morgan has three completed historical records.
- Hours: 6.5 + 8.0 + 4.0 = 18.5.
- My Events shows 18.5.
- Leaderboard uses 18.5 for Alex.
- Coordinator Reports uses 18.5 for Alex.
- Coordinator report summary metrics are seeded demo figures.

### Future Production Flow

```mermaid
flowchart TD
    A[Event participation] --> B[Check-in record]
    B --> C[Checkout or event completion]
    C --> D[Hours calculation]
    D --> E[Coordinator review]
    E --> F[Approved volunteer-hour record]
    F --> G[My Events history]
    F --> H[Leaderboards]
    F --> I[Coordinator reports]
```

Not implemented:

- Check-in methodology.
- Checkout methodology.
- Hour calculation rules.
- Approval rules.
- No-show and cancellation handling.

These require discovery and product validation.

## 6. Demo Role-Switch Flow

### Current Demo Behavior

```mermaid
flowchart TD
    A[Officer View] --> B[Demo menu]
    B --> C[Coordinator View]
    C --> D[Make operational change]
    D --> E[Demo menu]
    E --> F[Officer View]
    F --> G[Observe effect]
```

Notes:

- Role switching is a presentation mechanism.
- It is not production authorization.
- Session state is preserved while switching.

## 7. Demo Reset Flow

### Current Demo Behavior

```mermaid
flowchart TD
    A[Presenter clicks Reset Demo State] --> B[Clear demo_signups]
    B --> C[Clear coordinator assignment overrides]
    C --> D[Clear added demo volunteers]
    D --> E[Return to Opportunities]
```

Reset restores:

- Fall Festival unsigned/officer clean state.
- Fall Festival coordinator staffing to 12 / 16.
- Bocce Awards to 3 / 3 filled.
- Sports Arena to 2 / 4, 2 officers needed.
- Main Awards to 3 / 3 filled.
- LDR Awards to 2 / 2 filled.
- Cafeteria to 2 / 4, 2 officers needed.
- Alex preferred assignment to Bocce Awards.
- Alex assigned assignment to Bocce Awards.
- Alex status to Confirmed.

Reset clears:

- Assignment changed state.
- Previous assignment.
- Acknowledgment state.
- Pending assignment-change notification.
- Non-Alex coordinator assignment overrides.
- Added demo volunteers.

Reset preserves:

- Bowling Classic mocked signed-up state.
- Completed historical records.
- 18.5 credited hours.
- Leaderboard seed data.
- Coordinator report demo metrics.

## 8. Future Event-Day Flow

This flow is not implemented and requires discovery.

Candidate future flow:

```mermaid
flowchart TD
    A[Upcoming event] --> B[Reminder]
    B --> C[Check in]
    C --> D[Confirm assignment]
    D --> E[Event participation]
    E --> F[Check out]
    F --> G[Hours calculation]
    G --> H[Coordinator approval]
    H --> I[Volunteer hour record]
    I --> J[My Events history]
    I --> K[Leaderboards]
    I --> L[Reports]
```

Open questions:

- Is checkout required?
- Are hours credited by shift, check-in duration, coordinator approval, or another rule?
- Are officer assignments final before the event or adjustable on event day?
- What happens for cancellations and no-shows?
- What notifications are required?

Do not treat this candidate flow as finalized.
