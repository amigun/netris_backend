import redis

r = redis.Redis(
    host='127.0.0.1',
    port=6379
)


def set_classes(
        filename: str,
        timestamp: str,
        classes: list[str]
):
    classes = map(str, classes)

    if classes:
        return r.lpush(
            f'{filename}:{timestamp}',
            *classes
        )


def get_classes(
        filename: str
):
    keys = r.keys(f'{filename}:*')

    latest_key = keys[-1] if keys else None

    if latest_key:
        values = r.lrange(latest_key, 0, -1)

        decoded_values = [value.decode('utf-8') for value in values]

        return decoded_values
    else:
        return []


def set_timestamp(
        filename: str,
        timestamp: int,
        klass: str,
        type_: str
):
    klass = str(klass)

    return r.set(
        f'{filename}:{klass}',
        f'{timestamp}:{type_}'
    )
