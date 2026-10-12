# topic_6/final_soc_center/main.py
import subprocess
import sys
from pathlib import Path

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.router import router
from backend.agents import create_agents

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.supervisor = await create_agents()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)


def main():
    project_dir = Path(__file__).parent
    ui_file = project_dir / "ui.py"

    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", str(ui_file)]
    )

    try:
        # Reload only the FastAPI worker when Python files in this project change.
        # `reload=True` requires an import string rather than the app object.
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            reload_dirs=[str(project_dir)],
        )
    finally:
        # Stop Streamlit when FastAPI / this launcher stops
        streamlit_process.terminate()
        streamlit_process.wait()


if __name__ == "__main__":
    main()
