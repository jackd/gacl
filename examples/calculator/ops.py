import gin


@gin.configurable
def add(x, y):
    result = x + y
    print(f"{x} + {y} = {result}")
    return result


@gin.configurable
def mul(x, y):
    result = x * y
    print(f"{x} * {y} = {result}")
    return result
