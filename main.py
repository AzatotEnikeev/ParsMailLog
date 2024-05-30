from typing import Annotated

from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import sql.models as models
from backend.parse_log import parse_log_file
from sql.database import Session, engine
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


@app.get("/index/", response_class=HTMLResponse)
async def index(
    request: Request,
    hx_request: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
):
    print("it's working")

    records = select_values_from_tables(
        db, "kuxanwyqalsszn@gmail.com"
    )
    context = {"request": request, "records": records}
    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse(name="index.html", context=context)


if __name__ == "__main__":
    print("create session")
    current_session = Session()
    """
    
    print("parse file")
    result_from_log = parse_log_file("data/out")
    print("into base")
    set_values_from_mail_log(current_session, result_from_log )
    print("select_values_from_tables")
    """

    result_from_select = select_values_from_tables(
        current_session, "kuxanwyqalsszn@gmail.com"
    )
    print(result_from_select)
    """
    for row in result_from_select:
        row_as_dict = row._mapping
        print(row_as_dict)
    """
