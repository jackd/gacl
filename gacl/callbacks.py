import functools
import random
import typing as tp

import gin

register = functools.partial(gin.register, module="gacl.callbacks")


class Callback:
    def on_start(self):
        pass

    def on_completed(self, result):
        pass

    def on_exception(self, exception: Exception):
        pass

    def on_interrupt(self, interrupt: KeyboardInterrupt):
        pass


class CallbackList(Callback):
    def __init__(self, *callbacks):
        assert all(isinstance(callback, Callback) for callback in callbacks)
        self.callbacks: tp.Tuple[Callback, ...] = callbacks

    def on_start(self):
        for callback in self.callbacks:
            callback.on_start()

    def on_completed(self, result):
        for callback in self.callbacks:
            callback.on_completed(result)

    def on_exception(self, exception: Exception):
        for callback in self.callbacks:
            callback.on_exception(exception)

    def on_interrupt(self, interrupt: KeyboardInterrupt):
        for callback in self.callbacks:
            callback.on_interrupt(interrupt)


@register
class LambdaCallback(Callback):
    def __init__(
        self,
        on_start: tp.Optional[tp.Callable] = None,
        on_completed: tp.Optional[tp.Callable] = None,
        on_exception: tp.Optional[tp.Callable] = None,
        on_interrupt: tp.Optional[tp.Callable] = None,
    ):
        self._on_start = on_start
        self._on_completed = on_completed
        self._on_exception = on_exception
        self._on_interrupt = on_interrupt

    def on_start(self):
        if self._on_start is not None:
            self._on_start()

    def on_completed(self, result):
        if self._on_completed is not None:
            self._on_completed(result)

    def on_exception(self, exception: Exception):
        if self._on_exception is not None:
            self._on_exception(exception)

    def on_interrupt(self, interrupt: KeyboardInterrupt):
        if self._on_interrupt is not None:
            self._on_interrupt(interrupt)


@register
class GinConfigLogger(Callback):
    def __init__(
        self,
        config_on_start: bool = True,
        operative_config_on_end: bool = False,
        print_fun: tp.Callable[[str], tp.Any] = print,
    ):
        self.config_on_start = config_on_start
        self.operative_config_on_end = operative_config_on_end
        self.print_fun = print_fun

    def on_start(self):
        if self.config_on_start:
            self.print_fun(gin.config.config_str())

    def on_end(self, result):
        del result
        if self.operative_config_on_end:
            self.print_fun(gin.config.operative_config_str())


@register
class RandomSeedSeeter(Callback):
    def __init__(self, seed: int = 0):
        self.seed = seed

    def on_start(self):
        random.seed(self.seed)
