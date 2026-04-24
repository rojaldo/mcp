---

description: "Task list for MCP GUI Client implementation"
---

# Tasks: MCP GUI Client

**Input**: Design documents from `/specs/002-mcp-gui-client/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: REQUIRED - Constitution mandates TDD (Test-First Development is NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create pyproject.toml with dependencies (tkinter, pytest, pytest-asyncio, ruff, mypy)
- [ ] T002 Create src/mcp_gui_client/__init__.py with package metadata
- [ ] T003 [P] Create src/mcp_gui_client/mcp_client/__init__.py
- [ ] T004 [P] Create src/mcp_gui_client/views/__init__.py
- [ ] T005 [P] Create src/mcp_gui_client/widgets/__init__.py
- [ ] T006 [P] Create src/mcp_gui_client/utils/__init__.py
- [ ] T007 [P] Create tests/__init__.py
- [ ] T008 [P] Create tests/unit/__init__.py
- [ ] T009 [P] Create tests/integration/__init__.py
- [ ] T010 [P] Create tests/contract/__init__.py
- [ ] T011 Configure ruff in pyproject.toml for linting
- [ ] T012 Configure mypy in pyproject.toml for type checking

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T013 Create tests/conftest.py with pytest fixtures for GUI testing and MCP mocking
- [ ] T014 Write unit test for input validators in tests/unit/test_validators.py
- [ ] T015 Implement validators in src/mcp_gui_client/utils/validators.py
- [ ] T016 Verify validator tests pass
- [ ] T017 Write unit test for MCP client tools in tests/unit/test_mcp_client.py
- [ ] T018 Implement MCP client connection in src/mcp_gui_client/mcp_client/connection.py
- [ ] T019 Implement MCP tool invocations in src/mcp_gui_client/mcp_client/tools.py
- [ ] T020 Verify MCP client tests pass
- [ ] T021 Implement config management in src/mcp_gui_client/config.py
- [ ] T022 Create application entry point in src/mcp_gui_client/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Create Questions via GUI (Priority: P1) -> MVP

**Goal**: Enable test administrators to create questions through graphical forms

**Independent Test**: Enter question text, add options, select correct answer, verify question created with ID

### Tests for User Story 1 (TDD - write first, must fail initially)

- [ ] T023 [P] [US1] Write contract test for question form in tests/contract/test_ui_contracts.py
- [ ] T024 [P] [US1] Write unit test for form validation in tests/unit/test_validators.py

### Implementation for User Story 1

- [ ] T025 [US1] Implement QuestionFormPanel in src/mcp_gui_client/views/question_form.py
- [ ] T026 [US1] Integrate form with MCP client tools
- [ ] T027 [US1] Add real-time validation feedback per contracts/ui-components.md
- [ ] T028 [US1] Write integration test for create flow in tests/integration/test_gui_flows.py

**Checkpoint**: User Story 1 should be fully functional - questions can be created via GUI

---

## Phase 4: User Story 2 - Browse and View Questions (Priority: P1)

**Goal**: Enable browsing questions in a scrollable list with detail view

**Independent Test**: Create questions, view in list, select to see details, get random question

### Tests for User Story 2 (TDD - write first, must fail initially)

- [ ] T029 [P] [US2] Write contract test for question list in tests/contract/test_ui_contracts.py
- [ ] T030 [P] [US2] Write unit test for list panel in tests/unit/test_gui_components.py

### Implementation for User Story 2

- [ ] T031 [US2] Implement QuestionListPanel in src/mcp_gui_client/views/question_list.py
- [ ] T032 [US2] Implement QuestionDetailPanel in src/mcp_gui_client/views/question_detail.py
- [ ] T033 [US2] Implement MainWindow layout in src/mcp_gui_client/views/main_window.py
- [ ] T034 [US2] Add random question button functionality
- [ ] T035 [US2] Write integration test for browse/view flow in tests/integration/test_gui_flows.py

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Edit Questions via GUI (Priority: P2)

**Goal**: Enable editing existing questions with pre-populated form

**Independent Test**: Select question, edit form opens with data, modify and save, verify changes

### Tests for User Story 3 (TDD - write first, must fail initially)

- [ ] T036 [P] [US3] Write contract test for edit mode in tests/contract/test_ui_contracts.py
- [ ] T037 [P] [US3] Write unit test for form populate in tests/unit/test_gui_components.py

### Implementation for User Story 3

- [ ] T038 [US3] Add edit mode to QuestionFormPanel
- [ ] T039 [US3] Implement partial updates logic
- [ ] T040 [US3] Add edit button to QuestionDetailPanel
- [ ] T041 [US3] Write integration test for edit flow in tests/integration/test_gui_flows.py

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Questions via GUI (Priority: P2)

**Goal**: Enable deletion with confirmation dialog

**Independent Test**: Select question, click delete, confirm, verify removed from list

### Tests for User Story 4 (TDD - write first, must fail initially)

- [ ] T042 [P] [US4] Write contract test for confirmation dialog in tests/contract/test_ui_contracts.py
- [ ] T043 [P] [US4] Write unit test for delete operation in tests/unit/test_gui_components.py

### Implementation for User Story 4

- [ ] T044 [US4] Implement ConfirmationDialog in src/mcp_gui_client/widgets/confirmation_dialog.py
- [ ] T045 [US4] Add delete button to QuestionDetailPanel
- [ ] T046 [US4] Wire delete with MCP client and list refresh
- [ ] T047 [US4] Write integration test for delete flow in tests/integration/test_gui_flows.py

**Checkpoint**: User Stories 1, 2, 3, AND 4 should all work independently (complete CRUD)

---

## Phase 7: User Story 5 - View Question in Multiple Formats (Priority: P3)

**Goal**: Switch between formatted, JSON, and Markdown view formats

**Independent Test**: View question, switch formats, verify each renders correctly

### Tests for User Story 5 (TDD - write first, must fail initially)

- [ ] T048 [P] [US5] Write contract test for format switcher in tests/contract/test_ui_contracts.py
- [ ] T049 [P] [US5] Write unit test for format rendering in tests/unit/test_gui_components.py

### Implementation for User Story 5

- [ ] T050 [US5] Implement FormatSwitcher in src/mcp_gui_client/widgets/format_switcher.py
- [ ] T051 [US5] Add JSON format renderer to QuestionDetailPanel
- [ ] T052 [US5] Add Markdown format renderer to QuestionDetailPanel
- [ ] T053 [US5] Write integration test for format switching in tests/integration/test_gui_flows.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T054 Implement StatusBar in src/mcp_gui_client/widgets/status_bar.py
- [ ] T055 Implement SettingsDialog in src/mcp_gui_client/views/settings_dialog.py
- [ ] T056 Add menu bar and toolbar to MainWindow
- [ ] T057 [P] Run ruff check and fix all linting issues
- [ ] T058 [P] Run mypy and fix all type errors
- [ ] T059 Run pytest with coverage, ensure 60%+ coverage
- [ ] T060 [P] Add docstrings to all public APIs per constitution requirements
- [ ] T061 Create README.md with quickstart instructions
- [ ] T062 Test application starts correctly with python -m mcp_gui_client.main

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 & US2 -> US3 & US4 -> US5)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - Independent from US1 but shares MainWindow
- **User Story 3 (P2)**: Can start after Foundational - Extends QuestionFormPanel from US1
- **User Story 4 (P2)**: Can start after Foundational - Extends QuestionDetailPanel from US2
- **User Story 5 (P3)**: Can start after Foundational - Extends QuestionDetailPanel from US2

### Within Each User Story (TDD Flow)

1. Write tests first (must fail)
2. Implement code
3. Verify tests pass
4. Move to next story

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tests marked [P] within phase can run in parallel
- Once Foundational completes, all user stories can start in parallel
- Tests within a story marked [P] can run in parallel
- Different user stories can be worked on by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write contract test for question form in tests/contract/test_ui_contracts.py"
Task: "Write unit test for form validation in tests/unit/test_validators.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. STOP and VALIDATE: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add User Story 1 -> Test independently -> Deploy/Demo (MVP!)
3. Add User Story 2 -> Test independently -> Deploy/Demo
4. Add User Story 3 -> Test independently -> Deploy/Demo
5. Add User Story 4 -> Test independently -> Deploy/Demo
6. Add User Story 5 -> Test independently -> Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- TDD is NON-NEGOTIABLE per constitution - tests must fail before implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total tasks: 62