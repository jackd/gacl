"""
gin-config + absl command line.

Example usage:

python -m gacl \\
    config1.gin config2.gin \\
    --bindings="
        custom_int_binding = 3
        custom_str_binding = 'hello world'
        configured_fun.foo = 'bar'
        main.fun = @configured_fun
"
"""

import gacl

if __name__ == "__main__":
    gacl.cli_main()
