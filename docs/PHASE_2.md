# Phase 2: Safe Agent Workflow

## Goal

Turn the CLI from a basic tool runner into a reliable coding assistant with stronger workflows and persistence.

## Priority Tasks

- [ ] Expand agent state beyond `messages`
- [ ] Track current session, cwd, last tool result, and task status
- [ ] Add a planning layer before tool execution
- [ ] Add retry/fallback behavior for failed model/tool calls
- [ ] Add approval levels: safe, sensitive, destructive
- [ ] Approve tools one-by-one, not only as a batch
- [ ] Support command timeout configuration
- [ ] Support streaming stdout/stderr
- [ ] Support long-running commands
- [ ] Support cancelling running commands
- [ ] Add cwd control for shell commands
- [ ] Add env isolation for shell commands
- [ ] Add `git status` tool
- [ ] Add `git diff` tool
- [ ] Add branch info command
- [ ] Add staged/unstaged change visibility
- [ ] Add `/diff` and `/commit` commands
- [ ] Add tests for shell tool failures/timeouts
- [ ] Add tests for file tool edge cases
- [ ] Add tests for session resume behavior
- [ ] Add tests for saved-session listing
- [ ] Add tests for status output

## Exit Criteria

- [ ] Tool execution is safer and more inspectable
- [ ] The agent can work with git-aware coding workflows
- [ ] Sessions resume cleanly and predictably
- [ ] Verification coverage exists for the main agent loop
