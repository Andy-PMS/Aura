#!/usr/bin/env python3
"""Aura AI Video Studio MCP: safe offline preflight, no paid provider calls."""
import json
import re
import sys
import uuid

TOOLS = [
    {"name": "video_studio_capabilities", "description": "Read-only integration status; does not call providers.", "annotations": {"readOnlyHint": True}, "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "video_studio_prepare", "description": "Validate a proposed authorized video job offline. Never uploads media or spends credits.", "annotations": {"readOnlyHint": True}, "inputSchema": {"type": "object", "properties": {"image_asset_id": {"type": "string"}, "voice_asset_id": {"type": "string"}, "text": {"type": "string"}, "consent_image": {"type": "boolean"}, "consent_voice": {"type": "boolean"}, "duration_seconds": {"type": "integer"}, "resolution": {"type": "string"}}, "required": ["image_asset_id", "voice_asset_id", "text", "consent_image", "consent_voice"], "additionalProperties": False}},
    {"name": "video_studio_generate", "description": "Disabled until provider API contracts, identity-scoped credentials and explicit payment approval are verified.", "annotations": {"destructiveHint": True}, "inputSchema": {"type": "object", "properties": {"request_id": {"type": "string"}}, "required": ["request_id"], "additionalProperties": False}}
]

def validate(args):
    errors = []
    for key in ("image_asset_id", "voice_asset_id"):
        value = args.get(key)
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", value):
            errors.append(key + " must be a valid local asset identifier")
    value = args.get("text")
    if not isinstance(value, str) or not value.strip() or len(value) > 500:
        errors.append("text must contain 1-500 characters")
    if args.get("consent_image") is not True:
        errors.append("image consent required")
    if args.get("consent_voice") is not True:
        errors.append("voice consent required")
    duration = args.get("duration_seconds", 10)
    if type(duration) is not int or duration != 10:
        errors.append("pilot duration must be 10 seconds")
    if args.get("resolution", "480p") != "480p":
        errors.append("pilot resolution must be 480p")
    return errors

def execute(name, args):
    if name == "video_studio_capabilities":
        return {"status": "preflight_only", "fish_audio": "not_connected", "seedance_reference_audio": "not_connected", "provider_calls": False, "estimated_usd": None, "reason": "Verify current OpenRouter schemas and account prices before implementing paid endpoints."}
    if name == "video_studio_prepare":
        errors = validate(args)
        if errors:
            return {"ready": False, "errors": errors, "provider_calls": False}
        return {"ready": False, "validation_passed": True, "request_id": str(uuid.uuid4()), "duration_seconds": 10, "resolution": "480p", "provider_calls": False, "reason": "API adapters, asset access, identity-scoped credentials and verified quote not yet connected. No upload or payment performed."}
    if name == "video_studio_generate":
        return {"status": "blocked", "provider_calls": False, "reason": "Paid generation deliberately disabled pending verified integration and explicit quote approval."}
    raise ValueError("unknown tool")

def reply(msg):
    method = msg.get("method")
    if method == "notifications/initialized":
        return None
    if method == "initialize":
        result = {"protocolVersion": "2025-03-26", "capabilities": {"tools": {}}, "serverInfo": {"name": "aura-ai-video-studio", "version": "0.2.0-preflight"}}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        try:
            payload = execute(name, params.get("arguments") or {})
            result = {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}], "isError": False}
        except (ValueError, TypeError) as exc:
            result = {"content": [{"type": "text", "text": str(exc)}], "isError": True}
    else:
        return {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": msg.get("id"), "result": result}

def main():
    for line in sys.stdin:
        try:
            msg = json.loads(line)
            result = reply(msg)
            if result is not None and "id" in msg:
                sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            print("MCP error: " + str(exc), file=sys.stderr)

if __name__ == "__main__":
    main()
