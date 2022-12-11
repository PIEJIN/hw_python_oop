class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type,
                 duration, distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (
            # ("{:.2f}".format(number))
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:5.3f} ч.; '
            f'Дистанция: {self.distance:5.3f} км; '
            f'Ср. скорость: {self.speed:5.3f} км/ч; '
            f'Потрачено ккал: {self.calories:5.3f}. ')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.M_IN_KM = 1000
        self.LEN_STEP: float = 0.65

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

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.LEN_STEP: float = 0.65
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        CALORIES_MEAN_SPEED_MULTIPLIER = 18
        CALORIES_MEAN_SPEED_SHIFT = 1.79
        Hours_to_Mins = 60
# (18 * средняя_скорость + 1.79)
# * вес_спортсмена / M_IN_KM
# * время_тренировки_в_минутах
        return ((CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * Hours_to_Mins)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        self.height = height
        self.LEN_STEP: float = 0.65
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        CALORIES_MEAN_WEIGHT_MULTIPLIER1 = 0.035
        CALORIES_MEAN_WEIGHT_MULTIPLIER2 = 0.029
        # Часы в секунды
        Hrs_to_seconds = 3600
        # Часы в минуты
        Hrs_to_mins = 60
        # Метры в сантиметры
        M_to_sm = 100
        # Среднюю скорость км\ч в метры в секунду
        AVG_speed_m_per_sec = (self.get_mean_speed()
                               * self.M_IN_KM / Hrs_to_seconds)

        # ((0.035 * вес + (средняя_скорость_в_метрах_в_секунду**2
        #  / рост_в_метрах)* 0.029 * вес) * время_тренировки_в_минутах)
        result = (((CALORIES_MEAN_WEIGHT_MULTIPLIER1 * self.weight
                  + (AVG_speed_m_per_sec**2 / (self.height / M_to_sm))
                  * CALORIES_MEAN_WEIGHT_MULTIPLIER2 * self.weight)
                  * (self.duration * Hrs_to_mins)))
        return result


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self, action: int, duration: float, weight: float,
                 lenght_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool
        self.LEN_STEP: float = 1.38

    def get_mean_speed(self) -> float:
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        result = (self.lenght_pool * self.count_pool
                  / self.M_IN_KM / self.duration)
        return result

    def get_spent_calories(self) -> float:
        Speed_plus = 1.1
        Weight_multiplier = 2
        # (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        result = ((self.get_mean_speed() + Speed_plus)
                  * Weight_multiplier * self.weight * self.duration)
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
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
