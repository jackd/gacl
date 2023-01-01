import sys
import typing as tp

import gin
from absl import app, flags

from gacl.callbacks import Callback, CallbackList

flags.DEFINE_multi_string("gin_file", default=[], help="gin files to include")
flags.DEFINE_multi_string("bindings", default=[], help="Additional gin bindings")
flags.DEFINE_boolean(
    "finalize_config", default=True, help="Finalize gin config in main"
)
flags.DEFINE_multi_string(
    "config_path", default=[], help="Additional paths to search for .gin files"
)
flags.DEFINE_bool(
    "clargs_as_config",
    default=True,
    help="Interpret command line arguments as config files",
)


@gin.register(module="gacl")
def print_gin_config():
    print(gin.config.config_str())


@gin.configurable(module="gacl")
def main(
    fun: tp.Callable[[], tp.Any] = print_gin_config,
    callbacks: tp.Union[Callback, tp.Iterable[Callback]] = (),
    num_trials: int = 1,
):
    if isinstance(callbacks, Callback):
        callback = callbacks
    else:
        assert hasattr(callbacks, "__iter__"), callbacks
        callback = CallbackList(*callbacks)
    callback.on_start(num_trials)
    for trial_id in range(num_trials):
        callback.on_trial_start(trial_id)
        try:
            result = fun()
            callback.on_trial_completed(trial_id, result)
        except KeyboardInterrupt as interrupt:
            callback.on_trial_interrupt(trial_id, interrupt)
            raise interrupt
        except Exception as exception:  # pylint: disable=broad-except
            callback.on_trial_exception(trial_id, exception)
            raise exception
    callback.on_end()


def parse_clargs(args=None):
    if args is None:
        args = sys.argv
    FLAGS = flags.FLAGS
    files = FLAGS.gin_file
    if FLAGS.clargs_as_config:
        files = files + args[1:]
        del args[1:]
    bindings = FLAGS.bindings
    for path in FLAGS.config_path:
        gin.config.add_config_file_search_path(path)
    gin.parse_config_files_and_bindings(
        files, bindings, finalize_config=FLAGS.finalize_config
    )


def app_main(args=None):
    parse_clargs(args)
    main()


def cli_main():
    app.run(app_main)
