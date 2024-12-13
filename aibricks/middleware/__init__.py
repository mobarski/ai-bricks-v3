from .middleware import MiddlewareBase, MiddlewareMixin  # noqa

from .timing import TimingMiddleware  # noqa
from .logging import LoggingMiddleware  # noqa
from .summary import ChatSummaryMiddleware  # noqa
from .saveload import SaveLoadMiddleware  # noqa


# create mapping from middleware class name to class itself
MIDDLEWARE_MAPPING = {
    name: cls for name, cls in locals().items()
    if isinstance(cls, type) and issubclass(cls, MiddlewareBase) and cls != MiddlewareBase
}
