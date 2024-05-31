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
    mail_name: str = 'default',
):
    print(f'its working, email = {mail_name}')

    if mail_name != 'default':
        records = select_values_from_tables(
            db, mail_name
        )
        context = {"request": request, "records": records}
        if hx_request:
            return templates.TemplateResponse("table.html", context)
    records=[]
    context = {"request": request, "records": records}
    return templates.TemplateResponse(name="index.html", context=context)


@app.get('/disable')
def disable_mail(mail_name: str):
    return f'{mail_name} Введенное значение'


if __name__ == "__main__":
    print("create session")
    current_session = Session()

    result_from_select = select_values_from_tables(
        current_session, "kuxanwyqalsszn@gmail.com"
    )
    print(result_from_select)
    """
    for row in result_from_select:
        row_as_dict = row._mapping
        print(row_as_dict)
    """
