# main.py

from typing import Tuple, List, Dict, Union

class CoffeeOrder:
    """
    Класс для оформления заказа кофе в кофейне.
    Пользователь настраивает напиток: база, размер, молоко, сиропы, сахар, лед.
    """

    # --- Константы цен и лимитов ---
    BASE_PRICES: Dict[str, float] = {
        "espresso": 200.0,
        "americano": 250.0,
        "latte": 300.0,
        "cappuccino": 320.0,
    }
    SIZE_MULTIPLIERS: Dict[str, float] = {
        "small": 1.0,
        "medium": 1.2,
        "large": 1.4,
    }
    MILK_SURCHARGES: Dict[str, float] = {
        "none": 0.0,
        "whole": 30.0,
        "skim": 30.0,
        "oat": 60.0,
        "soy": 50.0,
    }
    SYRUP_SURCHARGE_PER_ITEM: float = 40.0
    ICED_SURCHARGE: float = 0.2  # Фиксированная доплата, НЕ множитель.

    MAX_SUGAR: int = 5
    MAX_SYRUPS: int = 4

    VALID_BASES: Tuple[str, ...] = tuple(BASE_PRICES.keys())
    VALID_SIZES: Tuple[str, ...] = tuple(SIZE_MULTIPLIERS.keys())
    VALID_MILKS: Tuple[str, ...] = tuple(MILK_SURCHARGES.keys())

    def __init__(
        self,
        base: str,
        size: str,
        milk: str = "none",
        syrups: Tuple[str, ...] = (),
        sugar: int = 0,
        iced: bool = False,
    ) -> None:
        """
        Инициализирует новый заказ кофе.

        Args:
            base (str): Основа напитка (espresso, americano, latte, cappuccino). Не может быть пустым.
            size (str): Размер напитка (small, medium, large). Не может быть пустым.
            milk (str, optional): Тип молока (none, whole, skim, oat, soy). По умолчанию "none".
            syrups (Tuple[str, ...], optional): Кортеж сиропов. По умолчанию пусто.
            sugar (int, optional): Количество ложек сахара. По умолчанию 0.
            iced (bool, optional): Напиток со льдом. По умолчанию False.

        Raises:
            ValueError: Если базовые параметры или опции не соответствуют ограничениям.
        """
        self.base: str = self._validate_base(base)
        self.size: str = self._validate_size(size)
        self.milk: str = self._validate_milk(milk)
        self.syrups: Tuple[str, ...] = self._validate_syrups(syrups)
        self.sugar: int = self._validate_sugar(sugar)
        self.iced: bool = iced

        self.price: float = self._calculate_price()
        self.description: str = self._generate_description()

    def _validate_base(self, base: str) -> str:
        """Валидирует основу напитка."""
        if not base:
            raise ValueError("Основа напитка не может быть пустой.")
        if base not in self.VALID_BASES:
            raise ValueError(
                f"Неверная основа напитка: '{base}'. Допустимые: {', '.join(self.VALID_BASES)}"
            )
        return base

    def _validate_size(self, size: str) -> str:
        """Валидирует размер напитка."""
        if not size:
            raise ValueError("Размер напитка не может быть пустым.")
        if size not in self.VALID_SIZES:
            raise ValueError(
                f"Неверный размер напитка: '{size}'. Допустимые: {', '.join(self.VALID_SIZES)}"
            )
        return size

    def _validate_milk(self, milk: str) -> str:
        """Валидирует тип молока."""
        if milk not in self.VALID_MILKS:
            raise ValueError(
                f"Неверный тип молока: '{milk}'. Допустимые: {', '.join(self.VALID_MILKS)}"
            )
        return milk

    def _validate_syrups(self, syrups: Tuple[str, ...]) -> Tuple[str, ...]:
        """Валидирует сиропы."""
        if not isinstance(syrups, tuple):
            raise TypeError("Сиропы должны быть кортежем.")
        if len(syrups) > self.MAX_SYRUPS:
            raise ValueError(
                f"Слишком много сиропов. Максимум {self.MAX_SYRUPS}."
            )
        # Можно добавить валидацию на конкретные виды сиропов, если они известны.
        # Например: VALID_SYRUPS = ("vanilla", "caramel")
        # if not all(s in VALID_SYRUPS for s in syrups):
        #    raise ValueError("Неверный сироп.")
        return syrups

    def _validate_sugar(self, sugar: int) -> int:
        """Валидирует количество сахара."""
        if not isinstance(sugar, int):
            raise TypeError("Сахар должен быть целым числом.")
        if not (0 <= sugar <= self.MAX_SUGAR):
            raise ValueError(
                f"Количество сахара должно быть от 0 до {self.MAX_SUGAR}."
            )
        return sugar

    def _calculate_price(self) -> float:
        """Подсчитывает итоговую цену заказа."""
        base_price = self.BASE_PRICES[self.base]
        size_multiplier = self.SIZE_MULTIPLIERS[self.size]
        milk_surcharge = self.MILK_SURCHARGES[self.milk]
        syrup_surcharge = len(self.syrups) * self.SYRUP_SURCHARGE_PER_ITEM
        iced_surcharge = self.ICED_SURCHARGE if self.iced else 0.0

        # Формула расчета цены: (базовая_цена * множитель_размера) + доплата_за_молоко + доплата_за_сиропы + доплата_за_лед
        total_price = (
            base_price * size_multiplier + milk_surcharge + syrup_surcharge + iced_surcharge
        )
        return round(total_price, 2)  # Округляем до двух знаков после запятой

    def _generate_description(self) -> str:
        """Генерирует человекочитаемое описание заказа."""
        parts: List[str] = [f"{self.size} {self.base}"]

        if self.milk != "none":
            parts.append(f"with {self.milk} milk")

        if self.syrups:
            syrup_list = ", ".join(self.syrups)
            parts.append(f"with {syrup_list} syrup{'s' if len(self.syrups) > 1 else ''}")

        if self.iced:
            parts.append("(iced)")

        if self.sugar > 0:
            parts.append(f"{self.sugar} tsp sugar")

        return " ".join(parts).replace(" /", "/") # Удаляем лишний пробел перед слешем, если он возникнет

    def __str__(self) -> str:
        """
        Возвращает описание заказа или краткую строку с ценой,
        если описание по какой-то причине пусто.
        """
        if self.description:
            return self.description
        return f"Кофе стоимостью {self.price}."


# --- Блок проверки реализации ---
if __name__ == "__main__":
    print("--- Проверка базовых заказов и валидации ---")

    # 1. Базовый заказ
    try:
        order1 = CoffeeOrder(base="latte", size="medium")
        print(f"Заказ 1: {order1} (Цена: {order1.price}$)")
        assert order1.base == "latte"
        assert order1.size == "medium"
        assert order1.milk == "none"
        assert order1.syrups == ()
        assert order1.sugar == 0
        assert order1.iced is False
        expected_price = CoffeeOrder.BASE_PRICES["latte"] * CoffeeOrder.SIZE_MULTIPLIERS["medium"]
        assert order1.price == round(expected_price, 2)
        print("Тест 1 пройден: Базовый заказ.")
    except Exception as e:
        print(f"Тест 1 провален: {e}")

    # 2. Заказ с молоком, сиропами, сахаром и льдом
    try:
        order2 = CoffeeOrder(
            base="cappuccino",
            size="large",
            milk="oat",
            syrups=("vanilla", "caramel"),
            sugar=2,
            iced=True,
        )
        print(f"Заказ 2: {order2} (Цена: {order2.price}$)")
        assert order2.base == "cappuccino"
        assert order2.size == "large"
        assert order2.milk == "oat"
        assert order2.syrups == ("vanilla", "caramel")
        assert order2.sugar == 2
        assert order2.iced is True
        expected_price = (
            CoffeeOrder.BASE_PRICES["cappuccino"] * CoffeeOrder.SIZE_MULTIPLIERS["large"]
            + CoffeeOrder.MILK_SURCHARGES["oat"]
            + 2 * CoffeeOrder.SYRUP_SURCHARGE_PER_ITEM
            + CoffeeOrder.ICED_SURCHARGE
        )
        assert order2.price == round(expected_price, 2)
        print("Тест 2 пройден: Полностью кастомизированный заказ.")
    except Exception as e:
        print(f"Тест 2 провален: {e}")

    # 3. Заказ с одной доп. опцией (iced)
    try:
        order3 = CoffeeOrder(base="americano", size="small", iced=True)
        print(f"Заказ 3: {order3} (Цена: {order3.price}$)")
        assert "iced" in str(order3)
        expected_price = CoffeeOrder.BASE_PRICES["americano"] * CoffeeOrder.SIZE_MULTIPLIERS["small"] + CoffeeOrder.ICED_SURCHARGE
        assert order3.price == round(expected_price, 2)
        print("Тест 3 пройден: Заказ со льдом.")
    except Exception as e:
        print(f"Тест 3 провален: {e}")
        
    # 4. Проверка исключений (пустая база)
    print("\n--- Проверка валидации (ошибки) ---")
    try:
        CoffeeOrder(base="", size="medium")
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")
        assert "Основа напитка не может быть пустой." in str(e)
    else:
        print("Ошибка: Пустая база не вызвала исключение.")

    # 5. Проверка исключений (неверный размер)
    try:
        CoffeeOrder(base="espresso", size="gigantic")
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")
        assert "Неверный размер напитка" in str(e)
    else:
        print("Ошибка: Неверный размер не вызвал исключение.")

    # 6. Проверка исключений (слишком много сахара)
    try:
        CoffeeOrder(base="latte", size="medium", sugar=10)
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")
        assert "Количество сахара должно быть" in str(e)
    else:
        print("Ошибка: Слишком много сахара не вызвало исключение.")

    # 7. Проверка исключений (слишком много сиропов)
    try:
        CoffeeOrder(base="latte", size="medium", syrups=("v", "c", "h", "m", "p"))
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")
        assert "Слишком много сиропов" in str(e)
    else:
        print("Ошибка: Слишком много сиропов не вызвало исключение.")
        
    # 8. Проверка описания с одним сиропом
    try:
        order4 = CoffeeOrder(base="espresso", size="small", syrups=("vanilla",))
        print(f"Заказ 4: {order4} (Цена: {order4.price}$)")
        assert "with vanilla syrup" in str(order4)
        print("Тест 4 пройден: Описание с одним сиропом.")
    except Exception as e:
        print(f"Тест 4 провален: {e}")

    print("\n--- Все основные проверки завершены. ---")

