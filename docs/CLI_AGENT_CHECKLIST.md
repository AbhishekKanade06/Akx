# CLI Agent Checklist

## 1. Core Agent Architecture

- [ ] Split chat mode and agent mode clearly
- [ ] Add a planning layer before tool execution
- [ ] Expand agent state beyond `messages`
- [ ] Track current session, cwd, last tool result, and task status
- [ ] Add retry/fallback behavior for failed model/tool calls
- [ ] Add context summarization when history gets long
- [ ] Add structured error messages instead of raw tracebacks
- [ ] Recreate the LLM client per config change instead of module-global init
- [ ] Add provider capability detection for tool calling support
- [ ] Make tool binding behavior consistent across providers

## 2. Model / Provider Layer

- [ ] Standardize provider config for `openai`, `groq`, `google`, `ollama`
- [ ] Validate env vars at startup
- [ ] Add startup diagnostics for missing API key/model/base URL
- [ ] Add `/provider` command
- [ ] Add `/model set` support
- [ ] Add graceful fallback when a model does not support tools
- [ ] Show token usage and latency per response
- [ ] Add provider-specific defaults and validation

## 3. Command Execution Safety

- [ ] Replace `shell=True` execution with safer argument-based execution where possible
- [ ] Add command allow/deny checks
- [ ] Block obviously destructive commands by default
- [ ] Add approval levels: safe, sensitive, destructive
- [ ] Approve tools one-by-one, not only as a batch
- [ ] Show exact command before execution
- [ ] Support command timeout configuration
- [ ] Support streaming stdout/stderr
- [ ] Support long-running commands
- [ ] Support cancelling running commands
- [ ] Capture exit code, stdout, stderr separately
- [ ] Add cwd control for shell commands
- [ ] Add env isolation for shell commands

## 4. File Editing / Coding Tools

- [ ] Add search tool using `rg`
- [ ] Add `read_file` with line ranges
- [ ] Add file metadata tool
- [ ] Add glob/find files tool
- [ ] Add patch/apply-diff tool
- [ ] Add rename/move/delete tools
- [ ] Add append/insert/replace-by-lines tools
- [ ] Add directory tree view
- [ ] Add file size safeguards for large reads
- [ ] Add binary-file detection
- [ ] Add diff preview before writes
- [ ] Add undo for last file change

## 5. Git Integration

- [ ] Add `git status` tool
- [ ] Add `git diff` tool
- [ ] Add `git log` tool
- [ ] Add branch info command
- [ ] Add staged/unstaged change visibility
- [ ] Add commit creation flow
- [ ] Add commit message generation
- [ ] Add safety against overwriting user changes
- [ ] Add PR-style summary generation
- [ ] Add `/diff` and `/commit` commands

## 6. Testing / Verification

- [ ] Add project test suite
- [ ] Add tests for CLI slash commands
- [ ] Add tests for session resume behavior
- [ ] Add tests for saved-session listing
- [ ] Add tests for status output
- [ ] Add tests for shell tool failures/timeouts
- [ ] Add tests for file tool edge cases
- [ ] Add tests for provider selection
- [ ] Add verification loop: edit -> run tests -> summarize result
- [ ] Add `/test` command

## 7. Session / Memory

- [ ] Store session metadata cleanly
- [ ] Show recent sessions with timestamps
- [ ] Add session rename support
- [ ] Add session delete/archive support
- [ ] Add `/history` command
- [ ] Add resume of interrupted tool workflows
- [ ] Add session summaries
- [ ] Add memory compaction for long chats
- [ ] Add export chat/session to markdown or json
- [ ] Add `/clear` for starting fresh within same session

## 8. CLI UX

- [ ] Add `/help`
- [ ] Add `/tools`
- [ ] Add `/provider`
- [ ] Add `/history`
- [ ] Add `/diff`
- [ ] Add `/test`
- [ ] Add `/clear`
- [ ] Add `/rename-session`
- [ ] Add `/delete-session`
- [ ] Add command autocomplete if possible
- [ ] Add relative time like `2m ago` beside timestamps
- [ ] Add better loading/progress indicators
- [ ] Add tool execution log panel
- [ ] Add status bar/footer with model/session/provider
- [ ] Add copyable plain-text output mode

## 9. Observability / Debugging

- [ ] Add structured logs
- [ ] Log tool calls and outcomes
- [ ] Log model errors with provider context
- [ ] Add debug mode
- [ ] Add `/logs` command
- [ ] Add response timing
- [ ] Add command/tool history
- [ ] Add crash-safe error reporting

## 10. Safety / Policy

- [ ] Define safe filesystem boundaries
- [ ] Restrict writes outside repo unless approved
- [ ] Restrict shell access categories
- [ ] Add secret detection before displaying file/env content
- [ ] Mask API keys in output
- [ ] Add confirmation for destructive actions
- [ ] Add confirmation for external network use if later supported
- [ ] Add user-change preservation rules

## 11. Docs

- [ ] Update README with full command list
- [ ] Document providers and example env configs
- [ ] Document session behavior
- [ ] Document tool approval flow
- [ ] Document safety constraints
- [ ] Document development workflow
- [ ] Add troubleshooting section
- [ ] Add architecture section

## 12. Nice-to-Have Later

- [ ] Web search tool
- [ ] Multi-agent/subtask support
- [ ] Background jobs
- [ ] Task queue
- [ ] Voice input/output
- [ ] TUI dashboard
- [ ] Plugin/tool extension system
- [ ] MCP/tool server support

## Recommended Build Order

1. Safe shell runner
2. Search + patch tools
3. Provider/tool consistency
4. Tests
5. Git tools
6. Better session/history commands
7. Planning + summarization
8. Observability and polish
