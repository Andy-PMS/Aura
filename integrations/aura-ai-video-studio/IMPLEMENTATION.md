# Aura AI Video Studio — isolated MCP integration

Status: design/integration branch only. No provider calls, no deployment, no spending.

## Verified Aura surfaces

- `internal/agent/tools/video_generate.go` currently supports `audio` as a boolean but does not expose an audio reference asset for lip sync.
- `docs/mcp-manager.md` documents registered local/HTTP MCP servers and trust/approval controls.
- Production auto-updates from `chetto1983/Aura`; this fork branch must never be merged or deployed without checking update and rollback behavior.

## Proposed external MCP server

Tools (draft contracts; not yet operational):

- `video_studio_capabilities`: report verified model/provider capability and pricing metadata, no paid calls.
- `video_studio_prepare`: validate photo/audio/text/consent, estimate and return a request preview, no generation.
- `video_studio_generate`: require explicit approval token for a bounded price; generate authorized voice through a confirmed supported OpenRouter audio endpoint and video through a confirmed supported OpenRouter video endpoint with audio references.
- `video_studio_status`: inspect asynchronous job and deliver final MP4 without resubmitting.

Implementation gates:

1. Verify official live OpenRouter API schemas and Fish/Seedance model IDs, audio sample encoding, video reference-audio parameters, duration/resolution constraints, and pricing. Do not assume the proposed endpoint signatures work.
2. Identify a supported way to access the user's scoped OpenRouter key without exposing it in the sandbox or source control. Never copy production secrets into the repo.
3. Keep consent and media retention explicit; no transfer to new providers before authorization.
4. Mock API tests for validation, billing gate, async polling, retries, audio reference payload, and MP4 delivery.
5. Test MCP registration and invocation on an isolated environment; ensure upstream auto-updates do not remove the integration.
6. Request approval for a 10-second 480p paid trial only after quoting a verified total price. The earlier ~$1.03 estimate is not an authorization.
7. Record measured output quality and operational results.

## Safe deployment

Prefer an independently versioned MCP service with managed registration in Aura. Do not patch the upstream auto-update branch unless absolutely necessary. Deploy only after isolated testing and a documented rollback.
