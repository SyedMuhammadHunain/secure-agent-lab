# Secure Agent Lab

Welcome to the Secure Agent Lab! This repository serves as a secure development environment for building and experimenting with AI agents using the Google Agent Development Kit (ADK 2.0).

## Included Agents

### 1. [Shopping Assistant](./shopping-assistant)
A retail shopping assistant agent designed to help users with their shopping experience.
- **Key Feature**: Secure discount code redemption tool (`redeem_discount_code`) that prevents double-spending and enforces strict logic.
- **Security Validation**: Validates user identity and tracks state in an in-memory store.

## Security Guardrails & Paved Roads

This workspace is strictly configured with security in mind. Our `.agents/CONTEXT.md` enforces a "Paved Road" approach:
1. **Pre-Commit Enforcement**: Commits are automatically formatted using standard hooks.
2. **Semgrep Scanning**: A local Semgrep hook runs on commit to block any hardcoded secrets (e.g., Google API keys).
3. **STRIDE Threat Modeling**: Includes a custom `stride-threat-model` skill to formally evaluate new features against the STRIDE methodology.
4. **Tool Input Validation**: All tools are mandated to use strict schema validation to prevent malformed or malicious inputs.
