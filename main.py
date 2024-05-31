from typing import Annotated

from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.parse_log import parse_log_file
from sql.database import Session
from sql.database_func import select_values_from_tables, set_values_from_mail_log

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_populate_db():
    print("startup begin")

    current_session = Session()
    result_of_parse = parse_log_file("data/out")
    set_values_from_mail_log(current_session, result_of_parse)

    print("startup end")


@app.get("/index/", response_class=HTMLResponse)
async def index(
    request: Request,
    hx_request: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
    mail_name: str = "default",
):
    if mail_name != "default":
        records = select_values_from_tables(db, mail_name)
        context = {"request": request, "records": records}
        if hx_request:
            return templates.TemplateResponse("table.html", context)
    records = []
    context = {"request": request, "records": records}
    return templates.TemplateResponse(name="index.html", context=context)
