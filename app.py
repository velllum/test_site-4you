import uvicorn

from application import create_app
from application.config.settings import settings

app = create_app()

conf = app.state.config

if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        host=settings.host,
        port=settings.port,
        reload=True,
        debug=True,
        log_config='application/config/logging.conf'
    )
