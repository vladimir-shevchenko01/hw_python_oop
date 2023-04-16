"""
Модуль фитнес-трекера, который обрабатывает данные
для трёх видов тренировок: бега, спортивной ходьбы
и плавания.
"""


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65                          # Коэфицент расчета длины шага.
    M_IN_KM = 1000                           # М. в км..
    MIN_IN_HOUR = 60                         # М. в часе

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
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        av_speed = dist / self.duration
        return av_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> str:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__,
                           self.duration, distance,
                           speed, calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18    # множитель средней скорости
    CALORIES_MEAN_SPEED_SHIFT = 1.79       # коэфицент расхода калорий

    def get_spent_calories(self) -> float:
        av_speed = Training.get_mean_speed(self)
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * av_speed
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight
                          / self.M_IN_KM
                          * self.duration
                          * self.MIN_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_KMH_MS = 0.278                     # Константа скорости - м/c
    WEIGHT_COEF1 = 0.035                    # константа  множителя веса.
    WEIGHT_COEF2 = 0.029                    # 2я константа  множителя веса.
    M_TO_SM = 100                           # Константа метры в сантиметры.

    def __init__(self, action: int, duration: float,
                 weight: float, height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Подсчет сожжённых калорий."""
        si_av_speed = Training.get_mean_speed(self)
        si_height = self.height / self.M_TO_SM
        spent_calories = ((self.WEIGHT_COEF1 * self.weight
                           + ((si_av_speed * self.COEF_KMH_MS) ** 2
                               / si_height) * self.WEIGHT_COEF2 * self.weight)
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIM_CONST1 = 1.1
    SWIM_CONST2 = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: int, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        swim_av_speed = (self.length_pool
                         * self.count_pool
                         / self.M_IN_KM
                         / self.duration)
        return swim_av_speed

    def get_spent_calories(self) -> float:
        swim_av_speed = Swimming.get_mean_speed(self)
        swim_cal = ((swim_av_speed + self.SWIM_CONST1)
                    * self.SWIM_CONST2
                    * self.weight
                    * self.duration)
        return swim_cal


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывод сообщения о пройденой тренировке"""
        return ((f'Тип тренировки: {self.training_type}; '
                 f'Длительность: {self.duration:.3f} ч.; '
                 f'Дистанция: {self.distance:.3f} км; '
                 f'Ср. скорость: {self.speed:.3f} км/ч; '
                 f'Потрачено ккал: {self.calories:.3f}.'))


workout_dict = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in workout_dict:
        return workout_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
