from fastapi import FastAPI, Response

# I like to launch directly and not use the standard FastAPI startup
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the Merry Men Trading App Securities Microservice. Stay tuned for future updates!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"AWSome Merry Men cloud developer rao2140 says hello {name}"}


@app.get("/hello_text/{name}")
async def say_hello_text(name: str):
    the_message = f"AWSome Merry Men cloud developer rao2140 says Hello {name}"
    rsp = Response(content=the_message, media_type="text/plain")
    return rsp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8015)
