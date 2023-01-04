import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar, Union

F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger("logger")


def backoff(
    exceptions: tuple,
    start_sleep_time: Union[int, float] = 0.1,
    factor: Union[int, float] = 2,
    border_sleep_time: Union[int, float] = 10,
) -> Callable[[F], F]:
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка. Использует наивный экспоненциальный рост времени
    повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func: Callable[[F], F]) -> Callable[[F], F]:
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            try:
                return func(*args, **kwargs)
            except exceptions as error:
                msg = "Error {error} from funk: {func}"
                logger.debug(msg.format(error=error, func=func.__name__))
                sleep_time = sleep_time * factor
                if sleep_time > border_sleep_time:
                    sleep_time = border_sleep_time
                time.sleep(sleep_time)

        return inner

    return func_wrapper
