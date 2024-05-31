from typing import Annotated

from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.parse_log import parse_log_file
from backend.constants import COL_SHOW_TEXT, COL_SHOW_TIME
from sql.database import Session
from sql.database_func import select_values_from_tables, set_values_from_mail_log

# models.Base.metadata.create_all(bind=engine)
MAX_COUNT_LENGTH_RECORDS = 100

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def is_constrain_length_for_records(records: list) -> bool:
    """
    Проверяет на удовлетв размерам
    :param records:
    :return:
    """
    if len(records) > MAX_COUNT_LENGTH_RECORDS:
        return False
    else:
        return True


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
    mail_name: str = "default",
):
    if mail_name != "default":
        records = select_values_from_tables(db, mail_name)

        # проверяем укладываемся ли в количество записей
        if not is_constrain_length_for_records(records):
            # если нет, генерируем текст сообщения
            records = [{COL_SHOW_TIME: f'Количество записей больше ограничения {MAX_COUNT_LENGTH_RECORDS}',
                       COL_SHOW_TEXT: ''}]

        context = {"request": request, "records": records}
        if hx_request:
            return templates.TemplateResponse("table.html", context)

    records = []
    context = {"request": request, "records": records}
    return templates.TemplateResponse(name="index.html", context=context)


if __name__ == '__main__':
    current_session = Session()
    print('Загружаем лог из файла')
    result_of_parse = parse_log_file("data/out")
    print('Сохраняем в базу')
    set_values_from_mail_log(current_session, result_of_parse)
    current_session.close()

