# CONN-QBITTORRENT-AGENT-SURFACE — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-QBITTORRENT-AGENT-SURFACE-R001` | `tests/test_surface.py::test_every_upstream_operation_has_a_client_method`, `tests/test_surface.py::test_every_client_method_is_served_as_a_tool` | Each fixture operation has a client method, each client route is an upstream operation, each method is a served tool. |
| T-002 | `CONN-QBITTORRENT-AGENT-SURFACE-R002` | `tests/test_surface.py::test_no_action_routed_or_untyped_tool`, `tests/test_surface.py::test_destructive_operations_ask_for_confirmation` | No tool has `params_json` or `action`; delete and remove tools are destructive; reads are read-only. |
| T-003 | `CONN-QBITTORRENT-AGENT-SURFACE-R003` | `tests/test_surface.py::test_a_failed_call_raises_with_qbittorrents_reason`, `tests/test_surface.py::test_answers_are_json_objects_and_values_travel_on_the_wire`, `tests/test_surface.py::test_api_key_is_a_bearer_and_a_placeholder_falls_back_to_login` | A 409 raises with its reason; a list answer is wrapped; a boolean and a JSON object reach the wire; an export is base64; a valid key is a bearer and a placeholder logs in. |
| T-004 | `CONN-QBITTORRENT-AGENT-SURFACE-R004` | `tests/test_surface.py::test_contract_and_skill_tools_are_served`, `tests/test_surface.py::test_contract_steps_are_ordered_and_bound` | Every contract and skill tool is served; steps are numbered 1..n; every contract's skill exists. |
| T-005 | `CONN-QBITTORRENT-AGENT-SURFACE-R005` | `tests/test_surface.py::test_operator_and_role_prompts_exist`, `tests/test_surface.py::test_prompt_is_a_complete_agent_definition` | Each prompt is served, names only served tools, has every section, and its ontology links equal its tool list. |
| T-006 | `CONN-QBITTORRENT-AGENT-SURFACE-R006` | `tests/test_surface.py::test_data_locations_routing_and_federation` | The instance has its URL setting and save paths; at least 4 routes and 4 federation links. |
| T-007 | `CONN-QBITTORRENT-AGENT-SURFACE-R007` | `tests/test_surface.py::test_every_class_reaches_medulla_core_without_imports` | No import; every class is in `qbt:`, has a core ancestor and reaches `BFO_0000001`. |
| T-008 | `CONN-QBITTORRENT-AGENT-SURFACE-R008` | `tests/test_surface.py::test_ingest_uses_core_classes_and_a_pinned_served_tool` | Every emitted node type is a core class; the preset tool is served with a matching pin. |
