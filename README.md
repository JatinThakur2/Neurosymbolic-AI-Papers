# Neurosymbolic AI — Paper Collection (ICML, NeurIPS, ICLR, AAAI, IJCAI, TMLR, JMLR, TPAMI)

A curated collection of papers on **neurosymbolic AI** across major ML/AI venues (2020–2026), organized by venue and year. Neurosymbolic AI combines neural network–based learning with symbolic reasoning (logic, rules, programs) to build systems that are more interpretable, data-efficient, and capable of structured reasoning than pure deep learning approaches.

## Structure

Each venue gets one folder per year, named `<venue>-<year>-paper/` (e.g. `iclr-2020-paper/`), containing the PDFs for that venue/year:

```
├── aaai-2020-paper/ … aaai-2026-paper/
├── iclr-2020-paper/ … iclr-2026-paper/
├── icml-2020-paper/ … icml-2026-paper/
├── ijcai-2020-paper/ … ijcai-2025-paper/
├── neurips-2020-paper/ … neurips-2025-paper/
├── tmlr-2022-paper/, tmlr-2023-paper/, tmlr-2025-paper/, tmlr-2026-paper/
├── tpami-2023-paper/ … tpami-2026-paper/
└── README.md
```

Gaps in the year sequence mean no qualifying papers were found for that venue/year (or, for a few 2026 slots, the event hasn't happened yet / isn't indexed yet — see the per-venue notes below).

| Venue | Years covered | Papers found | Notes |
|---|---|---|---|
| **ICML** | 2020–2026 | 61 | 2026 sourced from arXiv (PMLR proceedings not yet published) |
| **NeurIPS** | 2020–2025 | 78 | 2026 conference hasn't been held yet (scheduled Dec 2026) |
| **AAAI** | 2020–2026 | 101 | Fully open-access via OJS |
| **IJCAI** | 2020–2025 | 75 | 2026 not yet indexed by dblp |
| **ICLR** | 2020–2026 | 56 | Hosted on OpenReview (PDF access partially blocked — see note) |
| **TMLR** | 2022–2026 | 14 | Rolling-review journal, started 2022; hosted on OpenReview |
| **JMLR** | 2020–2026 | 0 | Searched all volumes — genuinely no qualifying papers (see note) |
| **TPAMI** | 2023–2026 | 6 | Paywalled (IEEE) — metadata + DOI only, except where a free arXiv preprint exists |

**~391 papers total**, ~367 with a locally-stored PDF.

## Methodology

Papers were identified with a two-tier keyword classifier applied to each venue's title index: a **core** pattern (`neuro-symbolic` / `neural-symbolic` / `neurosymbolic`, explicit) and an **adjacent** pattern covering closely related subfields (program synthesis/induction, symbolic regression/policy learning, inductive logic programming, rule/constraint induction, abductive learning, differentiable logic/reasoning, probabilistic logic programming, complex query answering over knowledge graphs, temporal logic rules, neural theorem proving, answer-set programming). Every hit was then manually reviewed against its title/abstract to drop false positives (e.g. generic "temporal point process" or "differentiable programming" papers that don't involve symbolic/logical reasoning, pure-LLM analogical-reasoning benchmarks with no symbolic component, workshop-only submissions).

Sourcing per venue:
- **ICML, NeurIPS, AAAI, IJCAI**: official open-access proceedings (PMLR, papers.nips.cc, AAAI OJS, ijcai.org), located via [dblp](https://dblp.org/) title listings.
- **ICLR, TMLR**: hosted on OpenReview, which blocks automated PDF downloads behind a Cloudflare bot-challenge (confirmed via direct testing — both the OpenReview API and direct PDF endpoints return 403). PDFs are the authors' own arXiv preprints where one exists; the remainder are listed with an OpenReview forum link only.
- **JMLR**: searched directly on jmlr.org; no qualifying papers exist in this venue for 2020–2026 (see note in that section).
- **TPAMI**: IEEE-paywalled; listed via dblp with DOI links, PDF included only for the one paper with a free arXiv preprint.
- **2026 entries** for venues whose proceedings/dblp indexing lag behind the event (ICML, ICLR) were found via targeted arXiv searches for preprints explicitly tagged with the venue/year in their arXiv comment metadata, excluding workshop-track papers.


## Papers by Venue

### ICML

> Sourced from the official [PMLR ICML proceedings](https://proceedings.mlr.press/) (volumes v119–v267), fully open-access, except 2026 (see note in Structure above).

#### ICML 2020

| Paper | Authors | Summary |
|---|---|---|
| [Neuro-Symbolic Visual Reasoning: Disentangling "Visual" from "Reasoning"](icml-2020-paper/Neuro-Symbolic%20Visual%20Reasoning%3A%20Disentangling%20'Visual'%20from%20'Reasoning'.pdf) | Amizadeh, Palangi, Polozov, Huang, Koishida | Introduces a differentiable first-order-logic formalism for VQA that decouples reasoning from visual perception, enabling disentangled evaluation of neuro-symbolic reasoning models independent of perception quality. |
| [Closed Loop Neural-Symbolic Learning via Integrating Neural Perception, Grammar Parsing, and Symbolic Reasoning](icml-2020-paper/Closed%20Loop%20Neural-Symbolic%20Learning%20via%20Integrating%20Neural%20Perception%2C%20Grammar%20Parsing%2C%20and%20Symbolic%20Reasoning.pdf) | Li, Huang, Hong, Chen, Wu, Zhu | Proposes a grammar-model-based "back-search" algorithm that closes the loop between neural perception and symbolic reasoning, propagating errors through the symbolic module far more efficiently than prior RL-based neuro-symbolic training. |
| [Generating Programmatic Referring Expressions via Program Synthesis](icml-2020-paper/Generating%20Programmatic%20Referring%20Expressions%20via%20Program%20Synthesis.pdf) | Huang, Smith, Bastani, Singh, Albarghouthi, Naik | Combines a policy neural network with enumerative search to synthesize "referring relational programs" that uniquely identify a target object in an image via its attributes and relations. |
| [Temporal Logic Point Processes](icml-2020-paper/Temporal%20Logic%20Point%20Processes.pdf) | Li, Wang, Zhang, Chang, Liu, Xie, Qi, Song | Models event-sequence dynamics with intensity functions structured by first-order temporal logic rules, allowing accurate, interpretable predictions in small-data regimes by incorporating domain knowledge as logic. |

#### ICML 2021

| Paper | Authors | Summary |
|---|---|---|
| [A large-scale benchmark for few-shot program induction and synthesis](icml-2021-paper/A%20large-scale%20benchmark%20for%20few-shot%20program%20induction%20and%20synthesis.pdf) | Alet, Lopez-Contreras, Koppel, Nye, Solar-Lezama, Lozano-Pérez, Kaelbling, Tenenbaum | Introduces P3 (ProgRes), a large-scale few-shot program-induction benchmark built by mining subprograms and their I/O tests from real programs, and analyzes transformer-based synthesis methods on it. |
| [An Integer Linear Programming Framework for Mining Constraints from Data](icml-2021-paper/An%20Integer%20Linear%20Programming%20Framework%20for%20Mining%20Constraints%20from%20Data.pdf) | Meng, Chang | Proposes an ILP-based framework to automatically mine logical constraints over structured-output label spaces from data, instead of relying on hand-crafted rules, validated on Sudoku and spanning-tree tasks. |
| [Discovering symbolic policies with deep reinforcement learning](icml-2021-paper/Discovering%20symbolic%20policies%20with%20deep%20reinforcement%20learning.pdf) | Landajuela, Petersen, Kim, Santiago, Glatt, Mundhenk, Pettit, Faissol | Presents "deep symbolic policy," which uses an autoregressive RNN with risk-seeking policy gradients to directly search for compact, interpretable symbolic-expression control policies that outperform state-of-the-art DRL. |
| [Latent Programmer: Discrete Latent Codes for Program Synthesis](icml-2021-paper/Latent%20Programmer%3A%20Discrete%20Latent%20Codes%20for%20Program%20Synthesis.pdf) | Hong, Dohan, Singh, Sutton, Zaheer | Proposes a two-level search for program synthesis where a discrete latent "plan" code is predicted first and used to organize the subsequent search over full programs, improving accuracy on longer programs. |
| [Leveraging Language to Learn Program Abstractions and Search Heuristics](icml-2021-paper/Leveraging%20Language%20to%20Learn%20Program%20Abstractions%20and%20Search%20Heuristics.pdf) | Wong, Ellis, Tenenbaum, Andreas | Introduces LAPS, which uses natural-language annotations to jointly learn reusable program libraries and neurally-guided search heuristics for program synthesis, integrated into DreamCoder. |
| [Neural Symbolic Regression that Scales](icml-2021-paper/Neural%20Symbolic%20Regression%20that%20scales.pdf) | Biggio, Bendinelli, Neitz, Lucchi, Parascandolo | Introduces the first large-scale-pretrained symbolic regression method: a Transformer trained on procedurally generated equations that predicts symbolic expressions from input-output pairs and improves with more data/compute. |

#### ICML 2022

| Paper | Authors | Summary |
|---|---|---|
| [Deep symbolic regression for recurrence prediction](icml-2022-paper/Deep%20symbolic%20regression%20for%20recurrence%20prediction.pdf) | d'Ascoli, Kamienny, Lample, Charton | Trains Transformers to infer the closed-form function or recurrence relation underlying integer/float sequences, outperforming Mathematica's built-in recurrence solvers and generalizing to unseen functions. |
| [Neural-Symbolic Models for Logical Queries on Knowledge Graphs](icml-2022-paper/Neural-Symbolic%20Models%20for%20Logical%20Queries%20on%20Knowledge%20Graphs.pdf) | Zhu, Galkin, Zhang, Tang | Proposes GNN-QE, which decomposes complex first-order-logic queries over knowledge graphs into relation projections and fuzzy-set logical operations executed by a GNN, combining the interpretability of symbolic traversal with the robustness of neural link prediction. |
| [Neuro-Symbolic Hierarchical Rule Induction](icml-2022-paper/Neuro-Symbolic%20Hierarchical%20Rule%20Induction.pdf) | Glanois, Jiang, Feng, Weng, Zimmer, Li, Liu, Hao | Proposes HRI, an interpretable neuro-symbolic model for Inductive Logic Programming that learns first-order rules via embeddings matched against a hierarchy of pre-defined meta-rules, trainable via supervised or reinforcement learning. |
| [Neuro-Symbolic Language Modeling with Automaton-augmented Retrieval](icml-2022-paper/Neuro-Symbolic%20Language%20Modeling%20with%20Automaton-augmented%20Retrieval.pdf) | Alon, Xu, He, Sengupta, Roth, Neubig | Introduces RetoMaton, which builds a weighted finite automaton over a retrieval datastore to approximate costly nearest-neighbor search in retrieval-augmented language models, cutting perplexity while reducing lookup cost. |
| [Parametric Visual Program Induction with Function Modularization](icml-2022-paper/Parametric%20Visual%20Program%20Induction%20with%20Function%20Modularization.pdf) | Duan, Wang, Zhang, Zhu | Proposes modeling parametric primitive functions as multi-head neural modules combined with a hierarchical Monte Carlo tree search, extending visual program induction beyond fixed, non-parametric functions to complex scenes. |

#### ICML 2023

| Paper | Authors | Summary |
|---|---|---|
| [Controllable Neural Symbolic Regression](icml-2023-paper/Controllable%20Neural%20Symbolic%20Regression.pdf) | Bendinelli, Biggio, Kamienny | Proposes NSRwH, a neural symbolic regression method that lets users inject prior hypotheses about the expected structure of the target expression, improving accuracy over unconditioned neural SR while giving explicit control. |
| [Deep Generative Symbolic Regression with Monte-Carlo-Tree-Search](icml-2023-paper/Deep%20Generative%20Symbolic%20Regression%20with%20Monte-Carlo-Tree-Search.pdf) | Kamienny, Lample, Lamprier, Virgolin | Combines a pretrained, context-aware neural mutation model with Monte Carlo Tree Search to give deep generative symbolic regression the search ability of genetic programming, achieving state-of-the-art results on SRBench. |
| [Eventual Discounting Temporal Logic Counterfactual Experience Replay](icml-2023-paper/Eventual%20Discounting%20Temporal%20Logic%20Counterfactual%20Experience%20Replay.pdf) | Voloshin, Verma, Yue | Introduces an "eventual discounting" value-function proxy and a counterfactual experience-replay method for RL policies optimized against Linear Temporal Logic (LTL) task specifications, overcoming the myopia of standard RL on LTL objectives. |
| [Interpretable Neural-Symbolic Concept Reasoning](icml-2023-paper/Interpretable%20Neural-Symbolic%20Concept%20Reasoning.pdf) | Barbiero, Ciravegna, Giannini, Espinosa Zarlenga, Magister, Tonda, Lió, Precioso, Jamnik, Marra | Introduces the Deep Concept Reasoner (DCR), which builds differentiable syntactic rule structures over concept embeddings so predictions are fully interpretable while retaining the accuracy benefits of embeddings. |
| [Neuro-Symbolic Continual Learning](icml-2023-paper/Neuro-Symbolic%20Continual%20Learning.pdf) | Marconato, Bontempo, Ficarra, Calderara, Passerini, Teso | Defines Neuro-Symbolic Continual Learning (NeSy-CL), shows that combining NeSy architectures with continual learning avoids catastrophic forgetting but induces "reasoning shortcuts," and proposes COOL, a concept-level rehearsal strategy to address this. |
| [Parallel Neurosymbolic Integration with Concordia](icml-2023-paper/Parallel%20Neurosymbolic%20Integration%20with%20Concordia.pdf) | Feldstein, Jurčius, Tsamoura | Presents Concordia, a framework for parallel neurosymbolic integration that is agnostic to both the deep network and the logic theory, supporting a wide range of probabilistic theories and both supervised and unsupervised training of the neural component. |

#### ICML 2024

| Paper | Authors | Summary |
|---|---|---|
| [Ambiguity-Aware Abductive Learning](icml-2024-paper/Ambiguity-Aware%20Abductive%20Learning.pdf) | He, Sun, Xie, Li | Proposes A³BL, which evaluates all plausible candidates (and their probabilities) produced by the abduction step in Abductive Learning, instead of committing to a single minimal-inconsistency candidate, reducing sensitivity to ambiguous abduced supervision. |
| [Amortizing Pragmatic Program Synthesis with Rankings](icml-2024-paper/Amortizing%20Pragmatic%20Program%20Synthesis%20with%20Rankings.pdf) | Pu, Vaduguru, Vaithilingam, Glassman, Fried | Distills the slow, exact Rational Speech Acts (RSA) pragmatic program synthesizer into a single global program ranking, giving orders-of-magnitude speedups while remaining more accurate than non-pragmatic synthesizers. |
| [Analysis for Abductive Learning and Neural-Symbolic Reasoning Shortcuts](icml-2024-paper/Analysis%20for%20Abductive%20Learning%20and%20Neural-Symbolic%20Reasoning%20Shortcuts.pdf) | Yang, Wei, Shao, Li, Zhou | Provides a theoretical analysis quantifying how knowledge-base complexity, sample size, and hypothesis space drive "reasoning shortcuts" in abductive/neuro-symbolic learning, and shows abductive learning can mitigate them via distance-function choice. |
| [Convex and Bilevel Optimization for Neural-Symbolic Inference and Learning](icml-2024-paper/Convex%20and%20Bilevel%20Optimization%20for%20Neural-Symbolic%20Inference%20and%20Learning.pdf) | Dickens, Gao, Pryor, Wright, Getoor | Develops a general gradient-based learning framework for NeSy energy-based models (demonstrated on NeuPSL) using a smooth primal-dual inference formulation and a dual block-coordinate-descent algorithm, yielding 100× faster inference. |
| [End-to-End Neuro-Symbolic Reinforcement Learning with Textual Explanations](icml-2024-paper/End-to-End%20Neuro-Symbolic%20Reinforcement%20Learning%20with%20Textual%20Explanations.pdf) | Luo, Zhang, Xu, Yang, Fang, Li | Presents INSIGHT, which jointly learns structured visual states and symbolic RL policies by distilling a vision foundation model into an efficient, reward-refinable perception module, and uses GPT-4 to generate natural-language explanations of learned policies. |
| [Federated Neuro-Symbolic Learning](icml-2024-paper/Federated%20Neuro-Symbolic%20Learning.pdf) | Xing, Lu, Yu | Proposes FedNSL, the first framework extending neuro-symbolic learning to federated settings by using latent rule-distribution variables as the communication medium, with a KL-divergence constraint to handle rule distribution heterogeneity across clients. |
| [Neuro-Symbolic Temporal Point Processes](icml-2024-paper/Neuro-Symbolic%20Temporal%20Point%20Processes.pdf) | Yang, Yang, Li, Fu, Li | Introduces a neuro-symbolic rule-induction framework within temporal point processes that learns compact, human-readable temporal logic rules end-to-end via a sequential covering algorithm, applied to irregular event data such as clinical records. |
| [On the Hardness of Probabilistic Neurosymbolic Learning](icml-2024-paper/On%20the%20Hardness%20of%20Probabilistic%20Neurosymbolic%20Learning.pdf) | Maene, Derkinderen, De Raedt | Proves that exact gradient computation for probabilistic NeSy models is intractable in general but becomes tractable during training, and introduces WeightME, an unbiased gradient estimator based on weighted model sampling with a SAT oracle. |
| [On the Independence Assumption in Neurosymbolic Learning](icml-2024-paper/On%20the%20Independence%20Assumption%20in%20Neurosymbolic%20Learning.pdf) | van Krieken, Minervini, Ponti, Vergari | Critiques the common conditional-independence assumption in NeSy probabilistic losses, proving it biases models toward overconfidence and produces non-convex, highly disconnected optima, motivating more expressive alternatives. |
| [StackSight: Unveiling WebAssembly through Large Language Models and Neurosymbolic Chain-of-Thought Decompilation](icml-2024-paper/StackSight%3A%20Unveiling%20WebAssembly%20through%20Large%20Language%20Models%20and%20Neurosymbolic%20Chain-of-Thought%20Decompilation.pdf) | Fang, Zhou, He, Wang | Combines LLMs with program-analysis techniques and chain-of-thought prompting to decompile complex WebAssembly bytecode into readable C++ code, improving reverse-engineering of stack-machine binaries. |
| [Subgoal-based Demonstration Learning for Formal Theorem Proving](icml-2024-paper/Subgoal-based%20Demonstration%20Learning%20for%20Formal%20Theorem%20Proving.pdf) | Zhao, Li, Kong | Constructs subgoal-structured in-context demonstrations (organized via a diffusion-model-based selector) to improve LLM proof search efficiency and accuracy on the miniF2F formal theorem-proving benchmark. |
| [Temporal Logic Specification-Conditioned Decision Transformer for Offline Safe Reinforcement Learning](icml-2024-paper/Temporal%20Logic%20Specification-Conditioned%20Decision%20Transformer%20for%20Offline%20Safe%20Reinforcement%20Learning.pdf) | Guo, Zhou, Li | Proposes SDT, a Decision Transformer conditioned on signal temporal logic (STL) specifications, enabling offline safe-RL policies that satisfy rich temporal/logical constraints and align with different desired satisfaction levels. |

#### ICML 2025

| Paper | Authors | Summary |
|---|---|---|
| [Ab Initio Nonparametric Variable Selection for Scalable Symbolic Regression with Large p](icml-2025-paper/Ab%20Initio%20Nonparametric%20Variable%20Selection%20for%20Scalable%20Symbolic%20Regression%20with%20Large%20p.pdf) | Ye, Li | Proposes PAN+SR, which pre-screens large input-variable spaces via nonparametric variable selection before symbolic regression, scaling SR to "large p" scientific datasets while keeping expressions compact and accurate. |
| [Dataflow-Guided Neuro-Symbolic Language Models for Type Inference](icml-2025-paper/Dataflow-Guided%20Neuro-Symbolic%20Language%20Models%20for%20Type%20Inference.pdf) | Li, Wan, Zhang, Zhao, Jiang, Shi, Jin, Wang | Presents NESTER, which enhances small local LMs for code type inference by decomposing the task into a symbolic, dataflow-driven program of sub-steps (without increasing model size), outperforming larger cloud-based type inference systems. |
| [DOLPHIN: A Programmable Framework for Scalable Neurosymbolic Learning](icml-2025-paper/DOLPHIN%3A%20A%20Programmable%20Framework%20for%20Scalable%20Neurosymbolic%20Learning.pdf) | Naik, Liu, Wang, Sethi, Dutta, Naik, Wong | Presents DOLPHIN, a framework for writing neurosymbolic programs in Python that executes symbolic reasoning on CPU while vectorizing probabilistic computation and gradient propagation on GPU, scaling to 13 benchmarks with recursion and black-box functions. |
| [Is Complex Query Answering Really Complex?](icml-2025-paper/Is%20Complex%20Query%20Answering%20Really%20Complex.pdf) | Gregucci, Xiong, Hernández, Loconte, Minervini, Staab, Vergari | Shows that most queries in standard complex query answering (CQA) benchmarks over knowledge graphs trivially reduce to simple link prediction, and proposes harder benchmarks that better reflect genuine multi-hop reasoning difficulty. |
| [MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving](icml-2025-paper/MA-LoT%3A%20Model-Collaboration%20Lean-based%20Long%20Chain-of-Thought%20Reasoning%20enhances%20Formal%20Theorem%20Proving.pdf) | Wang, Pan, Li, Zhang, Jia, Diao, Pi, Hu, Zhang | Proposes MA-LoT, which separates whole-proof generation and error-correction into a model-collaboration pipeline for Lean4 theorem proving, structuring long chain-of-thought interaction between an LLM and the Lean verifier. |
| [Neurosymbolic World Models for Sequential Decision Making](icml-2025-paper/Neurosymbolic%20World%20Models%20for%20Sequential%20Decision%20Making.pdf) | Hernández Cano, Perroni-Scharf, Dhir, Ramamurthy, Solar-Lezama | Presents SWMPO, which unsupervised-learns neurosymbolic Finite State Machine world models capturing an environment's structural regimes (e.g. water vs. land) for use in model-based policy optimization. |
| [Pareto-Optimal Fronts for Benchmarking Symbolic Regression Algorithms](icml-2025-paper/Pareto-Optimal%20Fronts%20for%20Benchmarking%20Symbolic%20Regression%20Algorithms.pdf) | Fong, Motani | Introduces absolute Pareto-optimal (APO) fronts, computed via exhaustive search over SRBench datasets, as an algorithm-independent performance ceiling for benchmarking symbolic regression methods. |
| [ProofAug: Efficient Neural Theorem Proving via Fine-grained Proof Structure Analysis](icml-2025-paper/ProofAug%3A%20Efficient%20Neural%20Theorem%20Proving%20via%20Fine-grained%20Proof%20Structure%20Analysis.pdf) | Liu, Sun, Li, Yao | Proposes ProofAug, which applies automation tools (tactics, ATPs) at multiple granularities of an LLM's proof proposals via fine-grained structure analysis, plug-and-play with tree search, improving neural theorem proving efficiency. |
| [Regret-Free Reinforcement Learning for Temporal Logic Specifications](icml-2025-paper/Regret-Free%20Reinforcement%20Learning%20for%20Temporal%20Logic%20Specifications.pdf) | Majumdar, Salamati, Soudjani | Gives the first regret-free online learning algorithm for synthesizing controllers that satisfy Linear Temporal Logic (LTL) specifications on MDPs with unknown dynamics, with sharp finite-episode bounds rather than only asymptotic guarantees. |
| [Self-Improving Language Models for Evolutionary Program Synthesis: A Case Study on ARC-AGI](icml-2025-paper/Self-Improving%20Language%20Models%20for%20Evolutionary%20Program%20Synthesis%3A%20A%20Case%20Study%20on%20ARC-AGI.pdf) | Pourcel, Colas, Oudeyer | Introduces SOAR, which integrates an LLM into a self-improving evolutionary program-synthesis loop, alternating evolutionary search with hindsight fine-tuning on past search attempts to solve 52% of the public ARC-AGI test set. |
| [STP: Self-play LLM Theorem Provers with Iterative Conjecturing and Proving](icml-2025-paper/STP%3A%20Self-play%20LLM%20Theorem%20Provers%20with%20Iterative%20Conjecturing%20and%20Proving.pdf) | Dong, Ma | Proposes STP, a self-play theorem prover where one LLM role generates novel provable conjectures and another proves them, providing mutual training signal to overcome the sparse-reward/scarce-data bottleneck in formal theorem proving. |
| [TeLoGraF: Temporal Logic Planning via Graph-encoded Flow Matching](icml-2025-paper/TeLoGraF%3A%20Temporal%20Logic%20Planning%20via%20Graph-encoded%20Flow%20Matching.pdf) | Meng, Fan | Uses a GNN encoder plus flow-matching to learn general signal temporal logic (STL) planning solutions from a large paired dataset of specifications and demonstrations, running 10-100x faster than classical STL planners. |
| [Verification Learning: Make Unsupervised Neuro-Symbolic System Feasible](icml-2025-paper/Verification%20Learning%3A%20Make%20Unsupervised%20Neuro-Symbolic%20System%20Feasible.pdf) | Jia, Hu, Shao, Guo, Li | Introduces Verification Learning, which reframes label-based NeSy reasoning as a label-free constraint-verification process solved via a Dynamic Combinatorial Sorting algorithm, enabling fully unsupervised neuro-symbolic learning. |
| [ZebraLogic: On the Scaling Limits of LLMs for Logical Reasoning](icml-2025-paper/ZebraLogic%3A%20On%20the%20Scaling%20Limits%20of%20LLMs%20for%20Logical%20Reasoning.pdf) | Lin, Le Bras, Richardson, Sabharwal, Poovendran, Clark, Choi | Introduces ZebraLogic, a controllable-complexity benchmark of logic-grid puzzles (as constraint satisfaction problems) that reveals a "curse of complexity" — LLM logical-reasoning accuracy declines sharply as problem complexity grows, even with more scale/inference compute. |

#### ICML 2026

> Sourced from arXiv preprints marked "ICML 2026" (main track; workshop-only papers excluded). PMLR proceedings not yet published — see note above.

| Paper | Authors | Summary |
|---|---|---|
| [A Deep Learning Model of Mental Rotation Informed by Interactive VR Experiments](icml-2026-paper/A%20Deep%20Learning%20Model%20of%20Mental%20Rotation%20Informed%20by%20Interactive%20VR%20Experiments.pdf) | Khazoum, Fernandes, Krylov, Li, Deny | Proposes a mechanistic model of human mental rotation combining an equivariant neural encoder, a neuro-symbolic object encoder, and a neural decision agent, to explain spatial reasoning behavior observed in interactive VR experiments. |
| [Automated Formal Proofs of Combinatorial Identities via Wilf-Zeilberger Guidance and LLMs](icml-2026-paper/Automated%20Formal%20Proofs%20of%20Combinatorial%20Identities%20via%20Wilf-Zeilberger%20Guidance%20and%20LLMs.pdf) | Xiong, Lv, Liu, Wang, Chen, Wang, Yang, Zhi | Introduces WZ-LLM, a neuro-symbolic framework that turns symbolic Wilf-Zeilberger proof plans into executable proof skeletons for LLMs, automating formal proofs of combinatorial identities that were previously hard to fully automate. |
| [A Minimal Agent for Automated Theorem Proving](icml-2026-paper/A%20Minimal%20Agent%20for%20Automated%20Theorem%20Proving.pdf) | Requena, Letson, Nowakowski, Beltran-Ferreiro, Sarra | Presents a minimal agentic baseline implementing the core features shared by state-of-the-art LLM theorem provers (iterative proof refinement, library search, context management), enabling systematic comparison across prover architectures and frontier models. |
| [Breaking the Simplification Bottleneck in Amortized Neural Symbolic Regression](icml-2026-paper/Breaking%20the%20Simplification%20Bottleneck%20in%20Amortized%20Neural%20Symbolic%20Regression.pdf) | Saegert, Köthe | Identifies slow, general-purpose computer-algebra-system simplification as the key bottleneck limiting amortized symbolic regression's scalability, and proposes a fast, learned normalization method to reduce equivalent expressions to concise canonical form. |
| [Decompose, Structure, and Repair: A Neuro-Symbolic Framework for Autoformalization via Operator Trees](icml-2026-paper/Decompose%2C%20Structure%2C%20and%20Repair%20-%20A%20Neuro-Symbolic%20Framework%20for%20Autoformalization%20via%20Operator%20Trees.pdf) | Liu, Dong, Bai, Li, Liu, Luo | Proposes DSR, a neuro-symbolic autoformalization framework that represents formal code as hierarchical operator trees (rather than flat token sequences) so LLMs can decompose, structure, and repair mathematical formalizations more reliably. |
| [Deliberate Evolution: Agentic Reasoning for Sample-Efficient Symbolic Regression with LLMs](icml-2026-paper/Deliberate%20Evolution%20-%20Agentic%20Reasoning%20for%20Sample-Efficient%20Symbolic%20Regression%20with%20LLMs.pdf) | Pang, Zhou, Li, Lv, Wei, Cui, Han, Zhang | Introduces Deliberate Evolution, an agentic LLM-based symbolic regression method that separates candidate proposal from search guidance instead of conflating them via a single scalar fitness score, improving sample efficiency over prior LLM-evolutionary SR methods. |
| [DisjunctiveNet: Neural Symbolic Learning via Differentiable Convexified Optimization Layers](icml-2026-paper/DisjunctiveNet%20-%20Neural%20Symbolic%20Learning%20via%20Differentiable%20Convexified%20Optimization%20Layers.pdf) | Pal, Li | Proposes DisjunctiveNet, which enforces logical-proposition and linear-inequality domain-knowledge rules exactly (via differentiable convexified optimization layers) rather than approximately via soft penalties, targeting sparse-data science/engineering problems. |
| [Distilling Neuro-Symbolic Programs into 3D Multi-modal LLMs](icml-2026-paper/Distilling%20Neuro-Symbolic%20Programs%20into%203D%20Multi-modal%20LLMs.pdf) | Mo, Liu | Introduces APEIRIA, which bridges interpretable but closed-vocabulary neuro-symbolic 3D concept learners with open-vocabulary but black-box 3D multi-modal LLMs, distilling compositional program-based reasoning into the LLM for verifiable 3D spatial reasoning. |
| [Faults in Our Formal Benchmarking: Dataset Defects and Evaluation Failures in Lean Theorem Proving](icml-2026-paper/Faults%20in%20Our%20Formal%20Benchmarking%20-%20Dataset%20Defects%20and%20Evaluation%20Failures%20in%20Lean%20Theorem%20Proving.pdf) | Ammanamanchi, Bhat, Biderman | Audits five widely-used Lean theorem-proving benchmarks and finds that machine-checked proof success doesn't guarantee the formal statement faithfully encodes the intended informal problem, nor that evaluation harnesses resist trivial or adversarial solutions. |
| [From LLM-Generated Conjectures to Lean Formalizations: Automated Polynomial Inequality Proving via Sum-of-Squares Certificates](icml-2026-paper/From%20LLM-Generated%20Conjectures%20to%20Lean%20Formalizations%20-%20Automated%20Polynomial%20Inequality%20Proving%20via%20Sum-of-Squares%20Certificates.pdf) | Zuo, Zhao, He, Yang, Wang | Combines LLM-generated conjectures with symbolic sum-of-squares certificate search to automate polynomial inequality proving and formalize the results in Lean, addressing the poor scaling of purely symbolic algebraic methods. |
| [Geodesic Flow Matching for Denoising High-Dimensional Structured Representations](icml-2026-paper/Geodesic%20Flow%20Matching%20for%20Denoising%20High-Dimensional%20Structured%20Representations.pdf) | Habashy, Eliasmith | Extends flow matching to respect the toroidal-manifold geometry of Spatial Semantic Pointers in Vector Symbolic Algebras, fixing a flat-Euclidean-geometry assumption that breaks neurosymbolic reasoning built on high-dimensional distributed symbolic representations. |
| [Influence-Guided Symbolic Regression: Scientific Discovery via LLM-Driven Equation Search with Granular Feedback](icml-2026-paper/Influence-Guided%20Symbolic%20Regression%20-%20Scientific%20Discovery%20via%20LLM-Driven%20Equation%20Search%20with%20Granular%20Feedback.pdf) | Saveliev, Holt, Seedat, Bentley, Weatherall, van der Schaar | Introduces IGSR, which guides LLM-driven symbolic regression with per-component influence feedback instead of a single global error score, helping the LLM identify which parts of a candidate equation are driving performance or error. |
| [Lifting Traces to Logic: Programmatic Skill Induction with Neuro-Symbolic Learning for Long-Horizon Agentic Tasks](icml-2026-paper/Lifting%20Traces%20to%20Logic%20-%20Programmatic%20Skill%20Induction%20with%20Neuro-Symbolic%20Learning%20for%20Long-Horizon%20Agentic%20Tasks.pdf) | Shao, Yin, Lyu, Yu, Guo, Tsang, Kwok, Li | Proposes Neuro-Symbolic Skill Induction (NSI), which lifts foundation-model agent interaction traces into modular, logic-grounded programs (rather than state-blind scripts), improving robustness for long-horizon planning in dynamic environments. |
| [Sonar-TS: Search-Then-Verify Natural Language Querying for Time Series Databases](icml-2026-paper/Sonar-TS%20-%20Search-Then-Verify%20Natural%20Language%20Querying%20for%20Time%20Series%20Databases.pdf) | Tan, Zhao, Wang, Xu, Liang, Liu, Pan, Jin | Introduces Sonar-TS, a neuro-symbolic framework for natural-language querying of time-series databases that pairs a feature-index-based candidate search with a verification step, handling continuous morphological intents that text-to-SQL methods cannot. |

### NeurIPS

> Sourced from the official [NeurIPS proceedings](https://papers.nips.cc/) (fully open-access). NeurIPS 2026 has not been held yet (scheduled for December 2026), so no 2026 papers exist.


#### NeurIPS 2020

| Paper | Authors |
|---|---|
| [Compositional Generalization via Neural-Symbolic Stack Machines](neurips-2020-paper/Compositional%20Generalization%20via%20Neural-Symbolic%20Stack%20Machines.pdf) | Xinyun Chen; Chen Liang; Adams Wei Yu; Dawn Song; Denny Zhou |
| [Learning abstract structure for drawing by efficient motor program induction](neurips-2020-paper/Learning%20abstract%20structure%20for%20drawing%20by%20efficient%20motor%20program%20induction.pdf) | Lucas Tian; Kevin Ellis; Marta Kryven; Josh Tenenbaum |
| [AI Feynman 2.0: Pareto-optimal symbolic regression exploiting graph modularity](neurips-2020-paper/AI%20Feynman%202.0%20-%20Pareto-optimal%20symbolic%20regression%20exploiting%20graph%20modularity.pdf) | Silviu-Marian Udrescu; Andrew Tan; Jiahai Feng; Orisvaldo Neto; Tailin Wu; Max Tegmark |
| [Learning Differentiable Programs with Admissible Neural Heuristics](neurips-2020-paper/Learning%20Differentiable%20Programs%20with%20Admissible%20Neural%20Heuristics.pdf) | Ameesh Shah; Eric Zhan; Jennifer Sun; Abhinav Verma; Yisong Yue; Swarat Chaudhuri |
| [Neurosymbolic Reinforcement Learning with Formally Verified Exploration](neurips-2020-paper/Neurosymbolic%20Reinforcement%20Learning%20with%20Formally%20Verified%20Exploration.pdf) | Greg Anderson; Abhinav Verma; Isil Dillig; Swarat Chaudhuri |
| [Multi-Plane Program Induction with 3D Box Priors](neurips-2020-paper/Multi-Plane%20Program%20Induction%20with%203D%20Box%20Priors.pdf) | Yikai Li; Jiayuan Mao; Xiuming Zhang; Bill Freeman; Josh Tenenbaum; Noah Snavely; Jiajun Wu |
| [Learning Compositional Rules via Neural Program Synthesis](neurips-2020-paper/Learning%20Compositional%20Rules%20via%20Neural%20Program%20Synthesis.pdf) | Maxwell Nye; Armando Solar-Lezama; Josh Tenenbaum; Brenden Lake |
| [Generative Neurosymbolic Machines](neurips-2020-paper/Generative%20Neurosymbolic%20Machines.pdf) | Jindong Jiang; Sungjin Ahn |
| [Program Synthesis with Pragmatic Communication](neurips-2020-paper/Program%20Synthesis%20with%20Pragmatic%20Communication.pdf) | Yewen Pu; Kevin Ellis; Marta Kryven; Josh Tenenbaum; Armando Solar-Lezama |
| [Neurosymbolic Transformers for Multi-Agent Communication](neurips-2020-paper/Neurosymbolic%20Transformers%20for%20Multi-Agent%20Communication.pdf) | Jeevana Priya Inala; Yichen Yang; James Paulos; Yewen Pu; Osbert Bastani; Vijay Kumar; Martin Rinard; Armando Solar-Lezama |
| [Synthesize, Execute and Debug: Learning to Repair for Neural Program Synthesis](neurips-2020-paper/Synthesize%2C%20Execute%20and%20Debug%20-%20Learning%20to%20Repair%20for%20Neural%20Program%20Synthesis.pdf) | Kavi Gupta; Peter Ebert Christensen; Xinyun Chen; Dawn Song |
| [Beta Embeddings for Multi-Hop Logical Reasoning in Knowledge Graphs](neurips-2020-paper/Beta%20Embeddings%20for%20Multi-Hop%20Logical%20Reasoning%20in%20Knowledge%20Graphs.pdf) | Hongyu Ren; Jure Leskovec |
| [PLANS: Neuro-Symbolic Program Learning from Videos](neurips-2020-paper/PLANS%20-%20Neuro-Symbolic%20Program%20Learning%20from%20Videos.pdf) | Raphaël Dang-Nhu |

#### NeurIPS 2021

| Paper | Authors |
|---|---|
| [Learning to Combine Per-Example Solutions for Neural Program Synthesis](neurips-2021-paper/Learning%20to%20Combine%20Per-Example%20Solutions%20for%20Neural%20Program%20Synthesis.pdf) | Disha Shrivastava; Hugo Larochelle; Daniel Tarlow |
| [SQALER: Scaling Question Answering by Decoupling Multi-Hop and Logical Reasoning](neurips-2021-paper/SQALER%20-%20Scaling%20Question%20Answering%20by%20Decoupling%20Multi-Hop%20and%20Logical%20Reasoning.pdf) | Mattia Atzeni; Jasmina Bogojeska; Andreas Loukas |
| [Latent Execution for Neural Program Synthesis Beyond Domain-Specific Languages](neurips-2021-paper/Latent%20Execution%20for%20Neural%20Program%20Synthesis%20Beyond%20Domain-Specific%20Languages.pdf) | Xinyun Chen; Dawn Song; Yuandong Tian |
| [Symbolic Regression via Deep Reinforcement Learning Enhanced Genetic Programming Seeding](neurips-2021-paper/Symbolic%20Regression%20via%20Deep%20Reinforcement%20Learning%20Enhanced%20Genetic%20Programming%20Seeding.pdf) | Terrell Mundhenk; Mikel Landajuela; Ruben Glatt; Claudio P Santiago; Daniel faissol; Brenden K Petersen |
| [Scallop: From Probabilistic Deductive Databases to Scalable Differentiable Reasoning](neurips-2021-paper/Scallop%20-%20From%20Probabilistic%20Deductive%20Databases%20to%20Scalable%20Differentiable%20Reasoning.pdf) | Jiani Huang; Ziyang Li; Binghong Chen; Karan Samel; Mayur Naik; Le Song; Xujie Si |
| [Improving Coherence and Consistency in Neural Sequence Models with Dual-System, Neuro-Symbolic Reasoning](neurips-2021-paper/Improving%20Coherence%20and%20Consistency%20in%20Neural%20Sequence%20Models%20with%20Dual-System%2C%20Neuro-Symbolic%20Reasoning.pdf) | Maxwell Nye; Michael Tessler; Josh Tenenbaum; Brenden Lake |
| [Fast Abductive Learning by Similarity-based Consistency Optimization](neurips-2021-paper/Fast%20Abductive%20Learning%20by%20Similarity-based%20Consistency%20Optimization.pdf) | Yu-Xuan Huang; Wang-Zhou Dai; Le-Wen Cai; Stephen H Muggleton; Yuan Jiang |
| [Open Rule Induction](neurips-2021-paper/Open%20Rule%20Induction.pdf) | Wanyun Cui; Xingran Chen |
| [Program Synthesis Guided Reinforcement Learning for Partially Observed Environments](neurips-2021-paper/Program%20Synthesis%20Guided%20Reinforcement%20Learning%20for%20Partially%20Observed%20Environments.pdf) | Yichen Yang; Jeevana Priya Inala; Osbert Bastani; Yewen Pu; Armando Solar-Lezama; Martin Rinard |

#### NeurIPS 2022

| Paper | Authors |
|---|---|
| [Neural-Symbolic Entangled Framework for Complex Query Answering](neurips-2022-paper/Neural-Symbolic%20Entangled%20Framework%20for%20Complex%20Query%20Answering.pdf) | Zezhong Xu; Wen Zhang; Peng Ye; Hui Chen; Huajun Chen |
| [Deep Differentiable Logic Gate Networks](neurips-2022-paper/Deep%20Differentiable%20Logic%20Gate%20Networks.pdf) | Felix Petersen; Christian Borgelt; Hilde Kuehne; Oliver Deussen |
| [VAEL: Bridging Variational Autoencoders and Probabilistic Logic Programming](neurips-2022-paper/VAEL%20-%20Bridging%20Variational%20Autoencoders%20and%20Probabilistic%20Logic%20Programming.pdf) | Eleonora Misino; Giuseppe Marra; Emanuele Sansone |
| [CoNSoLe: Convex Neural Symbolic Learning](neurips-2022-paper/CoNSoLe%20-%20Convex%20Neural%20Symbolic%20Learning.pdf) | Haoran Li; Yang Weng; Hanghang Tong |
| [ZeroC: A Neuro-Symbolic Model for Zero-shot Concept Recognition and Acquisition at Inference Time](neurips-2022-paper/ZeroC%20-%20A%20Neuro-Symbolic%20Model%20for%20Zero-shot%20Concept%20Recognition%20and%20Acquisition%20at%20Inference%20Time.pdf) | Tailin Wu; Megan Tjandrasuwita; Zhengxuan Wu; Xuelin Yang; Kevin Liu; Rok Sosic; Jure Leskovec |
| [End-to-end Symbolic Regression with Transformers](neurips-2022-paper/End-to-end%20Symbolic%20Regression%20with%20Transformers.pdf) | Pierre-alexandre Kamienny; Stéphane d'Ascoli; Guillaume Lample; Francois Charton |
| [NS3: Neuro-symbolic Semantic Code Search](neurips-2022-paper/NS3%20-%20Neuro-symbolic%20Semantic%20Code%20Search.pdf) | Shushan Arakelyan; Anna Hakhverdyan; Miltiadis Allamanis; Luis Garcia; Christophe Hauser; Xiang Ren |
| [Drawing out of Distribution with Neuro-Symbolic Generative Models](neurips-2022-paper/Drawing%20out%20of%20Distribution%20with%20Neuro-Symbolic%20Generative%20Models.pdf) | Yichao Liang; Josh Tenenbaum; Tuan Anh Le; Siddharth N |
| [LogiGAN: Learning Logical Reasoning via Adversarial Pre-training](neurips-2022-paper/LogiGAN%20-%20Learning%20Logical%20Reasoning%20via%20Adversarial%20Pre-training.pdf) | Xinyu Pi; Wanjun Zhong; Yan Gao; Nan Duan; Jian-Guang Lou |
| [HyperTree Proof Search for Neural Theorem Proving](neurips-2022-paper/HyperTree%20Proof%20Search%20for%20Neural%20Theorem%20Proving.pdf) | Guillaume Lample; Timothee Lacroix; Marie-Anne Lachaux; Aurelien Rodriguez; Amaury Hayat; Thibaut Lavril; Gabriel Ebner; Xavier Martinet |
| [Semantic Probabilistic Layers for Neuro-Symbolic Learning](neurips-2022-paper/Semantic%20Probabilistic%20Layers%20for%20Neuro-Symbolic%20Learning.pdf) | Kareem Ahmed; Stefano Teso; Kai-Wei Chang; Guy Van den Broeck; Antonio Vergari |
| [A Unified Framework for Deep Symbolic Regression](neurips-2022-paper/A%20Unified%20Framework%20for%20Deep%20Symbolic%20Regression.pdf) | Mikel Landajuela; Chak Shing Lee; Jiachen Yang; Ruben Glatt; Claudio P Santiago; Ignacio Aravena; Terrell Mundhenk; Garrett Mulcahy; Brenden K Petersen |
| [Improving Certified Robustness via Statistical Learning with Logical Reasoning](neurips-2022-paper/Improving%20Certified%20Robustness%20via%20Statistical%20Learning%20with%20Logical%20Reasoning.pdf) | Zhuolin Yang; Zhikuan Zhao; Boxin Wang; Jiawei Zhang; Linyi Li; Hengzhi Pei; Bojan Karlaš; Ji Liu; Heng Guo; Ce Zhang; Bo Li |
| [Neurosymbolic Deep Generative Models for Sequence Data with Relational Constraints](neurips-2022-paper/Neurosymbolic%20Deep%20Generative%20Models%20for%20Sequence%20Data%20with%20Relational%20Constraints.pdf) | Halley Young; Maxwell Du; Osbert Bastani |

#### NeurIPS 2023

| Paper | Authors |
|---|---|
| [Enhancing Robot Program Synthesis Through Environmental Context](neurips-2023-paper/Enhancing%20Robot%20Program%20Synthesis%20Through%20Environmental%20Context.pdf) | Tianyi Chen; Qidi Wang; Zhen Dong; Liwei Shen; Xin Peng |
| [Neuro-symbolic Learning Yielding Logical Constraints](neurips-2023-paper/Neuro-symbolic%20Learning%20Yielding%20Logical%20Constraints.pdf) | Zenan Li; Yunpeng Huang; Zhaoyu Li; Yuan Yao; Jingwei Xu; Taolue Chen; Xiaoxing Ma; Jian Lu |
| [A-NeSI: A Scalable Approximate Method for Probabilistic Neurosymbolic Inference](neurips-2023-paper/A-NeSI%20-%20A%20Scalable%20Approximate%20Method%20for%20Probabilistic%20Neurosymbolic%20Inference.pdf) | Emile van Krieken; Thiviyan Thanapalasingam; Jakub Tomczak; Frank van Harmelen; Annette Ten Teije |
| [Adapting Neural Link Predictors for Data-Efficient Complex Query Answering](neurips-2023-paper/Adapting%20Neural%20Link%20Predictors%20for%20Data-Efficient%20Complex%20Query%20Answering.pdf) | Erik Arakelyan; Pasquale Minervini; Daniel Daza; Michael Cochez; Isabelle Augenstein |
| [Differentiable Neuro-Symbolic Reasoning on Large-Scale Knowledge Graphs](neurips-2023-paper/Differentiable%20Neuro-Symbolic%20Reasoning%20on%20Large-Scale%20Knowledge%20Graphs.pdf) | CHEN SHENGYUAN; Yunfeng Cai; Huang Fang; Xiao Huang; Mingming Sun |
| [Complex Query Answering on Eventuality Knowledge Graph with Implicit Logical Constraints](neurips-2023-paper/Complex%20Query%20Answering%20on%20Eventuality%20Knowledge%20Graph%20with%20Implicit%20Logical%20Constraints.pdf) | Jiaxin Bai; Xin Liu; Weiqi Wang; Chen Luo; Yangqiu Song |
| [LoRA: A Logical Reasoning Augmented Dataset for Visual Question Answering](neurips-2023-paper/LoRA%20-%20A%20Logical%20Reasoning%20Augmented%20Dataset%20for%20Visual%20Question%20Answering.pdf) | Jingying Gao; Qi Wu; Alan Blair; Maurice Pagnucco |
| [Efficient Symbolic Policy Learning with Differentiable Symbolic Expression](neurips-2023-paper/Efficient%20Symbolic%20Policy%20Learning%20with%20Differentiable%20Symbolic%20Expression.pdf) | Jiaming Guo; Rui Zhang; Shaohui Peng; Qi Yi; Xing Hu; Ruizhi Chen; Zidong Du; xishan zhang; Ling Li; Qi Guo; Yunji Chen |
| [Transformer-based Planning for Symbolic Regression](neurips-2023-paper/Transformer-based%20Planning%20for%20Symbolic%20Regression.pdf) | Parshin Shojaee; Kazem Meidani; Amir Barati Farimani; Chandan Reddy |
| [Human spatiotemporal pattern learning as probabilistic program synthesis](neurips-2023-paper/Human%20spatiotemporal%20pattern%20learning%20as%20probabilistic%20program%20synthesis.pdf) | Tracey Mills; Josh Tenenbaum; Samuel Cheyette |
| [Soft-Unification in Deep Probabilistic Logic](neurips-2023-paper/Soft-Unification%20in%20Deep%20Probabilistic%20Logic.pdf) | Jaron Maene; Luc De Raedt |
| [Discovering Intrinsic Spatial-Temporal Logic Rules to Explain Human Actions](neurips-2023-paper/Discovering%20Intrinsic%20Spatial-Temporal%20Logic%20Rules%20to%20Explain%20Human%20Actions.pdf) | Chengzhi Cao; Chao Yang; Ruimao Zhang; Shuang Li |
| [Not All Neuro-Symbolic Concepts Are Created Equal: Analysis and Mitigation of Reasoning Shortcuts](neurips-2023-paper/Not%20All%20Neuro-Symbolic%20Concepts%20Are%20Created%20Equal%20-%20Analysis%20and%20Mitigation%20of%20Reasoning%20Shortcuts.pdf) | Emanuele Marconato; Stefano Teso; Antonio Vergari; Andrea Passerini |

#### NeurIPS 2024

| Paper | Authors |
|---|---|
| [HYSYNTH: Context-Free LLM Approximation for Guiding Program Synthesis](neurips-2024-paper/HYSYNTH%20-%20Context-Free%20LLM%20Approximation%20for%20Guiding%20Program%20Synthesis.pdf) | Shraddha Barke; Emmanuel Anaya Gonzalez; Saketh Ram Kasibatla; Taylor Berg-Kirkpatrick; Nadia Polikarpova |
| [Interpret Your Decision: Logical Reasoning Regularization for Generalization in Visual Classification](neurips-2024-paper/Interpret%20Your%20Decision%20-%20Logical%20Reasoning%20Regularization%20for%20Generalization%20in%20Visual%20Classification.pdf) | Zhaorui Tan; Xi Yang; Qiufeng Wang; Anh Nguyen; Kaizhu Huang |
| [Neuro-Symbolic Data Generation for Math Reasoning](neurips-2024-paper/Neuro-Symbolic%20Data%20Generation%20for%20Math%20Reasoning.pdf) | Zenan Li; Zhi Zhou; Yuan Yao; Yu-Feng Li; Chun Cao; Fan Yang; Xian Zhang; Xiaoxing Ma |
| [Symbolic Regression with a Learned Concept Library](neurips-2024-paper/Symbolic%20Regression%20with%20a%20Learned%20Concept%20Library.pdf) | Arya Grayeli; Atharva Sehgal; Omar Costilla-Reyes; Miles Cranmer; Swarat Chaudhuri |
| [LogiCity: Advancing Neuro-Symbolic AI with Abstract Urban Simulation](neurips-2024-paper/LogiCity%20-%20Advancing%20Neuro-Symbolic%20AI%20with%20Abstract%20Urban%20Simulation.pdf) | Bowen Li; Zhaoyu Li; Qiwei Du; Jinqi Luo; Wenshan Wang; Yaqi Xie; Simon Stepputtis; Chen Wang; Katia Sycara; Pradeep Ravikumar; Alexander Gray; Xujie Si; Sebastian Scherer |
| [A Neuro-Symbolic Benchmark Suite for Concept Quality and Reasoning Shortcuts](neurips-2024-paper/A%20Neuro-Symbolic%20Benchmark%20Suite%20for%20Concept%20Quality%20and%20Reasoning%20Shortcuts.pdf) | Samuele Bortolotti; Emanuele Marconato; Tommaso Carraro; Paolo Morettin; Emile van Krieken; Antonio Vergari; Stefano Teso; Andrea Passerini |
| [Convolutional Differentiable Logic Gate Networks](neurips-2024-paper/Convolutional%20Differentiable%20Logic%20Gate%20Networks.pdf) | Felix Petersen; Hilde Kuehne; Christian Borgelt; Julian Welzel; Stefano Ermon |

#### NeurIPS 2025

| Paper | Authors |
|---|---|
| [Graph-based Symbolic Regression with Invariance and Constraint Encoding](neurips-2025-paper/Graph-based%20Symbolic%20Regression%20with%20Invariance%20and%20Constraint%20Encoding.pdf) | Ziyu Xiang; Kenna Ashen; Xiaofeng Qian; Xiaoning Qian |
| [Skill-Driven Neurosymbolic State Abstractions](neurips-2025-paper/Skill-Driven%20Neurosymbolic%20State%20Abstractions.pdf) | Alper Ahmetoglu; Steven James; Cameron Allen; Sam Lobel; David Abel; George Konidaris |
| [Program Synthesis via Test-Time Transduction](neurips-2025-paper/Program%20Synthesis%20via%20Test-Time%20Transduction.pdf) | Kang-il Lee; Jahyun Koo; Seunghyun Yoon; Minbeom Kim; Hyukhun Koh; Dongryeol Lee; Kyomin Jung |
| [Improving Monte Carlo Tree Search for Symbolic Regression](neurips-2025-paper/Improving%20Monte%20Carlo%20Tree%20Search%20for%20Symbolic%20Regression.pdf) | Zhengyao Huang; Daniel Huang; Tiannan Xiao; Dina Ma; Zhenyu Ming; Hao Shi; Yuanhui Wen |
| [Embeddings as Probabilistic Equivalence in Logic Programs](neurips-2025-paper/Embeddings%20as%20Probabilistic%20Equivalence%20in%20Logic%20Programs.pdf) | Jaron Maene; Efthymia Tsamoura |
| [MuSLR: Multimodal Symbolic Logical Reasoning](neurips-2025-paper/MuSLR%20-%20Multimodal%20Symbolic%20Logical%20Reasoning.pdf) | Jundong Xu; Hao Fei; Yuhui Zhang; Liangming Pan; Qijun Huang; Qian Liu; Preslav Nakov; Min-Yen Kan; William Yang Wang; Mong-Li Lee; Wynne Hsu |
| [Model Reconciliation via Cost-Optimal Explanations in Probabilistic Logic Programming](neurips-2025-paper/Model%20Reconciliation%20via%20Cost-Optimal%20Explanations%20in%20Probabilistic%20Logic%20Programming.pdf) | Yinxu Tang; Stylianos Loukas Vasileiou; Vincent Derkinderen; William Yeoh |
| [Discovering Symbolic Partial Differential Equation by Abductive Learning](neurips-2025-paper/Discovering%20Symbolic%20Partial%20Differential%20Equation%20by%20Abductive%20Learning.pdf) | En-Hao Gao; Cunjing Ge; Yuan Jiang; Zhi-Hua Zhou |
| [WALL-E: World Alignment by NeuroSymbolic Learning improves World Model-based LLM Agents](neurips-2025-paper/WALL-E%20-%20World%20Alignment%20by%20NeuroSymbolic%20Learning%20improves%20World%20Model-based%20LLM%20Agents.pdf) | Siyu Zhou; Tianyi Zhou; Yijun Yang; Guodong Long; Deheng Ye; Jing Jiang; Chengqi Zhang |
| [Are Language Models Efficient Reasoners? A Perspective from Logic Programming](neurips-2025-paper/Are%20Language%20Models%20Efficient%20Reasoners%3F%20A%20Perspective%20from%20Logic%20Programming.pdf) | Andreas Opedal; Yanick Zengaffinen; Haruki Shirakami; Clemente Pasti; Mrinmaya Sachan; Abulhair Saparov; Ryan Cotterell; Bernhard Schölkopf |
| [Towards Reliable Code-as-Policies: A Neuro-Symbolic Framework for Embodied Task Planning](neurips-2025-paper/Towards%20Reliable%20Code-as-Policies%20-%20A%20Neuro-Symbolic%20Framework%20for%20Embodied%20Task%20Planning.pdf) | Sanghyun Ahn; Wonje Choi; Junyong Lee; Jinwoo Park; Honguk Woo |
| [CTSketch: Compositional Tensor Sketching for Scalable Neurosymbolic Learning](neurips-2025-paper/CTSketch%20-%20Compositional%20Tensor%20Sketching%20for%20Scalable%20Neurosymbolic%20Learning.pdf) | Seewon Choi; Alaia Solko-Breslin; Rajeev Alur; Eric Wong |
| [A learnability analysis on neuro-symbolic learning](neurips-2025-paper/A%20learnability%20analysis%20on%20neuro-symbolic%20learning.pdf) | Hao-Yuan He; Ming LI |
| [NeuSymEA: Neuro-symbolic Entity Alignment via Variational Inference](neurips-2025-paper/NeuSymEA%20-%20Neuro-symbolic%20Entity%20Alignment%20via%20Variational%20Inference.pdf) | Shengyuan Chen; Zheng Yuan; Qinggang Zhang; Wen Hua; Jiannong Cao; Xiao Huang |
| [Mind the Gap: Removing the Discretization Gap in Differentiable Logic Gate Networks](neurips-2025-paper/Mind%20the%20Gap%20-%20Removing%20the%20Discretization%20Gap%20in%20Differentiable%20Logic%20Gate%20Networks.pdf) | Shakir Yousefi; Andreas Plesner; Till Aczel; Roger Wattenhofer |
| [Neurosymbolic Diffusion Models](neurips-2025-paper/Neurosymbolic%20Diffusion%20Models.pdf) | Emile van Krieken; Pasquale Minervini; Edoardo Maria Ponti; Antonio Vergari |
| [Once Upon an Input: Reasoning via Per-Instance Program Synthesis](neurips-2025-paper/Once%20Upon%20an%20Input%20-%20Reasoning%20via%20Per-Instance%20Program%20Synthesis.pdf) | Adam Stein; Neelay Velingker; Mayur Naik; Eric Wong |
| [Imbalances in Neurosymbolic Learning: Characterization and Mitigating Strategies](neurips-2025-paper/Imbalances%20in%20Neurosymbolic%20Learning%20-%20Characterization%20and%20Mitigating%20Strategies.pdf) | Efthymia Tsamoura; Kaifu Wang; Dan Roth |
| [Right for the Right Reasons: Avoiding Reasoning Shortcuts via Prototypical Neurosymbolic AI](neurips-2025-paper/Right%20for%20the%20Right%20Reasons%20-%20Avoiding%20Reasoning%20Shortcuts%20via%20Prototypical%20Neurosymbolic%20AI.pdf) | Luca Andolfi; Eleonora Giunchiglia |
| [Shortcuts and Identifiability in Concept-based Models from a Neuro-Symbolic Lens](neurips-2025-paper/Shortcuts%20and%20Identifiability%20in%20Concept-based%20Models%20from%20a%20Neuro-Symbolic%20Lens.pdf) | Samuele Bortolotti; Emanuele Marconato; Paolo Morettin; Andrea Passerini; Stefano Teso |
| [Curriculum Abductive Learning](neurips-2025-paper/Curriculum%20Abductive%20Learning.pdf) | Wen-Chao Hu; Qi-Jie Li; Lin-Han Jia; Cunjing Ge; Yu-Feng Li; Yuan Jiang; Zhi-Hua Zhou |
| [NeSyPr: Neurosymbolic Proceduralization For Efficient Embodied Reasoning](neurips-2025-paper/NeSyPr%20-%20Neurosymbolic%20Proceduralization%20For%20Efficient%20Embodied%20Reasoning.pdf) | Wonje Choi; Jooyoung Kim; Honguk Woo |

### AAAI

> Sourced via [dblp](https://dblp.org/db/conf/aaai/) with PDFs resolved through each paper's DOI to the open-access [AAAI OJS proceedings](https://ojs.aaai.org/index.php/AAAI) (AAAI has been fully open-access since moving to OJS).


#### AAAI 2020

| Paper | Authors |
|---|---|
| [Structural Decompositions of Epistemic Logic Programs](aaai-2020-paper/Structural%20Decompositions%20of%20Epistemic%20Logic%20Programs.pdf) | Markus Hecher; Michael Morak; Stefan Woltran |
| [FastLAS: Scalable Inductive Logic Programming Incorporating Domain-Specific Optimisation Criteria](aaai-2020-paper/FastLAS%20-%20Scalable%20Inductive%20Logic%20Programming%20Incorporating%20Domain-Specific%20Optimisation%20Criteria.pdf) | Mark Law; Alessandra Russo; Elisa Bertino; Krysia Broda; Jorge Lobo |
| [Resilient Logic Programs: Answer Set Programs Challenged by Ontologies](aaai-2020-paper/Resilient%20Logic%20Programs%20-%20Answer%20Set%20Programs%20Challenged%20by%20Ontologies.pdf) | Sanja Lukumbuzya; Magdalena Ortiz; Mantas Simkus |
| [Forgetting to Learn Logic Programs](aaai-2020-paper/Forgetting%20to%20Learn%20Logic%20Programs.pdf) | Andrew Cropper |
| [Differentiable Reasoning on Large Knowledge Bases and Natural Language](aaai-2020-paper/Differentiable%20Reasoning%20on%20Large%20Knowledge%20Bases%20and%20Natural%20Language.pdf) | Pasquale Minervini; Matko Bosnjak; Tim Rocktäschel; Sebastian Riedel; Edward Grefenstette |
| [Just Add Functions: A Neural-Symbolic Language Model](aaai-2020-paper/Just%20Add%20Functions%20-%20A%20Neural-Symbolic%20Language%20Model.pdf) | David Demeter; Doug Downey |
| [Beyond the Grounding Bottleneck: Datalog Techniques for Inference in Probabilistic Logic Programs](aaai-2020-paper/Beyond%20the%20Grounding%20Bottleneck%20-%20Datalog%20Techniques%20for%20Inference%20in%20Probabilistic%20Logic%20Programs.pdf) | Efthymia Tsamoura; Víctor Gutiérrez-Basulto; Angelika Kimmig |

#### AAAI 2021

| Paper | Authors |
|---|---|
| [Conversational Neuro-Symbolic Commonsense Reasoning](aaai-2021-paper/Conversational%20Neuro-Symbolic%20Commonsense%20Reasoning.pdf) | Forough Arabshahi; Jennifer Lee; Mikayla Gawarecki; Kathryn Mazaitis; Amos Azaria; Tom M. Mitchell |
| [Dynamic Neuro-Symbolic Knowledge Graph Construction for Zero-shot Commonsense Question Answering](aaai-2021-paper/Dynamic%20Neuro-Symbolic%20Knowledge%20Graph%20Construction%20for%20Zero-shot%20Commonsense%20Question%20Answering.pdf) | Antoine Bosselut; Ronan Le Bras; Yejin Choi |
| [Self-Supervised Self-Supervision by Combining Deep Learning and Probabilistic Logic](aaai-2021-paper/Self-Supervised%20Self-Supervision%20by%20Combining%20Deep%20Learning%20and%20Probabilistic%20Logic.pdf) | Hunter Lang; Hoifung Poon |
| [A Scalable Reasoning and Learning Approach for Neural-Symbolic Stream Fusion](aaai-2021-paper/A%20Scalable%20Reasoning%20and%20Learning%20Approach%20for%20Neural-Symbolic%20Stream%20Fusion.pdf) | Danh Le Phuoc; Thomas Eiter; Anh Lê Tuán |
| [Differentiable Inductive Logic Programming for Structured Examples](aaai-2021-paper/Differentiable%20Inductive%20Logic%20Programming%20for%20Structured%20Examples.pdf) | Hikaru Shindo; Masaaki Nishino; Akihiro Yamamoto |
| [Neural-Symbolic Integration: A Compositional Perspective](aaai-2021-paper/Neural-Symbolic%20Integration%20-%20A%20Compositional%20Perspective.pdf) | Efthymia Tsamoura; Timothy M. Hospedales; Loizos Michael |
| [Constraint Logic Programming for Real-World Test Laboratory Scheduling](aaai-2021-paper/Constraint%20Logic%20Programming%20for%20Real-World%20Test%20Laboratory%20Scheduling.pdf) | Tobias Geibinger; Florian Mischek; Nysret Musliu |
| [Knowledge Refactoring for Inductive Program Synthesis](aaai-2021-paper/Knowledge%20Refactoring%20for%20Inductive%20Program%20Synthesis.pdf) | Sebastijan Dumancic; Tias Guns; Andrew Cropper |
| [Constraint-Driven Learning of Logic Programs](aaai-2021-paper/Constraint-Driven%20Learning%20of%20Logic%20Programs.pdf) | Rolf Morel |
| [Neuro-Symbolic Techniques for Description Logic Reasoning (Student Abstract)](aaai-2021-paper/Neuro-Symbolic%20Techniques%20for%20Description%20Logic%20Reasoning%20%28Student%20Abstract%29.pdf) | Gunjan Singh; Sutapa Mondal; Sumit Bhatia; Raghava Mutharaju |
| [IBM Scenario Planning Advisor: A Neuro-Symbolic ERM Solution](aaai-2021-paper/IBM%20Scenario%20Planning%20Advisor%20-%20A%20Neuro-Symbolic%20ERM%20Solution.pdf) | Mark Feblowitz; Oktie Hassanzadeh; Michael Katz; Shirin Sohrabi; Kavitha Srinivas; Octavian Udrea |

#### AAAI 2022

| Paper | Authors |
|---|---|
| [Axiomatization of Aggregates in Answer Set Programming](aaai-2022-paper/Axiomatization%20of%20Aggregates%20in%20Answer%20Set%20Programming.pdf) | Jorge Fandinno; Zachary Hansen; Yuliya Lierler |
| [Weakly Supervised Neural Symbolic Learning for Cognitive Tasks](aaai-2022-paper/Weakly%20Supervised%20Neural%20Symbolic%20Learning%20for%20Cognitive%20Tasks.pdf) | Jidong Tian; Yitian Li; Wenqing Chen; Liqiang Xiao; Hao He; Yaohui Jin |
| [Learning Logic Programs Though Divide, Constrain, and Conquer](aaai-2022-paper/Learning%20Logic%20Programs%20Though%20Divide%2C%20Constrain%2C%20and%20Conquer.pdf) | Andrew Cropper |
| [Scaling Neural Program Synthesis with Distribution-Based Search](aaai-2022-paper/Scaling%20Neural%20Program%20Synthesis%20with%20Distribution-Based%20Search.pdf) | Nathanaël Fijalkow; Guillaume Lagarde; Théo Matricon; Kevin Ellis; Pierre Ohlmann; Akarsh Nayan Potta |
| [Neuro-Symbolic Inductive Logic Programming with Logical Neural Networks](aaai-2022-paper/Neuro-Symbolic%20Inductive%20Logic%20Programming%20with%20Logical%20Neural%20Networks.pdf) | Prithviraj Sen; Breno W. S. R. de Carvalho; Ryan Riegel; Alexander G. Gray |
| [Inference and Learning with Model Uncertainty in Probabilistic Logic Programs](aaai-2022-paper/Inference%20and%20Learning%20with%20Model%20Uncertainty%20in%20Probabilistic%20Logic%20Programs.pdf) | Victor Verreet; Vincent Derkinderen; Pedro Zuidberg Dos Martires; Luc De Raedt |
| [DeepStochLog: Neural Stochastic Logic Programming](aaai-2022-paper/DeepStochLog%20-%20Neural%20Stochastic%20Logic%20Programming.pdf) | Thomas Winters; Giuseppe Marra; Robin Manhaeve; Luc De Raedt |
| [Weakly Supervised Neuro-Symbolic Module Networks for Numerical Reasoning over Text](aaai-2022-paper/Weakly%20Supervised%20Neuro-Symbolic%20Module%20Networks%20for%20Numerical%20Reasoning%20over%20Text.pdf) | Amrita Saha; Shafiq R. Joty; Steven C. H. Hoi |

#### AAAI 2023

| Paper | Authors |
|---|---|
| [PaTeCon: A Pattern-Based Temporal Constraint Mining Method for Conflict Detection on Knowledge Graphs](aaai-2023-paper/PaTeCon%20-%20A%20Pattern-Based%20Temporal%20Constraint%20Mining%20Method%20for%20Conflict%20Detection%20on%20Knowledge%20Graphs.pdf) | Jianhao Chen; Junyang Ren; Wentao Ding; Yuzhong Qu |
| [Rule Induction in Knowledge Graphs Using Linear Programming](aaai-2023-paper/Rule%20Induction%20in%20Knowledge%20Graphs%20Using%20Linear%20Programming.pdf) | Sanjeeb Dash; Joao P. Goncalves |
| [NQE: N-ary Query Embedding for Complex Query Answering over Hyper-Relational Knowledge Graphs](aaai-2023-paper/NQE%20-%20N-ary%20Query%20Embedding%20for%20Complex%20Query%20Answering%20over%20Hyper-Relational%20Knowledge%20Graphs.pdf) | Haoran Luo; Haihong E; Yuhao Yang; Gengxian Zhou; Yikai Guo; Tianyu Yao; Zichen Tang; Xueyuan Lin; Kaiyang Wan |
| [Online Symbolic Regression with Informative Query](aaai-2023-paper/Online%20Symbolic%20Regression%20with%20Informative%20Query.pdf) | Pengwei Jin; Di Huang; Rui Zhang; Xing Hu; Ziyuan Nan; Zidong Du; Qi Guo; Yunji Chen |
| [Learning Logic Programs by Discovering Where Not to Search](aaai-2023-paper/Learning%20Logic%20Programs%20by%20Discovering%20Where%20Not%20to%20Search.pdf) | Andrew Cropper; Céline Hocquette |
| [Evaluating Epistemic Logic Programs via Answer Set Programming with Quantifiers](aaai-2023-paper/Evaluating%20Epistemic%20Logic%20Programs%20via%20Answer%20Set%20Programming%20with%20Quantifiers.pdf) | Wolfgang Faber; Michael Morak |
| [Characterizing Structural Hardness of Logic Programs: What Makes Cycles and Reachability Hard for Treewidth?](aaai-2023-paper/Characterizing%20Structural%20Hardness%20of%20Logic%20Programs%20-%20What%20Makes%20Cycles%20and%20Reachability%20Hard%20for%20Treewidth%3F.pdf) | Markus Hecher |
| [Relational Program Synthesis with Numerical Reasoning](aaai-2023-paper/Relational%20Program%20Synthesis%20with%20Numerical%20Reasoning.pdf) | Céline Hocquette; Andrew Cropper |
| [Learning to Break Symmetries for Efficient Optimization in Answer Set Programming](aaai-2023-paper/Learning%20to%20Break%20Symmetries%20for%20Efficient%20Optimization%20in%20Answer%20Set%20Programming.pdf) | Alice Tarzariol; Martin Gebser; Konstantin Schekotihin; Mark Law |
| [Neurosymbolic Reasoning and Learning with Restricted Boltzmann Machines](aaai-2023-paper/Neurosymbolic%20Reasoning%20and%20Learning%20with%20Restricted%20Boltzmann%20Machines.pdf) | Son N. Tran; Artur S. d'Avila Garcez |
| [Learning Program Synthesis for Integer Sequences from Scratch](aaai-2023-paper/Learning%20Program%20Synthesis%20for%20Integer%20Sequences%20from%20Scratch.pdf) | Thibault Gauthier; Josef Urban |
| [Enabling Knowledge Refinement upon New Concepts in Abductive Learning](aaai-2023-paper/Enabling%20Knowledge%20Refinement%20upon%20New%20Concepts%20in%20Abductive%20Learning.pdf) | Yu-Xuan Huang; Wang-Zhou Dai; Yuan Jiang; Zhi-Hua Zhou |
| [Robust Neuro-Symbolic Goal and Plan Recognition](aaai-2023-paper/Robust%20Neuro-Symbolic%20Goal%20and%20Plan%20Recognition.pdf) | Leonardo Amado; Ramon Fraga Pereira; Felipe Meneguzzi |
| [Out-of-Distribution Generalization by Neural-Symbolic Joint Training](aaai-2023-paper/Out-of-Distribution%20Generalization%20by%20Neural-Symbolic%20Joint%20Training.pdf) | Anji Liu; Hongming Xu; Guy Van den Broeck; Yitao Liang |
| [Learning Logical Reasoning Using an Intelligent Tutoring System: A Hybrid Approach to Student Modeling](aaai-2023-paper/Learning%20Logical%20Reasoning%20Using%20an%20Intelligent%20Tutoring%20System%20-%20A%20Hybrid%20Approach%20to%20Student%20Modeling.pdf) | Roger Nkambou; Janie Brisson; Ange Tato; Serge Robert |
| [Modeling Strategies as Programs: How to Study Strategy Differences in Intelligent Systems with Program Synthesis](aaai-2023-paper/Modeling%20Strategies%20as%20Programs%20-%20How%20to%20Study%20Strategy%20Differences%20in%20Intelligent%20Systems%20with%20Program%20Synthesis.pdf) | James Ainooson |

#### AAAI 2024

| Paper | Authors |
|---|---|
| [Unveiling Implicit Deceptive Patterns in Multi-Modal Fake News via Neuro-Symbolic Reasoning](aaai-2024-paper/Unveiling%20Implicit%20Deceptive%20Patterns%20in%20Multi-Modal%20Fake%20News%20via%20Neuro-Symbolic%20Reasoning.pdf) | Yiqi Dong; Dongxiao He; Xiaobao Wang; Youzhu Jin; Meng Ge; Carl Yang; Di Jin |
| [On the Structural Hardness of Answer Set Programming: Can Structure Efficiently Confine the Power of Disjunctions?](aaai-2024-paper/On%20the%20Structural%20Hardness%20of%20Answer%20Set%20Programming%20-%20Can%20Structure%20Efficiently%20Confine%20the%20Power%20of%20Disjunctions%3F.pdf) | Markus Hecher; Rafael Kiesel |
| [Learning MDL Logic Programs from Noisy Data](aaai-2024-paper/Learning%20MDL%20Logic%20Programs%20from%20Noisy%20Data.pdf) | Céline Hocquette; Andreas Niskanen; Matti Järvisalo; Andrew Cropper |
| [A Unified View on Forgetting and Strong Equivalence Notions in Answer Set Programming](aaai-2024-paper/A%20Unified%20View%20on%20Forgetting%20and%20Strong%20Equivalence%20Notions%20in%20Answer%20Set%20Programming.pdf) | Zeynep G. Saribatur; Stefan Woltran |
| [Scalable Enumeration of Trap Spaces in Boolean Networks via Answer Set Programming](aaai-2024-paper/Scalable%20Enumeration%20of%20Trap%20Spaces%20in%20Boolean%20Networks%20via%20Answer%20Set%20Programming.pdf) | Giang V. Trinh; Belaid Benhamou; Samuel Pastva; Sylvain Soliman |
| [Symbolic Regression Enhanced Decision Trees for Classification Tasks](aaai-2024-paper/Symbolic%20Regression%20Enhanced%20Decision%20Trees%20for%20Classification%20Tasks.pdf) | Kei Sen Fong; Mehul Motani |
| [Racing Control Variable Genetic Programming for Symbolic Regression](aaai-2024-paper/Racing%20Control%20Variable%20Genetic%20Programming%20for%20Symbolic%20Regression.pdf) | Nan Jiang; Yexiang Xue |
| [NESTER: An Adaptive Neurosymbolic Method for Causal Effect Estimation](aaai-2024-paper/NESTER%20-%20An%20Adaptive%20Neurosymbolic%20Method%20for%20Causal%20Effect%20Estimation.pdf) | Abbavaram Gowtham Reddy; Vineeth N. Balasubramanian |
| [Deciphering Raw Data in Neuro-Symbolic Learning with Provable Guarantees](aaai-2024-paper/Deciphering%20Raw%20Data%20in%20Neuro-Symbolic%20Learning%20with%20Provable%20Guarantees.pdf) | Lue Tao; Yu-Xuan Huang; Wang-Zhou Dai; Yuan Jiang |
| [TEILP: Time Prediction over Knowledge Graphs via Logical Reasoning](aaai-2024-paper/TEILP%20-%20Time%20Prediction%20over%20Knowledge%20Graphs%20via%20Logical%20Reasoning.pdf) | Siheng Xiong; Yuan Yang; Ali Payani; James Clayton Kerce; Faramarz Fekri |
| [Safe Abductive Learning in the Presence of Inaccurate Rules](aaai-2024-paper/Safe%20Abductive%20Learning%20in%20the%20Presence%20of%20Inaccurate%20Rules.pdf) | Xiaowen Yang; Jie-Jing Shao; Wei-Wei Tu; Yufeng Li; Wang-Zhou Dai; Zhi-Hua Zhou |
| [Large Language Models Are Neurosymbolic Reasoners](aaai-2024-paper/Large%20Language%20Models%20Are%20Neurosymbolic%20Reasoners.pdf) | Meng Fang; Shilong Deng; Yudi Zhang; Zijing Shi; Ling Chen; Mykola Pechenizkiy; Jun Wang |
| [LR-XFL: Logical Reasoning-Based Explainable Federated Learning](aaai-2024-paper/LR-XFL%20-%20Logical%20Reasoning-Based%20Explainable%20Federated%20Learning.pdf) | Yanci Zhang; Han Yu |
| [From Statistical Relational to Neuro-Symbolic Artificial Intelligence](aaai-2024-paper/From%20Statistical%20Relational%20to%20Neuro-Symbolic%20Artificial%20Intelligence.pdf) | Giuseppe Marra |
| [Program Synthesis with Best-First Bottom-Up Search (Abstract Reprint)](aaai-2024-paper/Program%20Synthesis%20with%20Best-First%20Bottom-Up%20Search%20%28Abstract%20Reprint%29.pdf) | Saqib Ameen; Levi H. S. Lelis |
| [Learning Neuro-Symbolic Abstractions for Robot Planning and Learning](aaai-2024-paper/Learning%20Neuro-Symbolic%20Abstractions%20for%20Robot%20Planning%20and%20Learning.pdf) | Naman Shah |
| [Neuro-Symbolic Integration for Reasoning and Learning on Knowledge Graphs](aaai-2024-paper/Neuro-Symbolic%20Integration%20for%20Reasoning%20and%20Learning%20on%20Knowledge%20Graphs.pdf) | Luisa Werner |

#### AAAI 2025

| Paper | Authors |
|---|---|
| [Progressive Self-Learning for Domain Adaptation on Symbolic Regression of Integer Sequences](aaai-2025-paper/Progressive%20Self-Learning%20for%20Domain%20Adaptation%20on%20Symbolic%20Regression%20of%20Integer%20Sequences.pdf) | Yaohui Zhu; Kaiming Sun; Zhengdong Luo; Lingfeng Wang |
| [NeSyCoCo: A Neuro-Symbolic Concept Composer for Compositional Generalization](aaai-2025-paper/NeSyCoCo%20-%20A%20Neuro-Symbolic%20Concept%20Composer%20for%20Compositional%20Generalization.pdf) | Danial Kamali; Elham J. Barezi; Parisa Kordjamshidi |
| [Online Prompt Selection for Program Synthesis](aaai-2025-paper/Online%20Prompt%20Selection%20for%20Program%20Synthesis.pdf) | Yixuan Li; Lewis Frampton; Federico Mora; Elizabeth Polgreen |
| [Recursive Aggregates as Intensional Functions in Answer Set Programming: Semantics and Strong Equivalence](aaai-2025-paper/Recursive%20Aggregates%20as%20Intensional%20Functions%20in%20Answer%20Set%20Programming%20-%20Semantics%20and%20Strong%20Equivalence.pdf) | Jorge Fandinno; Zachary Hansen |
| [Solving Epistemic Logic Programs Using Generate-and-Test with Propagation](aaai-2025-paper/Solving%20Epistemic%20Logic%20Programs%20Using%20Generate-and-Test%20with%20Propagation.pdf) | Jorge Fandinno; Lute Lillo |
| [Hybrid Reasoning About Relative Position and Orientation of Objects and Navigating Agents Using Answer Set Programming](aaai-2025-paper/Hybrid%20Reasoning%20About%20Relative%20Position%20and%20Orientation%20of%20Objects%20and%20Navigating%20Agents%20Using%20Answer%20Set%20Programming.pdf) | Yusuf Izmirlioglu |
| [Relational Neurosymbolic Markov Models](aaai-2025-paper/Relational%20Neurosymbolic%20Markov%20Models.pdf) | Lennert De Smet; Gabriele Venturato; Luc De Raedt; Giuseppe Marra |
| [Efficient Rectification of Neuro-Symbolic Reasoning Inconsistencies by Abductive Reflection](aaai-2025-paper/Efficient%20Rectification%20of%20Neuro-Symbolic%20Reasoning%20Inconsistencies%20by%20Abductive%20Reflection.pdf) | Wen-Chao Hu; Wang-Zhou Dai; Yuan Jiang; Zhi-Hua Zhou |
| [Dimension Reduction for Symbolic Regression](aaai-2025-paper/Dimension%20Reduction%20for%20Symbolic%20Regression.pdf) | Paul Kahlmeyer; Markus Fischer; Joachim Giesen |
| [Discovering Symmetries of ODEs by Symbolic Regression](aaai-2025-paper/Discovering%20Symmetries%20of%20ODEs%20by%20Symbolic%20Regression.pdf) | Paul Kahlmeyer; Niklas Merk; Joachim Giesen |
| [Eco Search: A No-delay Best-First Search Algorithm for Program Synthesis](aaai-2025-paper/Eco%20Search%20-%20A%20No-delay%20Best-First%20Search%20Algorithm%20for%20Program%20Synthesis.pdf) | Théo Matricon; Nathanaël Fijalkow; Guillaume Lagarde |
| [Enhancing SQL Query Generation with Neurosymbolic Reasoning](aaai-2025-paper/Enhancing%20SQL%20Query%20Generation%20with%20Neurosymbolic%20Reasoning.pdf) | Henrijs Princis; Cristina David; Alan Mycroft |
| [Zero-Shot Conditioning of Score-Based Diffusion Models by Neuro-Symbolic Constraints](aaai-2025-paper/Zero-Shot%20Conditioning%20of%20Score-Based%20Diffusion%20Models%20by%20Neuro-Symbolic%20Constraints.pdf) | Davide Scassola; Sebastiano Saccani; Ginevra Carbone; Luca Bortolussi |
| [Noise-Resilient Symbolic Regression with Dynamic Gating Reinforcement Learning](aaai-2025-paper/Noise-Resilient%20Symbolic%20Regression%20with%20Dynamic%20Gating%20Reinforcement%20Learning.pdf) | Chenglu Sun; Shuo Shen; Wenzhi Tao; Deyi Xue; Zixia Zhou |
| [Neural-Symbolic Collaborative Distillation: Advancing Small Language Models for Complex Reasoning Tasks](aaai-2025-paper/Neural-Symbolic%20Collaborative%20Distillation%20-%20Advancing%20Small%20Language%20Models%20for%20Complex%20Reasoning%20Tasks.pdf) | Huanxuan Liao; Shizhu He; Yao Xu; Yuanzhe Zhang; Kang Liu; Jun Zhao |
| [GNS: Solving Plane Geometry Problems by Neural-Symbolic Reasoning with Multi-Modal LLMs](aaai-2025-paper/GNS%20-%20Solving%20Plane%20Geometry%20Problems%20by%20Neural-Symbolic%20Reasoning%20with%20Multi-Modal%20LLMs.pdf) | Maizhen Ning; Zihao Zhou; Qiufeng Wang; Xiaowei Huang; Kaizhu Huang |
| [MDD-5k: A New Diagnostic Conversation Dataset for Mental Disorders Synthesized via Neuro-Symbolic LLM Agents](aaai-2025-paper/MDD-5k%20-%20A%20New%20Diagnostic%20Conversation%20Dataset%20for%20Mental%20Disorders%20Synthesized%20via%20Neuro-Symbolic%20LLM%20Agents.pdf) | Congchi Yin; Feng Li; Shu Zhang; Zike Wang; Jun Shao; Piji Li; Jianhua Chen; Xun Jiang |
| [Learning Logic Specifications for Policy Guidance in POMDPs: an Inductive Logic Programming Approach](aaai-2025-paper/Learning%20Logic%20Specifications%20for%20Policy%20Guidance%20in%20POMDPs%20-%20an%20Inductive%20Logic%20Programming%20Approach.pdf) | Daniele Meli; Alberto Castellini; Alessandro Farinelli |
| [Neuro-Guided Graph Search for Symbolic Regression (Student Abstract)](aaai-2025-paper/Neuro-Guided%20Graph%20Search%20for%20Symbolic%20Regression%20%28Student%20Abstract%29.pdf) | Piotr Wyrwinski; Krzysztof Krawiec |
| [Neurosymbolic Reinforcement Learning: Playing MiniHack with Probabilistic Logic Shields](aaai-2025-paper/Neurosymbolic%20Reinforcement%20Learning%20-%20Playing%20MiniHack%20with%20Probabilistic%20Logic%20Shields.pdf) | David Debot; Gabriele Venturato; Giuseppe Marra; Luc De Raedt |

#### AAAI 2026

| Paper | Authors |
|---|---|
| [NeuS-QA: Grounding Long-Form Video Understanding in Temporal Logic and Neuro-Symbolic Reasoning](aaai-2026-paper/NeuS-QA%20-%20Grounding%20Long-Form%20Video%20Understanding%20in%20Temporal%20Logic%20and%20Neuro-Symbolic%20Reasoning.pdf) | Sahil Shah; S. P. Sharan; Harsh Goel; Minkyu Choi; Mustafa Munir; Manvik Pasula; Radu Marculescu; Sandeep Chinchali |
| [Efficient Rule Induction by Ignoring Pointless Rules](aaai-2026-paper/Efficient%20Rule%20Induction%20by%20Ignoring%20Pointless%20Rules.pdf) | Andrew Cropper; David M. Cerna |
| [Symmetry Breaking for Inductive Logic Programming](aaai-2026-paper/Symmetry%20Breaking%20for%20Inductive%20Logic%20Programming.pdf) | Andrew Cropper; David M. Cerna; Matti Järvisalo |
| [Self-Supervised Inductive Logic Programming](aaai-2026-paper/Self-Supervised%20Inductive%20Logic%20Programming.pdf) | Stassa Patsantzis |
| [Delphi: A Neuro-Symbolic Framework for Individualized, Safe and Interpretable Treatment Recommendation](aaai-2026-paper/Delphi%20-%20A%20Neuro-Symbolic%20Framework%20for%20Individualized%2C%20Safe%20and%20Interpretable%20Treatment%20Recommendation.pdf) | Muchan Tao; Haonan Qin; Yuqi Fang; Caifeng Shan; Tieniu Tan |
| [Socrates or Smartypants: Testing Logic Reasoning Capabilities of Large Language Models with Logic Programming-Based Test Oracles](aaai-2026-paper/Socrates%20or%20Smartypants%20-%20Testing%20Logic%20Reasoning%20Capabilities%20of%20Large%20Language%20Models%20with%20Logic%20Programming-Based%20Test%20Oracles.pdf) | Zihao Xu; Junchen Ding; Yiling Lou; Kun Zhang; Dong Gong; Yuekang Li |
| [ProbLog4Fairness: A Neurosymbolic Approach to Modeling and Mitigating Bias](aaai-2026-paper/ProbLog4Fairness%20-%20A%20Neurosymbolic%20Approach%20to%20Modeling%20and%20Mitigating%20Bias.pdf) | Rik Adriaensen; Lucas Van Praet; Jessa Bekker; Robin Manhaeve; Pieter Delobelle; Maarten Buyl |
| [DeepProofLog: Efficient Proving in Deep Stochastic Logic Programs](aaai-2026-paper/DeepProofLog%20-%20Efficient%20Proving%20in%20Deep%20Stochastic%20Logic%20Programs.pdf) | Ying Jiao; Rodrigo Castellano Ontiveros; Luc De Raedt; Marco Gori; Francesco Giannini; Michelangelo Diligenti; Giuseppe Marra |
| [Neuro-Symbolic Federated Learning over Heterogeneous Data-Views: A Structured Approach to Distributive EHR Modelling](aaai-2026-paper/Neuro-Symbolic%20Federated%20Learning%20over%20Heterogeneous%20Data-Views%20-%20A%20Structured%20Approach%20to%20Distributive%20EHR%20Modelling.pdf) | Soheila Molaei; Bahareh Fatemi; Anshul Thakur; Andrew A. S. Soltan; Fazle Rabbi; Andreas L. Opdahl; Kim Branson; Patrick Schwab; Danielle Belgrave; David A. Clifton |
| [A Solver-in-the-Loop Framework for Improving LLMs on Answer Set Programming for Logic Puzzle Solving](aaai-2026-paper/A%20Solver-in-the-Loop%20Framework%20for%20Improving%20LLMs%20on%20Answer%20Set%20Programming%20for%20Logic%20Puzzle%20Solving.pdf) | Timo Pierre Schrader; Lukas Lange; Tobias Kaminski; Simon Razniewski; Annemarie Friedrich |
| [Constraints-Guided Diffusion Reasoner for Neuro-Symbolic Learning](aaai-2026-paper/Constraints-Guided%20Diffusion%20Reasoner%20for%20Neuro-Symbolic%20Learning.pdf) | Xuan Zhang; Zhijian Zhou; Weidi Xu; Yanting Miao; Chao Qu; Yuan Qi |
| [Tapas Are Free! Training-Free Adaptation of Programmatic Agents via LLM-Guided Program Synthesis in Dynamic Environments](aaai-2026-paper/Tapas%20Are%20Free%21%20Training-Free%20Adaptation%20of%20Programmatic%20Agents%20via%20LLM-Guided%20Program%20Synthesis%20in%20Dynamic%20Environments.pdf) | Jinwei Hu; Yi Dong; Youcheng Sun; Xiaowei Huang |
| [Concept-RuleNet: Grounded Multi-Agent Neurosymbolic Reasoning in Vision Language Models](aaai-2026-paper/Concept-RuleNet%20-%20Grounded%20Multi-Agent%20Neurosymbolic%20Reasoning%20in%20Vision%20Language%20Models.pdf) | Sanchit Sinha; Guangzhi Xiong; Zhenghao He; Aidong Zhang |
| [From Hypothesis to Premises: LLM-based Backward Logical Reasoning with Selective Symbolic Translation](aaai-2026-paper/From%20Hypothesis%20to%20Premises%20-%20LLM-based%20Backward%20Logical%20Reasoning%20with%20Selective%20Symbolic%20Translation.pdf) | Qingchuan Li; Mingyue Cheng; Zirui Liu; Daoyu Wang; Yuting Zeng; Tongxuan Liu |
| [NeSTR: A Neuro-Symbolic Abductive Framework for Temporal Reasoning in Large Language Models](aaai-2026-paper/NeSTR%20-%20A%20Neuro-Symbolic%20Abductive%20Framework%20for%20Temporal%20Reasoning%20in%20Large%20Language%20Models.pdf) | Feng Liang; Weixin Zeng; Runhao Zhao; Xiang Zhao |
| [SheetBrain: A Neuro-Symbolic Agent for Accurate Reasoning over Complex and Large Spreadsheets](aaai-2026-paper/SheetBrain%20-%20A%20Neuro-Symbolic%20Agent%20for%20Accurate%20Reasoning%20over%20Complex%20and%20Large%20Spreadsheets.pdf) | Ziwei Wang; Jiayuan Su; Mengyu Zhou; Huaxing Zeng; Mengni Jia; Xiao Lv; Haoyu Dong; Xiaojun Ma; Shi Han; Dongmei Zhang |
| [Post-Hoc Refinement for Multitask Symbolic Regression via Consensus-Accelerated Shapley Analysis](aaai-2026-paper/Post-Hoc%20Refinement%20for%20Multitask%20Symbolic%20Regression%20via%20Consensus-Accelerated%20Shapley%20Analysis.pdf) | Xinyue Li; Wang Hu; Yu Zhang |
| [Language Models and Logic Programs for Trustworthy Tax Reasoning](aaai-2026-paper/Language%20Models%20and%20Logic%20Programs%20for%20Trustworthy%20Tax%20Reasoning.pdf) | William Jurayj; Nils Holzenberger; Benjamin Van Durme |
| [Complex Reasoning over Vision and Language -Leveraging Neurosymbolic AI](aaai-2026-paper/Complex%20Reasoning%20over%20Vision%20and%20Language%20-Leveraging%20Neurosymbolic%20AI.pdf) | Parisa Kordjamshidi |
| [CausalTrace: A Neurosymbolic Causal Analysis Agent for Smart Manufacturing](aaai-2026-paper/CausalTrace%20-%20A%20Neurosymbolic%20Causal%20Analysis%20Agent%20for%20Smart%20Manufacturing.pdf) | Chathurangi Shyalika; Aryaman Sharma; Fadi El Kalach; Utkarshani Jaimini; Cory A. Henson; Ramy F. Harik; Amit P. Sheth |
| [The Future Is Neuro-Symbolic: Where Has It Been, and Where Is It Going?](aaai-2026-paper/The%20Future%20Is%20Neuro-Symbolic%20-%20Where%20Has%20It%20Been%2C%20and%20Where%20Is%20It%20Going%3F.pdf) | Vaishak Belle; Gary Marcus |
| [Cylindrical Lattice Embedding for Program Induction](aaai-2026-paper/Cylindrical%20Lattice%20Embedding%20for%20Program%20Induction.pdf) | Jinseo Shim |

### IJCAI

> Sourced via [dblp](https://dblp.org/db/conf/ijcai/) with PDFs from the open-access [IJCAI proceedings](https://www.ijcai.org/all_proceedings). IJCAI 2026 is not yet indexed by dblp at the time of writing.


#### IJCAI 2020

| Paper | Authors |
|---|---|
| [NeurASP: Embracing Neural Networks into Answer Set Programming](ijcai-2020-paper/NeurASP%20-%20Embracing%20Neural%20Networks%20into%20Answer%20Set%20Programming.pdf) | Zhun Yang; Adam Ishay; Joohyung Lee |
| [Learning Large Logic Programs By Going Beyond Entailment](ijcai-2020-paper/Learning%20Large%20Logic%20Programs%20By%20Going%20Beyond%20Entailment.pdf) | Andrew Cropper; Sebastijan Dumancic |
| [Learning Neural-Symbolic Descriptive Planning Models via Cube-Space Priors: The Voyage Home (to STRIPS)](ijcai-2020-paper/Learning%20Neural-Symbolic%20Descriptive%20Planning%20Models%20via%20Cube-Space%20Priors%20-%20The%20Voyage%20Home%20%28to%20STRIPS%29.pdf) | Masataro Asai; Christian Muise |
| [LogiQA: A Challenge Dataset for Machine Reading Comprehension with Logical Reasoning](ijcai-2020-paper/LogiQA%20-%20A%20Challenge%20Dataset%20for%20Machine%20Reading%20Comprehension%20with%20Logical%20Reasoning.pdf) | Jian Liu; Leyang Cui; Hanmeng Liu; Dandan Huang; Yile Wang; Yue Zhang |
| [A Formal Approach for Cautious Reasoning in Answer Set Programming (Extended Abstract)](ijcai-2020-paper/A%20Formal%20Approach%20for%20Cautious%20Reasoning%20in%20Answer%20Set%20Programming%20%28Extended%20Abstract%29.pdf) | Giovanni Amendola; Carmine Dodaro; Marco Maratea |
| [On the Splitting Property for Epistemic Logic Programs (Extended Abstract)](ijcai-2020-paper/On%20the%20Splitting%20Property%20for%20Epistemic%20Logic%20Programs%20%28Extended%20Abstract%29.pdf) | Pedro Cabalar; Jorge Fandinno; Luis Fariñas del Cerro |
| [Turning 30: New Ideas in Inductive Logic Programming](ijcai-2020-paper/Turning%2030%20-%20New%20Ideas%20in%20Inductive%20Logic%20Programming.pdf) | Andrew Cropper; Sebastijan Dumancic; Stephen H. Muggleton |
| [Graph Neural Networks Meet Neural-Symbolic Computing: A Survey and Perspective](ijcai-2020-paper/Graph%20Neural%20Networks%20Meet%20Neural-Symbolic%20Computing%20-%20A%20Survey%20and%20Perspective.pdf) | Luís C. Lamb; Artur S. d'Avila Garcez; Marco Gori; Marcelo O. R. Prates; Pedro H. C. Avelar; Moshe Y. Vardi |
| [From Statistical Relational to Neuro-Symbolic Artificial Intelligence](ijcai-2020-paper/From%20Statistical%20Relational%20to%20Neuro-Symbolic%20Artificial%20Intelligence.pdf) | Luc De Raedt; Sebastijan Dumancic; Robin Manhaeve; Giuseppe Marra |
| [Determining Inference Semantics for Disjunctive Logic Programs (Extended Abstract)](ijcai-2020-paper/Determining%20Inference%20Semantics%20for%20Disjunctive%20Logic%20Programs%20%28Extended%20Abstract%29.pdf) | Yi-Dong Shen; Thomas Eiter |
| [An Interactive Visualization Platform for Deep Symbolic Regression](ijcai-2020-paper/An%20Interactive%20Visualization%20Platform%20for%20Deep%20Symbolic%20Regression.pdf) | Joanne Taery Kim; Sookyung Kim; Brenden K. Petersen |

#### IJCAI 2021

| Paper | Authors |
|---|---|
| [Abductive Learning with Ground Knowledge Base](ijcai-2021-paper/Abductive%20Learning%20with%20Ground%20Knowledge%20Base.pdf) | Le-Wen Cai; Wang-Zhou Dai; Yu-Xuan Huang; Yufeng Li; Stephen H. Muggleton; Yuan Jiang |
| [Program Synthesis as Dependency Quantified Formula Modulo Theory](ijcai-2021-paper/Program%20Synthesis%20as%20Dependency%20Quantified%20Formula%20Modulo%20Theory.pdf) | Priyanka Golia; Subhajit Roy; Kuldeep S. Meel |
| [A Description Logic for Analogical Reasoning](ijcai-2021-paper/A%20Description%20Logic%20for%20Analogical%20Reasoning.pdf) | Steven Schockaert; Yazmín Ibáñez-García; Víctor Gutiérrez-Basulto |
| [Lifting Symmetry Breaking Constraints with Inductive Logic Programming](ijcai-2021-paper/Lifting%20Symmetry%20Breaking%20Constraints%20with%20Inductive%20Logic%20Programming.pdf) | Alice Tarzariol; Martin Gebser; Konstantin Schekotihin |
| [Compositional Neural Logic Programming](ijcai-2021-paper/Compositional%20Neural%20Logic%20Programming.pdf) | Son N. Tran |
| [A Rule Mining-based Advanced Persistent Threats Detection System](ijcai-2021-paper/A%20Rule%20Mining-based%20Advanced%20Persistent%20Threats%20Detection%20System.pdf) | Sidahmed Benabderrahmane; Ghita Berrada; James Cheney; Petko Valtchev |
| [Defining the Semantics of Abstract Argumentation Frameworks through Logic Programs and Partial Stable Models (Extended Abstract)](ijcai-2021-paper/Defining%20the%20Semantics%20of%20Abstract%20Argumentation%20Frameworks%20through%20Logic%20Programs%20and%20Partial%20Stable%20Models%20%28Extended%20Abstract%29.pdf) | Gianvincenzo Alfano; Sergio Greco; Francesco Parisi; Irina Trubitsyna |

#### IJCAI 2022

| Paper | Authors |
|---|---|
| [Simulating Sets in Answer Set Programming](ijcai-2022-paper/Simulating%20Sets%20in%20Answer%20Set%20Programming.pdf) | Sarah Alice Gaggl; Philipp Hanisch; Markus Krötzsch |
| [Search Space Expansion for Efficient Incremental Inductive Logic Programming from Streamed Data](ijcai-2022-paper/Search%20Space%20Expansion%20for%20Efficient%20Incremental%20Inductive%20Logic%20Programming%20from%20Streamed%20Data.pdf) | Mark Law; Krysia Broda; Alessandra Russo |
| [Learning Higher-Order Logic Programs From Failures](ijcai-2022-paper/Learning%20Higher-Order%20Logic%20Programs%20From%20Failures.pdf) | Stanislaw J. Purgal; David M. Cerna; Cezary Kaliszyk |
| [Considering Constraint Monotonicity and Foundedness in Answer Set Programming](ijcai-2022-paper/Considering%20Constraint%20Monotonicity%20and%20Foundedness%20in%20Answer%20Set%20Programming.pdf) | Yi-Dong Shen; Thomas Eiter |
| [Learning First-Order Rules with Differentiable Logic Program Semantics](ijcai-2022-paper/Learning%20First-Order%20Rules%20with%20Differentiable%20Logic%20Program%20Semantics.pdf) | Kun Gao; Katsumi Inoue; Yongzhi Cao; Hanpin Wang |
| [Neuro-Symbolic Verification of Deep Neural Networks](ijcai-2022-paper/Neuro-Symbolic%20Verification%20of%20Deep%20Neural%20Networks.pdf) | Xuan Xie; Kristian Kersting; Daniel Neider |
| [Utilizing Treewidth for Quantitative Reasoning on Epistemic Logic Programs (Extended Abstract)](ijcai-2022-paper/Utilizing%20Treewidth%20for%20Quantitative%20Reasoning%20on%20Epistemic%20Logic%20Programs%20%28Extended%20Abstract%29.pdf) | Viktor Besin; Markus Hecher; Stefan Woltran |
| [Complex Query Answering with Neural Link Predictors (Extended Abstract)](ijcai-2022-paper/Complex%20Query%20Answering%20with%20Neural%20Link%20Predictors%20%28Extended%20Abstract%29.pdf) | Pasquale Minervini; Erik Arakelyan; Daniel Daza; Michael Cochez |
| [Detect, Understand, Act: A Neuro-Symbolic Hierarchical Reinforcement Learning Framework (Extended Abstract)](ijcai-2022-paper/Detect%2C%20Understand%2C%20Act%20-%20A%20Neuro-Symbolic%20Hierarchical%20Reinforcement%20Learning%20Framework%20%28Extended%20Abstract%29.pdf) | Ludovico Mitchener; David Tuckey; Matthew Crosby; Alessandra Russo |
| [Decomposition Methods for Solving Scheduling Problem Using Answer Set Programming](ijcai-2022-paper/Decomposition%20Methods%20for%20Solving%20Scheduling%20Problem%20Using%20Answer%20Set%20Programming.pdf) | Mohammed M. S. El-Kholany |
| [Application of Neurosymbolic AI to Sequential Decision Making](ijcai-2022-paper/Application%20of%20Neurosymbolic%20AI%20to%20Sequential%20Decision%20Making.pdf) | Carlos Núñez-Molina |
| [A Model-Oriented Approach for Lifting Symmetry-Breaking Constraints in Answer Set Programming](ijcai-2022-paper/A%20Model-Oriented%20Approach%20for%20Lifting%20Symmetry-Breaking%20Constraints%20in%20Answer%20Set%20Programming.pdf) | Alice Tarzariol |
| [Interactive Reinforcement Learning for Symbolic Regression from Multi-Format Human-Preference Feedbacks](ijcai-2022-paper/Interactive%20Reinforcement%20Learning%20for%20Symbolic%20Regression%20from%20Multi-Format%20Human-Preference%20Feedbacks.pdf) | Laure Crochepierre; Lydia Boudjeloud-Assala; Vincent Barbesant |

#### IJCAI 2023

| Paper | Authors |
|---|---|
| [Sequential Recommendation with Probabilistic Logical Reasoning](ijcai-2023-paper/Sequential%20Recommendation%20with%20Probabilistic%20Logical%20Reasoning.pdf) | Huanhuan Yuan; Pengpeng Zhao; Xuefeng Xian; Guanfeng Liu; Yanchi Liu; Victor S. Sheng; Lei Zhao |
| [Treewidth-Aware Complexity for Evaluating Epistemic Logic Programs](ijcai-2023-paper/Treewidth-Aware%20Complexity%20for%20Evaluating%20Epistemic%20Logic%20Programs.pdf) | Jorge Fandinno; Markus Hecher |
| [Neuro-Symbolic Learning of Answer Set Programs from Raw Data](ijcai-2023-paper/Neuro-Symbolic%20Learning%20of%20Answer%20Set%20Programs%20from%20Raw%20Data.pdf) | Daniel Cunnington; Mark Law; Jorge Lobo; Alessandra Russo |
| [Scalable Coupling of Deep Learning with Logical Reasoning](ijcai-2023-paper/Scalable%20Coupling%20of%20Deep%20Learning%20with%20Logical%20Reasoning.pdf) | Marianne Defresne; Sophie Barbe; Thomas Schiex |
| [Neuro-Symbolic Class Expression Learning](ijcai-2023-paper/Neuro-Symbolic%20Class%20Expression%20Learning.pdf) | Caglar Demir; Axel-Cyrille Ngonga Ngomo |
| [A Logic-based Approach to Contrastive Explainability for Neurosymbolic Visual Question Answering](ijcai-2023-paper/A%20Logic-based%20Approach%20to%20Contrastive%20Explainability%20for%20Neurosymbolic%20Visual%20Question%20Answering.pdf) | Thomas Eiter; Tobias Geibinger; Nelson Higuera; Johannes Oetsch |
| [Enabling Abductive Learning to Exploit Knowledge Graph](ijcai-2023-paper/Enabling%20Abductive%20Learning%20to%20Exploit%20Knowledge%20Graph.pdf) | Yu-Xuan Huang; Zequn Sun; Guangyao Li; Xiaobin Tian; Wang-Zhou Dai; Wei Hu; Yuan Jiang; Zhi-Hua Zhou |
| [Probabilistic Rule Induction from Event Sequences with Logical Summary Markov Models](ijcai-2023-paper/Probabilistic%20Rule%20Induction%20from%20Event%20Sequences%20with%20Logical%20Summary%20Markov%20Models.pdf) | Debarun Bhattacharjya; Oktie Hassanzadeh; Ronny Luss; Keerthiram Murugesan |
| [Safe Reinforcement Learning via Probabilistic Logic Shields](ijcai-2023-paper/Safe%20Reinforcement%20Learning%20via%20Probabilistic%20Logic%20Shields.pdf) | Wen-Chi Yang; Giuseppe Marra; Gavin Rens; Luc De Raedt |
| [Towards Formal Verification of Neuro-symbolic Multi-agent Systems](ijcai-2023-paper/Towards%20Formal%20Verification%20of%20Neuro-symbolic%20Multi-agent%20Systems.pdf) | Panagiotis Kouvaros |
| [Reliable Neuro-Symbolic Abstractions for Planning and Learning](ijcai-2023-paper/Reliable%20Neuro-Symbolic%20Abstractions%20for%20Planning%20and%20Learning.pdf) | Naman Shah |

#### IJCAI 2024

| Paper | Authors |
|---|---|
| [Formal Verification of Parameterised Neural-symbolic Multi-agent Systems](ijcai-2024-paper/Formal%20Verification%20of%20Parameterised%20Neural-symbolic%20Multi-agent%20Systems.pdf) | Panagiotis Kouvaros; Elena Botoeva; Cosmo De Bonis-Campbell |
| [AMO-aware Aggregates in Answer Set Programming](ijcai-2024-paper/AMO-aware%20Aggregates%20in%20Answer%20Set%20Programming.pdf) | Mario Alviano; Carmine Dodaro; Salvatore Fiorentino; Marco Maratea |
| [Epistemic Logic Programs: Non-Ground and Counting Complexity](ijcai-2024-paper/Epistemic%20Logic%20Programs%20-%20Non-Ground%20and%20Counting%20Complexity.pdf) | Thomas Eiter; Johannes Klaus Fichte; Markus Hecher; Stefan Woltran |
| [Improved Encodings of Acyclicity for Translating Answer Set Programming into Integer Programming](ijcai-2024-paper/Improved%20Encodings%20of%20Acyclicity%20for%20Translating%20Answer%20Set%20Programming%20into%20Integer%20Programming.pdf) | Masood Feyzbakhsh Rankooh; Tomi Janhunen |
| [Learning Logic Programs by Discovering Higher-Order Abstractions](ijcai-2024-paper/Learning%20Logic%20Programs%20by%20Discovering%20Higher-Order%20Abstractions.pdf) | Céline Hocquette; Sebastijan Dumancic; Andrew Cropper |
| [NELLIE: A Neuro-Symbolic Inference Engine for Grounded, Compositional, and Explainable Reasoning](ijcai-2024-paper/NELLIE%20-%20A%20Neuro-Symbolic%20Inference%20Engine%20for%20Grounded%2C%20Compositional%2C%20and%20Explainable%20Reasoning.pdf) | Nathaniel Weir; Peter Clark; Benjamin Van Durme |
| [Scaling Up Unbiased Search-based Symbolic Regression](ijcai-2024-paper/Scaling%20Up%20Unbiased%20Search-based%20Symbolic%20Regression.pdf) | Paul Kahlmeyer; Joachim Giesen; Michael Habeck; Henrik Voigt |
| [Vertical Symbolic Regression via Deep Policy Gradient](ijcai-2024-paper/Vertical%20Symbolic%20Regression%20via%20Deep%20Policy%20Gradient.pdf) | Nan Jiang; Md. Nasim; Yexiang Xue |
| [Capturing (Optimal) Relaxed Plans with Stable and Supported Models of Logic Programs (Extended Abstract)](ijcai-2024-paper/Capturing%20%28Optimal%29%20Relaxed%20Plans%20with%20Stable%20and%20Supported%20Models%20of%20Logic%20Programs%20%28Extended%20Abstract%29.pdf) | Masood Feyzbakhsh Rankooh; Tomi Janhunen |
| [Hybrid planning for challenging construction problems: An Answer Set Programming approach (Abstract Reprint)](ijcai-2024-paper/Hybrid%20planning%20for%20challenging%20construction%20problems%20-%20An%20Answer%20Set%20Programming%20approach%20%28Abstract%20Reprint%29.pdf) | Faseeh Ahmad; Volkan Patoglu; Esra Erdem |
| [A differentiable first-order rule learner for inductive logic programming (Abstract Reprint)](ijcai-2024-paper/A%20differentiable%20first-order%20rule%20learner%20for%20inductive%20logic%20programming%20%28Abstract%20Reprint%29.pdf) | Kun Gao; Katsumi Inoue; Yongzhi Cao; Hanpin Wang |
| [NeuroSymbolic LLM for Mathematical Reasoning and Software Engineering](ijcai-2024-paper/NeuroSymbolic%20LLM%20for%20Mathematical%20Reasoning%20and%20Software%20Engineering.pdf) | Prithwish Jana |

#### IJCAI 2025

| Paper | Authors |
|---|---|
| [A Unifying Framework for Semiring-Based Constraint Logic Programming With Negation](ijcai-2025-paper/A%20Unifying%20Framework%20for%20Semiring-Based%20Constraint%20Logic%20Programming%20With%20Negation.pdf) | Jeroen Paul Spaans; Jesse Heyninck |
| [Integrating Answer Set Programming and Large Language Models for Enhanced Structured Representation of Complex Knowledge in Natural Language](ijcai-2025-paper/Integrating%20Answer%20Set%20Programming%20and%20Large%20Language%20Models%20for%20Enhanced%20Structured%20Representation%20of%20Complex%20Knowledge%20in%20Natural%20Language.pdf) | Mario Alviano; Lorenzo Grillo; Fabrizio Lo Scudo; Luis Angel Rodriguez Reiners |
| [Relational Decomposition for Program Synthesis](ijcai-2025-paper/Relational%20Decomposition%20for%20Program%20Synthesis.pdf) | Céline Hocquette; Andrew Cropper |
| [Approximation Fixpoint Theory as a Unifying Framework for Fuzzy Logic Programming Semantics](ijcai-2025-paper/Approximation%20Fixpoint%20Theory%20as%20a%20Unifying%20Framework%20for%20Fuzzy%20Logic%20Programming%20Semantics.pdf) | Pascal Kettmann; Jesse Heyninck; Hannes Strass |
| [Instantiation-based Formalization of Logical Reasoning Tasks Using Language Models and Logical Solvers](ijcai-2025-paper/Instantiation-based%20Formalization%20of%20Logical%20Reasoning%20Tasks%20Using%20Language%20Models%20and%20Logical%20Solvers.pdf) | Mohammad Raza; Natasa Milic-Frayling |
| [Witnesses for Answer Sets of Basic Logic Programs](ijcai-2025-paper/Witnesses%20for%20Answer%20Sets%20of%20Basic%20Logic%20Programs.pdf) | Yisong Wang; Xianglong Wang; Zhongtao Xie; Thomas Eiter |
| [Grounding Methods for Neural-Symbolic AI](ijcai-2025-paper/Grounding%20Methods%20for%20Neural-Symbolic%20AI.pdf) | Rodrigo Castellano Ontiveros; Francesco Giannini; Marco Gori; Giuseppe Marra; Michelangelo Diligenti |
| [A Neuro-Symbolic Framework for Sequence Classification with Relational and Temporal Knowledge](ijcai-2025-paper/A%20Neuro-Symbolic%20Framework%20for%20Sequence%20Classification%20with%20Relational%20and%20Temporal%20Knowledge.pdf) | Luca Salvatore Lorello; Marco Lippi; Stefano Melacci |
| [NeSyA: Neurosymbolic Automata](ijcai-2025-paper/NeSyA%20-%20Neurosymbolic%20Automata.pdf) | Nikolaos Manginas; George Paliouras; Luc De Raedt |
| [Breaking the Self-Evaluation Barrier: Reinforced Neuro-Symbolic Planning with Large Language Models](ijcai-2025-paper/Breaking%20the%20Self-Evaluation%20Barrier%20-%20Reinforced%20Neuro-Symbolic%20Planning%20with%20Large%20Language%20Models.pdf) | Jie-Jing Shao; Hong-Jie You; Guohao Cai; Quanyu Dai; Zhenhua Dong; Lan-Zhe Guo |
| [Curriculum Abductive Learning for Mitigating Reasoning Shortcuts](ijcai-2025-paper/Curriculum%20Abductive%20Learning%20for%20Mitigating%20Reasoning%20Shortcuts.pdf) | Wen-Da Wei; Xiao-Wen Yang; Jie-Jing Shao; Lan-Zhe Guo |
| [Most Probable Explanation in Probabilistic Answer Set Programming](ijcai-2025-paper/Most%20Probable%20Explanation%20in%20Probabilistic%20Answer%20Set%20Programming.pdf) | Damiano Azzolini; Giuseppe Mazzotta; Francesco Ricca; Fabrizio Riguzzi |
| [NSF-MAP: Neurosymbolic Multimodal Fusion for Robust and Interpretable Anomaly Prediction in Assembly Pipelines](ijcai-2025-paper/NSF-MAP%20-%20Neurosymbolic%20Multimodal%20Fusion%20for%20Robust%20and%20Interpretable%20Anomaly%20Prediction%20in%20Assembly%20Pipelines.pdf) | Chathurangi Shyalika; Renjith Prasad; Fadi El Kalach; Revathy Venkataramanan; Ramtin Zand; Ramy F. Harik; Amit P. Sheth |
| [Integrating Neurosymbolic AI in Advanced Air Mobility: A Comprehensive Survey](ijcai-2025-paper/Integrating%20Neurosymbolic%20AI%20in%20Advanced%20Air%20Mobility%20-%20A%20Comprehensive%20Survey.pdf) | Kamal Acharya; Iman Sharifi; Mehul Lad; Liang Sun; Houbing Song |
| [Empowering LLMs with Logical Reasoning: A Comprehensive Survey](ijcai-2025-paper/Empowering%20LLMs%20with%20Logical%20Reasoning%20-%20A%20Comprehensive%20Survey.pdf) | Fengxiang Cheng; Haoxuan Li; Fenrong Liu; Robert van Rooij; Kun Zhang; Zhouchen Lin |
| [Neuro-Symbolic Artificial Intelligence: A Task-Directed Survey in the Black-Box Models Era](ijcai-2025-paper/Neuro-Symbolic%20Artificial%20Intelligence%20-%20A%20Task-Directed%20Survey%20in%20the%20Black-Box%20Models%20Era.pdf) | Giovanni Pio Delvecchio; Lorenzo Molfetta; Gianluca Moro |
| [Neuro-Symbolic Artificial Intelligence: Towards Improving the Reasoning Abilities of Large Language Models](ijcai-2025-paper/Neuro-Symbolic%20Artificial%20Intelligence%20-%20Towards%20Improving%20the%20Reasoning%20Abilities%20of%20Large%20Language%20Models.pdf) | Xiao-Wen Yang; Jie-Jing Shao; Lan-Zhe Guo; Bo-Wen Zhang; Zhi Zhou; Lin-Han Jia; Wang-Zhou Dai; Yufeng Li |
| [Efficient Rectification of Neuro-Symbolic Reasoning Inconsistencies by Abductive Reflection (Extended Abstract)](ijcai-2025-paper/Efficient%20Rectification%20of%20Neuro-Symbolic%20Reasoning%20Inconsistencies%20by%20Abductive%20Reflection%20%28Extended%20Abstract%29.pdf) | Wen-Chao Hu; Wang-Zhou Dai; Yuan Jiang; Zhi-Hua Zhou |
| [A Semantic Framework for Neurosymbolic Computation (Abstract Reprint)](ijcai-2025-paper/A%20Semantic%20Framework%20for%20Neurosymbolic%20Computation%20%28Abstract%20Reprint%29.pdf) | Simon Odense; Artur S. d'Avila Garcez |
| [A Semantic Framework for Neurosymbolic Computation (Abstract Reprint)](ijcai-2025-paper/A%20Semantic%20Framework%20for%20Neurosymbolic%20Computation%20%28Abstract%20Reprint%29.pdf) | Simon Odense; Artur S. d'Avila Garcez |
| [Enhancing the Logical Reasoning Abilities of Large Language Models](ijcai-2025-paper/Enhancing%20the%20Logical%20Reasoning%20Abilities%20of%20Large%20Language%20Models.pdf) | Fengxiang Cheng |

### JMLR

> Searched [JMLR](https://jmlr.org/papers/) volumes 21–27 (2020–2026) for neurosymbolic-AI-related titles. **No qualifying papers were found** — this niche is published almost exclusively at conferences (ICML/NeurIPS/AAAI/IJCAI/ICLR) rather than in JMLR, which skews toward learning theory and methodology.


### TMLR

> Sourced via [dblp](https://dblp.org/db/journals/tmlr/) (TMLR is a rolling-review journal that started in 2022, hosted on OpenReview). OpenReview blocks automated PDF downloads (Cloudflare bot-challenge), so PDFs here are the authors' own arXiv preprints where one exists; papers without a matching arXiv preprint are listed with an OpenReview link only.


#### TMLR 2022

| Paper | Authors |
|---|---|
| [Unsupervised Learning of Neurosymbolic Encoders](tmlr-2022-paper/Unsupervised%20Learning%20of%20Neurosymbolic%20Encoders.pdf) | Eric Zhan; Jennifer J. Sun; Ann Kennedy; Yisong Yue; Swarat Chaudhuri |
| [Symbolic Regression is NP-hard](tmlr-2022-paper/Symbolic%20Regression%20is%20NP-hard.pdf) | Marco Virgolin; Solon P. Pissis |

#### TMLR 2023

| Paper | Authors |
|---|---|
| [GSR: A Generalized Symbolic Regression Approach](tmlr-2023-paper/GSR%20-%20A%20Generalized%20Symbolic%20Regression%20Approach.pdf) | Tony Tohme; Dehong Liu; Kamal Youcef-Toumi |
| [Sequential Query Encoding for Complex Query Answering on Knowledge Graphs](tmlr-2023-paper/Sequential%20Query%20Encoding%20for%20Complex%20Query%20Answering%20on%20Knowledge%20Graphs.pdf) | Jiaxin Bai; Tianshi Zheng; Yangqiu Song |
| [Differentiable Logic Machines](tmlr-2023-paper/Differentiable%20Logic%20Machines.pdf) | Matthieu Zimmer; Xuening Feng; Claire Glanois; Zhaohui Jiang; Jianyi Zhang; Paul Weng; Dong Li; Jianye Hao; Wulong Liu |

#### TMLR 2025

| Paper | Authors |
|---|---|
| [Robust Symbolic Regression for Dynamical System Identification](https://openreview.net/forum?id=ZfPbCFZQbx) | Ramzi Dakhmouche; Ivan Lunati; M. Hossein Gorji |
| [LeanProgress: Guiding Search for Neural Theorem Proving via Proof Progress Prediction](tmlr-2025-paper/LeanProgress%20-%20Guiding%20Search%20for%20Neural%20Theorem%20Proving%20via%20Proof%20Progress%20Prediction.pdf) | Robert Joseph George; Suozhi Huang; Peiyang Song; Anima Anandkumar |

#### TMLR 2026

| Paper | Authors |
|---|---|
| [Concept Flow Models: Anchoring Concept-Based Reasoning with Hierarchical Bottlenecks](tmlr-2026-paper/Concept%20Flow%20Models%20-%20Anchoring%20Concept-Based%20Reasoning%20with%20Hierarchical%20Bottlenecks.pdf) | Ya Wang; Adrian Paschke |
| [Don't Let It Hallucinate: Premise Verification via Retrieval-Augmented Logical Reasoning](tmlr-2026-paper/Don%27t%20Let%20It%20Hallucinate%20-%20Premise%20Verification%20via%20Retrieval-Augmented%20Logical%20Reasoning.pdf) | Yuehan Qin; Li Li; Yi Nian; Xinyan Velocity Yu; Yue Zhao; Xuezhe Ma |
| [Counting Still Counts: Understanding Neural Complex Query Answering Through Query Relaxation](tmlr-2026-paper/Counting%20Still%20Counts%20-%20Understanding%20Neural%20Complex%20Query%20Answering%20Through%20Query%20Relaxation.pdf) | Yannick Brunink; Daniel Daza; Yunjie He; Michael Cochez |
| [Semantic-Drive: Trustworthy and Efficient Long-Tail Data Curation via Open-Vocabulary Grounding and Neuro-Symbolic VLM Consensus](https://openreview.net/forum?id=qN2oN36L3k) | Antonio Guillen-Perez |
| [Automaton Distillation: Neuro-Symbolic Transfer Learning for Deep Reinforcement Learning](tmlr-2026-paper/Automaton%20Distillation%20-%20Neuro-Symbolic%20Transfer%20Learning%20for%20Deep%20Reinforcement%20Learning.pdf) | Precious Nwaorgu; Suraj Singireddy; Andre Beckus; Aden McKinney; Mahyar Alinejad; Chinwendu Enyioha; Sumit Kumar Jha; Alvaro Velasquez; George K. Atia |
| [Can VLMs Reason Robustly? A Neuro-Symbolic Investigation](tmlr-2026-paper/Can%20VLMs%20Reason%20Robustly%3F%20A%20Neuro-Symbolic%20Investigation.pdf) | Weixin Chen; Antonio Vergari; Han Zhao |
| [Towards Overcoming Reasoning Shortcuts in Neurosymbolic Learning via Efficient Generative Proxies](https://openreview.net/forum?id=Sl2aC9hiaN) | Panagiotis Lymperopoulos; Liping Liu |

### ICLR

> Sourced via [dblp](https://dblp.org/db/conf/iclr/) (2020–2025); dblp had not indexed ICLR 2026 yet at the time of writing, so 2026 uses an arXiv search for preprints explicitly marked "ICLR 2026" (main track only). ICLR papers are hosted on OpenReview, which blocks automated PDF downloads (Cloudflare bot-challenge) — PDFs here are the authors' arXiv preprints where available; the rest are listed with an OpenReview forum link only.


#### ICLR 2020

| Paper | Authors |
|---|---|
| [ReClor: A Reading Comprehension Dataset Requiring Logical Reasoning](iclr-2020-paper/ReClor%20-%20A%20Reading%20Comprehension%20Dataset%20Requiring%20Logical%20Reasoning.pdf) | Weihao Yu; Zihang Jiang; Yanfei Dong; Jiashi Feng |
| [Guiding Program Synthesis by Learning to Generate Examples](https://openreview.net/forum?id=BJl07ySKvS) | Larissa Laich; Pavol Bielik; Martin T. Vechev |
| [Efficient Probabilistic Logic Reasoning with Graph Neural Networks](iclr-2020-paper/Efficient%20Probabilistic%20Logic%20Reasoning%20with%20Graph%20Neural%20Networks.pdf) | Yuyu Zhang; Xinshi Chen; Yuan Yang; Arun Ramamurthy; Bo Li; Yuan Qi; Le Song |
| [Neural Symbolic Reader: Scalable Integration of Distributed and Symbolic Representations for Reading Comprehension](https://openreview.net/forum?id=ryxjnREFwH) | Xinyun Chen; Chen Liang; Adams Wei Yu; Denny Zhou; Dawn Song; Quoc V. Le |
| [Differentiable Reasoning over a Virtual Knowledge Base](iclr-2020-paper/Differentiable%20Reasoning%20over%20a%20Virtual%20Knowledge%20Base.pdf) | Bhuwan Dhingra; Manzil Zaheer; Vidhisha Balachandran; Graham Neubig; Ruslan Salakhutdinov; William W. Cohen |

#### ICLR 2021

| Paper | Authors |
|---|---|
| [Deep symbolic regression: Recovering mathematical expressions from data via risk-seeking policy gradients](iclr-2021-paper/Deep%20symbolic%20regression%20-%20Recovering%20mathematical%20expressions%20from%20data%20via%20risk-seeking%20policy%20gradients.pdf) | Brenden K. Petersen; Mikel Landajuela; T. Nathan Mundhenk; Cláudio Prata Santiago; Sookyung Kim; Joanne Taery Kim |
| [Complex Query Answering with Neural Link Predictors](iclr-2021-paper/Complex%20Query%20Answering%20with%20Neural%20Link%20Predictors.pdf) | Erik Arakelyan; Daniel Daza; Pasquale Minervini; Michael Cochez |
| [BUSTLE: Bottom-Up Program Synthesis Through Learning-Guided Exploration](iclr-2021-paper/BUSTLE%20-%20Bottom-Up%20Program%20Synthesis%20Through%20Learning-Guided%20Exploration.pdf) | Augustus Odena; Kensen Shi; David Bieber; Rishabh Singh; Charles Sutton; Hanjun Dai |
| [Learning Task-General Representations with Generative Neuro-Symbolic Modeling](iclr-2021-paper/Learning%20Task-General%20Representations%20with%20Generative%20Neuro-Symbolic%20Modeling.pdf) | Reuben Feinman; Brenden M. Lake |

#### ICLR 2022

| Paper | Authors |
|---|---|
| [CrossBeam: Learning to Search in Bottom-Up Program Synthesis](iclr-2022-paper/CrossBeam%20-%20Learning%20to%20Search%20in%20Bottom-Up%20Program%20Synthesis.pdf) | Kensen Shi; Hanjun Dai; Kevin Ellis; Charles Sutton |
| [Neural Methods for Logical Reasoning over Knowledge Graphs](iclr-2022-paper/Neural%20Methods%20for%20Logical%20Reasoning%20over%20Knowledge%20Graphs.pdf) | Alfonso Amayuelas; Shuai Zhang; Susie Xi Rao; Ce Zhang |
| [Neural Program Synthesis with Query](iclr-2022-paper/Neural%20Program%20Synthesis%20with%20Query.pdf) | Di Huang; Rui Zhang; Xing Hu; Xishan Zhang; Pengwei Jin; Nan Li; Zidong Du; Qi Guo; Yunji Chen |
| [Explaining Point Processes by Learning Interpretable Temporal Logic Rules](https://openreview.net/forum?id=P07dq7iSAGr) | Shuang Li; Mingquan Feng; Lu Wang; Abdelmajid Essofi; Yufeng Cao; Junchi Yan; Le Song |
| [Safe Neurosymbolic Learning with Differentiable Symbolic Execution](iclr-2022-paper/Safe%20Neurosymbolic%20Learning%20with%20Differentiable%20Symbolic%20Execution.pdf) | Chenxi Yang; Swarat Chaudhuri |

#### ICLR 2023

| Paper | Authors |
|---|---|
| [Learning where and when to reason in neuro-symbolic inference](https://openreview.net/forum?id=en9V5F8PR-) | Cristina Cornelio; Jan Stuehmer; Shell Xu Hu; Timothy M. Hospedales |
| [Selection-Inference: Exploiting Large Language Models for Interpretable Logical Reasoning](iclr-2023-paper/Selection-Inference%20-%20Exploiting%20Large%20Language%20Models%20for%20Interpretable%20Logical%20Reasoning.pdf) | Antonia Creswell; Murray Shanahan; Irina Higgins |
| [CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis](iclr-2023-paper/CodeGen%20-%20An%20Open%20Large%20Language%20Model%20for%20Code%20with%20Multi-Turn%20Program%20Synthesis.pdf) | Erik Nijkamp; Bo Pang; Hiroaki Hayashi; Lifu Tu; Huan Wang; Yingbo Zhou; Silvio Savarese; Caiming Xiong |
| [Neuro-Symbolic Procedural Planning with Commonsense Prompting](iclr-2023-paper/Neuro-Symbolic%20Procedural%20Planning%20with%20Commonsense%20Prompting.pdf) | Yujie Lu; Weixi Feng; Wanrong Zhu; Wenda Xu; Xin Eric Wang; Miguel P. Eckstein; William Yang Wang |
| [Softened Symbol Grounding for Neuro-symbolic Systems](iclr-2023-paper/Softened%20Symbol%20Grounding%20for%20Neuro-symbolic%20Systems.pdf) | Zenan Li; Yuan Yao; Taolue Chen; Jingwei Xu; Chun Cao; Xiaoxing Ma; Jian Lü |
| [Transformer-based model for symbolic regression via joint supervised learning](https://openreview.net/forum?id=ULzyv9M1j5) | Wenqiang Li; Weijun Li; Linjun Sun; Min Wu; Lina Yu; Jingyi Liu; Yanjie Li; Songsong Tian |
| Rethinking Symbolic Regression: Morphology and Adaptability in the Context of Evolutionary Algorithms | Kei Sen Fong; Shelvia Wongso; Mehul Motani |
| LogicDP: Creating Labels for Graph Data via Inductive Logic Programming | Yuan Yang; Faramarz Fekri; James Clayton Kerce; Ali Payani |
| [Weakly Supervised Knowledge Transfer with Probabilistic Logical Reasoning for Object Detection](iclr-2023-paper/Weakly%20Supervised%20Knowledge%20Transfer%20with%20Probabilistic%20Logical%20Reasoning%20for%20Object%20Detection.pdf) | Martijn Oldenhof; Adam Arany; Yves Moreau; Edward De Brouwer |
| [Deep Generative Symbolic Regression](iclr-2023-paper/Deep%20Generative%20Symbolic%20Regression.pdf) | Samuel Holt; Zhaozhi Qian; Mihaela van der Schaar |
| [Multimodal Analogical Reasoning over Knowledge Graphs](iclr-2023-paper/Multimodal%20Analogical%20Reasoning%20over%20Knowledge%20Graphs.pdf) | Ningyu Zhang; Lei Li; Xiang Chen; Xiaozhuan Liang; Shumin Deng; Huajun Chen |

#### ICLR 2024

| Paper | Authors |
|---|---|
| [ExeDec: Execution Decomposition for Compositional Generalization in Neural Program Synthesis](iclr-2024-paper/ExeDec%20-%20Execution%20Decomposition%20for%20Compositional%20Generalization%20in%20Neural%20Program%20Synthesis.pdf) | Kensen Shi; Joey Hong; Yinlin Deng; Pengcheng Yin; Manzil Zaheer; Charles Sutton |
| [LEGO-Prover: Neural Theorem Proving with Growing Libraries](iclr-2024-paper/LEGO-Prover%20-%20Neural%20Theorem%20Proving%20with%20Growing%20Libraries.pdf) | Haiming Wang; Huajian Xin; Chuanyang Zheng; Zhengying Liu; Qingxing Cao; Yinya Huang; Jing Xiong; Han Shi; Enze Xie; Jian Yin; Zhenguo Li; Xiaodan Liang |
| [A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis](iclr-2024-paper/A%20Real-World%20WebAgent%20with%20Planning%2C%20Long%20Context%20Understanding%2C%20and%20Program%20Synthesis.pdf) | Izzeddin Gur; Hiroki Furuta; Austin V. Huang; Mustafa Safdari; Yutaka Matsuo; Douglas Eck; Aleksandra Faust |
| [ODEFormer: Symbolic Regression of Dynamical Systems with Transformers](iclr-2024-paper/ODEFormer%20-%20Symbolic%20Regression%20of%20Dynamical%20Systems%20with%20Transformers.pdf) | Stéphane d'Ascoli; Sören Becker; Philippe Schwaller; Alexander Mathis; Niki Kilbertus |
| [B-Coder: Value-Based Deep Reinforcement Learning for Program Synthesis](iclr-2024-paper/B-Coder%20-%20Value-Based%20Deep%20Reinforcement%20Learning%20for%20Program%20Synthesis.pdf) | Zishun Yu; Yunzhe Tao; Liyu Chen; Tao Sun; Hongxia Yang |
| [Neural-Symbolic Recursive Machine for Systematic Generalization](iclr-2024-paper/Neural-Symbolic%20Recursive%20Machine%20for%20Systematic%20Generalization.pdf) | Qing Li; Yixin Zhu; Yitao Liang; Ying Nian Wu; Song-Chun Zhu; Siyuan Huang |
| [GENOME: Generative Neuro-Symbolic Visual Reasoning by Growing and Reusing Modules](iclr-2024-paper/GENOME%20-%20Generative%20Neuro-Symbolic%20Visual%20Reasoning%20by%20Growing%20and%20Reusing%20Modules.pdf) | Zhenfang Chen; Rui Sun; Wenjun Liu; Yining Hong; Chuang Gan |
| [LogicMP: A Neuro-symbolic Approach for Encoding First-order Logic Constraints](iclr-2024-paper/LogicMP%20-%20A%20Neuro-symbolic%20Approach%20for%20Encoding%20First-order%20Logic%20Constraints.pdf) | Weidi Xu; Jingwei Wang; Lele Xie; Jianshan He; Hongting Zhou; Taifeng Wang; Xiaopei Wan; Jingdong Chen; Chao Qu; Wei Chu |
| [Neurosymbolic Grounding for Compositional World Models](iclr-2024-paper/Neurosymbolic%20Grounding%20for%20Compositional%20World%20Models.pdf) | Atharva Sehgal; Arya Grayeli; Jennifer J. Sun; Swarat Chaudhuri |
| [Reinforcement Symbolic Regression Machine](iclr-2024-paper/Reinforcement%20Symbolic%20Regression%20Machine.pdf) | Yilong Xu; Yang Liu; Hao Sun |

#### ICLR 2025

| Paper | Authors |
|---|---|
| [miniCTX: Neural Theorem Proving with (Long-)Contexts](iclr-2025-paper/miniCTX%20-%20Neural%20Theorem%20Proving%20with%20%28Long-%29Contexts.pdf) | Jiewen Hu; Thomas Zhu; Sean Welleck |
| [R2-Guard: Robust Reasoning Enabled LLM Guardrail via Knowledge-Enhanced Logical Reasoning](https://openreview.net/forum?id=CkgKSqZbuC) | Mintong Kang; Bo Li |
| [VisualPredicator: Learning Abstract World Models with Neuro-Symbolic Predicates for Robot Planning](iclr-2025-paper/VisualPredicator%20-%20Learning%20Abstract%20World%20Models%20with%20Neuro-Symbolic%20Predicates%20for%20Robot%20Planning.pdf) | Yichao Liang; Nishanth Kumar; Hao Tang; Adrian Weller; Joshua B. Tenenbaum; Tom Silver; João F. Henriques; Kevin Ellis |
| [RAG-SR: Retrieval-Augmented Generation for Neural Symbolic Regression](https://openreview.net/forum?id=NdHka08uWn) | Hengzhe Zhang; Qi Chen; Bing Xue; Wolfgang Banzhaf; Mengjie Zhang |
| [Diffusion On Syntax Trees For Program Synthesis](iclr-2025-paper/Diffusion%20On%20Syntax%20Trees%20For%20Program%20Synthesis.pdf) | Shreyas Kapur; Erik Jenner; Stuart Russell |
| [NeSyC: A Neuro-symbolic Continual Learner For Complex Embodied Tasks in Open Domains](iclr-2025-paper/NeSyC%20-%20A%20Neuro-symbolic%20Continual%20Learner%20For%20Complex%20Embodied%20Tasks%20in%20Open%20Domains.pdf) | Wonje Choi; Jinwoo Park; Sanghyun Ahn; Daehee Lee; Honguk Woo |
| [Logically Consistent Language Models via Neuro-Symbolic Integration](iclr-2025-paper/Logically%20Consistent%20Language%20Models%20via%20Neuro-Symbolic%20Integration.pdf) | Diego Calanzone; Stefano Teso; Antonio Vergari |
| [CARTS: Advancing Neural Theorem Proving with Diversified Tactic Calibration and Bias-Resistant Tree Search](https://openreview.net/forum?id=VQwI055flA) | Xiao-Wen Yang; Zhi Zhou; Haiming Wang; Aoxue Li; Wen-Da Wei; Hui Jin; Zhenguo Li; Yu-Feng Li |
| [GeoILP: A Synthetic Dataset to Guide Large-Scale Rule Induction](https://openreview.net/forum?id=cfGpIcOIa5) | Si Chen; Richong Zhang; Xu Zhang |
| ParFam - (Neural Guided) Symbolic Regression via Continuous Global Optimization | Philipp Scholl; Katharina Bieker; Hillary Hauger; Gitta Kutyniok |
| [Divide and Translate: Compositional First-Order Logic Translation and Verification for Complex Logical Reasoning](iclr-2025-paper/Divide%20and%20Translate%20-%20Compositional%20First-Order%20Logic%20Translation%20and%20Verification%20for%20Complex%20Logical%20Reasoning.pdf) | Hyun Ryu; Gyeongman Kim; Hyemin S. Lee; Eunho Yang |
| INFER: A Neural-symbolic Model For Extrapolation Reasoning on Temporal Knowledge Graph | Ningyuan Li; Haihong E; Tianyu Yao; Tianyi Hu; Yuhan Li; Haoran Luo; Meina Song; Yifan Zhu |
| [KinFormer: Generalizable Dynamical Symbolic Regression for Catalytic Organic Reaction Kinetics](https://openreview.net/forum?id=nhrXqy5d5q) | Jindou Chen; Jidong Tian; Liang Wu; ChenXinWei; Xiaokang Yang; Yaohui Jin; Yanyan Xu |
| [Symbolic regression via MDLformer-guided search: from minimizing prediction error to minimizing description length](iclr-2025-paper/Symbolic%20regression%20via%20MDLformer-guided%20search%20-%20from%20minimizing%20prediction%20error%20to%20minimizing%20description%20length.pdf) | Zihan Yu; Jingtao Ding; Yong Li; Depeng Jin |
| [KLay: Accelerating Arithmetic Circuits for Neurosymbolic AI](iclr-2025-paper/KLay%20-%20Accelerating%20Arithmetic%20Circuits%20for%20Neurosymbolic%20AI.pdf) | Jaron Maene; Vincent Derkinderen; Pedro Zuidberg Dos Martires |
| [LASER: A Neuro-Symbolic Framework for Learning Spatio-Temporal Scene Graphs with Weak Supervision](https://openreview.net/forum?id=HEXtydywnE) | Jiani Huang; Ziyang Li; Mayur Naik; Ser-Nam Lim |
| [Differentiable Rule Induction from Raw Sequence Inputs](iclr-2025-paper/Differentiable%20Rule%20Induction%20from%20Raw%20Sequence%20Inputs.pdf) | Kun Gao; Katsumi Inoue; Yongzhi Cao; Hanpin Wang; Yang Feng |
| [Large Language Models Meet Symbolic Provers for Logical Reasoning Evaluation](iclr-2025-paper/Large%20Language%20Models%20Meet%20Symbolic%20Provers%20for%20Logical%20Reasoning%20Evaluation.pdf) | Chengwen Qi; Ren Ma; Bowen Li; He Du; Binyuan Hui; Jinwang Wu; Yuanjun Laili; Conghui He |

#### ICLR 2026

| Paper | Authors |
|---|---|
| [Neuro-Symbolic Decoding of Neural Activity](iclr-2026-paper/Neuro-Symbolic%20Decoding%20of%20Neural%20Activity.pdf) | Yanchen Wang; Joy Hsu; Ehsan Adeli; Jiajun Wu |
| [MultiMat - Multimodal Program Synthesis for Procedural Materials using Large Multimodal Models](iclr-2026-paper/MultiMat%20-%20Multimodal%20Program%20Synthesis%20for%20Procedural%20Materials%20using%20Large%20Multimodal%20Models.pdf) | Jonas Belouadi; Tamy Boubekeur; Adrien Kaiser |
| [EGG-SR - Embedding Symbolic Equivalence into Symbolic Regression via Equality Graph](iclr-2026-paper/EGG-SR%20-%20Embedding%20Symbolic%20Equivalence%20into%20Symbolic%20Regression%20via%20Equality%20Graph.pdf) | Nan Jiang; Ziyi Wang; Yexiang Xue |

### TPAMI

> IEEE TPAMI is **paywalled** (not open-access). Sourced via [dblp](https://dblp.org/db/journals/pami/); PDFs are included only where a free arXiv preprint exists (1 of 6). The rest are listed with title/authors/DOI only — see each DOI link for access via your institution.


#### TPAMI 2023

| Paper | Authors | DOI |
|---|---|---|
| DeepLogic: Joint Learning of Neural Perception and Logical Reasoning | Xuguang Duan; Xin Wang; Peilin Zhao; Guangyao Shen; Wenwu Zhu | [10.1109/TPAMI.2022.3191093](https://doi.org/10.1109/TPAMI.2022.3191093) |
| Differentiable Logic Policy for Interpretable Deep Reinforcement Learning: A Study From an Optimization Perspective | Xin Li; Haojie Lei; Li Zhang; Mingzhong Wang | [10.1109/TPAMI.2023.3285634](https://doi.org/10.1109/TPAMI.2023.3285634) |
| [Discourse-Aware Graph Networks for Textual Logical Reasoning](tpami-2023-paper/Discourse-Aware%20Graph%20Networks%20for%20Textual%20Logical%20Reasoning.pdf) | Yinya Huang; Lemao Liu; Kun Xu; Meng Fang; Liang Lin; Xiaodan Liang | [10.1109/TPAMI.2023.3280178](https://doi.org/10.1109/TPAMI.2023.3280178) |

#### TPAMI 2024

| Paper | Authors | DOI |
|---|---|---|
| Integrating Neural-Symbolic Reasoning With Variational Causal Inference Network for Explanatory Visual Question Answering | Dizhan Xue; Shengsheng Qian; Changsheng Xu | [10.1109/TPAMI.2024.3398012](https://doi.org/10.1109/TPAMI.2024.3398012) |

#### TPAMI 2025

| Paper | Authors | DOI |
|---|---|---|
| Towards Data-And Knowledge-Driven AI: A Survey on Neuro-Symbolic Computing | Wenguan Wang; Yi Yang; Fei Wu | [10.1109/TPAMI.2024.3483273](https://doi.org/10.1109/TPAMI.2024.3483273) |

#### TPAMI 2026

| Paper | Authors | DOI |
|---|---|---|
| Unveiling Fine-Grained Deceptive Patterns in Multimodal Fake News: An Explainable Neuro-Symbolic Framework With LVLMs | Dongxiao He; Yiqi Dong; Xiaobao Wang; Meng Ge; Carl Yang; Di Jin; Witold Pedrycz | [10.1109/TPAMI.2025.3642831](https://doi.org/10.1109/TPAMI.2025.3642831) |

## Notes

- Summaries in the ICML section are condensed from each paper's own abstract; other venues list title + authors only (writing per-paper summaries for ~330 additional papers was out of scope for this pass).
- These PDFs are the authors' published works, included here for personal research/reference use — see each paper for its original copyright and license terms.
- This collection was assembled via automated scraping of public proceedings/index sites plus manual keyword curation; it aims to be thorough but is very unlikely to be 100% exhaustive. If you spot a missing or miscategorized paper, feel free to add it.
