import functools
import random
import typing as tp

import gin

register = functools.partial(gin.register, module="gacl.callbacks")


class Callback:
    def on_start(self, num_trials: tp.Optional[int]):
        pass

    def on_end(self):
        pass

    def on_trial_start(self, trial_id: int):
        pass

    def on_trial_exception(self, trial_id: int, exception: Exception):
        pass

    def on_trial_interrupt(self, trial_id: int, interrupt: KeyboardInterrupt):
        pass

    def on_trial_completed(self, trial_id: int, result):
        pass


class CallbackList(Callback):
    def __init__(self, *callbacks):
        assert all(isinstance(callback, Callback) for callback in callbacks)
        self.callbacks: tp.Tuple[Callback, ...] = callbacks

    def on_start(self, num_trials: tp.Optional[int]):
        for callback in self.callbacks:
            callback.on_start(num_trials)

    def on_end(self):
        for callback in self.callbacks:
            callback.on_end()

    def on_trial_start(self, trial_id: int):
        for callback in self.callbacks:
            callback.on_trial_start(trial_id)

    def on_trial_completed(self, trial_id: int, result):
        for callback in self.callbacks:
            callback.on_trial_completed(trial_id, result)

    def on_trial_exception(self, trial_id: int, exception: Exception):
        for callback in self.callbacks:
            callback.on_trial_exception(trial_id, exception)

    def on_trial_interrupt(self, trial_id, interrupt: KeyboardInterrupt):
        for callback in self.callbacks:
            callback.on_trial_interrupt(trial_id, interrupt)


@register
class LambdaCallback(Callback):
    def __init__(
        self,
        *,
        on_start: tp.Optional[tp.Callable[[tp.Optional[int]], tp.Any]] = None,
        on_end: tp.Optional[tp.Callable] = None,
        on_trial_start: tp.Optional[tp.Callable[[int], tp.Any]] = None,
        on_trial_completed: tp.Optional[tp.Callable[[int, tp.Any], tp.Any]] = None,
        on_trial_exception: tp.Optional[tp.Callable[[int, Exception], tp.Any]] = None,
        on_trial_interrupt: tp.Optional[
            tp.Callable[[int, KeyboardInterrupt], tp.Any]
        ] = None,
    ):
        self._on_start = on_start
        self._on_end = on_end
        self._on_trial_start = on_trial_start
        self._on_trial_completed = on_trial_completed
        self._on_trial_exception = on_trial_exception
        self._on_trial_interrupt = on_trial_interrupt

    def on_start(self, num_trials: tp.Optional[int]):
        if self._on_start is not None:
            self._on_start(num_trials)

    def on_end(self):
        if self._on_end is not None:
            self._on_end()

    def on_trial_start(self, trial_id: int):
        if self._on_trial_start is not None:
            self._on_trial_start(trial_id)

    def on_trial_completed(self, trial_id: int, result):
        if self._on_trial_completed is not None:
            self._on_trial_completed(trial_id, result)

    def on_trial_exception(self, trial_id: int, exception: Exception):
        if self._on_trial_exception is not None:
            self._on_trial_exception(trial_id, exception)

    def on_trial_interrupt(self, trial_id: int, interrupt: KeyboardInterrupt):
        if self._on_trial_interrupt is not None:
            self._on_trial_interrupt(trial_id, interrupt)


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

    def on_start(self, num_trials: tp.Optional[int]):
        del num_trials
        if self.config_on_start:
            self.print_fun(gin.config.config_str())

    def on_end(self):
        if self.operative_config_on_end:
            self.print_fun(gin.config.operative_config_str())


@register
class RandomSeedSetter(Callback):
    def __init__(self, seed: int = 0):
        self.seed = seed

    def on_trial_start(self, trial_id: int):
        random.seed(self.seed + trial_id)
