# Human Review Samples

total_samples: 30

## Coverage

- student_persona: {'novice_closed_book': 19, 'rote_memorizer': 9, 'misconception_prone': 2}
- condition: {'node_only': 11, 'hidden_transfer': 9, 'chain_so_far': 7, 'no_course_baseline': 3}
- node_id: {'gross_margin': 3, 'accrual_vs_cash': 4, 'net_profit': 4, 'income_statement_boundary': 6, 'revenue_recognition': 3, 'revenue_not_cash_receipt': 2, 'depreciation_amortization': 3, 'expense_recognition': 5}
- conflict_type: {'rule_pass_llm_fail': 2, 'both_fail': 12, 'both_pass': 1, 'rule_fail_llm_pass': 15}

## Samples

### 1. `c8a1cd8fb15a26c6`
- review_reason: all_rule_pass_llm_fail
- node_id / condition / persona: `gross_margin` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.6667 / 0.0
- rule_passed / judge_passed: True / False
- conflict_type: `rule_pass_llm_fail`
- misconception_tags: insufficient_materials
- matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入
- missing_reasoning_points: 毛利还没有扣除销售管理研发财务等期间费用
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 根据材料，毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。材料没有提到净利润的计算，所以无法从当前课程材料推出完整答案。

human_passed:
human_failure_type:
human_comment:

### 2. `cec6e305439237b9`
- review_reason: all_rule_pass_llm_fail
- node_id / condition / persona: `gross_margin` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.6667 / 0.67
- rule_passed / judge_passed: True / False
- conflict_type: `rule_pass_llm_fail`
- misconception_tags: rote_repetition
- matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入
- missing_reasoning_points: 毛利还没有扣除销售管理研发财务等期间费用
- judge_matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入
- judge_missing_reasoning_points: 毛利还没有扣除销售管理研发财务等期间费用
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 规则说：毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。所以毛利率高不等于净利润一定高。

human_passed:
human_failure_type:
human_comment:

### 3. `8c10722bfd204831`
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
- student_answer: 根据材料，权责发生制关注交易归属期间，现金制关注现金实际收付时间。

human_passed:
human_failure_type:
human_comment:

### 4. `db9a7f70f02cb56e`
- review_reason: accrual_vs_cash_node_only_failure
- node_id / condition / persona: `accrual_vs_cash` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.5 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: rote_repetition
- matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- missing_reasoning_points: 满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 规则说：权责发生制关注交易归属期间，现金制关注现金实际收付时间。

human_passed:
human_failure_type:
human_comment:

### 5. `b498fa1bf5bd5471`
- review_reason: accrual_vs_cash_node_only_failure
- node_id / condition / persona: `accrual_vs_cash` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.5 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: expense_payment_confusion；revenue_cash_confusion
- matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- missing_reasoning_points: 满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 权责发生制和现金制的核心区别是：权责发生制关注交易归属期间，现金制关注现金实际收付时间。但我觉得，没收到钱就不算收入，没付款就没有费用，所以权责发生制其实也是看现金的。

human_passed:
human_failure_type:
human_comment:

### 6. `01668fda41cabddc`
- review_reason: net_profit_node_only_failure
- node_id / condition / persona: `net_profit` / `node_only` / `rote_memorizer`
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

### 7. `d9c0aa5717c689e5`
- review_reason: net_profit_node_only_failure
- node_id / condition / persona: `net_profit` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: profit_cash_confusion；净利润为正就一定不缺钱。
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 净利润为正说明公司赚了钱，那现金应该也增加了才对。材料说净利润不等于现金，但我觉得利润高现金肯定多，不然怎么叫赚钱呢？

human_passed:
human_failure_type:
human_comment:

### 8. `8299a8a38986d125`
- review_reason: hidden_transfer_pass
- node_id / condition / persona: `gross_margin` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 1.0 / 1.0
- rule_passed / judge_passed: True / True
- conflict_type: `both_pass`
- misconception_tags: -
- matched_reasoning_points: 本例毛利等于 10000 - 6500 = 3500 元；本例毛利率等于 3500 / 10000 = 35%；毛利还没有扣除销售管理研发财务等期间费用
- missing_reasoning_points: -
- judge_matched_reasoning_points: 本例毛利等于 10000 - 6500 = 3500 元；本例毛利率等于 3500 / 10000 = 35%；毛利还没有扣除销售管理研发财务等期间费用
- judge_missing_reasoning_points: -
- question: 服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。 如何推出毛利和毛利率？它们还没有扣除哪些费用？
- student_answer: 根据材料，毛利等于收入减销售成本，所以毛利是10000-6500=3500元，毛利率是3500/10000=35%。材料说毛利还不是净利润，但没具体说还要扣除哪些费用。

human_passed:
human_failure_type:
human_comment:

### 9. `a15875025c353cca`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.3333 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: 利润表记录一段期间的经营成果
- missing_reasoning_points: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- student_answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能进入利润表作为收入。而银行借款只是资金来源变化，不是经营收入，所以不应进入利润表。

human_passed:
human_failure_type:
human_comment:

### 10. `5d70ff16349ce408`
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

### 11. `72dc184657b65977`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `revenue_not_cash_receipt` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: 收入增加就等于现金增加；赊销没有收到钱所以没有任何经营成果
- matched_reasoning_points: -
- missing_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- student_answer: 

human_passed:
human_failure_type:
human_comment:

### 12. `a8027fffd436418b`
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
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以今年的折旧会影响利润，但通常不代表今年再次付现金。

human_passed:
human_failure_type:
human_comment:

### 13. `f599d9bb1b2418b3`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

human_passed:
human_failure_type:
human_comment:

### 14. `79c64d2597f89e85`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 根据课程材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。员工已经完成本月工作，但工资下月发放，耗费服务于本期经营，所以应记入本期费用。

human_passed:
human_failure_type:
human_comment:

### 15. `a306b041336c2cf6`
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
- student_answer: 根据材料，费用确认关注的是耗费是否服务于本期经营，而不是是否支付现金。员工本月工作服务于本期经营，所以本月可以确认工资费用。材料说“费用发生不一定等于当期现金付款”，所以下月发工资不影响本月确认费用。

human_passed:
human_failure_type:
human_comment:

### 16. `ef006d458bad3b49`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 根据课程材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

human_passed:
human_failure_type:
human_comment:

### 17. `bf2dc9120ce2ddfd`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入。

human_passed:
human_failure_type:
human_comment:

### 18. `7839880dba2edf96`
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
- student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款不是销售商品或提供服务，所以不应作为营业收入。

human_passed:
human_failure_type:
human_comment:

### 19. `b0d2294580e19c10`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

human_passed:
human_failure_type:
human_comment:

### 20. `ee1fd11f257df05d`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 规则说费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

human_passed:
human_failure_type:
human_comment:

### 21. `31a950c3a9c59009`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 规则说折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

human_passed:
human_failure_type:
human_comment:

### 22. `d2ba14e5050c1df2`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `net_profit` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.95
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收款，费用发生不等于现金支付，折旧和摊销会减少利润但不代表现金流出。所以，净利润为正时，可能因为赊销、未付款的费用或折旧等原因，现金并没有同步增加。

human_passed:
human_failure_type:
human_comment:

### 23. `317a2d076fd28871`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.9
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入确认不一定依赖现金已经到账；完成交付或服务后可能满足收入确认条件
- judge_missing_reasoning_points: 收入来自销售商品或提供服务
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 规则说：收入确认不一定等于收到现金。所以本月完成服务，即使客户下月付款，仍可能确认收入。

human_passed:
human_failure_type:
human_comment:

### 24. `1d2f4a510281905d`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.8
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

human_passed:
human_failure_type:
human_comment:

### 25. `54985bb56e4c1e7b`
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
- student_answer: 根据课程材料，权责发生制关注交易归属期间，而不是现金实际收付时间。所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用。现金制则关注现金实际收付时间，所以6月没有收款和付款，收入和费用都不确认。

human_passed:
human_failure_type:
human_comment:

### 26. `1cfaba10d861f9c4`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.75
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但员工已经完成本月工作，耗费服务于本期经营，因此应作为本月费用。

human_passed:
human_failure_type:
human_comment:

### 27. `8305819be1ae4571`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `net_profit` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.75
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_missing_reasoning_points: 本例净利润为 8000 元
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 根据材料，净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。材料说收入记录赚到的经营成果，收款记录现金进入，赊销会让收入和现金流入出现时间差。所以净利润为正仍不必然表示现金充足，因为可能有赊销等未收现的情况。

human_passed:
human_failure_type:
human_comment:

### 28. `bae9fb5e0a7d3761`
- review_reason: no_course_baseline_fail
- node_id / condition / persona: `income_statement_boundary` / `no_course_baseline` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: insufficient_materials
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 无法从当前课程材料推出完整答案

human_passed:
human_failure_type:
human_comment:

### 29. `abe2e7353f1ea759`
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

### 30. `58601fac79dbc131`
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
