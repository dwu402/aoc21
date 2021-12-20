import enum

class Node():
    def __init__(self, string=None):
        self.left = None
        self.right = None
        self.up = None
        self.depth = 0
        self._side = 'left'

        if string is not None:
            self.parse(string)


    def __repr__(self):
        return f"[{repr(self.left)}, {repr(self.right)}]"

    def parse(self, string):
        nd = None
        for symbol in string:
            if symbol == '[':
                if nd is None:
                    nd = self
                else:
                    new_nd = Node()
                    if nd._side == 'left':
                        new_nd.depth = nd.depth + 1
                        nd.left = new_nd
                        new_nd.up = nd
                        nd = new_nd
                    else:
                        new_nd.depth = nd.depth + 1
                        nd.right = new_nd
                        new_nd.up = nd
                        nd = new_nd
            elif symbol == ',':
                nd._side = 'right'
            elif symbol == ']':
                nd = nd.up
            else:
                if nd._side == 'left':
                    nd.left = int(symbol)
                else:
                    nd.right = int(symbol)

    def scan(self):
        changed = False
        srch = [self]
        while len(srch) > 0:
            cand = srch.pop()
            if isinstance(cand, Node) and cand.depth > 3:
                # left search
                lval = cand.left
                lsrch = cand.up
                llast = cand
                while lsrch.up is not None:
                    if not isinstance(lsrch.right, Node):
                        lsrch.right += lval
                        break
                    if not isinstance(lsrch.left, Node):
                        lsrch.left += lval
                        break
                    elif lsrch.right is not llast:
                        llast = lsrch
                        lsrch = lsrch.right
                    elif lsrch.left is not llast:
                        llast = lsrch
                        lsrch = lsrch.left
                    else:
                        llast = lsrch
                        lsrch = lsrch.up
                # right search
                rval = cand.right
                rsrch = cand.up
                rlast = cand
                while rsrch.up is not None:
                    if not isinstance(rsrch.left, Node):
                        rsrch.left += rval
                        break
                    if not isinstance(rsrch.right, Node):
                        rsrch.right += rval
                        break
                    elif rsrch.left is not rlast:
                        rlast = rsrch
                        rsrch = rsrch.left
                    elif rsrch.right is not rlast:
                        rlast = rsrch
                        rsrch = rsrch.right
                    else:
                        rlast = rsrch
                        rsrch = rsrch.up
                # replace self with 0
                if cand.up.left is cand:
                    cand.up.left = 0
                else:
                    cand.up.right = 0
                changed = True
                break
            elif isinstance(cand, Node):
                for side in ['left', 'right']:
                    cnd = getattr(cand, side)
                    if not isinstance(cnd, Node) and cnd > 9:
                        cval = cnd
                        nnd = Node()
                        nnd.up = cand
                        nnd.left = cval//2
                        nnd.right = (cval+1)//2
                        nnd.depth = cand.depth + 1
                        setattr(cand, side, nnd)
                        changed = True
                        break
                if changed:
                    break

            if isinstance(cand.right, Node):
                srch.append(cand.right)
            if isinstance(cand.left, Node):
                srch.append(cand.left)

        return changed

    def simplify(self):
        changed = True
        while changed:
            print(self)
            changed = self.scan()

    def __add__(self, other):
        nt = Node()
        nt.left = self
        nt.right = other

        self.up = nt
        other.up = nt

        self.add_depth()
        other.add_depth()

        nt.simplify()

        return nt

    def add_depth(self):
        self.depth += 1
        if isinstance(self.left, Node):
            self.left.add_depth()
        if isinstance(self.right, Node):
            self.right.add_depth()


if __name__ == "__main__":
    x = Node('[[[[4,3],4],4],[7,[[8,4],9]]]') + Node('[1,1]')
    print(x)