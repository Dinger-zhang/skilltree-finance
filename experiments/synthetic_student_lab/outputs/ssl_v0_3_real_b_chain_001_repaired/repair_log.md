# Synthetic Student Lab Bad Record Repair Log

- source_dir: `E:\program\skilltree-finance\experiments\synthetic_student_lab\outputs\ssl_v0_3_real_b_chain_001`
- target_dir: `E:\program\skilltree-finance\experiments\synthetic_student_lab\outputs\ssl_v0_3_real_b_chain_001_repaired`
- total_simulation_records: 96
- total_judge_records: 96
- bad_run_ids: 5
- max_retries_per_step: 3
- student_model: `deepseek-v4-flash`
- judge_model: `deepseek-v4-flash`

## `28922aa745eb2000`
- node_id: `depreciation_amortization`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- original_error_message: student_llm_error: The read operation timed out
- action: student_then_judge
  - student attempt 1: success
  - judge attempt 1: success

## `28f8b62354b3b43f`
- node_id: `income_statement_boundary`
- condition: `no_course_baseline`
- student_persona: `novice_closed_book`
- original_error_message: judge_llm_error: The read operation timed out
- action: judge_only
  - judge attempt 1: success

## `64c06390d142e8d2`
- node_id: `net_profit`
- condition: `node_only`
- student_persona: `rote_memorizer`
- original_error_message: student_llm_error: The read operation timed out
- action: student_then_judge
  - student attempt 1: success
  - judge attempt 1: success

## `79ffc109344fe36b`
- node_id: `expense_recognition`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- original_error_message: student_llm_error: The read operation timed out
- action: student_then_judge
  - student attempt 1: success
  - judge attempt 1: success

## `81eb5c38a64cb9a7`
- node_id: `net_profit`
- condition: `hidden_transfer`
- student_persona: `novice_closed_book`
- original_error_message: judge_llm_error: The read operation timed out
- action: judge_only
  - judge attempt 1: success

## Summary
- output_simulation_records: 96
- output_judge_records: 96
- repaired_run_ids: 28922aa745eb2000, 28f8b62354b3b43f, 64c06390d142e8d2, 79ffc109344fe36b, 81eb5c38a64cb9a7
- failed_after_retries_count: 0
