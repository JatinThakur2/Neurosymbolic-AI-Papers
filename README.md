# Neurosymbolic AI — ICML Paper Collection

A curated collection of papers on **neurosymbolic AI** accepted at ICML (2021–2025), organized by year. Neurosymbolic AI combines neural network–based learning with symbolic reasoning (logic, rules, programs) to build systems that are more interpretable, data-efficient, and capable of structured reasoning than pure deep learning approaches.

## Structure

```
ICML/
├── 2021/
├── 2022/
├── 2023/
├── 2024/
├── 2025/
└── README.md
```

Each folder contains the original PDFs for papers published in that year's ICML proceedings.

## Papers by Year

### 2021

| Paper | Authors | Summary |
|---|---|---|
| [A large-scale benchmark for few-shot program induction and synthesis](2021/A%20large-scale%20benchmark%20for%20few-shot%20program%20induction%20and%20synthesis.pdf) | Alet, Lopez-Contreras, Koppel, Nye, Solar-Lezama, Lozano-Pérez, Kaelbling, Tenenbaum | Introduces P3 (ProgRes), a large-scale few-shot program-induction benchmark built by mining subprograms and their I/O tests from real programs, and analyzes transformer-based synthesis methods on it. |
| [An Integer Linear Programming Framework for Mining Constraints from Data](2021/An%20Integer%20Linear%20Programming%20Framework%20for%20Mining%20Constraints%20from%20Data.pdf) | Meng, Chang | Proposes an ILP-based framework to automatically mine logical constraints over structured-output label spaces from data, instead of relying on hand-crafted rules, validated on Sudoku and spanning-tree tasks. |
| [Discovering symbolic policies with deep reinforcement learning](2021/Discovering%20symbolic%20policies%20with%20deep%20reinforcement%20learning.pdf) | Landajuela, Petersen, Kim, Santiago, Glatt, Mundhenk, Pettit, Faissol | Presents "deep symbolic policy," which uses an autoregressive RNN with risk-seeking policy gradients to directly search for compact, interpretable symbolic-expression control policies that outperform state-of-the-art DRL. |
| [Leveraging Language to Learn Program Abstractions and Search Heuristics](2021/Leveraging%20Language%20to%20Learn%20Program%20Abstractions%20and%20Search%20Heuristics.pdf) | Wong, Ellis, Tenenbaum, Andreas | Introduces LAPS, which uses natural-language annotations to jointly learn reusable program libraries and neurally-guided search heuristics for program synthesis, integrated into DreamCoder. |

### 2022

| Paper | Authors | Summary |
|---|---|---|
| [Neuro-Symbolic Hierarchical Rule Induction](2022/Neuro-Symbolic%20Hierarchical%20Rule%20Induction.pdf) | Glanois, Jiang, Feng, Weng, Zimmer, Li, Liu, Hao | Proposes HRI, an interpretable neuro-symbolic model for Inductive Logic Programming that learns first-order rules via embeddings matched against a hierarchy of pre-defined meta-rules, trainable via supervised or reinforcement learning. |

### 2023

| Paper | Authors | Summary |
|---|---|---|
| [Interpretable Neural-Symbolic Concept Reasoning](2023/Interpretable%20Neural-Symbolic%20Concept%20Reasoning.pdf) | Barbiero, Ciravegna, Giannini, Espinosa Zarlenga, Magister, Tonda, Lió, Precioso, Jamnik, Marra | Introduces the Deep Concept Reasoner (DCR), which builds differentiable syntactic rule structures over concept embeddings so predictions are fully interpretable while retaining the accuracy benefits of embeddings. |
| [Neuro-Symbolic Continual Learning](2023/Neuro-Symbolic%20Continual%20Learning.pdf) | Marconato, Bontempo, Ficarra, Calderara, Passerini, Teso | Defines Neuro-Symbolic Continual Learning (NeSy-CL), shows that combining NeSy architectures with continual learning avoids catastrophic forgetting but induces "reasoning shortcuts," and proposes COOL, a concept-level rehearsal strategy to address this. |

### 2024

| Paper | Authors | Summary |
|---|---|---|
| [Analysis for Abductive Learning and Neural-Symbolic Reasoning Shortcuts](2024/Analysis%20for%20Abductive%20Learning%20and%20Neural-Symbolic%20Reasoning%20Shortcuts.pdf) | Yang, Wei, Shao, Li, Zhou | Provides a theoretical analysis quantifying how knowledge-base complexity, sample size, and hypothesis space drive "reasoning shortcuts" in abductive/neuro-symbolic learning, and shows abductive learning can mitigate them via distance-function choice. |
| [Convex and Bilevel Optimization for Neural-Symbolic Inference and Learning](2024/Convex%20and%20Bilevel%20Optimization%20for%20Neural-Symbolic%20Inference%20and%20Learning.pdf) | Dickens, Gao, Pryor, Wright, Getoor | Develops a general gradient-based learning framework for NeSy energy-based models (demonstrated on NeuPSL) using a smooth primal-dual inference formulation and a dual block-coordinate-descent algorithm, yielding 100× faster inference. |
| [Federated Neuro-Symbolic Learning](2024/Federated%20Neuro-Symbolic%20Learning.pdf) | Xing, Lu, Yu | Proposes FedNSL, the first framework extending neuro-symbolic learning to federated settings by using latent rule-distribution variables as the communication medium, with a KL-divergence constraint to handle rule distribution heterogeneity across clients. |
| [Neuro-Symbolic Temporal Point Processes](2024/Neuro-Symbolic%20Temporal%20Point%20Processes.pdf) | Yang, Yang, Li, Fu, Li | Introduces a neuro-symbolic rule-induction framework within temporal point processes that learns compact, human-readable temporal logic rules end-to-end via a sequential covering algorithm, applied to irregular event data such as clinical records. |
| [On the Hardness of Probabilistic Neurosymbolic Learning](2024/On%20the%20Hardness%20of%20Probabilistic%20Neurosymbolic%20Learning.pdf) | Maene, Derkinderen, De Raedt | Proves that exact gradient computation for probabilistic NeSy models is intractable in general but becomes tractable during training, and introduces WeightME, an unbiased gradient estimator based on weighted model sampling with a SAT oracle. |
| [On the Independence Assumption in Neurosymbolic Learning](2024/On%20the%20Independence%20Assumption%20in%20Neurosymbolic%20Learning.pdf) | van Krieken, Minervini, Ponti, Vergari | Critiques the common conditional-independence assumption in NeSy probabilistic losses, proving it biases models toward overconfidence and produces non-convex, highly disconnected optima, motivating more expressive alternatives. |

### 2025

| Paper | Authors | Summary |
|---|---|---|
| [DOLPHIN: A Programmable Framework for Scalable Neurosymbolic Learning](2025/DOLPHIN%3A%20A%20Programmable%20Framework%20for%20Scalable%20Neurosymbolic%20Learning.pdf) | Naik, Liu, Wang, Sethi, Dutta, Naik, Wong | Presents DOLPHIN, a framework for writing neurosymbolic programs in Python that executes symbolic reasoning on CPU while vectorizing probabilistic computation and gradient propagation on GPU, scaling to 13 benchmarks with recursion and black-box functions. |
| [Is Complex Query Answering Really Complex?](2025/Is%20Complex%20Query%20Answering%20Really%20Complex.pdf) | Gregucci, Xiong, Hernández, Loconte, Minervini, Staab, Vergari | Shows that most queries in standard complex query answering (CQA) benchmarks over knowledge graphs trivially reduce to simple link prediction, and proposes harder benchmarks that better reflect genuine multi-hop reasoning difficulty. |

## Topics at a Glance

- **Program synthesis & induction**: `2021/A large-scale benchmark...`, `2021/Leveraging Language to Learn Program Abstractions...`
- **Rule induction & logic learning**: `2021/An Integer Linear Programming Framework...`, `2022/Neuro-Symbolic Hierarchical Rule Induction`, `2024/Neuro-Symbolic Temporal Point Processes`
- **Interpretability & concept-based reasoning**: `2021/Discovering symbolic policies...`, `2023/Interpretable Neural-Symbolic Concept Reasoning`
- **Learning theory & optimization foundations**: `2024/Convex and Bilevel Optimization...`, `2024/On the Hardness of Probabilistic Neurosymbolic Learning`, `2024/On the Independence Assumption in Neurosymbolic Learning`
- **Reasoning shortcuts & continual/federated learning**: `2023/Neuro-Symbolic Continual Learning`, `2024/Analysis for Abductive Learning and Neural-Symbolic Reasoning Shortcuts`, `2024/Federated Neuro-Symbolic Learning`
- **Systems & benchmarks**: `2025/DOLPHIN...`, `2025/Is Complex Query Answering Really Complex?`

## Notes

- Summaries above are condensed from each paper's own abstract.
- These PDFs are the authors' published works and are included here for personal research/reference use; see each paper for its original copyright and license terms.
