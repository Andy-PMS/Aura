# Aura AI Video Studio MCP — preflight v0.2

This is a **working stdio MCP server for offline validation only**, not a Fish/Seedance video generator.

## Local test
```bash
cd integrations/aura-ai-video-studio
python3 -m unittest -v test_server.py
python3 server.py
```

The MCP tools are `video_studio_capabilities`, `video_studio_prepare` and a deliberately blocked `video_studio_generate`.

No third-party packages, keys, uploads or spending are required. This branch is not deployed to production.

## Before enabling generation
Verify OpenRouter's current Fish speech and Seedance video endpoints, supported reference audio format, asset handling, identity-scoped key access, current prices, consent logging, async completion, and operator approval. Then add mock-based integration tests and a rollback plan. Do not merge into the upstream auto-updating installation without separate review.
