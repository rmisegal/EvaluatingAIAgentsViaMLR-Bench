# MLR-Bench Testing Checklist

## Critical Tests

### ✅ A. Unit Tests (Completed)
- [x] Data models working
- [x] Task manager working
- [x] All 9 unit tests pass

### ⏳ B. MCP & Internet Connectivity
- [ ] Semantic Scholar API connection
- [ ] Search real papers online
- [ ] Handle API errors
- [ ] Python code execution

### ⏳ C. Tool Usage by Agents
- [ ] Literature Reviewer uses search_papers_sync()
- [ ] Experimenter uses execute_python_code_sync()
- [ ] Evaluators use calculate_average_score()
- [ ] Paper Writer uses format_paper_section()

### ⏳ D. Data Flow Between Agents
- [ ] Idea → Literature Reviewer
- [ ] Idea + Literature → Proposal Writer
- [ ] All data → Experimenter
- [ ] All data → Paper Writer
- [ ] No data loss between stages

### ⏳ E. Event Bus & Visualization
- [ ] Events emitted for each stage
- [ ] Flask server starts
- [ ] WebSocket updates work
- [ ] UI displays pipeline correctly

### ⏳ F. End-to-End Integration
- [ ] Run single task completely
- [ ] All 5 stages execute
- [ ] Results saved correctly
- [ ] Evaluation completes

## Test Execution Plan

1. Test internet connectivity (Semantic Scholar)
2. Test tool usage
3. Test data flow
4. Test with visualization
5. Run full end-to-end test
