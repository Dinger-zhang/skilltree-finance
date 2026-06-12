# Conflict Samples

rule_pass_llm_fail_count: 1
rule_fail_llm_pass_listed_count: 20

## rule_pass_llm_fail

### 1. `0e9191c369ce91ef`
- node_id / condition / persona: `revenue_not_cash_receipt` / `chain_so_far` / `misconception_prone`
- rule_score / judge_score: 0.6667 / 0.5
- matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
- missing_reasoning_points: 可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
- judge_missing_reasoning_points: 可能形成应收账款而不是现金流入
- student_answer: 因为收入确认看的是商品是否卖出，不是看有没有收到钱。赊销时商品已经卖出，所以可以确认收入，但现金还没收到，所以现金没有增加。不过我觉得这有点奇怪，没收到钱怎么能算收入呢？收入增加应该意味着现金也增加才对。

## rule_fail_llm_pass

### 1. `6ac87983201c5f3d`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 根据材料，利润表记录的是经营成果，而不是所有现金流入。银行借款属于资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

### 2. `07a7bc27537b666b`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务并交付，符合收入确认条件，所以即使客户下月付款，本月仍可能确认收入。

### 3. `ae2796aa8b8a9207`
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- student_answer: 根据材料，收入确认关注的是服务是否完成或商品是否交付，而不是是否收到现金。材料中设计公司本月完成并交付海报，所以本月可能确认收入。但客户下月付款，这属于现金流入的时间差异，不影响收入确认。

### 4. `282b0ca91b15a302`
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但员工本月已经完成了工作，耗费服务于本期经营，因此可以作为本月费用。

### 5. `2461ec4dfa2f2a24`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 根据材料，费用确认关注的是耗费是否服务于本期经营，而不是现金支付时间。员工本月完成工作，工资虽下月发放，但耗费服务于本月，所以应作为本月费用。

### 6. `79ffc109344fe36b`
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 根据材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付。材料中员工已经完成本月工作，说明耗费服务于本期经营，因此本月可能确认工资费用。费用发生不一定等于当期现金付款。

### 7. `b488edcce2fd39d2`
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 8. `72309d416d4e32b1`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 9. `28922aa745eb2000`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以今年的折旧会影响利润，但通常不代表今年再次付现金。

### 10. `674855dfd46b5316`
- node_id / condition / persona: `net_profit` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收款，费用发生也不等于现金付款，折旧和摊销会减少利润但不代表现金流出。所以净利润是收入减成本和费用的结果，但现金可能因为赊销、未付款项或折旧等原因而不足。

### 11. `8e09a404abd044c5`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: 完成交付或服务后可能满足收入确认条件
- student_answer: 规则说：收入确认不一定等于收到现金。所以本月完成服务，即使客户下月付款，仍可能确认收入。

### 12. `38a7bf97530f3c27`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- student_answer: 规则说：收入通常来自销售商品或提供服务；在权责发生制下，收入确认不一定等于收到现金。所以本月完成服务，即使客户下月付款，仍可能确认收入。

### 13. `ee674563f4bc3832`
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- student_answer: 规则说：收入确认不一定等于收到现金。本月完成并交付海报，服务已完成，所以本月可能确认收入。收到现金是下月的事，不影响本月收入确认。

### 14. `7d4cbb5e8302ca64`
- node_id / condition / persona: `expense_recognition` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

### 15. `1263b89da49fd4bd`
- node_id / condition / persona: `expense_recognition` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_missing_reasoning_points: -
- student_answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月可能确认工资费用，因为员工已经完成本月工作，耗费服务于本期经营，即使工资下月发放。

### 16. `b22acdb7d11176f2`
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 规则说：折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 17. `4061f0b899f30c3e`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 材料说折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 18. `7256fc8eb185966f`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 规则说：折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 19. `fcf96c5662b0148f`
- node_id / condition / persona: `net_profit` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；本例净利润为 8000 元；净利润可能包含未收现收入或非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- student_answer: 规则说净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。材料说收入记录赚到的经营成果，收款记录现金进入，赊销会让收入和现金流入出现时间差。所以净利润为正仍不必然表示现金充足。

### 20. `72822b00a8aa744d`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `misconception_prone`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 折旧会减少利润，因为折旧是费用，但折旧不是现金流出，因为买资产的时候已经付过钱了，所以折旧不会影响现金。
