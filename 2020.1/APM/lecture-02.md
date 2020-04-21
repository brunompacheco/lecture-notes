# Mathematical Background

Lecturer: Sebastiaan J. can Zelst

Date: 13.04.2020

## Mathematical Preliminaries

> **Set**: a group of objects without duplicates.

Sets allow for union, intersection, difference and complement

#### Power of a set

> *P(X) = {X' c= X}

Remember that the empty group is always in the Power of any set.

#### Cartesian product

> Given X_1, ..., X_n sets, X_1 x ... x X_n = {(x_1, ..., x_n) | x_i \in X_i, for every 1 <= i <= n}

#### Functions

> Given sets X and Y, a set f c= X x Y is a function iff for every x \in X \exists y \in Y such that (x, y) \in f and \existsnot y' \in Y, y' != y, such that (x, y') \in f.

_I.e._, in a function f:X->Y, there is one, and only one mapping for every element of X. Basic function definition.

> A partial function f:X-/>Y is a partial function iff \exists X' \in X such that f:X'->Y (same mapping) is a function.

_I.e._, the partial function map elements from a subset of the domain

> A function f:X->Y is **injective** iff f^-1:Y->X is a partial function.

> A function f:X->Y is **surjective** iff for every y \in Y, \exists x \in X such that (x, y) \in f.

_I.e._, surjectiveness is the coverness of all Y.

> A function f:X->Y is **bijective** iff it is both **injective** and **surjective**.

#### Multisets

Multisets are sets that allow for multiple elements. Usually written as B = {a², b³, c, d²}, given X = {a, b, c, d}. They are represented as a function.

> A Multiset is a function B:X->\N that maps the elements of a set X in its amount.

Multisets allow for several operations as extension and union (across different sets).

#### Sequences

Sequences are enumerated collection of objects. Given a set X = {a, b, c}, a sequence is usually written as <b, c, b, a>

> Given a set X, a sequence sigma is a function sigma:{1,...,n}->X for n \in \N.

Sequences are a subset of \N x X.

> Given X a set, X* is the set of all possible sequences over X.

Sequences can be concatenated: sig_1 = <a, b>, sig_2 = <c, d>, sig_1 \crossproduct sig_2 = <a, b, c, d>.

## Petri Nets

[ADD PETRI NET IMAGE]

#### Definitions

> A **Bipartite graph** is a graph G = {(v,e) | v \in V,e \in E c= V x V}, where V represent the vertices (or nodes) and E represent the edges, where \exists V_1, V_2 c= V with V_1 \intersect V_2 = \empty and V_1 U V_2 = V, such that for every e = (v_1, v_2) \in E, v_1 \in V_1 and v_2 \in V_2.

_I.e._, there is no edge between the elements of V_1 or V_2.

> Given P, T the sets of places and transitions, respectively, and F c= (P x T) U (T x P) the set of arcs, a tuple N \in P x T x F is a **Petri Net** iff P and T are partitions of the graph {(v, e) | v \in P U T, e \in F}.

Let N = (P, T, F) be a Petri Net, we can define

- \dot x = {y \in P U T | (y, x) \in F} as the pre-set of a vertex
- x \dot = {y \in P U T | (x, y) \in F} as the post-set of a vertex
- M \in B(P) is called a marking of N
  - Given p \in P, we write M(p) to denote the number of tokens in p

> A transition t \in T is **enabled**, written M[t>, iff for every p \in \dot t, M(p) > 0.

If a transition t \in T is **fired**, we obtain a new marking M' \in B(P) in the following way:

- M'(p) = M(p) + 1, for every p \in t \dot \\ \dot t
- M'(p) = M(p) - 1, for every p \in \dot t \\ t \dot
- M'(p) = M(p), otherwise