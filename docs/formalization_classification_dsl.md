# ResumeLens Formalization: Classification and Candidate Profile DSL

## 1. Qualification Pattern Recognition with Finite Automata

ResumeLens uses deterministic finite automata to determine whether a sequence of normalized qualifications satisfies the qualification pattern defined for a professional profile.

A single general construction is used for every profile. If a profile contains `N` ordered qualification categories, the corresponding automaton contains states `q0, q1, ..., qN`. State `q0` is the initial state and `qN` is the only accepting state.

For each category, every valid qualification produces a transition from the state associated with that category to the next state. Therefore, a candidate is accepted only when the input contains one valid qualification from every required category and follows the canonical category order.

The transition function is deterministic and partial. When no transition exists for a state-symbol pair, the sequence is rejected.

---

## 1.1 Full Stack Developer

### Formal Definition

The automaton is defined as:

**M_FS = (Q, Σ, δ, q0, F)**

where:

**Q**

```text
Q = {q0, q1, q2, q3, q4, q5}