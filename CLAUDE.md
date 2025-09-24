# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

CMM-AI - AI for Culture Media Models (CMMs)

## Commands

### Dependency Management
- **Always use `uv`** for managing dependencies. Never use `pip`.
- `uv run <command>` - Run commands in the project environment
- `uv sync` - Install dependencies

### Testing Commands
- `just --list` - View all available commands
- `just test` - Run unit tests, doctests, and ruff linting
- `just test-full` - Run all tests including integration tests
- `uv run pytest tests/test_specific.py::test_name` - Run a single test

### AI Setup Commands (from ai.just)
- `just -f ai.just setup-ai` - Complete AI setup
- `just -f ai.just claude` - Create CLAUDE.md symlink
- `just -f ai.just setup-gh` - Setup GitHub secrets and topics

## Architecture

### Directory Structure
```
src/cmm_ai/     # Main source code
docs/           # MkDocs documentation  
tests/          # Test files
  input/        # Example/test input files
mkdocs.yml      # Documentation index
```

### Key Development Principles
- **Testing**: Use doctests liberally as both examples and tests. Write pytest functional style (not unittest OO).
- **Type Safety**: Always use type hints and document all methods/classes
- **Data Models**: Use Pydantic or LinkML for data objects, dataclasses for engine-style OO state
- **Error Handling**: Fail fast, avoid try/except blocks that mask bugs
- **Integration Tests**: Mark with `@pytest.mark.integration` for external dependencies

### GitHub Actions Integration
- Claude Code triggered via `@claude` mentions in issues/PRs
- MCP servers configured: OLS (Ontology Lookup Service) and sequential-thinking
- Allowed tools include Bash, FileEdit, WebSearch, and OLS MCP functions

### Testing Best Practices
- Use `@pytest.mark.parametrize` for testing input combinations
- Never write mock tests unless explicitly requested
- Don't weaken test conditions to make them pass - fix the underlying issue