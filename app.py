import uvicorn

from application import create_app

app = create_app()

conf = app.state.config

if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        host=conf.host,
        port=conf.port,
        reload=True,
        debug=True,
        # log_config='application/config/logging.conf'
    )
