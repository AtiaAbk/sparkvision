# SparkVision — Unreal MCP-First Development Rules

For all SparkVision development tasks, adhere strictly to the following rules:

1. **Unreal MCP as Primary Interface**:
   Use the connected Unreal MCP server as the primary interface for inspecting and modifying the live Unreal Editor whenever the required tool is available.

2. **Inspect Before Modify**:
   Before modifying any Level, Actor, Material, Blueprint, Lighting configuration, Landscape, Foliage, or other Editor object, inspect its current state through MCP first.

3. **Tool Discovery & Invocation**:
   Discover tools using `list_toolsets` and `describe_toolset`. Invoke tools using `call_tool`.

4. **Sequential Execution**:
   Execute Unreal MCP tool calls sequentially. Never send overlapping Editor modification calls because Unreal MCP synchronizes tool execution through the game thread.

5. **MCP vs Filesystem Scope**:
   Use MCP for live Editor operations. Use filesystem and code-editing tools for C++, project source files, configuration files, and other tasks that are not exposed through MCP.

6. **Post-Modification Verification**:
   After Editor modifications, inspect the actual result through MCP and verify that the intended changes exist.

7. **Evidence-Based Runtime Verification**:
   Use PIE (Play-In-Editor), automation tests, build tools, or packaged runtime testing where the available tools support them. Never claim runtime verification without actual evidence.

8. **Transparency on MCP Limitations**:
   If a required operation is unavailable through MCP, report the limitation and use the appropriate alternative method. Never pretend that an MCP operation succeeded.

9. **Architecture & History Preservation**:
   Preserve existing project architecture, user changes, assets, and Git history.

10. **Localhost-Only Security Boundary**:
    Maintain the existing localhost-only MCP connection at `http://127.0.0.1:8000/mcp`. Never expose it to external networks.

11. **Milestone Git Workflow**:
    For every meaningful milestone, inspect Git status, commit verified changes, push to the existing remote, and verify the push. Never force-push or rewrite history.

12. **Continuous Documentation**:
    Keep a continuously updated `Documentation/PROJECT_MASTER_STATUS.md` containing verified progress, changed assets, current issues, latest commit, and next tasks.
