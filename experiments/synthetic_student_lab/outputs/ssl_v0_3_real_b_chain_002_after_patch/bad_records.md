# Bad Records

total_bad_records: 60

## 1. `f599d9bb1b2418b3`
- reason: error_message, judge_error
- run_id: `f599d9bb1b2418b3`
- node_id: `income_statement_boundary`
- condition: `node_only`
- student_persona: `novice_closed_book`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款属于资金来源变化，不是销售商品或提供服务产生的，所以不应作为营业收入进入利润表。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 2. `1d2f4a510281905d`
- reason: error_message, judge_error
- run_id: `1d2f4a510281905d`
- node_id: `income_statement_boundary`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 根据材料，利润表记录的是经营成果，而不是所有现金流入。银行借款是资金来源的变化，不是销售商品或提供服务产生的收入，所以不应作为营业收入进入利润表。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 3. `9f925b57d5ef9706`
- reason: error_message, judge_error
- run_id: `9f925b57d5ef9706`
- node_id: `revenue_recognition`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 根据材料，收入确认关注的是赚到收入而不是收到现金。材料中的设计公司本月完成并交付海报，即使客户下月付款，本月仍可能确认收入，因为服务已经完成。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 4. `5d70ff16349ce408`
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

## 5. `58601fac79dbc131`
- reason: error_message, empty_student_answer, judge_error
- run_id: `58601fac79dbc131`
- node_id: `revenue_not_cash_receipt`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 6. `585ba193316e1153`
- reason: error_message, empty_student_answer
- run_id: `585ba193316e1153`
- node_id: `revenue_not_cash_receipt`
- condition: `node_only`
- student_persona: `novice_closed_book`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 7. `5597cb7ad2db9ba6`
- reason: error_message, judge_error
- run_id: `5597cb7ad2db9ba6`
- node_id: `revenue_not_cash_receipt`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 根据材料，收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以可能确认收入但现金没有增加。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 8. `f360e8fa7f1125ec`
- reason: error_message, empty_student_answer, judge_error
- run_id: `f360e8fa7f1125ec`
- node_id: `expense_recognition`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 9. `1cfaba10d861f9c4`
- reason: error_message, judge_error
- run_id: `1cfaba10d861f9c4`
- node_id: `expense_recognition`
- condition: `node_only`
- student_persona: `novice_closed_book`
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，不一定等于当期现金付款。本月工资虽然下月才发，但它是本月员工工作产生的耗费，服务于本月经营，所以可能作为本月费用。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 10. `79c64d2597f89e85`
- reason: error_message, judge_error
- run_id: `79c64d2597f89e85`
- node_id: `expense_recognition`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但因为它服务于本月经营，所以可以作为本月费用。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 11. `ff04d3360d229fb1`
- reason: error_message, empty_student_answer
- run_id: `ff04d3360d229fb1`
- node_id: `depreciation_amortization`
- condition: `node_only`
- student_persona: `novice_closed_book`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 12. `ef006d458bad3b49`
- reason: error_message, empty_student_answer
- run_id: `ef006d458bad3b49`
- node_id: `depreciation_amortization`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 13. `a8027fffd436418b`
- reason: error_message, empty_student_answer
- run_id: `a8027fffd436418b`
- node_id: `depreciation_amortization`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 14. `95fde13b00513088`
- reason: error_message, empty_student_answer
- run_id: `95fde13b00513088`
- node_id: `gross_margin`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 15. `c8a1cd8fb15a26c6`
- reason: error_message, empty_student_answer
- run_id: `c8a1cd8fb15a26c6`
- node_id: `gross_margin`
- condition: `node_only`
- student_persona: `novice_closed_book`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 16. `d2ba14e5050c1df2`
- reason: error_message, judge_error
- run_id: `d2ba14e5050c1df2`
- node_id: `net_profit`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收到现金（如赊销），费用发生也不等于现金支付（如工资下月发放），折旧和摊销会减少利润但通常不代表当期现金流出。所以净利润为正时，可能因为赊销、未付款的费用或折旧等原因，现金并没有同步增加。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 17. `8305819be1ae4571`
- reason: error_message, empty_student_answer
- run_id: `8305819be1ae4571`
- node_id: `net_profit`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 18. `5a56b9a3f8278455`
- reason: error_message, empty_student_answer, judge_error
- run_id: `5a56b9a3f8278455`
- node_id: `accrual_vs_cash`
- condition: `chain_so_far`
- student_persona: `novice_closed_book`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 19. `923f6441dfad2f14`
- reason: error_message, empty_student_answer
- run_id: `923f6441dfad2f14`
- node_id: `income_statement_boundary`
- condition: `no_course_baseline`
- student_persona: `rote_memorizer`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 20. `bf2dc9120ce2ddfd`
- reason: error_message, empty_student_answer
- run_id: `bf2dc9120ce2ddfd`
- node_id: `income_statement_boundary`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 21. `71fa0e4523ba0495`
- reason: error_message, empty_student_answer, judge_error
- run_id: `71fa0e4523ba0495`
- node_id: `revenue_recognition`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 22. `317a2d076fd28871`
- reason: error_message, empty_student_answer
- run_id: `317a2d076fd28871`
- node_id: `revenue_recognition`
- condition: `chain_so_far`
- student_persona: `rote_memorizer`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 23. `4ab92215771f559d`
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

## 24. `e4e4b528edb49ba4`
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

## 25. `41af28eab7e61792`
- reason: error_message, empty_student_answer
- run_id: `41af28eab7e61792`
- node_id: `expense_recognition`
- condition: `no_course_baseline`
- student_persona: `rote_memorizer`
- question: 为什么本月工资下月才发，也可能作为本月费用？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 26. `81c401580ed00066`
- reason: error_message, empty_student_answer, judge_error
- run_id: `81c401580ed00066`
- node_id: `expense_recognition`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 27. `64c302be5617b405`
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

## 28. `8f51208f00adaff0`
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

## 29. `31a950c3a9c59009`
- reason: error_message, empty_student_answer, judge_error
- run_id: `31a950c3a9c59009`
- node_id: `depreciation_amortization`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 
- error_message: student_llm_error: LLM request failed: status_code=; request_url=https://uni-api.cstcloud.cn/v1/chat/completions; response_text= error=URLError: <urlopen error _ssl.c:1112: The handshake operation timed out>; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 30. `28d034207968af6f`
- reason: error_message, empty_student_answer, judge_error
- run_id: `28d034207968af6f`
- node_id: `gross_margin`
- condition: `no_course_baseline`
- student_persona: `rote_memorizer`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: LLM request failed: status_code=; request_url=https://uni-api.cstcloud.cn/v1/chat/completions; response_text= error=URLError: <urlopen error _ssl.c:1112: The handshake operation timed out>; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 31. `cec6e305439237b9`
- reason: error_message, empty_student_answer, judge_error
- run_id: `cec6e305439237b9`
- node_id: `gross_margin`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: LLM request failed: status_code=; request_url=https://uni-api.cstcloud.cn/v1/chat/completions; response_text= error=URLError: <urlopen error _ssl.c:1112: The handshake operation timed out>; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 32. `89a5e43e27ea7c6e`
- reason: error_message, empty_student_answer, judge_error
- run_id: `89a5e43e27ea7c6e`
- node_id: `gross_margin`
- condition: `chain_so_far`
- student_persona: `rote_memorizer`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: LLM request failed: status_code=; request_url=https://uni-api.cstcloud.cn/v1/chat/completions; response_text= error=URLError: <urlopen error _ssl.c:1112: The handshake operation timed out>; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 33. `91911382ccb93783`
- reason: error_message, empty_student_answer, judge_error
- run_id: `91911382ccb93783`
- node_id: `gross_margin`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。 如何推出毛利和毛利率？它们还没有扣除哪些费用？
- student_answer: 
- error_message: student_llm_error: LLM request failed: status_code=; request_url=https://uni-api.cstcloud.cn/v1/chat/completions; response_text= error=URLError: <urlopen error [Errno 2] No such file or directory>; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 34. `bd12c173fbb8f4f9`
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

## 35. `01668fda41cabddc`
- reason: error_message, judge_error
- run_id: `01668fda41cabddc`
- node_id: `net_profit`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 材料说净利润不等于现金，所以净利润为正不一定代表现金充足。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 36. `4e0aad17637d82ae`
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

## 37. `fb09023b6c461873`
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

## 38. `db9a7f70f02cb56e`
- reason: error_message, empty_student_answer
- run_id: `db9a7f70f02cb56e`
- node_id: `accrual_vs_cash`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 39. `6f9da756a4a58197`
- reason: error_message, empty_student_answer, judge_error
- run_id: `6f9da756a4a58197`
- node_id: `accrual_vs_cash`
- condition: `hidden_transfer`
- student_persona: `rote_memorizer`
- question: 咨询公司 6 月完成服务，7 月收款；6 月发生房租但 7 月付款。 权责发生制下 6 月应如何看收入和费用？它和现金制的关注点有什么不同？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 40. `16d7b0406bfc8948`
- reason: error_message, empty_student_answer
- run_id: `16d7b0406bfc8948`
- node_id: `income_statement_boundary`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 41. `bee48c2ac1d6d055`
- reason: error_message, empty_student_answer
- run_id: `bee48c2ac1d6d055`
- node_id: `income_statement_boundary`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 42. `4b6cc7d618879fba`
- reason: error_message, judge_error
- run_id: `4b6cc7d618879fba`
- node_id: `revenue_recognition`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- student_answer: 因为收入确认看的是服务完成，不是收到现金，所以本月完成服务就可以确认收入，但客户下月才付款，所以现金还没收到，收入已经确认了。不过我觉得没收到钱就确认收入有点奇怪，毕竟钱还没到账。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 43. `90ffab514a6ce477`
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

## 44. `1b8d3d51286c162a`
- reason: error_message, empty_student_answer
- run_id: `1b8d3d51286c162a`
- node_id: `revenue_not_cash_receipt`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 45. `b7c79c56ca63ca4c`
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

## 46. `876c4b3ac062bd2b`
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

## 47. `b3cd9f655a514dd1`
- reason: error_message, empty_student_answer
- run_id: `b3cd9f655a514dd1`
- node_id: `expense_recognition`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 48. `83e7249776e6fea2`
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

## 49. `801b3238e4c0630e`
- reason: error_message, judge_error
- run_id: `801b3238e4c0630e`
- node_id: `depreciation_amortization`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 为什么折旧会减少利润，但通常不是当期现金流出？
- student_answer: 折旧会减少利润，因为折旧是费用，但折旧不是现金流出，因为折旧是长期资产成本的分摊，不是真的付钱。不过，折旧减少利润，那现金应该也会减少吧？因为利润少了，现金肯定也少了。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 50. `99080fad5a427dab`
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

## 51. `84591106c3523017`
- reason: error_message, judge_error
- run_id: `84591106c3523017`
- node_id: `gross_margin`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 毛利率高说明收入减去销售成本后剩下的钱多，那净利润应该也高啊。材料说毛利还不是净利润，但我觉得毛利高的话，净利润肯定也高，因为剩下的钱多嘛。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 52. `5e8f09219a82b69d`
- reason: error_message, empty_student_answer
- run_id: `5e8f09219a82b69d`
- node_id: `gross_margin`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 为什么毛利率高不等于净利润一定高？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 53. `a40ddd549a31f9ec`
- reason: error_message, empty_student_answer
- run_id: `a40ddd549a31f9ec`
- node_id: `gross_margin`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。 如何推出毛利和毛利率？它们还没有扣除哪些费用？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 54. `d9c0aa5717c689e5`
- reason: error_message, empty_student_answer
- run_id: `d9c0aa5717c689e5`
- node_id: `net_profit`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 55. `a3c7062b5c479e04`
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

## 56. `f6001906a04e3a51`
- reason: error_message, empty_student_answer, judge_error
- run_id: `f6001906a04e3a51`
- node_id: `net_profit`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 57. `0b72d7f34f95519b`
- reason: error_message, judge_error
- run_id: `0b72d7f34f95519b`
- node_id: `accrual_vs_cash`
- condition: `no_course_baseline`
- student_persona: `misconception_prone`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 无法从当前课程材料推出完整答案
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 58. `b498fa1bf5bd5471`
- reason: error_message, empty_student_answer, judge_error
- run_id: `b498fa1bf5bd5471`
- node_id: `accrual_vs_cash`
- condition: `node_only`
- student_persona: `misconception_prone`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 59. `1e07b89d2e8529b1`
- reason: error_message, empty_student_answer
- run_id: `1e07b89d2e8529b1`
- node_id: `accrual_vs_cash`
- condition: `chain_so_far`
- student_persona: `misconception_prone`
- question: 权责发生制和现金制的核心区别是什么？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 60. `3d22b87b3201f13d`
- reason: error_message, empty_student_answer, judge_error
- run_id: `3d22b87b3201f13d`
- node_id: `accrual_vs_cash`
- condition: `hidden_transfer`
- student_persona: `misconception_prone`
- question: 咨询公司 6 月完成服务，7 月收款；6 月发生房租但 7 月付款。 权责发生制下 6 月应如何看收入和费用？它和现金制的关注点有什么不同？
- student_answer: 
- error_message: student_llm_error: The read operation timed out; judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude
