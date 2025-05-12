from functools import wraps
from app.db.database import sync_engine, async_engine


def sync_echo():
    """ Синхронный декоратор, позволяет прослушать echo конкретной функции """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            default_echo = sync_engine.echo

            if default_echo:
                return func(*args, **kwargs)

            print(f"Echo включен для функции {func.__name__}():")  # todo: добавить логирование вместо print()
            sync_engine.echo = True
            try:
                return func(*args, **kwargs)
            finally:
                sync_engine.echo = default_echo
                print(f"Echo возвращен к дефолтным настройкам")
        return wrapper
    return decorator


def async_echo():
    """ Асинхронный декоратор, позволяет прослушать echo конкретной функции """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            default_echo = async_engine.echo

            if default_echo:
                return await func(*args, *kwargs)

            print(f"Echo включен для функции {func.__name__}():")  # todo: добавить логирование вместо print()
            async_engine.echo = True
            try:
                return await func(*args, *kwargs)
            finally:
                async_engine.echo = default_echo
                print(f"Echo возвращен к дефолтным настройкам")
        return wrapper
    return decorator
