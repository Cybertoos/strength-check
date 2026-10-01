# Numbers, sweep

Written by analyze_sweep.py. Do not edit.

## Per arm: "claims more" and invalid replies

Rates over cases with a valid verdict. Separation: real stronger minus controls.

| Arm | Real stronger | Planted | Controls | Separation (points) | Invalid |
|---|---|---|---|---|---|
| qwen-none | 8 of 9 (89%, 95% CI 56 to 98%) | 15 of 23 (65%, 95% CI 45 to 81%) | 10 of 14 (71%, 95% CI 45 to 88%) | +17 (95% CI -19 to +45) | 0 of 52 |
| gptoss-low | 3 of 9 (33%, 95% CI 12 to 65%) | 11 of 23 (48%, 95% CI 29 to 67%) | 3 of 13 (23%, 95% CI 8 to 50%) | +10 (95% CI -24 to +45) | 1 of 52 |
| qwen-low | 9 of 9 (100%, 95% CI 70 to 100%) | 19 of 23 (83%, 95% CI 63 to 93%) | 9 of 14 (64%, 95% CI 39 to 84%) | +36 (95% CI +0 to +61) | 0 of 52 |
| gptoss-high | 4 of 5 (80%, 95% CI 38 to 96%) | 10 of 16 (62%, 95% CI 39 to 82%) | 3 of 13 (23%, 95% CI 8 to 50%) | +57 (95% CI +7 to +79) | 13 of 52 |
| glm4 | 8 of 9 (89%, 95% CI 56 to 98%) | 9 of 23 (39%, 95% CI 22 to 59%) | 6 of 14 (43%, 95% CI 21 to 67%) | +46 (95% CI +5 to +69) | 0 of 52 |
| phi4 | 7 of 8 (88%, 95% CI 53 to 98%) | 11 of 23 (48%, 95% CI 29 to 67%) | 3 of 12 (25%, 95% CI 9 to 53%) | +62 (95% CI +18 to +82) | 3 of 52 |

## Invalid replies after one retry, by cause of the last attempt
- qwen-low: 0: {}; ids []
- gptoss-high: 13: {'output token cap': 13}; ids ['r01', 'r06', 'r10', 'r12', 'r13', 'r20', 'p07', 'p09', 'p10', 'p13', 'p14', 'p19', 'p22']
- glm4: 0: {}; ids []
- phi4: 3: {'reply failed validation': 3}; ids ['r13', 'r20', 'r26']

## All verdicts per arm and set
- qwen-low, real stronger: {'claims_more': 9}
- qwen-low, planted: {'claims_more': 19, 'matches': 2, 'claims_less': 2}
- qwen-low, controls: {'claims_more': 9, 'matches': 4, 'claims_less': 1}
- gptoss-high, real stronger: {None: 4, 'claims_less': 1, 'claims_more': 4}
- gptoss-high, planted: {'claims_more': 10, 'claims_less': 4, None: 7, 'matches': 2}
- gptoss-high, controls: {'claims_less': 5, None: 1, 'matches': 5, 'claims_more': 3}
- glm4, real stronger: {'claims_more': 8, 'claims_less': 1}
- glm4, planted: {'claims_less': 4, 'claims_more': 9, 'matches': 10}
- glm4, controls: {'claims_less': 1, 'claims_more': 6, 'matches': 7}
- phi4, real stronger: {'claims_more': 7, 'claims_less': 1, None: 1}
- phi4, planted: {'claims_less': 6, 'matches': 6, 'claims_more': 11}
- phi4, controls: {'matches': 6, None: 2, 'claims_less': 3, 'claims_more': 3}

## Surprise test: at least 7 of 9 real stronger and at most 4 of 14 controls
- qwen-low: 9 of 9 and 9 of 14 (0 controls invalid): not met
- gptoss-high: 4 of 9 and 3 of 14 (1 controls invalid): not met
- glm4: 8 of 9 and 6 of 14 (0 controls invalid): not met
- phi4: 7 of 9 and 3 of 14 (2 controls invalid): met

## Two-model rule for every pair (flag / ask a person / pass)

A case is left out of a pair when either arm has no valid verdict on it.

| Pair | Real stronger | Planted | Controls |
|---|---|---|---|
| qwen-none + qwen-low | 8 / 1 / 0 of 9; flag or ask 9 | 14 / 6 / 3 of 23; flag or ask 20 | 8 / 3 / 3 of 14; flag or ask 11 |
| qwen-none + gptoss-high | 4 / 1 / 0 of 5; flag or ask 5 | 6 / 9 / 1 of 16; flag or ask 15 | 3 / 6 / 4 of 13; flag or ask 9 |
| qwen-none + glm4 | 7 / 2 / 0 of 9; flag or ask 9 | 7 / 10 / 6 of 23; flag or ask 17 | 6 / 4 / 4 of 14; flag or ask 10 |
| qwen-none + phi4 | 6 / 2 / 0 of 8; flag or ask 8 | 8 / 10 / 5 of 23; flag or ask 18 | 3 / 5 / 4 of 12; flag or ask 8 |
| gptoss-low + qwen-low | 3 / 6 / 0 of 9; flag or ask 9 | 10 / 10 / 3 of 23; flag or ask 20 | 3 / 5 / 5 of 13; flag or ask 8 |
| gptoss-low + gptoss-high | 2 / 3 / 0 of 5; flag or ask 5 | 6 / 6 / 4 of 16; flag or ask 12 | 2 / 2 / 8 of 12; flag or ask 4 |
| gptoss-low + glm4 | 3 / 5 / 1 of 9; flag or ask 8 | 4 / 12 / 7 of 23; flag or ask 16 | 1 / 7 / 5 of 13; flag or ask 8 |
| gptoss-low + phi4 | 3 / 4 / 1 of 8; flag or ask 7 | 6 / 10 / 7 of 23; flag or ask 16 | 1 / 4 / 7 of 12; flag or ask 5 |
| qwen-low + gptoss-high | 4 / 1 / 0 of 5; flag or ask 5 | 10 / 5 / 1 of 16; flag or ask 15 | 3 / 5 / 5 of 13; flag or ask 8 |
| qwen-low + glm4 | 8 / 1 / 0 of 9; flag or ask 9 | 8 / 12 / 3 of 23; flag or ask 20 | 5 / 5 / 4 of 14; flag or ask 10 |
| qwen-low + phi4 | 7 / 1 / 0 of 8; flag or ask 8 | 10 / 10 / 3 of 23; flag or ask 20 | 3 / 4 / 5 of 12; flag or ask 7 |
| gptoss-high + glm4 | 4 / 1 / 0 of 5; flag or ask 5 | 3 / 10 / 3 of 16; flag or ask 13 | 2 / 4 / 7 of 13; flag or ask 6 |
| gptoss-high + phi4 | 3 / 2 / 0 of 5; flag or ask 5 | 5 / 6 / 5 of 16; flag or ask 11 | 2 / 2 / 8 of 12; flag or ask 4 |
| glm4 + phi4 | 7 / 1 / 0 of 8; flag or ask 8 | 7 / 6 / 10 of 23; flag or ask 13 | 3 / 2 / 7 of 12; flag or ask 5 |
