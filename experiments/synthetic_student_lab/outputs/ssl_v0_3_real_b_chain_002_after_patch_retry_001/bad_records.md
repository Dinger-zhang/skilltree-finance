# Bad Records

total_bad_records: 55

## 1. `a15875025c353cca`
- reason: error_message, judge_error
- run_id: `a15875025c353cca`
- node_id: `income_statement_boundary`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- student_answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能进入利润表作为收入。而银行借款只是资金来源变化，不是经营收入，所以不应进入利润表。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 2. `abe2e7353f1ea759`
- reason: error_message, judge_error
- run_id: `abe2e7353f1ea759`
- node_id: `revenue_recognition`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 无法从当前课程材料推出完整答案
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 3. `4e12cea729ecaa0a`
- reason: error_message, judge_error
- run_id: `4e12cea729ecaa0a`
- node_id: `revenue_recognition`
- condition: `node_only`
- student_persona: `novice_closed_book`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务并交付，符合收入确认条件，所以即使客户下月付款，本月仍可能确认收入。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 4. `9f925b57d5ef9706`
- reason: error_message, empty_student_answer, judge_error
- run_id: `9f925b57d5ef9706`
- node_id: `revenue_recognition`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 5. `5d70ff16349ce408`
- reason: error_message, empty_student_answer
- run_id: `5d70ff16349ce408`
- node_id: `revenue_recognition`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 6. `58601fac79dbc131`
- reason: error_message, empty_student_answer
- run_id: `58601fac79dbc131`
- node_id: `revenue_not_cash_receipt`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 7. `72dc184657b65977`
- reason: error_message, empty_student_answer
- run_id: `72dc184657b65977`
- node_id: `revenue_not_cash_receipt`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 8. `bca00219ea6b43d5`
- reason: error_message, judge_error
- run_id: `bca00219ea6b43d5`
- node_id: `depreciation_amortization`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 无法从当前课程材料推出完整答案
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 9. `ff04d3360d229fb1`
- reason: error_message, judge_error
- run_id: `ff04d3360d229fb1`
- node_id: `depreciation_amortization`
- condition: `node_only`
- student_persona: `novice_closed_book`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以折旧减少利润是因为成本分摊，但不需要当期付出现金。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 10. `a8027fffd436418b`
- reason: error_message, judge_error
- run_id: `a8027fffd436418b`
- node_id: `depreciation_amortization`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以今年的折旧会影响利润，但通常不代表今年再次付现金。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 11. `95fde13b00513088`
- reason: error_message, judge_error
- run_id: `95fde13b00513088`
- node_id: `gross_margin`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 无法从当前课程材料推出完整答案
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 12. `c8a1cd8fb15a26c6`
- reason: error_message, judge_error
- run_id: `c8a1cd8fb15a26c6`
- node_id: `gross_margin`
- condition: `node_only`
- student_persona: `novice_closed_book`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 根据材料，毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。材料没有提到净利润的计算，所以无法从当前课程材料推出完整答案。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 13. `75e013c030b465ac`
- reason: error_message, empty_student_answer
- run_id: `75e013c030b465ac`
- node_id: `income_statement_boundary`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 14. `bcb84f9ceba8fce9`
- reason: error_message, empty_student_answer
- run_id: `bcb84f9ceba8fce9`
- node_id: `revenue_recognition`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 15. `e37cee0bc8cfc2cc`
- reason: error_message, empty_student_answer
- run_id: `e37cee0bc8cfc2cc`
- node_id: `revenue_not_cash_receipt`
- condition: `no_course_baseline`
- student_persona: `rote_memorizer`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 16. `4ab92215771f559d`
- reason: error_message, empty_student_answer
- run_id: `4ab92215771f559d`
- node_id: `revenue_not_cash_receipt`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 17. `e4e4b528edb49ba4`
- reason: error_message, empty_student_answer
- run_id: `e4e4b528edb49ba4`
- node_id: `revenue_not_cash_receipt`
- condition: `chain_so_far`
- student_persona: `rote_memorizer`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 18. `b1e0b16dffbdf58f`
- reason: error_message, empty_student_answer
- run_id: `b1e0b16dffbdf58f`
- node_id: `revenue_not_cash_receipt`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 19. `81c401580ed00066`
- reason: error_message, empty_student_answer
- run_id: `81c401580ed00066`
- node_id: `expense_recognition`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 20. `6d709799a10a5dcb`
- reason: error_message, empty_student_answer
- run_id: `6d709799a10a5dcb`
- node_id: `depreciation_amortization`
- condition: `no_course_baseline`
- student_persona: `rote_memorizer`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 21. `64c302be5617b405`
- reason: error_message, empty_student_answer
- run_id: `64c302be5617b405`
- node_id: `depreciation_amortization`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 22. `8f51208f00adaff0`
- reason: error_message, empty_student_answer
- run_id: `8f51208f00adaff0`
- node_id: `depreciation_amortization`
- condition: `chain_so_far`
- student_persona: `rote_memorizer`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 23. `89a5e43e27ea7c6e`
- reason: error_message, empty_student_answer
- run_id: `89a5e43e27ea7c6e`
- node_id: `gross_margin`
- condition: `chain_so_far`
- student_persona: `rote_memorizer`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 24. `91911382ccb93783`
- reason: error_message, empty_student_answer
- run_id: `91911382ccb93783`
- node_id: `gross_margin`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。 如何推出毛利和毛利率？它们还没有扣除哪些费用？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 25. `bd12c173fbb8f4f9`
- reason: error_message, empty_student_answer
- run_id: `bd12c173fbb8f4f9`
- node_id: `net_profit`
- condition: `no_course_baseline`
- student_persona: `rote_memorizer`
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 26. `01668fda41cabddc`
- reason: error_message, empty_student_answer
- run_id: `01668fda41cabddc`
- node_id: `net_profit`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 27. `4e0aad17637d82ae`
- reason: error_message, empty_student_answer
- run_id: `4e0aad17637d82ae`
- node_id: `net_profit`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 28. `fb09023b6c461873`
- reason: error_message, empty_student_answer, judge_error
- run_id: `fb09023b6c461873`
- node_id: `accrual_vs_cash`
- condition: `no_course_baseline`
- student_persona: `rote_memorizer`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 29. `db9a7f70f02cb56e`
- reason: error_message, judge_error
- run_id: `db9a7f70f02cb56e`
- node_id: `accrual_vs_cash`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 规则说：权责发生制关注交易归属期间，现金制关注现金实际收付时间。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 30. `74f9fc040694cb23`
- reason: error_message, judge_error
- run_id: `74f9fc040694cb23`
- node_id: `accrual_vs_cash`
- condition: `chain_so_far`
- student_persona: `rote_memorizer`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 规则说：权责发生制关注交易归属期间，现金制关注现金实际收付时间。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 31. `6f9da756a4a58197`
- reason: error_message, judge_error
- run_id: `6f9da756a4a58197`
- node_id: `accrual_vs_cash`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 咨询公司 6 月完成服务，7 月收款；6 月发生房租但 7 月付款。 权责发生制下 6 月应如何看收入和费用？它和现金制的关注点有什么不同？
- student_answer: 规则说：权责发生制关注交易归属期间，现金制关注现金实际收付时间。所以6月完成服务，收入属于6月；6月发生房租，费用属于6月。现金制下，7月收款才算收入，7月付款才算费用。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 32. `d7b6530f587d8487`
- reason: error_message, judge_error
- run_id: `d7b6530f587d8487`
- node_id: `income_statement_boundary`
- condition: `no_course_baseline`
- student_persona: `misconception_prone`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 无法从当前课程材料推出完整答案
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 33. `8bff312837528c9a`
- reason: error_message, judge_error
- run_id: `8bff312837528c9a`
- node_id: `income_statement_boundary`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 因为借款是收到的钱，所以应该算收入，但材料说不是所有收到的钱都是收入，借款不是卖东西得来的，所以不能进利润表。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 34. `16d7b0406bfc8948`
- reason: error_message, empty_student_answer, judge_error
- run_id: `16d7b0406bfc8948`
- node_id: `income_statement_boundary`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 35. `bee48c2ac1d6d055`
- reason: error_message, judge_error
- run_id: `bee48c2ac1d6d055`
- node_id: `income_statement_boundary`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- student_answer: 咖啡店卖咖啡的收入应该进利润表，因为那是经营成果。贷款不是营业收入，因为材料说不是所有现金流入都代表经营收入，借款只是资金来源变化。但是，我觉得贷款收到的钱也是钱，应该也算收入吧？不过材料说不能算，那就不算吧。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 36. `ae56893e7157dcb5`
- reason: error_message, empty_student_answer, judge_error
- run_id: `ae56893e7157dcb5`
- node_id: `revenue_recognition`
- condition: `no_course_baseline`
- student_persona: `misconception_prone`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 37. `4b6cc7d618879fba`
- reason: error_message, empty_student_answer, judge_error
- run_id: `4b6cc7d618879fba`
- node_id: `revenue_recognition`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 38. `3982efb926a2baf0`
- reason: error_message, empty_student_answer, judge_error
- run_id: `3982efb926a2baf0`
- node_id: `revenue_recognition`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 39. `90ffab514a6ce477`
- reason: error_message, empty_student_answer, judge_error
- run_id: `90ffab514a6ce477`
- node_id: `revenue_recognition`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 40. `8048e0b62e3b12be`
- reason: error_message, empty_student_answer, judge_error
- run_id: `8048e0b62e3b12be`
- node_id: `revenue_not_cash_receipt`
- condition: `no_course_baseline`
- student_persona: `misconception_prone`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 41. `1b8d3d51286c162a`
- reason: error_message, empty_student_answer, judge_error
- run_id: `1b8d3d51286c162a`
- node_id: `revenue_not_cash_receipt`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 42. `b7c79c56ca63ca4c`
- reason: error_message, empty_student_answer, judge_error
- run_id: `b7c79c56ca63ca4c`
- node_id: `revenue_not_cash_receipt`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 43. `7c7ea0608c54061f`
- reason: error_message, empty_student_answer, judge_error
- run_id: `7c7ea0608c54061f`
- node_id: `expense_recognition`
- condition: `no_course_baseline`
- student_persona: `misconception_prone`
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 44. `d3418a5ab6cd6832`
- reason: error_message, empty_student_answer, judge_error
- run_id: `d3418a5ab6cd6832`
- node_id: `expense_recognition`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 45. `876c4b3ac062bd2b`
- reason: error_message, empty_student_answer, judge_error
- run_id: `876c4b3ac062bd2b`
- node_id: `expense_recognition`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 46. `83e7249776e6fea2`
- reason: error_message, empty_student_answer
- run_id: `83e7249776e6fea2`
- node_id: `depreciation_amortization`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 47. `801b3238e4c0630e`
- reason: error_message, empty_student_answer
- run_id: `801b3238e4c0630e`
- node_id: `depreciation_amortization`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 48. `99080fad5a427dab`
- reason: error_message, empty_student_answer
- run_id: `99080fad5a427dab`
- node_id: `depreciation_amortization`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 49. `5432e54e4b2b9174`
- reason: error_message, empty_student_answer
- run_id: `5432e54e4b2b9174`
- node_id: `gross_margin`
- condition: `no_course_baseline`
- student_persona: `misconception_prone`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 50. `84591106c3523017`
- reason: error_message, empty_student_answer
- run_id: `84591106c3523017`
- node_id: `gross_margin`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 51. `5e8f09219a82b69d`
- reason: error_message, judge_error
- run_id: `5e8f09219a82b69d`
- node_id: `gross_margin`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 毛利率高说明收入减去销售成本后剩下的比例大，但净利润还要扣掉很多其他费用，比如工资、房租、折旧这些。不过我觉得如果毛利率高，那净利润应该也不会太差吧，毕竟收入多成本少，利润肯定高。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 52. `a3c7062b5c479e04`
- reason: error_message, empty_student_answer
- run_id: `a3c7062b5c479e04`
- node_id: `net_profit`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 53. `b498fa1bf5bd5471`
- reason: error_message, judge_error
- run_id: `b498fa1bf5bd5471`
- node_id: `accrual_vs_cash`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 权责发生制和现金制的核心区别是：权责发生制关注交易归属期间，现金制关注现金实际收付时间。但我觉得，没收到钱就不算收入，没付款就没有费用，所以权责发生制其实也是看现金的。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 54. `1e07b89d2e8529b1`
- reason: error_message, judge_error
- run_id: `1e07b89d2e8529b1`
- node_id: `accrual_vs_cash`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 权责发生制和现金制的核心区别是：权责发生制关注交易归属期间，现金制关注现金实际收付时间。但我觉得权责发生制其实也关注现金，没收到钱就不应该算收入，没付款就不应该有费用。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 55. `3d22b87b3201f13d`
- reason: error_message, judge_error
- run_id: `3d22b87b3201f13d`
- node_id: `accrual_vs_cash`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 咨询公司 6 月完成服务，7 月收款；6 月发生房租但 7 月付款。 权责发生制下 6 月应如何看收入和费用？它和现金制的关注点有什么不同？
- student_answer: 权责发生制下，6月应该确认收入和费用，因为服务已经完成，房租已经发生，但没收到钱也没付钱，所以收入和费用都不算。现金制下，6月没收到钱也没付钱，所以6月没有收入和费用，7月收款和付款时才确认。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry
