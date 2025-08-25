from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import httpx
import yaml
import os

app = FastAPI(title="Proxy API", version="1.0.0")

# 🔑 Store your API key in an environment variable
API_KEY = os.getenv("PROXY_API_KEY", "replace_me")
TARGET_URL = "https://proxy.denkers.co"  # your actual API target

# ✅ Proxy endpoint that GPT can POST to
@app.post("/proxy")
async def proxy(request: Request):
    try:
        data = await request.json()
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                TARGET_URL,
                json=data,
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
        return JSONResponse(status_code=resp.status_code, content=resp.json())
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ Serve YAML spec for GPT to load as a tool definition
@app.get("/adge.yaml")
async def adge_yaml():
    spec = {
        "openapi": "3.0.1",
        "info": {"title": "Adge Proxy API", "version": "1.0.0"},
        "paths": {
            "/proxy": {
                "post": {
                    "summary": "Forward request to real API",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {"application/json": {"schema": {"type": "object"}}},
                        }
                    },
                }
            }
        },
    }
    return PlainTextResponse(yaml.dump(spec), media_type="text/yaml")

@app.get("/becky.yaml")
async def becky_yaml():
    # You can duplicate / customize for Becky’s API
    spec = {
        "openapi": "3.0.1",
        "info": {"title": "Becky Proxy API", "version": "1.0.0"},
        "paths": {
            "/proxy": {
                "post": {
                    "summary": "Forward request to real API",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {"application/json": {"schema": {"type": "object"}}},
                        }
                    },
                }
            }
        },
    }
    return PlainTextResponse(yaml.dump(spec), media_type="text/yaml")
