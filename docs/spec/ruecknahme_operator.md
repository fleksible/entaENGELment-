# Rücknahme-Operator R↓

Status: specification anchor; not a tracking feature.

## Core thesis

The Rücknahme-Operator models leaving the application not as failure, abandonment, or data loss, but as the successful completion of a mediated transition.

The system fulfills its purpose when it releases the person without persistent digital binding.

```text
R↓(session, sediment, consent_exit) -> released_state + no_trace
```

## Semantics

`no_trace` is not an error state. `no_trace` is PASS.

The operator closes the loop by turning the system's post-exit non-knowledge into the strongest ethical confirmation: after the threshold, the application does not monitor, measure, infer, or retain the person's resonance.

## Inputs

- `session`: the local mediated interaction state
- `sediment`: local working residue created during the session
- `consent_exit`: an explicit exit gesture or equivalent local release action

## Operation

1. acknowledge the transition
2. release the mediated frame
3. discard local sediment or hand it back to the person as an explicit export
4. close the local session
5. create no server-side continuation
6. perform no post-exit telemetry

## Output

- `released_state`
- `no_trace: true`

## Non-goals

- no server-side tracking after exit
- no behavioral proof after tab close
- no claim that unmediated resonance is measured by the system
- no hidden identity continuation
- no post-exit reminders or re-engagement hooks unless separately and explicitly requested

## Technical boundary

The system may shape the threshold. It must not possess what happens beyond it.

In implementation terms, success is represented by local release plus absence of persistent binding. The application should be able to record that an exit gesture occurred only inside the local closing flow; it must not convert the after-exit silence into a surveillance problem.

## Card mapping

The machine-checkable working artifact is:

- `cards/templates/ruecknahme_exit.json`

Required invariant:

- `fields.no_trace` must be `true`

## Review note

This document intentionally keeps R↓ as a small spec anchor. UI affordances, storage behavior, and deletion/export mechanics should be added only in later narrow slices with explicit tests.
