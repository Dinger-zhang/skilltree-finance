# Human Review Samples

total_samples: 30

## Coverage

- student_persona: {'misconception_prone': 6, 'novice_closed_book': 18, 'rote_memorizer': 6}
- condition: {'chain_so_far': 7, 'node_only': 10, 'hidden_transfer': 9, 'no_course_baseline': 4}
- node_id: {'revenue_not_cash_receipt': 3, 'accrual_vs_cash': 3, 'net_profit': 3, 'income_statement_boundary': 3, 'revenue_recognition': 7, 'expense_recognition': 7, 'gross_margin': 1, 'depreciation_amortization': 3}
- conflict_type: {'rule_pass_llm_fail': 1, 'both_fail': 12, 'rule_fail_llm_pass': 16, 'both_pass': 1}

## Samples

### 1. `0e9191c369ce91ef`
- review_reason: all_rule_pass_llm_fail
- node_id / condition / persona: `revenue_not_cash_receipt` / `chain_so_far` / `misconception_prone`
- rule_score / judge_score: 0.6667 / 0.5
- rule_passed / judge_passed: True / False
- conflict_type: `rule_pass_llm_fail`
- misconception_tags: revenue_cash_confusion；收入增加就等于现金增加。
- matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
- missing_reasoning_points: 可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
- judge_missing_reasoning_points: 可能形成应收账款而不是现金流入
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 因为收入确认看的是商品是否卖出，不是看有没有收到钱。赊销时商品已经卖出，所以可以确认收入，但现金还没收到，所以现金没有增加。不过我觉得这有点奇怪，没收到钱怎么能算收入呢？收入增加应该意味着现金也增加才对。

human_passed:
human_failure_type:
human_comment:

### 2. `9ff4d5c34b4b8a1f`
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

### 3. `7310bfd7bfc9d79e`
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

### 4. `139b652418ab1cf8`
- review_reason: accrual_vs_cash_node_only_failure
- node_id / condition / persona: `accrual_vs_cash` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: expense_payment_confusion；revenue_cash_confusion；权责发生制更关注现金是否实际收付。；没付款就没有费用。
- matched_reasoning_points: -
- missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期；现金制关注现金实际收付时间
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 权责发生制和现金制的核心区别是：权责发生制关注现金是否实际收付，而现金制关注交易归属期间。没付款就没有费用。

human_passed:
human_failure_type:
human_comment:

### 5. `787b5003cc442550`
- review_reason: net_profit_node_only_failure
- node_id / condition / persona: `net_profit` / `node_only` / `novice_closed_book`
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

human_passed:
human_failure_type:
human_comment:

### 6. `426d4cdc6b395ec8`
- review_reason: net_profit_node_only_failure
- node_id / condition / persona: `net_profit` / `node_only` / `misconception_prone`
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

human_passed:
human_failure_type:
human_comment:

### 7. `8a26a66f246d453f`
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
- student_answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能进入利润表作为收入。而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表。

human_passed:
human_failure_type:
human_comment:

### 8. `585942f7bc6db083`
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
- student_answer: 根据材料，批发商本月赊销8000元商品，客户45天后付款。材料说“收入记录赚到的经营成果；收款记录现金进入。赊销会让收入和现金流入出现时间差。”所以本月利润表应该确认8000元收入，因为商品已经卖出，符合收入确认条件。现金方面，因为还没收到钱，所以现金没有增加。收入不等于收款，因为收入确认关注的是赚到经营成果，而不是收到现金。

human_passed:
human_failure_type:
human_comment:

### 9. `7a2d69dfbbeea172`
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
- student_answer: 没收到钱就不能算收入，因为客户下月才付款，所以本月不能确认收入。完成服务不等于收到现金，收入确认必须等到实际收款。

human_passed:
human_failure_type:
human_comment:

### 10. `4c33192e51dcb12c`
- review_reason: hidden_transfer_fail
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.3
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: expense_payment_confusion；没付款就没有费用
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 材料说费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。但我觉得工资还没付出去，没付款就没有费用，所以本月不应该确认工资费用。

human_passed:
human_failure_type:
human_comment:

### 11. `c51e61ab690c5041`
- review_reason: node_coverage_gross_margin
- node_id / condition / persona: `gross_margin` / `chain_so_far` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.3
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: profit_cash_confusion；revenue_cash_confusion；毛利率就是净利率。；毛利高就一定最终赚钱。
- matched_reasoning_points: -
- missing_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- judge_matched_reasoning_points: 毛利等于收入减销售成本
- judge_missing_reasoning_points: 毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 毛利率高说明收入减去销售成本后剩下的钱多，但净利润还要扣掉其他费用，比如折旧、工资这些。不过我觉得毛利率高的话，净利润应该也不会太差吧，毕竟毛利高说明赚得多，那现金也应该多，净利润肯定也高。

human_passed:
human_failure_type:
human_comment:

### 12. `6ac87983201c5f3d`
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
- student_answer: 根据材料，利润表记录的是经营成果，而不是所有现金流入。银行借款属于资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

human_passed:
human_failure_type:
human_comment:

### 13. `07a7bc27537b666b`
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
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务并交付，符合收入确认条件，所以即使客户下月付款，本月仍可能确认收入。

human_passed:
human_failure_type:
human_comment:

### 14. `ae2796aa8b8a9207`
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
- student_answer: 根据材料，收入确认关注的是服务是否完成或商品是否交付，而不是是否收到现金。材料中设计公司本月完成并交付海报，所以本月可能确认收入。但客户下月付款，这属于现金流入的时间差异，不影响收入确认。

human_passed:
human_failure_type:
human_comment:

### 15. `282b0ca91b15a302`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: -
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但员工本月已经完成了工作，耗费服务于本期经营，因此可以作为本月费用。

human_passed:
human_failure_type:
human_comment:

### 16. `2461ec4dfa2f2a24`
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
- student_answer: 根据材料，费用确认关注的是耗费是否服务于本期经营，而不是现金支付时间。员工本月完成工作，工资虽下月发放，但耗费服务于本月，所以应作为本月费用。

human_passed:
human_failure_type:
human_comment:

### 17. `79ffc109344fe36b`
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
- student_answer: 根据材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付。材料中员工已经完成本月工作，说明耗费服务于本期经营，因此本月可能确认工资费用。费用发生不一定等于当期现金付款。

human_passed:
human_failure_type:
human_comment:

### 18. `b488edcce2fd39d2`
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
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

human_passed:
human_failure_type:
human_comment:

### 19. `72309d416d4e32b1`
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

### 20. `28922aa745eb2000`
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
- student_answer: 根据课程材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以今年的折旧会影响利润，但通常不代表今年再次付现金。

human_passed:
human_failure_type:
human_comment:

### 21. `674855dfd46b5316`
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
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收款，费用发生也不等于现金付款，折旧和摊销会减少利润但不代表现金流出。所以净利润是收入减成本和费用的结果，但现金可能因为赊销、未付款项或折旧等原因而不足。

human_passed:
human_failure_type:
human_comment:

### 22. `8e09a404abd044c5`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: 完成交付或服务后可能满足收入确认条件
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 规则说：收入确认不一定等于收到现金。所以本月完成服务，即使客户下月付款，仍可能确认收入。

human_passed:
human_failure_type:
human_comment:

### 23. `38a7bf97530f3c27`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 规则说：收入通常来自销售商品或提供服务；在权责发生制下，收入确认不一定等于收到现金。所以本月完成服务，即使客户下月付款，仍可能确认收入。

human_passed:
human_failure_type:
human_comment:

### 24. `ee674563f4bc3832`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- student_answer: 规则说：收入确认不一定等于收到现金。本月完成并交付海报，服务已完成，所以本月可能确认收入。收到现金是下月的事，不影响本月收入确认。

human_passed:
human_failure_type:
human_comment:

### 25. `7d4cbb5e8302ca64`
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

### 26. `1263b89da49fd4bd`
- review_reason: high_judge_low_rule_rule_fail_llm_pass
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- rule_passed / judge_passed: False / True
- conflict_type: `rule_fail_llm_pass`
- misconception_tags: rote_repetition
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月可能确认工资费用，因为员工已经完成本月工作，耗费服务于本期经营，即使工资下月发放。

human_passed:
human_failure_type:
human_comment:

### 27. `28f8b62354b3b43f`
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

### 28. `c8cc6179f7cac6b4`
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

### 29. `43a82effa4627632`
- review_reason: no_course_baseline_fail
- node_id / condition / persona: `revenue_not_cash_receipt` / `no_course_baseline` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: insufficient_materials
- matched_reasoning_points: -
- missing_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 无法从当前课程材料推出完整答案

human_passed:
human_failure_type:
human_comment:

### 30. `1fbe8426edcfd641`
- review_reason: no_course_baseline_fail
- node_id / condition / persona: `expense_recognition` / `no_course_baseline` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.0
- rule_passed / judge_passed: False / False
- conflict_type: `both_fail`
- misconception_tags: insufficient_materials
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 无法从当前课程材料推出完整答案

human_passed:
human_failure_type:
human_comment:
