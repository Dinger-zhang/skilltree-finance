# Human Review Samples

total_samples: 30

## Coverage

- student_persona: {'misconception_prone': 5, 'novice_closed_book': 16, 'rote_memorizer': 9}
- condition: {'hidden_transfer': 12, 'node_only': 10, 'chain_so_far': 7, 'no_course_baseline': 1}
- node_id: {'revenue_not_cash_receipt': 2, 'accrual_vs_cash': 4, 'net_profit': 4, 'income_statement_boundary': 5, 'expense_recognition': 2, 'revenue_recognition': 5, 'gross_margin': 1, 'depreciation_amortization': 7}
- conflict_type: {'rule_pass_llm_fail': 1, 'both_fail': 10, 'rule_fail_llm_pass': 18, 'both_pass': 1}

## Samples

### 1. `b7c79c56ca63ca4c`
- review_reason: all_rule_pass_llm_fail
- node_id / condition / persona: `revenue_not_cash_receipt` / `hidden_transfer` / `misconception_prone`
- rule_score / judge_score: 0.6667 / 0.33
- rule_passed / judge_passed: True / False
- conflict_type: `rule_pass_llm_fail`
- misconception_tags: revenue_cash_confusion；收入增加就等于现金增加
- matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
- missing_reasoning_points: 可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: 未收现金时现金不一定增加
- judge_missing_reasoning_points: 赊销可能先确认收入；可能形成应收账款而不是现金流入
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- student_answer: 本月利润表上不应该确认收入，因为没有收到现金，现金也没变化。收入必须是在收到现金时才能确认，所以收入等于收款。赊销商品没收到钱，所以不能算收入。

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
- rule_score / judge_score: 0.5 / 0.5
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: rote_repetition
- matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- missing_reasoning_points: 满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- judge_matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- judge_missing_reasoning_points: 满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 权责发生制关注交易归属期间，现金制关注现金实际收付时间。

human_passed:
human_failure_type:
human_comment:

### 4. `b498fa1bf5bd5471`
- review_reason: accrual_vs_cash_node_only_failure
- node_id / condition / persona: `accrual_vs_cash` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.25 / 0.25
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: revenue_cash_confusion；权责发生制更关注现金是否实际收付。
- matched_reasoning_points: 现金制关注现金实际收付时间
- missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- judge_matched_reasoning_points: 现金制关注现金实际收付时间
- judge_missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 核心区别是权责发生制更关注现金是否实际收付，而现金制关注现金实际收付时间。

human_passed:
human_failure_type:
human_comment:

### 5. `d9da0fab40302700`
- review_reason: net_profit_node_only_failure
- node_id / condition / persona: `net_profit` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.33
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费
- judge_missing_reasoning_points: 净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金，所以净利润为正不代表现金充足。

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
- student_answer: 材料说净利润不等于现金。

human_passed:
human_failure_type:
human_comment:

### 7. `d9c0aa5717c689e5`
- review_reason: net_profit_node_only_failure
- node_id / condition / persona: `net_profit` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.33
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: profit_cash_confusion
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润可能包含未收现收入
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含非现金费用所以不等于现金
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 净利润为正说明公司赚了钱，按理现金应该增加，但可能是因为有些收入还没收到现金，比如应收账款，所以现金不一定充足。

human_passed:
human_failure_type:
human_comment:

### 8. `a15875025c353cca`
- review_reason: hidden_transfer_pass
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
- student_answer: 咖啡店向顾客出售咖啡获得的收入更可能进入利润表作为经营成果，因为它来自销售商品或提供服务。贷款是从银行借入的资金，不是营业收入，因为它不是销售所得，而是融资活动。根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入，所以贷款不属于营业收入。

human_passed:
human_failure_type:
human_comment:

### 9. `72dc184657b65977`
- review_reason: hidden_transfer_pass
- node_id / condition / persona: `revenue_not_cash_receipt` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.6667 / 1.0
- rule_passed / judge_passed: True / True
- conflict_type: `both_pass`
- misconception_tags: -
- matched_reasoning_points: 赊销可能先确认收入；可能形成应收账款而不是现金流入
- missing_reasoning_points: 未收现金时现金不一定增加
- judge_matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_missing_reasoning_points: -
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- student_answer: 根据课程材料，本月批发商赊销8000元商品，利润表可以确认8000元收入（因为商品已卖出），但现金不会增加（因为客户45天后才付款）。收入不等于收款是因为利润表记录的是赚到的经营成果，而收款记录的是现金进入，赊销导致收入和现金流入出现时间差。

human_passed:
human_failure_type:
human_comment:

### 10. `a306b041336c2cf6`
- review_reason: hidden_transfer_pass
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.6667
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 根据材料中的‘费用确认’部分，费用发生不一定等于现金付款。员工已完成本月工作，工资服务于本月经营，因此本月可以确认工资费用。现金付款在下月发生，不影响本月费用确认。

human_passed:
human_failure_type:
human_comment:

### 11. `81c401580ed00066`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.33
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；工资费用会减少本期利润
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 费用发生不一定等于当期现金付款，所以本月可能确认工资费用。

human_passed:
human_failure_type:
human_comment:

### 12. `6f9da756a4a58197`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `accrual_vs_cash` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.5 / 0.5
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: rote_repetition
- matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- missing_reasoning_points: 满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月
- judge_matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- judge_missing_reasoning_points: 满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月
- question: 咨询公司 6 月完成服务，7 月收款；6 月发生房租但 7 月付款。 权责发生制下 6 月应如何看收入和费用？它和现金制的关注点有什么不同？
- student_answer: 权责发生制关注交易归属期间，现金制关注现金实际收付时间。

human_passed:
human_failure_type:
human_comment:

### 13. `90ffab514a6ce477`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: revenue_cash_confusion；把收款作为收入确认的唯一条件；没收到现金就一定不能确认收入
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- student_answer: 不能确认收入，因为还没收到现金。客户下月才付款，所以收入应该在下月收到现金时确认。完成服务不等于收到钱，没收到钱就不能算收入。

human_passed:
human_failure_type:
human_comment:

### 14. `49702d7924a64a2f`
- review_reason: node_coverage_gross_margin
- node_id / condition / persona: `gross_margin` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.8
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- judge_matched_reasoning_points: 毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- judge_missing_reasoning_points: 毛利等于收入减销售成本
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 根据材料，毛利率是毛利除以收入，而净利润还需要减去其他费用和折旧摊销等，所以毛利率高不一定净利润高。材料说‘毛利还不是净利润’，因此不能直接等同。

human_passed:
human_failure_type:
human_comment:

### 15. `f599d9bb1b2418b3`
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
- student_answer: 根据课程材料，利润表记录经营成果，重点是收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，因此不应作为营业收入进入利润表。

human_passed:
human_failure_type:
human_comment:

### 16. `1d2f4a510281905d`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款属于资金来源变化，不是来自销售商品或提供服务，不反映经营成果，所以不应作为营业收入进入利润表。

human_passed:
human_failure_type:
human_comment:

### 17. `4e12cea729ecaa0a`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 根据材料，收入确认通常看服务是否完成或商品是否交付，而不是看是否收到现金。本月服务已完成，所以即使客户下月付款，本月仍可确认收入。

human_passed:
human_failure_type:
human_comment:

### 18. `9f925b57d5ef9706`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 根据课程材料，在权责发生制下，收入确认基于服务是否完成而非款项是否收到。本月已完成服务并交付，满足了收入确认条件，因此即使客户下月付款，本月仍可确认收入。

human_passed:
human_failure_type:
human_comment:

### 19. `5d70ff16349ce408`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- student_answer: 根据材料，本月可以确认收入，因为服务已完成并交付，收入确认关注的是是否赚到（即完成服务），而不是是否收到现金。客户下月付款不影响本月的收入确认。

human_passed:
human_failure_type:
human_comment:

### 20. `ff04d3360d229fb1`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

human_passed:
human_failure_type:
human_comment:

### 21. `ef006d458bad3b49`
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
- student_answer: 折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

human_passed:
human_failure_type:
human_comment:

### 22. `a8027fffd436418b`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 折旧是长期资产成本的分摊，会减少利润，但通常不代表当期现金流出，因为现金在购买时已经支付。

human_passed:
human_failure_type:
human_comment:

### 23. `d2ba14e5050c1df2`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `net_profit` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 根据课程材料，净利润为正不代表现金充足，因为净利润是基于权责发生制计算的。收入确认不等于收到现金，例如赊销会确认收入但现金未收到；费用确认也不等于当期现金付款，例如工资本月计提但下月发放；折旧和摊销会减少利润但通常不代表当期现金流出。所以利润为正时现金可能仍然紧张。

human_passed:
human_failure_type:
human_comment:

### 24. `75e013c030b465ac`
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
- student_answer: 出售咖啡是收入，应进入利润表；贷款不是收入，因为规则说利润表记录经营成果，不是所有现金流入。

human_passed:
human_failure_type:
human_comment:

### 25. `317a2d076fd28871`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 根据材料，在权责发生制下，收入确认不一定等于收到现金，所以本月完成服务后就可以确认收入。

human_passed:
human_failure_type:
human_comment:

### 26. `64c302be5617b405`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

human_passed:
human_failure_type:
human_comment:

### 27. `8f51208f00adaff0`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition；weak_transfer
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

human_passed:
human_failure_type:
human_comment:

### 28. `31a950c3a9c59009`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition；weak_transfer
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 折旧把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

human_passed:
human_failure_type:
human_comment:

### 29. `99080fad5a427dab`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `misconception_prone`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: expense_payment_confusion；折旧不影响利润表
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 折旧是成本分配，把烤箱的成本分摊到使用期间，所以会减少利润。但通常不代表今年再次付现金，因为现金已经在去年买烤箱时付过了。不过，我觉得折旧不应该算费用，因为今年根本没付出现金，没付钱就不应该影响利润。

human_passed:
human_failure_type:
human_comment:

### 30. `bae9fb5e0a7d3761`
- review_reason: no_course_baseline_fail
- node_id / condition / persona: `income_statement_boundary` / `no_course_baseline` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 无法从当前课程材料推出完整答案。

human_passed:
human_failure_type:
human_comment:
