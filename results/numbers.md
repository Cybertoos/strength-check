# Numbers

Written by analyze.py. Do not edit.

Replies: 104 records, 1 with no valid verdict after one retry: [('r26', 'openai/gpt-oss-20b')]

## real stronger: 9 cases, 9 with both verdicts
- flag: 3 of 9 (33%, 95% CI 12 to 65%)
- ask a person: 6 of 9 (67%, 95% CI 35 to 88%)
- flag or ask a person: 9 of 9 (100%, 95% CI 70 to 100%)
- qwen/qwen3.8-27b: claims_more 8 of 9 (89%, 95% CI 56 to 98%); all verdicts {'claims_more': 8, 'cannot_tell': 1}
- openai/gpt-oss-20b: claims_more 3 of 9 (33%, 95% CI 12 to 65%); all verdicts {'cannot_tell': 2, 'claims_more': 3, 'claims_less': 2, 'matches': 2}

## planted: 23 cases, 23 with both verdicts
- flag: 7 of 23 (30%, 95% CI 16 to 51%)
- ask a person: 12 of 23 (52%, 95% CI 33 to 71%)
- flag or ask a person: 19 of 23 (83%, 95% CI 63 to 93%)
- qwen/qwen3.8-27b: claims_more 15 of 23 (65%, 95% CI 45 to 81%); all verdicts {'claims_less': 5, 'claims_more': 15, 'matches': 2, 'cannot_tell': 1}
- openai/gpt-oss-20b: claims_more 11 of 23 (48%, 95% CI 29 to 67%); all verdicts {'claims_more': 11, 'matches': 8, 'claims_less': 4}

## controls (real holds): 14 cases, 13 with both verdicts
- flag: 2 of 13 (15%, 95% CI 4 to 42%)
- ask a person: 8 of 13 (62%, 95% CI 36 to 82%)
- flag or ask a person: 10 of 13 (77%, 95% CI 50 to 92%)
- qwen/qwen3.8-27b: claims_more 10 of 14 (71%, 95% CI 45 to 88%); all verdicts {'claims_more': 10, 'matches': 2, 'claims_less': 2}
- openai/gpt-oss-20b: claims_more 3 of 13 (23%, 95% CI 8 to 50%); all verdicts {'claims_less': 4, 'matches': 6, 'claims_more': 3}

## planted, per operator (flag or ask a person)
- hedge: 5 of 6 (83%, 95% CI 44 to 97%)
- range_upper: 4 of 5 (80%, 95% CI 38 to 96%)
- sample: 3 of 3 (100%, 95% CI 44 to 100%)
- scope: 7 of 9 (78%, 95% CI 45 to 94%)

## weaker lines (not in the headline)
- qwen/qwen3.8-27b: claims_less 1 of 3 (33%, 95% CI 6 to 79%); all {'claims_more': 1, 'cannot_tell': 1, 'claims_less': 1}
- openai/gpt-oss-20b: claims_less 1 of 3 (33%, 95% CI 6 to 79%); all {'matches': 1, 'cannot_tell': 1, 'claims_less': 1}

## ambiguous and reworded lines (not counted)
- r02 ambiguous: qwen3.8-27b cannot_tell, gpt-oss-20b cannot_tell
- r14 reworded: qwen3.8-27b matches, gpt-oss-20b matches
- r18 ambiguous: qwen3.8-27b claims_more, gpt-oss-20b claims_less

## agreement between the two models, all cases
- same verdict: 20 of 51 (39%, 95% CI 27 to 53%)
- same on claims_more or not: 24 of 51 (47%, 95% CI 34 to 60%)

## reasons given for claims_more on controls, verbatim
- r19 qwen3.8-27b: The sentence omits the specific population of 'nine open-weight monitors and two hosted models' and the detail about 'similarly large shifts on both hosted models', making the claim appear to apply generally to 'a summary' rather than the specific tested models.
- r20 qwen3.8-27b: The sentence introduces specific details about the mutation method ("20-operator AST mutator") and the sample size ("1,135 BigCodeBench tasks") that are not present in the source passage, which only mentions the benchmark name and the resulting count of killed mutants.
- r21 qwen3.8-27b: The sentence drops the condition 'Based on the evaluation' from the passage, presenting the coverage metrics as inherent properties of the benchmarks rather than results of a specific evaluation.
- r22 qwen3.8-27b: The sentence omits the specific condition 'with the augmented suites' and the context of 're-evaluating', making the claim appear to apply generally to the agents rather than only under the specific augmented test conditions described in the passage.
- r24 qwen3.8-27b: The sentence includes a claim about the protective effect of human annotations that is not present in the source passage, which only discusses the risk of accidental hacking and incorrect conclusion rates.
- r24 gpt-oss-20b: The sentence repeats the passage’s numbers but adds an unsubstantiated claim about human annotations, thereby extending beyond what the passage supports.
- r25 gpt-oss-20b: The sentence omits the prompting condition, comparison to original texts, and uncertainty intervals while retaining effect sizes, thus stating more than the passage supports.
- r26 qwen3.8-27b: The sentence drops the specific population ('all six model-task combinations') and the specific condition ('Comparing... to the Baseline'), making the claim appear to apply generally to any 'Guarded' instruction rather than the specific experimental comparison described.
- r28 qwen3.8-27b: The sentence adds specific conditions ('binary scores, uniform difficulty') that are not present in the source passage, which only refers to 'this example' without defining those specific parameters.
- r29 qwen3.8-27b: The sentence adds a specific detail about the token position of divergence that is not present in the source passage.
- r30 qwen3.8-27b: The sentence drops the specific population (22 models) and the condition (baseline vs prompt conditions) stated in the passage, making the claim appear more general than the source supports.
- r31 qwen3.8-27b: The sentence specifies 'OpenAI model' whereas the passage only says 'our models', attributing a specific identity not present in the source text.
- r31 gpt-oss-20b: The sentence generalizes the population to all OpenAI models and omits the investigative context, making it broader than the passage.

## run-to-run, 19 cases rerun once per model
- pairs with a valid verdict both times: 37 of 38
- same verdict: 36 of 37 (97%, 95% CI 86 to 100%)
- qwen/qwen3.8-27b: 18 of 19 (95%, 95% CI 75 to 99%)
- openai/gpt-oss-20b: 18 of 18 (100%, 95% CI 82 to 100%)
