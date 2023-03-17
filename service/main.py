import openai
import os
from os.path import abspath, dirname
from loguru import logger
from chatgpt_wapper import process
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from message_store import MessageStore
from whisper_wapper import process_audio
import argparse

log_folder = os.path.join(abspath(dirname(__file__)), "log")
logger.add(os.path.join(log_folder, "{time}.log"), level="INFO")

massage_store = MessageStore(db_path="message_store.json", table_name="chatgpt", max_size=100000)
openai_api_key = None
host = None
port = None
api_model = None
socks_proxy = None
timeout_ms = None

app = FastAPI()

stream_response_headers = {
    "Content-Type": "application/octet-stream",
    "Cache-Control": "no-cache",
}


@app.post("/config")
async def config():
    return JSONResponse(content=dict(
        message=None,
        status="Success",
        data=dict(
            apiModel=API_MODEL,
            socksProxy=SOCKS_PROXY,
            timeoutMs=TIMEOUT_MS
        )
    ))


@app.post("/chat-process")
async def chat_process(request_data: dict):
    prompt = request_data["prompt"]
    options = request_data["options"]

    if 1 == request_data["memory"]:
        memory_count = 5
    elif 50 == request_data["memory"]:
        memory_count = 20
    else:
        memory_count = 999

    if 1 == request_data["top_p"]:
        top_p = 0.2
    elif 50 == request_data["top_p"]:
        top_p = 0.5
    else:
        top_p = 1

    answer_text = process(prompt, options, memory_count, top_p, MASSAGE_STORE, model=API_MODEL)
    return StreamingResponse(content=answer_text, headers=stream_response_headers, media_type="text/event-stream")


@app.post("/audio-chat-process")
async def audio_chat_process(audio: UploadFile = File(...)):
    prompt = process_audio(audio, "whisper-1")
    return StreamingResponse(content=prompt, headers=stream_response_headers, media_type="text/event-stream")


def init_config():
    # 读取配置
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--openai_api_key', type=str, help='API key for OpenAI')
    parser.add_argument('--api_model', type=str, default="gpt-3.5-turbo",
                        help='OpenAI API model, default is gpt-3.5-turbo')
    parser.add_argument('--socks_proxy', type=str, default="",
                        help='Socks proxy, default is "", e.g. http://127.0.0.1:10808')
    parser.add_argument('--timeout_ms', type=str, default="100000", help="Timeout for OpenAI API, default is '100000'")
    parser.add_argument('--host', type=str, default="0.0.0.0", help='Host for server, default is 0.0.0.0')
    parser.add_argument('--port', type=str, default="3002", help="Port for server, default is '3002'")
    args = parser.parse_args()

    if not args.openai_api_key:
        err = "OpenAI API key is not found. use --openai_api_key to set it."
        logger.error(err)
        raise TypeError(err)
    openai_api_key = args.openai_api_key
    openai.api_key = args.openai_api_key

    api_model = args.api_model
    if not api_model:
        err = "API model is not found."
        logger.error(err)
        raise TypeError(err)
    if "gpt-3.5-turbo" != api_model:
        warning = "Api module '{}' has not been tested and there is no guarantee that it will work properly.".format(
            api_model
        )
        logger.warning(warning)

    socks_proxy = args.socks_proxy
    if socks_proxy:
        logger.info("Socks proxy is enabled.")
        logger.info("Socks proxy is {}.".format(socks_proxy))
        openai.proxy = socks_proxy
    else:
        logger.info("Socks proxy is disabled.")

    timeout_ms = args.timeout_ms or 100000
    if isinstance(timeout_ms, str):
        try:
            timeout_ms = int(timeout_ms)
        except:
            timeout_ms = 100000

    host = args.host or "0.0.0.0"
    port = args.port or 3002
    if isinstance(port, str):
        try:
            port = int(port)
        except:
            err = "Port must be a number."
            logger.error(err)
            raise TypeError(err)

    return massage_store, openai_api_key, host, port, api_model, socks_proxy, timeout_ms


if __name__ == "__main__":
    MASSAGE_STORE, OPENAI_API_KEY, HOST, PORT, API_MODEL, SOCKS_PROXY, TIMEOUT_MS = init_config()
    logger.info("OPENAI_API_KEY:{}".format(OPENAI_API_KEY))
    logger.info("HOST:{}".format(HOST))
    logger.info("PORT:{}".format(PORT))
    logger.info("API_MODEL:{}".format(API_MODEL))
    logger.info("SOCKS_PROXY:{}".format(SOCKS_PROXY))
    logger.info("TIMEOUT_MS:{}".format(TIMEOUT_MS))
    uvicorn.run(app, host=HOST, port=PORT)
