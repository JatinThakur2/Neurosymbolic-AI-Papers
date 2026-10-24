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

## Revision-2 amendments (2026-10-23, after the second referee report)
These amendments were made after the v2 decisions. They are listed here so that every change to the rulebook is visible; the decision files record which stage applied which version.

1. **Track rule (I1).** AAAI special research tracks (the 2023 "AAAI special track" and the 2021 "technical track focus area") are archival research tracks, as IJCAI's special tracks already were. They are added to Source B. IJCAI survey-track papers stay in Source B and are excluded by E5. NeurIPS position-track and journal-track papers, IAAI/EAAI, demonstrations, student and senior-member programmes, doctoral consortia, and ACL Findings volumes remain out of scope.
2. **Search (stage 2).** The augmented query (code/search/query.py, `LM_BLOCK_ADD`, `SYMBOLIC_BLOCK_ADD`) adds model checking, NuSMV, Dafny, Verus, Datalog, planner(s), planning domain/language/problem/task, automated planning, MILP, mixed-integer, integer/linear programming, optimisation models/modelling/problems/formulations, Pyomo, Gurobi, proof(s), SQL, execution traces, TLA+ and Alloy to the symbolic block, and Qwen, Mistral, Gemini, DeepSeek, Claude, GPT, reasoning models and language agents to the language-model block. Hits not screened in stage 1 are screened by two screeners with adjudication, as in stage 1.
3. **Clarification of R2 for optimisation solvers (applied in stage 2).** An LP/MILP or other optimisation solver that only configures the system around the model (architecture search, quantisation bit widths, serving schedules, ensemble weights) does not interact with what the model reasons about: E3 (R2). When the model writes the formulation, or the solver acts on the model's outputs as part of the reasoning task, the solver satisfies R3.
4. **Recall audit.** A second screener screened the audit sample independently. Every record that either screener did not exclude was adjudicated.
5. **Source B completion.** The main-conference volumes of ACL 2021-2025, EMNLP 2021-2024 and NAACL 2021-2025 in the ACL Anthology (commit 73f3b3a) were compared with the Paper Copilot lists; papers missing from the lists (mostly EMNLP 2023/2024 and NAACL 2025) were added to Source B. Added papers that the stage-1 or stage-2 query retrieves are screened in stage 2; the others join the audit strata.
6. **Audit extension.** A further seeded simple random sample (seed 2028) of 300 records from the "neither" stratum and 200 from the "language-model only" stratum of the revision-2 strata (records retrieved by neither query) was screened by two screeners with adjudication. Recall is reported as the posterior median of the Jeffreys-posterior Monte Carlo, with its 2.5% and 97.5% quantiles.
7. **Known-item check.** The references of Cheng et al. (2025), "Empowering LLMs with Logical Reasoning: A Comprehensive Survey" (arXiv:2502.15652v4), at the review's venues and years are traced through the review; references in Source B that no route screened are screened by two screeners with adjudication. The list is in `data/decisions/knownitem/`.
8. **Check strength for A1 (clarification, no recoding).** Check strength concerns a verdict on an output. When an engine computes the answer from the model's formal representation (A1), the execution is not a check: the code is `none` unless something also checks the result. This states the rule the coders applied.
9. **Supplementary coding.** Two independent coders record for every included study (i) its contribution type (method / benchmark / analysis; disagreements adjudicated) and (ii) every architecture pattern its own system uses (A1-A5, A7), judged independently of the decision-tree order.
10. **Full-text check.** For a seeded random sample of 60 A1/A2 studies (seed 20261023), one coder recodes check strength and faithfulness reporting from the full text, to measure the cost of abstract-level charting.
11. **Second human rater.** An independent second rater codes a stratified subset of the author's human-check samples (150 screening records, 75 pipeline inclusions and 75 exclusions; 60 coded studies).
