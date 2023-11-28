LEN_STEP = 0.65
M_IN_KM = 1000


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_MIN = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_speed = self.get_distance() / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / M_IN_KM
            * self.duration
            * self.H_IN_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CONST_AV_SPEED = 0.029
    WEIGHT_MULTIPLIER = 0.035
    KM_IN_M = 0.278
    SM_TO_M = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = (
            (
                self.WEIGHT_MULTIPLIER * self.weight
                + (
                    (self.get_mean_speed() * self.KM_IN_M) ** 2
                    / (self.height / self.SM_TO_M)
                )
                * self.CONST_AV_SPEED
                * self.weight
            )
            * self.duration
            * self.H_IN_MIN
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    SHIFT_AVERAGE_SPEED = 1.1
    SPEED_MULTIPLY = 2
    LEN_STEP = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        average_speed = (
            self.length_pool * self.count_pool
            / M_IN_KM / self.duration
        )
        return average_speed

    def get_spent_calories(self) -> float:
        spent_calories = (
            (self.get_mean_speed() + self.SHIFT_AVERAGE_SPEED)
            * self.SPEED_MULTIPLY
            * self.weight
            * self.duration
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return training_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
