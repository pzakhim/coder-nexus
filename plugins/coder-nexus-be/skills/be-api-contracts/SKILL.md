---
name: be-api-contracts
description: Contract-first API design, JSON Schema validation, and Frontend Handshake alignment.
---

# Backend API Contracts

Adheres to contract-first development:
- Every endpoint defines request schemas (body, query, headers) and response schemas with HTTP status codes.
- Read the installed plugin’s `shared_contracts/api_handshake_protocol.md` for lifecycle and evidence policy. Receive actual project contracts separately with source/revision and implement approved schemas faithfully.
- FE fixture approval is not BE approval. Live integration acceptance and `VERIFIED_CLOSED` require real endpoint evidence; never report fixture success as live success.
