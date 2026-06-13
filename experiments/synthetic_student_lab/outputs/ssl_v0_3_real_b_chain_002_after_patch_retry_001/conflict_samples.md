# Conflict Samples

rule_pass_llm_fail_count: 2
rule_fail_llm_pass_listed_count: 18

## rule_pass_llm_fail

### 1. `c8a1cd8fb15a26c6`
- node_id / condition / persona: `gross_margin` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.6667 / 0.0
- matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入
- missing_reasoning_points: 毛利还没有扣除销售管理研发财务等期间费用
- judge_matched_reasoning_points: -
- judge_missing_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- student_answer: 根据材料，毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。材料没有提到净利润的计算，所以无法从当前课程材料推出完整答案。

### 2. `cec6e305439237b9`
- node_id / condition / persona: `gross_margin` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.6667 / 0.67
- matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入
- missing_reasoning_points: 毛利还没有扣除销售管理研发财务等期间费用
- judge_matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入
- judge_missing_reasoning_points: 毛利还没有扣除销售管理研发财务等期间费用
- student_answer: 规则说：毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。所以毛利率高不等于净利润一定高。

## rule_fail_llm_pass

### 1. `f599d9bb1b2418b3`
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

### 2. `79c64d2597f89e85`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。员工已经完成本月工作，但工资下月发放，耗费服务于本期经营，所以应记入本期费用。

### 3. `a306b041336c2cf6`
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 根据材料，费用确认关注的是耗费是否服务于本期经营，而不是是否支付现金。员工本月工作服务于本期经营，所以本月可以确认工资费用。材料说“费用发生不一定等于当期现金付款”，所以下月发工资不影响本月确认费用。

### 4. `ef006d458bad3b49`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 5. `bf2dc9120ce2ddfd`
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入。

### 6. `7839880dba2edf96`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款不是销售商品或提供服务，所以不应作为营业收入。

### 7. `b0d2294580e19c10`
- node_id / condition / persona: `expense_recognition` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

### 8. `ee1fd11f257df05d`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- student_answer: 规则说费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

### 9. `31a950c3a9c59009`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 规则说折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 10. `d2ba14e5050c1df2`
- node_id / condition / persona: `net_profit` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.95
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收款，费用发生不等于现金支付，折旧和摊销会减少利润但不代表现金流出。所以，净利润为正时，可能因为赊销、未付款的费用或折旧等原因，现金并没有同步增加。

### 11. `317a2d076fd28871`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.9
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入确认不一定依赖现金已经到账；完成交付或服务后可能满足收入确认条件
- judge_missing_reasoning_points: 收入来自销售商品或提供服务
- student_answer: 规则说：收入确认不一定等于收到现金。所以本月完成服务，即使客户下月付款，仍可能确认收入。

### 12. `1d2f4a510281905d`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.8
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

### 13. `54985bb56e4c1e7b`
- node_id / condition / persona: `accrual_vs_cash` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.25 / 1.0
- matched_reasoning_points: 权责发生制关注交易归属期间
- missing_reasoning_points: 满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月；现金制关注现金实际收付时间
- judge_matched_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月；现金制关注现金实际收付时间
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，权责发生制关注交易归属期间，而不是现金实际收付时间。所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用。现金制则关注现金实际收付时间，所以6月没有收款和付款，收入和费用都不确认。

### 14. `1cfaba10d861f9c4`
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.75
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但员工已经完成本月工作，耗费服务于本期经营，因此应作为本月费用。

### 15. `8305819be1ae4571`
- node_id / condition / persona: `net_profit` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.75
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_missing_reasoning_points: 本例净利润为 8000 元
- student_answer: 根据材料，净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。材料说收入记录赚到的经营成果，收款记录现金进入，赊销会让收入和现金流入出现时间差。所以净利润为正仍不必然表示现金充足，因为可能有赊销等未收现的情况。

### 16. `d9da0fab40302700`
- node_id / condition / persona: `net_profit` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.7
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: 净利润可能包含未收现收入
- student_answer: 根据材料，净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。所以净利润为正不一定代表现金充足。

### 17. `57d885de1199748c`
- node_id / condition / persona: `revenue_not_cash_receipt` / `node_only` / `misconception_prone`
- rule_score / judge_score: 0.3333 / 1.0
- matched_reasoning_points: 赊销可能先确认收入
- missing_reasoning_points: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- judge_missing_reasoning_points: -
- student_answer: 因为赊销时商品已经卖出，所以确认收入，但没收到钱，所以现金没增加。

### 18. `5a56b9a3f8278455`
- node_id / condition / persona: `accrual_vs_cash` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.5 / 0.75
- matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- missing_reasoning_points: 满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- judge_matched_reasoning_points: 权责发生制关注交易归属期间；现金制关注现金实际收付时间
- judge_missing_reasoning_points: 满足条件时未收款也可能确认收入；已发生费用即使未付款也可能归入本期
- student_answer: 根据材料，权责发生制关注交易归属期间，现金制关注现金实际收付时间。
