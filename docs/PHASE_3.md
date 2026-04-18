# Phase 3: Full CLI Agent

## Goal

Push the CLI toward a full-featured Codex-style agent with memory management, observability, and strong developer ergonomics.

## Priority Tasks

- [ ] Add context summarization when history gets long
- [ ] Add session summaries
- [ ] Add memory compaction for long chats
- [ ] Add resume of interrupted tool workflows
- [ ] Add session rename support
- [ ] Add session delete/archive support
- [ ] Add export chat/session to markdown or json
- [ ] Show token usage and latency per response
- [ ] Add response timing
- [ ] Add structured logs
- [ ] Log tool calls and outcomes
- [ ] Log model errors with provider context
- [ ] Add debug mode
- [ ] Add `/logs` command
- [ ] Add command/tool history
- [ ] Add crash-safe error reporting
- [ ] Add secret detection before displaying file/env content
- [ ] Mask API keys in output
- [ ] Add confirmation for destructive actions
- [ ] Add user-change preservation rules
- [ ] Add architecture section in docs
- [ ] Add troubleshooting section in docs
- [ ] Add `/history`
- [ ] Add `/rename-session`
- [ ] Add `/delete-session`
- [ ] Add better loading/progress indicators
- [ ] Add tool execution log panel
- [ ] Add status bar/footer with model/session/provider

## Exit Criteria

- [ ] Long-lived sessions remain usable without runaway context
- [ ] The CLI exposes enough logs and metrics to debug failures
- [ ] Session management is practical for real work
- [ ] Safety behavior is explicit and documented
