from fastapi import APIRouter,HTTPException
from services.screenshot import start_screenshot_capture, stop_screenshot_capture, get_recent_screenshots, get_screenshot_by_id, get_screenshot_stats, delete_screenshot
router = APIRouter()
# Screenshot endpoints
@router.post("/start")
def start_screenshots(interval: int = 30):
    """Start automatic screenshot capture."""
    start_screenshot_capture(interval)
    return {"status": "ok", "message": f"Screenshot capture started with {interval}s interval"}

@router.post("/stop")
def stop_screenshots():
    """Stop automatic screenshot capture."""
    stop_screenshot_capture()
    return {"status": "ok", "message": "Screenshot capture stopped"}

@router.get("/recent")
def get_recent_screenshots_endpoint(limit: int = 10, application: str = None):
    """Get recent screenshots."""
    screenshots = get_recent_screenshots(limit=limit, application=application)
    return {"status": "ok", "screenshots": screenshots}

@router.get("/stats")
def get_screenshot_stats_endpoint():
    """Get screenshot statistics."""
    stats = get_screenshot_stats()
    return {"status": "ok", "stats": stats}

@router.get("/{screenshot_id}")
def get_screenshot_endpoint(screenshot_id: int):
    """Get screenshot data by ID."""
    screenshot_data = get_screenshot_by_id(screenshot_id)
    if screenshot_data:
        import base64
        return {"status": "ok", "data": base64.b64encode(screenshot_data).decode('utf-8')}
    else:
        return {"status": "error", "message": "Screenshot not found"}

@router.delete("/{screenshot_id}")
def delete_screenshot_endpoint(screenshot_id: int):
    """Delete screenshot by ID."""
    try:
        deleted = delete_screenshot(screenshot_id)
        if deleted:
            return {"status": "ok", "message": f"Deleted screenshot {screenshot_id}"}
        else:
            raise HTTPException(status_code=404, detail="Screenshot not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting screenshot: {str(e)}")