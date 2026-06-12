# Bad Records

total_bad_records: 5

## 1. `28f8b62354b3b43f`
- reason: error_message, judge_error
- run_id: `28f8b62354b3b43f`
- node_id: `income_statement_boundary`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- student_answer: 无法从当前课程材料推出完整答案
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 2. `79ffc109344fe36b`
- reason: error_message, empty_student_answer
- run_id: `79ffc109344fe36b`
- node_id: `expense_recognition`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 3. `28922aa745eb2000`
- reason: error_message, empty_student_answer
- run_id: `28922aa745eb2000`
- node_id: `depreciation_amortization`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 面包店去年一次性买入烤箱，今年继续使用并按月计提折旧。 今年的折旧为什么会影响利润，但通常不代表今年再次付现金？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude

## 4. `81eb5c38a64cb9a7`
- reason: error_message, judge_error
- run_id: `81eb5c38a64cb9a7`
- node_id: `net_profit`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- question: 公司收入 50000 元，销售成本 30000 元，期间费用 12000 元，暂不考虑税费。 如何推出净利润？为什么净利润为正仍不必然表示现金充足？
- student_answer: 根据材料，净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。材料说收入确认不一定等于收到现金，费用发生不一定等于当期现金付款，所以净利润为正仍不必然表示现金充足。
- error_message: judge_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: retry

## 5. `64c06390d142e8d2`
- reason: error_message, empty_student_answer
- run_id: `64c06390d142e8d2`
- node_id: `net_profit`
- condition: `node_only`
- student_persona: `rote_memorizer`
- question: 为什么净利润为正仍不一定代表现金充足？
- student_answer: 
- error_message: student_llm_error: The read operation timed out
- student_parse_error: 
- judge_parse_error: 
- suggested_action: exclude
