class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def unite(self, i, j):
        irep = self.find(i)
        jrep = self.find(j)
        self.parent[irep] = jrep

    def get_disjoint_sets(self):
        disjoint_sets = {}
        for i in range(len(self.parent)):
            root = self.find(i)

            if root not in disjoint_sets:
                disjoint_sets[root] = []
            disjoint_sets[root].append(i)

        return list(disjoint_sets.values())
