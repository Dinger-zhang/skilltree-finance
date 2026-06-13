# Conflict Samples

rule_pass_llm_fail_count: 1
rule_fail_llm_pass_listed_count: 20

## rule_pass_llm_fail

### 1. `b7c79c56ca63ca4c`
- node_id / condition / persona: `revenue_not_cash_receipt` / `hidden_transfer` / `misconception_prone`
- rule_score / judge_score: 0.6667 / 0.33
- matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
- missing_reasoning_points: 可能形成应收账款而不是现金流入
- judge_matched_reasoning_points: 未收现金时现金不一定增加
- judge_missing_reasoning_points: 赊销可能先确认收入；可能形成应收账款而不是现金流入
- student_answer: 本月利润表上不应该确认收入，因为没有收到现金，现金也没变化。收入必须是在收到现金时才能确认，所以收入等于收款。赊销商品没收到钱，所以不能算收入。

## rule_fail_llm_pass

### 1. `f599d9bb1b2418b3`
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，利润表记录经营成果，重点是收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，因此不应作为营业收入进入利润表。

### 2. `1d2f4a510281905d`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款属于资金来源变化，不是来自销售商品或提供服务，不反映经营成果，所以不应作为营业收入进入利润表。

### 3. `4e12cea729ecaa0a`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- student_answer: 根据材料，收入确认通常看服务是否完成或商品是否交付，而不是看是否收到现金。本月服务已完成，所以即使客户下月付款，本月仍可确认收入。

### 4. `9f925b57d5ef9706`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，在权责发生制下，收入确认基于服务是否完成而非款项是否收到。本月已完成服务并交付，满足了收入确认条件，因此即使客户下月付款，本月仍可确认收入。

### 5. `5d70ff16349ce408`
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- student_answer: 根据材料，本月可以确认收入，因为服务已完成并交付，收入确认关注的是是否赚到（即完成服务），而不是是否收到现金。客户下月付款不影响本月的收入确认。

### 6. `ff04d3360d229fb1`
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 7. `ef006d458bad3b49`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 8. `a8027fffd436418b`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 折旧是长期资产成本的分摊，会减少利润，但通常不代表当期现金流出，因为现金在购买时已经支付。

### 9. `d2ba14e5050c1df2`
- node_id / condition / persona: `net_profit` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: -
- student_answer: 根据课程材料，净利润为正不代表现金充足，因为净利润是基于权责发生制计算的。收入确认不等于收到现金，例如赊销会确认收入但现金未收到；费用确认也不等于当期现金付款，例如工资本月计提但下月发放；折旧和摊销会减少利润但通常不代表当期现金流出。所以利润为正时现金可能仍然紧张。

### 10. `75e013c030b465ac`
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 出售咖啡是收入，应进入利润表；贷款不是收入，因为规则说利润表记录经营成果，不是所有现金流入。

### 11. `317a2d076fd28871`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- judge_missing_reasoning_points: -
- student_answer: 根据材料，在权责发生制下，收入确认不一定等于收到现金，所以本月完成服务后就可以确认收入。

### 12. `64c302be5617b405`
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 13. `8f51208f00adaff0`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 14. `31a950c3a9c59009`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 折旧把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 15. `99080fad5a427dab`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `misconception_prone`
- rule_score / judge_score: 0.0 / 1.0
- matched_reasoning_points: -
- missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- judge_missing_reasoning_points: -
- student_answer: 折旧是成本分配，把烤箱的成本分摊到使用期间，所以会减少利润。但通常不代表今年再次付现金，因为现金已经在去年买烤箱时付过了。不过，我觉得折旧不应该算费用，因为今年根本没付出现金，没付钱就不应该影响利润。

### 16. `49702d7924a64a2f`
- node_id / condition / persona: `gross_margin` / `chain_so_far` / `novice_closed_book`
- rule_score / judge_score: 0.0 / 0.8
- matched_reasoning_points: -
- missing_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- judge_matched_reasoning_points: 毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- judge_missing_reasoning_points: 毛利等于收入减销售成本
- student_answer: 根据材料，毛利率是毛利除以收入，而净利润还需要减去其他费用和折旧摊销等，所以毛利率高不一定净利润高。材料说‘毛利还不是净利润’，因此不能直接等同。

### 17. `1101b9b1a3e1bef6`
- node_id / condition / persona: `net_profit` / `chain_so_far` / `rote_memorizer`
- rule_score / judge_score: 0.0 / 0.67
- matched_reasoning_points: -
- missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- judge_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含非现金费用所以不等于现金
- judge_missing_reasoning_points: 净利润可能包含未收现收入
- student_answer: 净利润为正不一定代表现金充足，因为净利润不等于现金。材料说净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金。

### 18. `16d7b0406bfc8948`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.67
- matched_reasoning_points: -
- missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- judge_missing_reasoning_points: 利润表记录一段期间的经营成果
- student_answer: 银行借款收到了现金，按理说应该算收入，但材料说借款只是资金来源变化，不是经营收入，所以不能进利润表。可能是因为借款不是通过卖商品或服务获得的，所以只能算资金来源变化。

### 19. `876c4b3ac062bd2b`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `misconception_prone`
- rule_score / judge_score: 0.0 / 0.67
- matched_reasoning_points: -
- missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- judge_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款
- judge_missing_reasoning_points: 工资费用会减少本期利润
- student_answer: 根据材料，费用确认规则说费用是为取得收入或维持经营发生的资源耗费，工资服务于本月经营，所以即使下月才发，也应当作为本月费用。但我还是觉得没付款就不能算费用，费用应该在付款时才发生。

### 20. `a15875025c353cca`
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `novice_closed_book`
- rule_score / judge_score: 0.3333 / 1.0
- matched_reasoning_points: 利润表记录一段期间的经营成果
- missing_reasoning_points: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- judge_missing_reasoning_points: -
- student_answer: 咖啡店向顾客出售咖啡获得的收入更可能进入利润表作为经营成果，因为它来自销售商品或提供服务。贷款是从银行借入的资金，不是营业收入，因为它不是销售所得，而是融资活动。根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入，所以贷款不属于营业收入。
