LOG_SEPARATOR = " "

# описание номера столбцов лог-файла
COL_LOG_DATE = 0  # дата
COL_LOG_TIME = 1  # время
COL_LOG_KEY_ID = 2  # внутренний id сообщения
COL_LOG_FLAG = 3  # флаг
COL_LOG_ADDRESS = 4  # email адрес
COL_LOG_ANOTHER_INFO = 5  # другая информация
COL_LOG_END = 6

# возможные значения столбца FLAG
FLAG_TYPE_DELIVERY_ARRIVAL = (
    "<="  # прибытие сообщения (в этом случае за флагом следует адрес отправителя)
)
FLAG_TYPE_DELIVERY_NORMAL = "=>"  # нормальная доставка сообщения
FLAG_TYPE_DELIVERY_ADDRESS = "->"  # дополнительный адрес в той же доставке
FLAG_TYPE_DELIVERY_FAILED = "**"  # доставка не удалась
FLAG_TYPE_DELIVERY_DELAY = "=="  # доставка задержана (временная проблема)

# значения для обработки случая, когда сообщения не типа "ПРИБЫТИЕ"
NOT_ARRIVAL_ARRAY_OF_FLAG_TYPE = (
    FLAG_TYPE_DELIVERY_NORMAL,
    FLAG_TYPE_DELIVERY_ADDRESS,
    FLAG_TYPE_DELIVERY_FAILED,
    FLAG_TYPE_DELIVERY_DELAY,
)
MIN_COLS_IF_NOT_ARRIVAL = 4  # ограничение по размеры, если нет ПРИБЫТИЕ сообщения
BLACKHOLE_STR = ":blackhole:"  # случай, когда вместо адреса тэг blackhole

#Формат для отображения типа datetime
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

#Название столбцов, которые выводим на форме
COL_SHOW_TIME = "time"
COL_SHOW_TEXT = "text"