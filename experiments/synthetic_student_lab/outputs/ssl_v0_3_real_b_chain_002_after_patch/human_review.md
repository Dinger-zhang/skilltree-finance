# Human Review Samples

total_samples: 30

## Coverage

- student_persona: {'novice_closed_book': 16, 'rote_memorizer': 10, 'misconception_prone': 4}
- condition: {'chain_so_far': 5, 'node_only': 9, 'hidden_transfer': 12, 'no_course_baseline': 4}
- node_id: {'revenue_not_cash_receipt': 4, 'accrual_vs_cash': 5, 'net_profit': 5, 'gross_margin': 1, 'revenue_recognition': 4, 'depreciation_amortization': 1, 'expense_recognition': 6, 'income_statement_boundary': 4}
- conflict_type: {'rule_pass_llm_fail': 1, 'both_fail': 14, 'both_pass': 2, 'rule_fail_llm_pass': 13}

## Samples

### 1. `5597cb7ad2db9ba6`
- review_reason: all_rule_pass_llm_fail
- node_id / condition / persona: `revenue_not_cash_receipt` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.6667 / 0.0
- rule_passed / judge_passed: True / False
- conflict_type: `rule_pass_llm_fail`
- misconception_tags: -
- matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
- missing_reasoning_points: 可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 根据材料，收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以可能确认收入但现金没有增加。

human_passed:
human_failure_type:
human_comment:

### 2. `8c10722bfd204831`
- review_reason: accrual_vs_cash_node_only_failure
- node_id / condition / persona: `accrual_vs_cash` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.5 / 0.5
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- missing_reasoning_points: 满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- judge_matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- judge_missing_reasoning_points: 满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 权责发生制关注交易归属期间，现金制关注现金实际收付时间。

human_passed:
human_failure_type:
human_comment:

### 3. `db9a7f70f02cb56e`
- review_reason: accrual_vs_cash_node_only_failure
- node_id / condition / persona: `accrual_vs_cash` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 4. `b498fa1bf5bd5471`
- review_reason: accrual_vs_cash_node_only_failure
- node_id / condition / persona: `accrual_vs_cash` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 5. `01668fda41cabddc`
- review_reason: net_profit_node_only_failure
- node_id / condition / persona: `net_profit` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 材料说净利润不等于现金，所以净利润为正不一定代表现金充足。

human_passed:
human_failure_type:
human_comment:

### 6. `d9c0aa5717c689e5`
- review_reason: net_profit_node_only_failure
- node_id / condition / persona: `net_profit` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 7. `72dc184657b65977`
- review_reason: hidden_transfer_pass
- node_id / condition / persona: `revenue_not_cash_receipt` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 1.0 / 1.0
- rule_passed / judge_passed: True / True
- conflict_type: `both_pass`
- misconception_tags: -
- matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- missing_reasoning_points: -
- judge_matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_missing_reasoning_points: -
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- student_answer: 根据材料，批发商本月赊销8000元商品，客户45天后付款。材料说“收入记录赚到的经营成果；收款记录现金进入。赊销会让收入和现金流入出现时间差。”所以本月利润表应该确认8000元收入，因为商品已经卖出，符合收入确认条件。现金方面，因为还没收到钱，所以现金没有增加。收入不等于收款，是因为收入确认关注的是赚到经营成果，而不是收到现金。

human_passed:
human_failure_type:
human_comment:

### 8. `8299a8a38986d125`
- review_reason: hidden_transfer_pass
- node_id / condition / persona: `gross_margin` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 1.0 / 1.0
- rule_passed / judge_passed: True / True
- conflict_type: `both_pass`
- misconception_tags: insufficient_materials
- matched_reasoning_points: 本例毛利等于 10000 - 6500 = 3500 元；本例毛利率等于 3500 / 10000 = 35%；毛利还没有扣除销售管理研发财务等期间费用
- missing_reasoning_points: -
- judge_matched_reasoning_points: 本例毛利等于 10000 - 6500 = 3500 元；本例毛利率等于 3500 / 10000 = 35%；毛利还没有扣除销售管理研发财务等期间费用
- judge_missing_reasoning_points: -
- question: 服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。 如何推出毛利和毛利率？它们还没有扣除哪些费用？
- student_answer: 根据材料，服装店销售收入10000元，进货成本6500元，毛利等于收入减销售成本，即10000-6500=3500元，毛利率等于毛利除以收入，即3500/10000=35%。但材料说毛利还不是净利润，还没有扣除期间费用，比如租金、工资、折旧等。不过材料没有具体列出所有费用项目，所以无法从当前课程材料推出完整答案。

human_passed:
human_failure_type:
human_comment:

### 9. `5d70ff16349ce408`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 10. `a8027fffd436418b`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 11. `8305819be1ae4571`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `net_profit` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 12. `81c401580ed00066`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 13. `a306b041336c2cf6`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付。材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用。因此，本月可以确认工资费用，费用发生与现金付款是两回事。

human_passed:
human_failure_type:
human_comment:

### 14. `7839880dba2edf96`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款不是来自销售商品或提供服务，所以不应作为营业收入。

human_passed:
human_failure_type:
human_comment:

### 15. `75e013c030b465ac`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- student_answer: 规则说利润表记录经营成果，看收入、成本、费用，不是所有现金流入。贷款不是销售商品或提供服务，所以不是营业收入。

human_passed:
human_failure_type:
human_comment:

### 16. `ee1fd11f257df05d`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 规则说费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

human_passed:
human_failure_type:
human_comment:

### 17. `d3418a5ab6cd6832`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: expense_payment_confusion
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 因为材料说费用是为取得收入或维持经营发生的资源耗费，员工本月工作服务于本月经营，所以即使没付款，也应该记作本月费用。不过，我还是觉得没付钱就算费用有点奇怪，毕竟钱还没出去。

human_passed:
human_failure_type:
human_comment:

### 18. `54985bb56e4c1e7b`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `accrual_vs_cash` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.25 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: 权责发生制关注交易归属期间
- missing_reasoning_points: 满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月；现金制关注现金实际收付时间
- judge_matched_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月；现金制关注现金实际收付时间
- judge_missing_reasoning_points: -
- question: 咨询公司 6 月完成服务，7 月收款；6 月发生房租但 7 月付款。 权责发生制下 6 月应如何看收入和费用？它和现金制的关注点有什么不同？
- student_answer: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间。所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用。现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用。

human_passed:
human_failure_type:
human_comment:

### 19. `4e12cea729ecaa0a`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.67
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务，即使客户下月付款，也可能确认收入。

human_passed:
human_failure_type:
human_comment:

### 20. `d9da0fab40302700`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `net_profit` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.67
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: 净利润可能包含未收现收入
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金。所以净利润为正不一定代表现金充足。

human_passed:
human_failure_type:
human_comment:

### 21. `b0d2294580e19c10`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.67
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

human_passed:
human_failure_type:
human_comment:

### 22. `bcb84f9ceba8fce9`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.667
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition；weak_transfer
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入确认不一定依赖现金已经到账；收入来自销售商品或提供服务
- judge_missing_reasoning_points: 完成交付或服务后可能满足收入确认条件
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- student_answer: 规则说收入确认不一定等于收到现金，所以本月完成服务就可以确认收入。

human_passed:
human_failure_type:
human_comment:

### 23. `a15875025c353cca`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.3333 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: 利润表记录一段期间的经营成果
- missing_reasoning_points: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- student_answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能形成收入进入利润表；而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表。

human_passed:
human_failure_type:
human_comment:

### 24. `b1e0b16dffbdf58f`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_not_cash_receipt` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.3333 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: 赊销可能先确认收入
- missing_reasoning_points: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_missing_reasoning_points: -
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- student_answer: 规则说收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以本月利润表收入增加8000元，现金不变。收入不等于收款是因为收入确认不一定等于收到现金。

human_passed:
human_failure_type:
human_comment:

### 25. `1101b9b1a3e1bef6`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `net_profit` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.6
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition；weak_transfer
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润为正不一定代表现金充足
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 规则说净利润不等于现金，所以净利润为正不一定代表现金充足。

human_passed:
human_failure_type:
human_comment:

### 26. `bae9fb5e0a7d3761`
- review_reason: no_course_baseline_fail
- node_id / condition / persona: `income_statement_boundary` / `no_course_baseline` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: insufficient_materials；把借款或股东投入当成利润。；把所有收到的钱都当成收入。
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 无法从当前课程材料推出完整答案

human_passed:
human_failure_type:
human_comment:

### 27. `abe2e7353f1ea759`
- review_reason: no_course_baseline_fail
- node_id / condition / persona: `revenue_recognition` / `no_course_baseline` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: insufficient_materials
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 无法从当前课程材料推出完整答案

human_passed:
human_failure_type:
human_comment:

### 28. `58601fac79dbc131`
- review_reason: no_course_baseline_fail
- node_id / condition / persona: `revenue_not_cash_receipt` / `no_course_baseline` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 29. `f360e8fa7f1125ec`
- review_reason: no_course_baseline_fail
- node_id / condition / persona: `expense_recognition` / `no_course_baseline` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 30. `1e07b89d2e8529b1`
- review_reason: focus_node_net_profit_or_accrual_vs_cash
- node_id / condition / persona: `accrual_vs_cash` / `chain_so_far` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 

human_passed:
human_failure_type:
human_comment:
