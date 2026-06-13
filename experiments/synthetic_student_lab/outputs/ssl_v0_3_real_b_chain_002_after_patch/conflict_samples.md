# Conflict Samples

rule_pass_llm_fail_count: 1
rule_fail_llm_pass_listed_count: 13

## rule_pass_llm_fail

### 1. `5597cb7ad2db9ba6`
- node_id / condition / persona: `revenue_not_cash_receipt` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.6667 / 0.0
- matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
- missing_reasoning_points: 可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- student_answer: 根据材料，收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以可能确认收入但现金没有增加。

## rule_fail_llm_pass

### 1. `a306b041336c2cf6`
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付。材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用。因此，本月可以确认工资费用，费用发生与现金付款是两回事。

### 2. `7839880dba2edf96`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款不是来自销售商品或提供服务，所以不应作为营业收入。

### 3. `75e013c030b465ac`
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 规则说利润表记录经营成果，看收入、成本、费用，不是所有现金流入。贷款不是销售商品或提供服务，所以不是营业收入。

### 4. `ee1fd11f257df05d`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 规则说费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

### 5. `d3418a5ab6cd6832`
- node_id / condition / persona: `expense_recognition` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 因为材料说费用是为取得收入或维持经营发生的资源耗费，员工本月工作服务于本月经营，所以即使没付款，也应该记作本月费用。不过，我还是觉得没付钱就算费用有点奇怪，毕竟钱还没出去。

### 6. `54985bb56e4c1e7b`
- node_id / condition / persona: `accrual_vs_cash` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.25 / 1.0
- matched_reasoning_points: 权责发生制关注交易归属期间
- missing_reasoning_points: 满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月；现金制关注现金实际收付时间
- judge_matched_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月；现金制关注现金实际收付时间
- judge_missing_reasoning_points: -
- student_answer: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间。所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用。现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用。

### 7. `4e12cea729ecaa0a`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.67
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务，即使客户下月付款，也可能确认收入。

### 8. `d9da0fab40302700`
- node_id / condition / persona: `net_profit` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.67
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: 净利润可能包含未收现收入
- student_answer: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金。所以净利润为正不一定代表现金充足。

### 9. `b0d2294580e19c10`
- node_id / condition / persona: `expense_recognition` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.67
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- student_answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

### 10. `bcb84f9ceba8fce9`
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.667
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入确认不一定依赖现金已经到账；收入来自销售商品或提供服务
- judge_missing_reasoning_points: 完成交付或服务后可能满足收入确认条件
- student_answer: 规则说收入确认不一定等于收到现金，所以本月完成服务就可以确认收入。

### 11. `a15875025c353cca`
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.3333 / 1.0
- matched_reasoning_points: 利润表记录一段期间的经营成果
- missing_reasoning_points: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能形成收入进入利润表；而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表。

### 12. `b1e0b16dffbdf58f`
- node_id / condition / persona: `revenue_not_cash_receipt` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.3333 / 1.0
- matched_reasoning_points: 赊销可能先确认收入
- missing_reasoning_points: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_missing_reasoning_points: -
- student_answer: 规则说收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以本月利润表收入增加8000元，现金不变。收入不等于收款是因为收入确认不一定等于收到现金。

### 13. `1101b9b1a3e1bef6`
- node_id / condition / persona: `net_profit` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.6
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润为正不一定代表现金充足
- judge_missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- student_answer: 规则说净利润不等于现金，所以净利润为正不一定代表现金充足。
