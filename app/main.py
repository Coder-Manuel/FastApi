import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.api.v1.api import router as api_router
from app.api.v1.endpoints.models import ErrorResponse, ForbiddenResponse, UnauthorizedResponse, BadRequestResponse
from app.config import AppConfig as config


title = config.APP_NAME
version = config.APP_VERSION
path = config.APP_PATH
docs_url = config.DOCS_URL

print(path)
print(docs_url)

app = FastAPI(title=title, version=version, docs_url="/api/v1/docs")

responses = {500: {"model": ErrorResponse}, 401: {"model": UnauthorizedResponse}, 403: {"model": ForbiddenResponse},
             400: {"model": BadRequestResponse}, }


# =========== Global Exception Handler =============
@app.exception_handler(ValidationError)
async def validation_exception_handler(exc):
    try:
        return JSONResponse(status_code=500, content={"message": "Failed", "status": 500, "detail": exc.errors()})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Failed", "status": 500, "detail": str(e)})

# ========= Exception Handler for Http Exceptions ===========
@app.exception_handler(HTTPException)
async def http_exception_handle(request: Request, exc: HTTPException):
    switcher = {
        "Not authenticated": JSONResponse(content=ForbiddenResponse(detail="Authorization code missing").dict(), status_code=403),
        "Invalid authentication credentials": JSONResponse(
            content=ForbiddenResponse(detail="Invalid authentication scheme").dict()),
        "Invalid code": JSONResponse(
            content=ForbiddenResponse(detail="Token is invalid or expired").dict()),
    }
    return switcher.get(exc.detail)


app.include_router(api_router, prefix="/api/v1", responses=responses)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
