# Screening and coding protocol, version 2 (revision, 2026-10-08)

This protocol is the single reference for all screeners and coders, human or AI.
It replaces version 1, whose rules R1–R3 are kept here as R1, R2 and part of R3.

## Topic
Studies in which a **language model** and an **explicit symbolic component** interact.

## Inclusion criteria (all must hold)
- **I1 Venue.** An archival research paper accepted at one of these venues, 2020–2026:
  - AAAI (technical track)
  - ICLR
  - ICML
  - IJCAI (main and special tracks)
  - NeurIPS (main, and Datasets & Benchmarks)
  - TMLR
  - IEEE TPAMI
  - ACL, EMNLP or NAACL (main conference, long or short)

  Findings, demos, industry tracks, student abstracts, doctoral consortia and invited talks do not count.
- **I2 Language model.** A language model (rule R1) is a core component of the method or the subject being evaluated.
- **I3 Symbolic component.** An explicit symbolic component (rule R3) interacts with the model (rule R2). Rules R4–R6 cover the boundary cases.
- **I4 Primary research.** The paper is a primary research contribution.

## Exclusion codes (give the single most fundamental one)
- **E1** No language model under R1.
- **E2** The language model appears only as background, as a baseline, or as a frozen feature encoder.
- **E3** No explicit symbolic component interacts with the model under R2–R6. Name the rule in the rationale, e.g. "E3 (R4)".
- **E4** Not an archival research paper of an in-scope track: talk, doctoral consortium, demo, student abstract, Findings, workshop.
- **E5** Secondary study or position paper: a survey or overview, or a position paper without new evidence.

## Rules
**R1 What counts as a language model.**
- Counts: a neural sequence model trained or pretrained on natural-language, mathematical-text or source-code corpora, at any scale from LSTM language models to LLMs.
- Counts: a vision-language or multimodal model built on such a model.
- Does not count: a sequence model trained *only* on task-generated symbolic data. Example: a transformer trained from scratch to emit expression trees or tactics, with no language or code pretraining.

**R2 Interaction.**
- Counts: the output of one component is the input, constraint, verdict or training signal of the other.
- Does not count: portfolios that merely choose between a language model and a solver.
- Evaluation studies satisfy R2 when a symbolic system generates the problems or certifies the answers the model is scored against.

**R3 What counts as a symbolic component.**

A symbolic component is a system that represents knowledge or computation in an explicit formal language and manipulates it by rule-governed procedures.
- Examples:
  - logic, SAT/SMT and constraint solvers; theorem provers and proof assistants
  - logic programs, answer-set programs and rule engines
  - planners (PDDL), temporal-logic monitors and model checkers
  - interpreters that execute model-written programs
  - computer-algebra systems; symbolic-regression or program-search procedures
  - grammars, automata, type systems and static or dataflow analyses that constrain or check the model
- Not symbolic components:
  - natural-language reasoning chains, even when called "symbolic"
  - retrieval stores of text or facts
  - neural modules with no formal representation

**R4 Program- and query-generation task families.**
- Covered families:
  - code generation from natural language, evaluated by tests
  - text-to-SQL
  - knowledge-base question answering by generating database or graph queries (SPARQL, S-expressions)
- In these families, executing or testing the generated program does **not by itself** satisfy I3.
- Such a study is included only if an *additional* symbolic component interacts with the model:
  - a formal verifier (proof assistant, verification-condition checker)
  - a type or dataflow analysis
  - a grammar- or constraint-based checker
  - a symbolic search over partial programs
- When the program or formal query is a *vehicle* for another task, I3 is satisfied. Examples of such tasks: math word problems, table or visual question answering, puzzles, planning, robot control, theorem proving, optimisation modelling.
- Formal proofs, verified programs and autoformalised statements checked by a proof assistant or verifier always satisfy I3.

**R5 Knowledge graphs.** A knowledge graph or knowledge base counts as symbolic only when the method performs *logical* inference over it: rule application, rule induction, or answering queries with logical operators. Retrieving triples or paths to put into a prompt does not count.

**R6 Tool use.**
- Generic tool-use frameworks (search engines, calculators, web APIs, several tools at once) do not satisfy I3.
- They do satisfy I3 when a specific formal engine under R3 is the object of the integration.

## Screening decisions (title/abstract stage)
- `include`: all criteria appear to hold.
- `exclude` + code: at least one criterion clearly fails.
- `unsure`: the abstract does not settle it. Unsure records go to adjudication with full text.

## Coding axes (included studies; exactly one primary code per axis)

### Architecture: apply this decision tree in order and stop at the first yes
1. **A6 Evaluation with a symbolic oracle.** The main contribution is a benchmark or evaluation, and a symbolic system generates the problems or certifies the answers.
2. **A5 Symbolic-to-neural transfer.** The symbolic component is used only to create training data, targets or a training signal, *offline*, and the deployed model runs without it.
3. **A1 Translate-and-solve.** The model writes a formal representation (program, logic, constraints, query, plan specification), and the symbolic engine **computes the answer**. There is no iterative checking loop.
4. **A2 Checker-in-the-loop.** A symbolic checker or executor returns verdicts or feedback on model outputs. These **select, repair, filter or reward** candidates during inference or online training. This *includes* proof search where the proof assistant checks each step and accepts the final proof. Value models or heuristics may guide that search, but the checker gives the verdict.
5. **A4 LM-induced symbolic artifacts.** The model writes rules, programs, predicates, concepts or modules that are stored and **reused beyond a single query**.
6. **A7 LM as interface to a symbolic core.** A language or vision-language model grounds perception or verbalises output. A symbolic core makes the decision.
7. **A3 Symbolic guidance or constraints.** Symbolic structure steers search, decoding, retrieval, decomposition or the training loss, and gives no verdict on the final output.

### Check strength (new attribute, all studies)
- **exact**: a sound formal verdict on the final output, from a proof assistant, a solver-checked certificate, a model checker, or a type-checked formal statement.
- **empirical**: an execution- or data-based check that can pass incorrect outputs: unit tests, execution results, fit to data, simulator success, answer matching.
- **none**: no check on the final output by the symbolic component (typical for A3, A5, A7).

### Domain (main evaluation)
- **D1** Formal theorem proving and autoformalisation, including formal software verification.
- **D2** Logical and deductive reasoning: natural-language or formal deduction, puzzles, constraint problems, consistency.
- **D3** Program synthesis and structured data: programming by example, code analysis, tables, spreadsheets, SQL when in scope.
- **D4** Symbolic regression and scientific discovery.
- **D5** Embodied planning and agents.
- **D6** Vision-language and multimodal reasoning.
- **D7** Mathematical problem solving with programs or symbolic tools (word problems, competition math), excluding formal proofs.
- **D8** Language modelling, knowledge and data: language modelling, knowledge construction, distillation, data synthesis, other NLP.

### Formalism (main symbolic representation)
- **F1** Logic: FOL, propositional logic, answer-set programs, Prolog, constraints, SAT/SMT, description logic.
- **F2** Proof assistants and verification languages: Lean, Isabelle, Coq, Dafny, Metamath.
- **F3** General-purpose programs: Python and other executable code.
- **F4** Symbolic mathematical expressions and computer algebra.
- **F5** Rules, knowledge graphs and scene graphs.
- **F6** Planning languages, temporal logic and symbolic world models.
- **F7** Domain-specific languages, grammars, automata and static analysis.

### Further extracted fields (from abstract; also from full text when available)
- **lm_named**: the language models named.
- **engine_named**: the symbolic engines or tools named.
- **benchmarks_named**: the benchmarks named.
- **faithfulness_reported**: for A1/A2 studies whose model writes formal statements, `yes` if the paper reports the accuracy or faithfulness of the formalisation separately from end-task accuracy; otherwise `no`, `unclear` or `n/a`.
