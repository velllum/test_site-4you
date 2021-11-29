import uvicorn

from application import create_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        host=app.state.config.host,
        port=app.state.config.port,
        reload=True,
        debug=True
    )
