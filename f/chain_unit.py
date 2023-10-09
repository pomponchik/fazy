from typing import Optional


class ChainUnit:
    def __init__(self, base: str, appendix: Optional[str] = None, lazy: bool = True) -> None:
        self.base = base
        self.appendix = appendix
        if self.appendix is not None:
            if self.appendix == '':
                raise SyntaxError('lazy f-string: empty expression not allowed')
