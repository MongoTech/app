import sentry_sdk
import uvicorn  # type: ignore
from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.middleware("http")
async def exception_handling(request: Request, call_next):  # type: ignore
    try:
        return await call_next(request)
    except Exception as exc:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENV,
            integrations=[FastApiIntegration()],
        )
        with sentry_sdk.push_scope() as scope:
            sentry_sdk.capture_exception(exc)
            scope.clear()

        return JSONResponse(status_code=400, content=f"Something going wrong {exc}")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)  # nosec
