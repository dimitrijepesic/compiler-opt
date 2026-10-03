# Provera izvodljivosti: adaptivni epsilon u idealloc-u (21. sept. 2026)

Pitanje: da li je predlog adaptivnog izbora epsilon-a u idealloc-u realan.
Ovo je kratka sonda (oko 3 sata), ne zamrznut eksperiment: nema protokola,
podele razvoj/test ni kontrolera. Meri samo da li poluga uopšte postoji.

Okruženje: jednokratni kontejner `memplan-probe` (ubuntu:22.04, amd64 pod
Rosettom, zaustavljen, nije obrisan). idealloc `3b7eb67f` (neizmenjen binarni
fajl sačuvan; zakrpljena KOPIJA dodaje samo `IDEALLOC_EPS_FRAC` i izvoz
rasporeda, `idealloc_probe_patch.diff`), MiniMalloc (revizija u
`minimalloc_revision.txt`; jedina izmena je minimalna cmake verzija). Svih 17
javnih ulaza osim `lldb0`; semantika `ex-csv`. Vremena su iz emulacije.

## Nalazi

1. **Tvrdnja o kodu je tačna.** `init_rogue` bira epsilon jednom, glavna petlja
   ga zadržava.
2. **Na 11 od 17 javnih ulaza (MiniMalloc A-K) poluga ne postoji.** Dozvoljeni
   interval je [76,341413; 76,341461], relativne širine 6e-7. Razlike između
   prisilnih vrednosti su u granicama šuma ponavljanja (`sweep.json`, 312
   rasporeda, svi nezavisno validni i jednaki prijavljenom makespan-u).
3. **Tamo gde je prostor veliki, već postoji optimalno rešenje.** idealloc na
   A-K ostavlja 28-41% fragmentacije i 100 iteracija to skoro ne menja (C, I, K:
   isti rezultat u sva 24 pokretanja). MiniMalloc rešava svih 11 na kapacitetu
   1.048.576 za 0,5-4,2 s, a resnet50 i G_1 na samoj donjoj granici (0%
   fragmentacije, validirano) za manje od 1 s.
4. **Tamo gde je epsilon stvarna poluga, prostor je mali.** Fragmentacija
   neizmenjenog idealloc-a: resnet50 0,35%, G_1 0,22%, Y_1 0,28-0,36%, S_1
   0,9-2,9%, pangu 2,3-3,3%. Arena ne može ispod opterećenja, pa je **prag od 5%
   manje arene aritmetički nedostižan** na svakom takvom ulazu.
5. **Šum restarta je veći od efekta epsilona.** Podrazumevani naspram uniformno
   nasumičnog epsilona, 20 iteracija (`default_vs_random_eps.json`): pangu 3,13%
   naspram 2,87% (sd 0,55-0,64, n=20), S_1 1,79% naspram 2,17% (n=12, obrnut
   smer), G_1 0,274% naspram 0,257%. Nema doslednog smera. Jedini dosledan
   efekat: G_1 sa najmanjim epsilonom i 100 iteracija, 0,22% -> 0,02% arene.
6. **Niša postoji, ali je uska.** MiniMalloc ne završava pangu i S_1 za 300 s i
   pada na Y_1, pa je idealloc tamo relevantan. To su 4 javna ulaza iz 3 izvora,
   sa najviše ~3% prostora.

## Zaključak

Predlog u ovom obliku nije realan: kriterijum arene je nedostižan, a kriterijum
"dvostruko brže do istog kvaliteta" bi morao da pobedi kontrolu "samo još
restarta" na šumu koji je veći od efekta, na premalo nezavisnih ulaza. Nije
mereno: `lldb0`, poravnanje, `in-csv` semantika, nativna vremena, pravi
kontroler.
