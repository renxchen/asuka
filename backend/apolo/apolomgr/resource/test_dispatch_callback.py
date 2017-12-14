class CollectionPolicy(object):
    def __init__(self, data):
        self.data = data

    def block1(self):
        return self.data + 'this is b1-->'

    def block2(self):
        return self.data + 'this is b2--> '

    def data1(self):
        return self.data + 'this is d1'


class Dispatch(object):
    def __init__(self):
        self.instance = CollectionPolicy('111')
        self.tree = {
            '1': 'block1',
            '2': 'block2',
            '3': 'data1'
        }

    def dispatch(self):
        result = None
        for order in sorted(self.tree.keys()):
            func_name = self.tree.get(order)
            result = getattr(self.instance, func_name)()
            setattr(self.instance, 'data', result)
        return result


def test():
    res = Dispatch().dispatch()
    print res


test()
