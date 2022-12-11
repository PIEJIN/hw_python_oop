class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type,
                 duration, distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Получаем дистанцию в километрах
        AVG_distance = self.get_distance()
        # Возвращаем сред.скорость в км\ч
        return AVG_distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        InfoMessageObject = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )  # training_type, duration, distance, speed, calories
        return InfoMessageObject


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.LEN_STEP: float = 0.65
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        Hours_to_Mins = 60
# (18 * средняя_скорость + 1.79)
# * вес_спортсмена / M_IN_KM
# * время_тренировки_в_минутах
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * Hours_to_Mins)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        self.height = height
        self.LEN_STEP: float = 0.65
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        # Часы в минуты
        Hrs_to_mins = 60
        # Среднюю скорость км\ч в метры в секунду
        AVG_speed_m_per_sec = (self.get_mean_speed()
                               * self.KMH_IN_MSEC)

        result = (((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                  + (AVG_speed_m_per_sec**2 / (self.height / self.CM_IN_M))
                  * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                  * (self.duration * Hrs_to_mins)))
        return result


class Swimming(Training):
    """Тренировка: плавание."""

    Speed_plus = 1.1
    Weight_multiplier = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP: float = 1.38

    def get_mean_speed(self) -> float:
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        result = (self.length_pool * self.count_pool
                  / self.M_IN_KM / self.duration)
        return result

    def get_spent_calories(self) -> float:
        # (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        result = ((self.get_mean_speed() + self.Speed_plus)
                  * self.Weight_multiplier * self.weight * self.duration)
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    code_and_class_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    object = code_and_class_dict[workout_type](*data)
    return object


def main(training: Training) -> str:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
