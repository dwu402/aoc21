class Expression():
    def __init__(self, parent=None):
        self.left = None
        self.right = None
        if parent:
            self.parent = parent
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.side = 'left'

    def __repr__(self):
        return f"[{repr(self.left)}, {repr(self.right)}]"

    def __add__(self, other):
        new_ex = Expression()
        self.parent = new_ex
        other.parent = new_ex

        new_ex.left = self
        new_ex.right = other

        self.add_depth()
        other.add_depth()

    def add_depth(self):
        self.depth += 1
        if isinstance(self.left, Expression):
            self.left.add_depth()
        if isinstance(self.right, Expression):
            self.right.add_depth()

    def explode(self):
        self.explode_left(self.left)
        self.explode_right(self.right)

        if self.parent.left is self:
            self.parent.left = 0
        elif self.parent.right is self:
            self.parent.right = 0
        else:
            raise RuntimeError()

    def explode_left(self, val):
        if not isinstance(self.parent.left, Expression):
            self.parent.left += val
        elif self.parent.depth > 0:
            self.parent.explode_left(val)

    def explode_right(self, val):
        if not isinstance(self.parent.right, Expression):
            self.parent.right += val
        elif self.parent.depth > 0:
            self.parent.explode_right(val)

    def split_left(self):
        lval = self.left
        new_ex = Expression(self)
        new_ex.left = lval//2
        new_ex.right = (lval+1)//2

    def split_right(self):
        rval = self.right
        new_ex = Expression(self)
        new_ex.left = rval//2
        new_ex.right = (rval+1)//2

def build(string):
    expression_stack = []
    for symbol in string:
        if symbol == '[':
            if len(expression_stack) == 0:
                expression_stack.append(Expression())
            else:
                expression_stack.append(Expression(parent=expression_stack[-1]))
        elif symbol == ']':
            expression_stack[-1].side = 'done'
            sub_ex = expression_stack.pop()
            if len(expression_stack) == 0:
                return sub_ex
            ex = expression_stack[-1]
            setattr(ex, ex.side, sub_ex)
        elif symbol == ',':
            expression_stack[-1].side = 'right'
        else:
            val = int(symbol)
            ex = expression_stack[-1]
            setattr(ex, ex.side, val)

def check(ex):
    if isinstance(ex.left, Expression):
        check(ex.left)
    elif isinstance(ex.right, Expression):
        check(ex.right)

    if ex.depth > 3:
        ex.explode()

    if not isinstance(ex.left, Expression) and ex.left > 9:
        ex.split_left()

    if not isinstance(ex.right, Expression) and ex.right > 9:
        ex.split_right()

if __name__ == '__main__':
    p = build('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
    check(p)
    print(p)