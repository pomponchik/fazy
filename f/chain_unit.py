class ChainUnit:
    def __init__(self, base, appendix=None, lazy=True):
        self.base = base
        self.appendix = appendix
        if self.appendix is not None:
            if self.appendix == '':
                raise SyntaxError('lazy f-string: empty expression not allowed')
