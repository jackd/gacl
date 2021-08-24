import sys
import typing as tp

import gin
from absl import app, flags

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


def print_gin_config():
    print(gin.config.config_str())


@gin.configurable(module="gacl")
def main(fun: tp.Callable[[], tp.Any] = print_gin_config):
    return fun()


def app_main(args=None):
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
    main()


def cli_main():
    app.run(app_main)
