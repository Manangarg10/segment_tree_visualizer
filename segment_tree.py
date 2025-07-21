class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.data = data
        self.build(0, 0, self.n - 1)

    def build(self, node, l, r):
        if l == r:
            self.tree[node] = self.data[l]
        else:
            mid = (l + r) // 2
            self.build(2 * node + 1, l, mid)
            self.build(2 * node + 2, mid + 1, r)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def push(self, node, l, r):
        if self.lazy[node] != 0:
            self.tree[node] += (r - l + 1) * self.lazy[node]
            if l != r:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0

    def range_update(self, ql, qr, val, node=0, l=0, r=None):
        if r is None:
            r = self.n - 1
        self.push(node, l, r)
        if qr < l or ql > r:
            return
        if ql <= l and r <= qr:
            self.lazy[node] += val
            self.push(node, l, r)
        else:
            mid = (l + r) // 2
            self.range_update(ql, qr, val, 2 * node + 1, l, mid)
            self.range_update(ql, qr, val, 2 * node + 2, mid + 1, r)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def range_query(self, ql, qr, node=0, l=0, r=None):
        if r is None:
            r = self.n - 1
        self.push(node, l, r)
        if qr < l or ql > r:
            return 0
        if ql <= l and r <= qr:
            return self.tree[node]
        mid = (l + r) // 2
        left = self.range_query(ql, qr, 2 * node + 1, l, mid)
        right = self.range_query(ql, qr, 2 * node + 2, mid + 1, r)
        return left + right

    def delete_index(self, idx):
        if 0 <= idx < len(self.data):
            self.data.pop(idx)
            self.__init__(self.data)
