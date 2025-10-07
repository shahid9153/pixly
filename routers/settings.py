from fastapi import APIRouter, HTTPException
from services.chatbot import set_api_key
from schemas.settings import ApiKeyRequest
import os
router = APIRouter()
@router.get("/api-key")
def get_api_key_status():
    """Return whether an API key is configured (masked)."""
    import os
    key = os.getenv('GOOGLE_API_KEY') or ""
    masked = (len(key) >= 8)
    preview = f"{key[:4]}***{key[-4:]}" if masked else ""
    return {"status": "ok", "configured": bool(key), "preview": preview}

@router.post("/api-key")
def update_api_key(req: ApiKeyRequest):
    """Save API key to .env and reconfigure the chatbot model."""
    try:
        key = (req.api_key or "").strip()
        if not key:
            raise HTTPException(status_code=400, detail="API key cannot be empty")
        # Persist to .env
        env_path = ".env"
        # Load existing lines if any
        lines = []
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
        # Update or append GOOGLE_API_KEY
        found = False
        for i, line in enumerate(lines):
            if line.startswith("GOOGLE_API_KEY="):
                lines[i] = f"GOOGLE_API_KEY={key}"
                found = True
                break
        if not found:
            lines.append(f"GOOGLE_API_KEY={key}")
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))
        # Reconfigure runtime
        if not set_api_key(key):
            raise HTTPException(status_code=500, detail="Failed to apply API key at runtime")
        return {"status": "ok", "message": "API key updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating API key: {str(e)}")