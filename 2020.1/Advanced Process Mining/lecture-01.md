# Introduction to Process Mining

Lecturer: Sebastiaan J. can Zelst

Date: 13.04.2020

## Overview

### Definitions

> **Process**: a discrete collection of activities executed to achieve a goal.

> **Mining**: "_Gaining knowledge of, and, insights in (business) processes by analysing the event data stored during execution of the process_".

Basic process data example:

| package   | task      | timestamp |
| --------- |:---------:| ---------:|
| 1eg081hr  | load      | 12:36     |
| 1eg081hr  | dispatch  | 12:38     |
| 41yp39he  | load      | 12:37     |

`package` column is the **Case identifier**, it identifies the instance of the process. `task` is the **Activity** column, it explains what is being performed at a data record (row). `timestamp` is the **Timestamp** column, a time reference to the data record. The last one is not necessary and can come in several different ways, even sometimes having record for beginning and end.

We can also have different data in a log, but these are the bare basics.

> **Event**: capture the (partial) execution of an activity within a process instance.

Events are the atoms of our data, the rows.

> **Trace**: collection of events related to a process instance.

We can make traces by the Case identifier reference.

### Process Mining - Analysis

Three branches:

> **Process Discovery**: deriving process models from process logs.

> **Conformance Checking**: assessing if reality in the data is conforming to specification (from a process model).

> **Process Enhancement**: providing performance information to a process model (as an overlay).

Process discovery acts from event logs, in the model. Conformance checking acts between the model and the event logs, acting on both. Enhancement acts from logs on the models, with a feedback from the model.
