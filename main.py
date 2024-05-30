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
    page: int = 1,
):
    print("it's working")
    # COUNT_ROWS = 2
    # offset = (page - 1) * COUNT_ROWS
    # print(f"page = {page}, offset = {offset}")
    #
    # records = db.query(models.Film).offset(offset).limit(COUNT_ROWS)
    records = [
        {"time": "10-11-2023", "text": "example1"},
        {"time": "11-11-2023", "text": "example2"},
        {"time": "12-11-2023", "text": "example3"},
    ]
    page = 1
    context = {"request": request, "records": records, "page": page}
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
    for row in result_from_select:
        row_as_dict = row._mapping
        print(row_as_dict)
