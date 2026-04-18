# Phase 1: Usable Foundation

## Goal

Make the CLI agent safe enough and capable enough for day-to-day coding tasks in a single repo.

## Priority Tasks

- [ ] Replace `shell=True` execution with a safer command runner
- [ ] Add command allow/deny checks
- [ ] Block obviously destructive commands by default
- [ ] Show exact command before execution
- [ ] Capture exit code, stdout, stderr separately
- [ ] Add search tool using `rg`
- [ ] Add `read_file` with line ranges
- [ ] Add patch/apply-diff tool
- [ ] Add diff preview before writes
- [ ] Add file size safeguards for large reads
- [ ] Make tool binding behavior consistent across providers
- [ ] Add startup diagnostics for missing API key/model/base URL
- [ ] Add `/help`
- [ ] Add `/tools`
- [ ] Add `/provider`
- [ ] Add `/clear`
- [ ] Add tests for slash commands
- [ ] Add tests for provider selection
- [ ] Add structured error messages instead of raw tracebacks

## Exit Criteria

- [ ] The agent can safely search, read, patch, and run commands in one repo
- [ ] Provider misconfiguration fails with clear startup feedback
- [ ] Users can discover commands without reading source
- [ ] Basic CLI behavior is covered by tests
