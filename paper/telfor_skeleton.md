# TELFOR 2026 — kostur rada (4 strane, IEEE A4 dvokolonski)

> **Kako se koristi ovaj dokument:** ovo je kompletna građa — struktura,
> raspodela prostora, sve tabele sa stvarnim brojevima i tačke argumentacije
> po sekcijama. Finalni tekst pišeš SVOJIM rečima u IEEE templejtu
> (Overleaf → "IEEE Conference Template", conference mode, A4).
> Draft rečenice ispod su radne skice — prepiši ih, ne kopiraj.
>
> Podsetnici iz regulacija: max 4 strane; copyright red na dnu prve strane
> (tačan format sa telfor.rs); engleski; regular sekcija (zbog Xplore);
> bez arXiv-a pre Foruma; lično prezentovanje.

---

## Naslov (izaberi jedan, ili izvedi svoj)

1. *Null Models and Sampling-Based Evaluation Expose the Real Value of
   Reinforcement Learning for LLVM Pass Ordering*
2. *Honest Baselines for Learned LLVM Pass Ordering: A Multi-Suite Study*
3. *What Actually Works in RL-Based LLVM Pass Ordering: Curated Action
   Spaces, Policy Sampling, and Encoder Pretraining*

Preporuka: #1 (teza u naslovu; recenzenti vole jasan claim).

## Apstrakt (~150 reči — tačke koje mora da pokrije)

- RL za uređivanje LLVM prolaza se tipično evaluira poređenjem sa fiksnim
  -O3/-Oz i determinističkim (argmax) rollout-ima.
- Uvodimo dva null-modela u kuriranом 36-pass prostoru (jedna random
  epizoda; best-of-N random pretraga) i sampling evaluaciju (best-of-k).
- Merenja: 380 programa iz 7 nezavisnih izvora (cBench, MiBench, CHStone,
  NPB, BLAS, POJ-104, csmith), PPO sa Autophase i GraphSAGE reprezentacijom,
  3 seed-a, kontrolisan protokol.
- Nalazi: (1) kurirani prostor + trivijalna pretraga tuče -Oz na svim
  real-code suite-ovima (+1.6% do +24.5%), granica: sintetički csmith;
  (2) argmax evaluacija obrće rangiranje agenata — GNN politika kao
  sampler sistematski tuče fer null (18/18 suite×seed) i dostiže greedy
  uz ~4.5x manje kompilacija; (3) RL gradijenti sami ne treniraju enkoder —
  jeftina distilacija Autophase featura ga otključava (0/3 → 2/2 proboja
  platoa, ~9% bolji argmax transfer).
- Poruka: izbor baseline-a i način dekodiranja politike menjaju zaključke
  više nego izbor reprezentacije.

**Keywords:** compiler optimization, LLVM, phase ordering, reinforcement
learning, graph neural networks, evaluation methodology

---

## I. INTRODUCTION (~0.5 kolone)

Tačke:
- Phase-ordering problem; -O3/-Oz su fiksne sekvence, per-program redosled
  obećava dobitke; RL pristupi (Autophase, CompilerGym) prijavljuju pobede
  nad -O3.
- Problem: evaluacione prakse — poređenje sa pogrešnim baseline-ом
  (-O3 za veličinu koda!), bez null-modela u istom action space-u,
  deterministički argmax kao jedini način čitanja politike.
- Doprinosi (nabroj eksplicitno, 3 tačke = 3 nalaza iz apstrakta).

Radna skica (prepiši): "Reported gains of learned pass ordering are
typically measured against fixed optimization levels and with
deterministic policy rollouts. We show, across 380 programs from seven
independent sources, that both choices materially change the conclusions."

## II. RELATED WORK (~0.5 kolone)

- Autophase (Haj-Ali et al.) — flat feature RL за pass ordering.
- CompilerGym (Cummins et al.) — okruženje koje koristimo (v0.2.5).
- ProGraML / graph reprezentacije programa.
- MLGO (Trofin et al.) — RL u produkcionom LLVM-u (inlining/regalloc).
- POSET-RL / pass-list radovi — redukcija action space-a.
- **Liang et al., ICML 2023 (Coreset + Normalized Value Prediction)** —
  NAJBLIŽI SUSED, citirati istaknuto: coreset od 50 pass sekvenci + GNN
  bira sekvencu, −4.7% vs -Oz na 4683 repoa u ≤45 kompilacija. RAZLIKA:
  oni predlažu metod i prijavljuju pobedu; mi merimo ODAKLE pobeda dolazi
  (null u istom prostoru — koji njihov apstrakt ne prijavljuje), kako
  dekodiranje (argmax vs sampling) menja zaključke, i zašto enkoder ne uči
  bez pretreninga. Naša pitanja se primenjuju i na njihov metod.
- LLM Compiler (Cummins et al. 2024) — LLM pravac, drugačiji budžet.
- Mammadli et al. 2020 (Static Neural Compiler Opt. via DRL) — rani
  signal da je random search konkurентan RL-u; mi to formalizujemo kao
  null-model protokol i repliciramo preko 7 suite-ova.
- Pozicioniranje: mi ne predlažemo novi agent nego mernu metodologiju +
  recept (pretraining) koji menja zaključke postojećih pristupa.

### Statistika za IV-B (izračunato, ubaci u tekst):
- GNN vs null, cBench: sign test 6/6, p=0.016; Wilcoxon per-benchmark
  (medijalni seed, n=9): **p=0.0039**. AP: 4/6, p=0.34 (nije značajno) —
  i to je nalaz: GNN jeste, AP nije.
- [TBD nakon battery podataka: sign test 18/18 → p≈3.8e-6]

### Pareto figura (gotova: paper/figures/pareto.pdf):
- GNN k=8 (360 komp./program): 110.789 — bolje od random k=50 (2.250
  komp.): 111.006; greedy 110.550 uz ~1.970 komp. → "greedy kvalitet za
  18% cene; random na 6× budžetu i dalje gori".

## III. EXPERIMENTAL PROTOCOL (~0.75 kolone)

- CompilerGym llvm-ic-v0, metrika: IR instruction count (proxy za
  veličinu koda; ograničenje diskutovano u V).
- Action space: 36 prolaza profilisanih na cBench trening skupu (od 124).
- Agenti: PPO+Autophase (56-dim log1p), PPO+GraphSAGE (edge-type-aware,
  CFG+DFG, 61-dim node features); identičan trening protokol: isti trening
  set (4 cBench programa), 100K koraka, 3 seed-a, KL early-stop, entropy
  decay, truncation-aware GAE. Checkpoint selekcija na val-small.
- **Null-modeli** (ključni pojam rada): (a) RndRed-1ep — jedna random
  epizoda od 45 koraka u 36-pass prostoru (prosek 20); (b) RndRed-N —
  best-of-N random epizoda. Fer po konstrukciji: isti prostor, isti budžet
  koraka kao politika.
- **Evaluacija politike**: argmax (mod) vs best-of-k sampling (k=8),
  null = best-of-8 od istih snimljenih random epizoda.
- Suite-ovi: Tabela I; uzorci fiksirani seed-om (poj104 n=100, csmith
  n=50, blas n=50), IC cap 120K (battery) / 6K (policy eval — trošak GNN
  rollout-a).
- Pretraining (Sekcija IV-C): distilacija log1p(Autophase) iz grafa
  (2430 stanja, MSE 0.025), pa RL fine-tune.

## IV. RESULTS (~2.5 kolone, 3 tabele)

### IV-A. Curated action space vs -Oz (TABLE I)

| Suite | n | O0 | -O3 | -Oz | RndRed-50 | Δ vs -Oz |
|---|---|---|---|---|---|---|
| MiBench | 40 | 12,270 | 6,317 | 4,841 | 4,765 | +1.6% |
| BLAS | 50 | 40,745 | 39,141 | 37,838 | 36,757 | +2.9% |
| cBench (val+test) | 9 | 232,442 | 163,834 | 115,987 | 111,006 | +4.3% |
| CHStone | 12 | 19,857 | 14,182 | 9,834 | 9,097 | +7.5% |
| POJ-104 | 97 | 21,099 | 11,083 | 8,334 | 7,622 | +8.5% |
| NPB | 122 | 130,327 | 70,659 | 59,542 | 44,981 | +24.5% |
| csmith (synth.) | 50 | 352,963 | 82,950 | 57,625 | 60,626 | **−5.2%** |

Tačke: 36-pass skup destilovan iz cBench-a transferuje se na sve
real-code suite-ove; -O3 je pogrešan aršin za veličinu (na malim
programima IC raste iznad O0); granica važenja = sintetički kod.
Napomena: RndRed-1ep ≈ -Oz na većini suite-ova (npr. cBench val-small:
640 vs 643) — vredi jedna rečenica.

### IV-B. Argmax vs sampling (TABLE II) — glavna tabela rada

Policy eval (k=8) preko 4 suite-a (295 programa, IC≤6K), medijalni seed;
[TBD: mibench+chstone gap-fill — ažuriraj kad legne]:

| Suite | Null bo8 | -Oz | AP argmax | AP bo8 | GNN argmax | GNN bo8 |
|---|---|---|---|---|---|---|
| BLAS | 37,099 | 37,838 | 40,264 | 36,998 | 40,500 | 36,847 |
| csmith | 17,555 | 20,226 | 33,325 | 17,179 | 39,323 | 17,064 |
| NPB | 40,301 | 53,085 | 57,498 | 40,822 | 79,686 | 39,909 |
| POJ-104 | 7,853 | 8,334 | 11,708 | 7,917 | 12,846 | 7,730 |

Plus cBench iz kontrolisane studije (pun val/test): GNN bo8
52,716/58,073 vs null 53,539/58,717 vs greedy 52,481/58,069.

Tačke:
- Argmax je katastrofalan van trening distribucije (GNN NPB: 79,686 vs
  Oz 53,085) — a IDENTIČNE politike kao sampler tuku sve (GNN bo8 39,909).
- GNN bo8 > null na **svakom** suite×seed paru (12/12 + 6/6 cBench = 18/18);
  AP 5/12. Mala margina (~1-2%), savršena konzistentnost → sign test.
- Politika trenirana na 4 sićušna cBench programa transferuje se kao
  sampler i na sintetički csmith (GNN bo8 tuče Oz za 16% tamo gde random
  pretraga gubi).
- Cena: 8 rollout-a × 45 koraka = 360 kompilacija vs greedy ~1,620 —
  greedy kvalitet za ~22% cene (cBench brojevi).

### IV-C. Encoder pretraining (TABLE III)

| GNN varijanta | val-small best (3 seeda) | Full val argmax | Full test argmax |
|---|---|---|---|
| From scratch | 689 / 689 / 689 (plato) | 64,550 | 69,180 |
| + Autophase distillation | 651 / 668 (2 seeda) | 55,593 | 61,015 |

Tačke: RL gradijenti sami nikad ne pomere enkoder sa platoa (0/3);
distilacija (jeftina: 2,430 stanja, ~1h CPU) → 2/2 proboja, argmax
transfer ~9-12% bolji, prva deterministička politika koja tuče
RndRed-1ep na punim splitovima. Trade-off: pretrening popravlja MOD,
plain GNN ostaje bolji SAMPLER (battery: pretrained bo8 gori od plain) —
biraš prema tome koliko kompilacija smeš da platiš u inference-u.

## V. DISCUSSION & LIMITATIONS (~0.5 kolone)

- **IC→.text anchor (izmereno, results/text_size_anchor.json)**: na
  programima ≥1.000 instrukcija relativna IC redukcija snažno korelira sa
  relativnom .text redukcijom (Pearson r=0.78, p=2.2e-6, n=26; Spearman
  0.60), a IC prednost random-36 nad -Oz prenosi se u stvarni .text
  (16.3% vs 14.0% prosečna redukcija; llc + llvm-size iz istog LLVM 10
  runtime-a). Ispod ~1K instrukcija proxy slabi (fiksni codegen overhead;
  pooled r=0.19) — granica se eksplicitno prijavljuje.
- CompilerGym 0.2.5 stack (arhiviran); runtime nije meren.
- Trening na 4 mala programa — namerno (kontrola), ali mala pokrivenost;
  mixed-size trening NIJE pomogao (jedna rečenica, negativan rezultat).
- Praktična preporuka za polje: (1) uvek prijaviti null u istom action
  space-u; (2) izveštavati i sampling i argmax; (3) porediti sa -Oz za
  veličinu, nikad sa -O3.
- Budući rad: .text metrika, AnghaBench skala, beam/temperature dekodiranje.

## VI. CONCLUSION (~0.25 kolone)

Jedna poenta po nalazu + poruka: "evaluation choices dominate
representation choices" — merna praksa menja zaključke više nego izbor
enkodera.

## ACKNOWLEDGMENT (opciono)

"The author thanks Prof. [ime] for an early discussion of this work."

## REFERENCES (~12-15, predlog)

1. Haj-Ali et al., "AutoPhase: Juggling HLS Phase Orderings in Random
   Forests with Deep RL", MLSys 2020.
2. Cummins et al., "CompilerGym: Robust, Performant Compiler Optimization
   Environments for AI Research", CGO 2022.
3. Cummins et al., "ProGraML: A Graph-based Program Representation for
   Data Flow Analysis and Compiler Optimizations", ICML 2021.
4. Trofin et al., "MLGO: a Machine Learning Guided Compiler Optimizations
   Framework", arXiv 2021.
5. Jain et al., "POSET-RL: Phase ordering for Optimizing Size and
   Execution Time using Reinforcement Learning", ISPASS 2022.
6. Cummins et al., "Meta Large Language Model Compiler", arXiv 2024.
7. Schulman et al., "Proximal Policy Optimization Algorithms", 2017.
8. Hamilton et al., "Inductive Representation Learning on Large Graphs"
   (GraphSAGE), NeurIPS 2017.
9. Fursin et al., cBench / MILEPOST.
10. Guthaus et al., "MiBench", WWC 2001.
11. Hara et al., "CHStone", ISCAS 2008.
12. Bailey et al., "NAS Parallel Benchmarks".
13. Yang et al., "Finding and Understanding Bugs in C Compilers" (csmith),
    PLDI 2011.
14. + IEEE format po templejtu.

---

## Checklist pre predaje

- [ ] mibench/chstone policy-eval gap popunjen → ažuriraj Tabelu II
- [ ] IEEE A4 template (Overleaf, conference mode), 4 strane MAX
- [ ] Copyright red na dnu prve strane (tačan string sa telfor.rs)
- [ ] PDF kroz IEEE PDF eXpress validaciju
- [ ] TELFOR ID nalog + registracija rada (Step 1) pa submisija (Step 2)
- [ ] Regular sekcija (ne studentska — zbog Xplore)
- [ ] Bez arXiv-a pre Foruma
- [ ] Afilijacija autora odlučena
- [ ] Repo link u radu (footnote) — javna reproducibilnost je adut
