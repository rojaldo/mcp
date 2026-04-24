---

description: "Task list for MCP Test Questions Server implementation"
---

# Tasks: MCP Test Questions Server

**Input**: Design documents from `/specs/001-mcp-test-questions/`
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

- [x] T001 Create pyproject.toml with dependencies (fastmcp, pydantic, pytest, pytest-asyncio, ruff, mypy)
- [x] T002 Create src/mcp_test_questions/__init__.py with package metadata
- [x] T003 [P] Create src/mcp_test_questions/models/__init__.py
- [x] T004 [P] Create src/mcp_test_questions/tools/__init__.py
- [x] T005 [P] Create src/mcp_test_questions/resources/__init__.py
- [x] T006 [P] Create src/mcp_test_questions/storage/__init__.py
- [x] T007 [P] Create tests/__init__.py
- [x] T008 [P] Create tests/unit/__init__.py
- [x] T009 [P] Create tests/integration/__init__.py
- [x] T010 [P] Create tests/contract/__init__.py
- [x] T011 Configure ruff in pyproject.toml for linting
- [x] T012 Configure mypy in pyproject.toml for type checking

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T013 Create tests/conftest.py with pytest fixtures for Question model and store
- [x] T014 [P] Write unit test for Question model validation in tests/unit/test_question_model.py
- [x] T015 Implement Question Pydantic model in src/mcp_test_questions/models/question.py
- [x] T016 Verify Question model tests pass
- [x] T017 Write unit test for QuestionStore CRUD operations in tests/unit/test_question_store.py
- [x] T018 Implement QuestionStore in src/mcp_test_questions/storage/question_store.py
- [x] T019 Verify QuestionStore tests pass
- [x] T020 Create MCP server scaffold in src/mcp_test_questions/server.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Test Questions (Priority: P1) -> MVP

**Goal**: Enable test administrators to create multiple-choice questions with correct answers

**Independent Test**: Create a question with text, options, and correct answer, verify returned ID and data

### Tests for User Story 1 (TDD - write first, must fail initially)

- [x] T021 [P] [US1] Write contract test for create_question tool in tests/contract/test_mcp_contracts.py
- [x] T022 [P] [US1] Add validation edge case tests in tests/unit/test_question_model.py

### Implementation for User Story 1

- [x] T023 [US1] Implement create_question tool in src/mcp_test_questions/tools/create_question.py
- [x] T024 [US1] Register create_question tool in server.py
- [x] T025 [US1] Add error handling for invalid params per contracts/tools.md
- [x] T026 [US1] Write integration test for create_question in tests/integration/test_mcp_tools.py

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Retrieve Questions (Priority: P1)

**Goal**: Enable retrieval of questions by ID or random selection

**Independent Test**: Create a question, retrieve by ID, verify data matches; request random question

### Tests for User Story 2 (TDD - write first, must fail initially)

- [x] T027 [P] [US2] Write contract test for get_question tool in tests/contract/test_mcp_contracts.py
- [x] T028 [P] [US2] Write test for random question retrieval in tests/unit/test_question_store.py

### Implementation for User Story 2

- [x] T029 [US2] Implement get_question tool in src/mcp_test_questions/tools/get_question.py
- [x] T030 [US2] Add QuestionStore.get_random method in src/mcp_test_questions/storage/question_store.py
- [x] T031 [US2] Register get_question tool in server.py
- [x] T032 [US2] Add error handling for not found and empty store per contracts/tools.md
- [x] T033 [US2] Write integration test for get_question in tests/integration/test_mcp_tools.py

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Questions (Priority: P2)

**Goal**: Enable partial updates to existing questions

**Independent Test**: Create a question, update text only, verify other fields unchanged

### Tests for User Story 3 (TDD - write first, must fail initially)

- [x] T034 [P] [US3] Write contract test for update_question tool in tests/contract/test_mcp_contracts.py
- [x] T035 [P] [US3] Write test for partial update logic in tests/unit/test_question_store.py

### Implementation for User Story 3

- [x] T036 [US3] Implement update_question tool in src/mcp_test_questions/tools/update_question.py
- [x] T037 [US3] Add QuestionStore.update method with partial update support in src/mcp_test_questions/storage/question_store.py
- [x] T038 [US3] Register update_question tool in server.py
- [x] T039 [US3] Add validation for correct_answer vs options per contracts/tools.md
- [x] T040 [US3] Write integration test for update_question in tests/integration/test_mcp_tools.py

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Questions (Priority: P2)

**Goal**: Enable deletion of questions by ID

**Independent Test**: Create a question, delete it, verify retrieval returns error

### Tests for User Story 4 (TDD - write first, must fail initially)

- [x] T041 [P] [US4] Write contract test for delete_question tool in tests/contract/test_mcp_contracts.py
- [x] T042 [P] [US4] Write test for delete operation in tests/unit/test_question_store.py

### Implementation for User Story 4

- [x] T043 [US4] Implement delete_question tool in src/mcp_test_questions/tools/delete_question.py
- [x] T044 [US4] Add QuestionStore.delete method in src/mcp_test_questions/storage/question_store.py
- [x] T045 [US4] Register delete_question tool in server.py
- [x] T046 [US4] Add error handling for not found per contracts/tools.md
- [x] T047 [US4] Write integration test for delete_question in tests/integration/test_mcp_tools.py

**Checkpoint**: User Stories 1, 2, 3, AND 4 should all work independently (complete CRUD)

---

## Phase 7: User Story 5 - Access Questions as Resources (Priority: P3)

**Goal**: Expose questions as MCP resources with URI pattern question://{id}

**Independent Test**: Request question:///{id} resource, verify JSON and Markdown formats

### Tests for User Story 5 (TDD - write first, must fail initially)

- [x] T048 [P] [US5] Write contract test for question resource in tests/contract/test_mcp_contracts.py
- [x] T049 [P] [US5] Write test for Markdown format generation in tests/unit/test_question_resource.py

### Implementation for User Story 5

- [x] T050 [US5] Create tests/unit/test_question_resource.py (if not exists)
- [x] T051 [US5] Implement question_resource in src/mcp_test_questions/resources/question_resource.py
- [x] T052 [US5] Register resource template in server.py
- [x] T053 [US5] Implement JSON and Markdown format handlers per contracts/resources.md
- [x] T054 [US5] Write integration test for resource access in tests/integration/test_mcp_tools.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T055 Create README.md with quickstart instructions per quickstart.md
- [x] T056 [P] Run ruff check and fix all linting issues
- [x] T057 [P] Run mypy and fix all type errors
- [x] T058 Run pytest with coverage, ensure 80%+ coverage
- [x] T059 [P] Add docstrings to all public APIs per constitution documentation requirements
- [x] T060 Verify all tools and resources are properly registered in server.py
- [x] T061 Test server starts correctly with python -m mcp_test_questions.server

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
- **User Story 2 (P1)**: Can start after Foundational - Uses Question model and store from US1 foundation
- **User Story 3 (P2)**: Can start after Foundational - Independent but benefits from US1 patterns
- **User Story 4 (P2)**: Can start after Foundational - Independent but benefits from US1 patterns
- **User Story 5 (P3)**: Can start after Foundational - Independent but needs questions to exist for testing

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
Task: "Write contract test for create_question tool in tests/contract/test_mcp_contracts.py"
Task: "Add validation edge case tests in tests/unit/test_question_model.py"
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
- Total tasks: 61