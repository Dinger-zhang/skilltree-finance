# Net Profit Human Review Samples

source_dir: `experiments\synthetic_student_lab\outputs\ssl_v0_3_real_b_chain_001_repaired`
total_samples: 12

## Coverage

- condition: {'node_only': 3, 'chain_so_far': 3, 'no_course_baseline': 3, 'hidden_transfer': 3}
- student_persona: {'novice_closed_book': 4, 'misconception_prone': 4, 'rote_memorizer': 4}
- conflict_type: {'both_fail': 6, 'rule_fail_llm_pass': 6}

## Samples

### 1. `787b5003cc442550`
- condition: `node_only`
- student_persona: `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.4
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 材料说净利润不等于现金，所以净利润为正不一定代表现金充足。

### 2. `426d4cdc6b395ec8`
- condition: `node_only`
- student_persona: `misconception_prone`
- rule_score / judge_score: 0.0 / 0.3
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: profit_cash_confusion；净利润为正就一定不缺钱。
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 净利润为正说明公司赚了钱，按理说现金应该增加，但材料说净利润不等于现金，所以可能现金还是紧张。不过我觉得既然利润是正的，现金应该不会太差吧。

### 3. `3773a9d792eed4f8`
- condition: `chain_so_far`
- student_persona: `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.33
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 规则说净利润不等于现金，所以净利润为正不一定代表现金充足。

### 4. `c053d0041d060612`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: insufficient_materials
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 无法从当前课程材料推出完整答案

### 5. `5be49900e2b368d6`
- condition: `no_course_baseline`
- student_persona: `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 无法从当前课程材料推出完整答案

### 6. `7477a3f0665a4cda`
- condition: `no_course_baseline`
- student_persona: `misconception_prone`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: profit_cash_confusion
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 无法从当前课程材料推出完整答案

### 7. `64c06390d142e8d2`
- condition: `node_only`
- student_persona: `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.67
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: 净利润可能包含未收现收入
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 规则说净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。

### 8. `674855dfd46b5316`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收款，费用发生也不等于现金付款，折旧和摊销会减少利润但不代表现金流出。所以净利润是收入减成本和费用的结果，但现金可能因为赊销、未付款项或折旧等原因而不足。

### 9. `f0fc3c7da8daca7d`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: profit_cash_confusion
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 净利润为正说明公司赚了钱，按理说现金应该也增加了，但材料说收入不等于收款，费用也不等于付款，所以可能利润是赚到了但钱还没收到，或者折旧这种费用减少了利润但没付出现金，所以现金不一定充足。

### 10. `81eb5c38a64cb9a7`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.9
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_missing_reasoning_points: 本例净利润为 8000 元
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 根据材料，净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。材料说收入确认不一定等于收到现金，费用发生不一定等于当期现金付款，所以净利润为正仍不必然表示现金充足。

### 11. `fcf96c5662b0148f`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 规则说净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。材料说收入记录赚到的经营成果，收款记录现金进入，赊销会让收入和现金流入出现时间差。所以净利润为正仍不必然表示现金充足。

### 12. `4adb424f71e94e05`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- rule_score / judge_score: 0.3333 / 0.67
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: profit_cash_confusion；净利润为正就一定现金充足
- matched_reasoning_points: 本例净利润为 8000 元
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元
- judge_missing_reasoning_points: 净利润可能包含未收现收入或非现金费用所以不等于现金
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 净利润就是收入减销售成本再减期间费用，50000减30000减12000等于8000元。净利润为正说明公司赚了钱，现金应该也增加了，所以现金应该是充足的。
