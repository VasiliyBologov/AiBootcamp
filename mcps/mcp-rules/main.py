from mcp.server.fastmcp import FastMCP
from typing import Dict, List

mcp = FastMCP("SupportBot")

# Категории по которым отвечает агент
FAQ_RESPONSES = {
    "доставка": (
        "Доставка осуществляется по всей территории Европы и стран СНГ. "
        "Срок доставки зависит от региона и обычно составляет от 2 до 7 рабочих дней.\n\n"
        "Стоимость доставки рассчитывается автоматически при оформлении заказа\n"
        "Бесплатная доставка действует при заказе от определённой суммы (уточняйте у оператора)\n"
        "Вы получаете трек-номер для отслеживания после отправки заказа"
    ),
    "гарантии": (
        "Гарантия качества распространяется на всю продукцию, сертифицированную по европейским стандартам (CPNP).\n\n"
        "Продукция оригинальна и проходит контроль качества\n"
        "При обнаружении производственного брака мы заменим товар за наш счёт\n"
        "Сохраняйте упаковку и чек — они нужны для оформления возврата"
    ),
    "возврат": (
        "Возврат товаров возможен в течение 14 дней с момента получения, если:\n"
        "Продукт не был в использовании\n"
        "Сохранена оригинальная упаковка\n"
        "Есть подтверждение покупки\n\n"
        "Возврат средств производится тем же способом, которым была совершена оплата, в течение 5 рабочих дней после получения возврата на склад."
    ),
    "скидки": (
        "Чтобы получать скидки и участвовать в программах лояльности, необходимо зарегистрироваться при первой покупке. "
        "Если сумма первой покупки менее 25 PV — клиент получает 10% скидку на один заказ, сгорающую при следующей покупке. "
        "После этого скидки накапливаются: 50 PV — 3%, 100 PV — 5%, 150 PV — 7%, 200 PV — 10% (постоянная).\n\n"
        "Если первая покупка от 25 PV, вы сразу становитесь партнёром и получаете скидку 30–40% плюс возможность участвовать в бонусной системе."
    ),
    "партнерская программа": (
        "Партнёр — это лояльный потребитель, совершающий ежемесячные покупки от 25 PV и более. "
        "Он автоматически попадает в партнёрскую систему и может:\n"
        "Получать скидку 30–40% на личные заказы\n"
        "Продавать продукцию онлайн и офлайн\n"
        "Получать выплаты от товарооборота своей сети\n"
        "Отслеживать бонусы и заказы в личном кабинете\n\n"
        "Статусы:\n"
        "Клиент «С» — менее 25 PV/мес\n"
        "Партнёр «Р» — от 25 PV/мес\n\n"
        "С GITER вы получаете не просто продукцию, а возможность развивать личный бренд и доход."
    ),
    "франшиза": (
        "Франшиза Giter — это готовый бизнес под брендом с высокой маржой и поддержкой на каждом этапе.\n\n"
        "Преимущества:\n"
        "Высокое качество продукции и европейская сертификация (CPNP)\n"
        "Доходность: маржа 120–150% с продаж\n"
        "Быстрая окупаемость: от 3 месяцев\n"
        "Гибкая бизнес-модель — подходит как для больших, так и для малых городов\n"
        "Не требует крупных инвестиций\n\n"
        "Финансовые условия:\n"
        "Вход от 5000€\n"
        "Закупка продукции от 3000€\n"
        "Роялти: 0€\n"
        "Паушальный взнос: 0€\n"
        "Средний доход: от 3000€/мес и выше\n\n"
        "Что вы получаете:\n"
        "Право использовать бренд на территории Европы и СНГ\n"
        "Поддержку и сопровождение бизнеса\n"
        "Разработку интернет-магазина и дизайн бутика\n"
        "Систему обучения персонала\n"
        "Рекламную и маркетинговую поддержку\n"
        "Бесплатные тестеры и бонусы в зависимости от объёма\n"
        "Эффективные методики управления и развития точки продаж\n\n"
        "С франшизой Giter вы входите в мир красоты с надёжной системой и перспективами роста."
    )
}
@mcp.tool(name="List-of-topics", description="Returns the list of topics for frequently asked questions")
def topics() -> List[str]:
    """
    Returns a list of topics that match frequently asked questions.

    This function iterates through the predefined FAQ topics and
    checks if they match the given question. It collects all
    the matched topics and returns them as a list.

    :returns: A list of topics that match questions based on the
              given FAQ_RESPONSES mapping.

    :rtype: List[str]
    """
    res = []
    for key in FAQ_RESPONSES.keys():
        res.append(key)
    return res


@mcp.tool(name="Info-by-key", description="Returns the answer to a frequently asked question using a provided key. ")
def info_by_key_of_topit(key: str) -> str:
    """
    Returns the answer to a frequently asked question using a provided key.

    This method uses a dictionary, `FAQ_RESPONSES`, to map provided keys to
    corresponding pre-defined responses. If the key exists in the dictionary,
    its associated response is returned. If the key is not found, a default
    response is returned, asking the user to rephrase or clarify their request.

    :param key: A string representing the key to lookup a corresponding
        response in the FAQ_RESPONSES dictionary.
    :return: A string containing the response to the corresponding key, or a
        empty string if the key is not found.
    """
    if key in FAQ_RESPONSES.keys():
        return FAQ_RESPONSES[key]
    return ""
