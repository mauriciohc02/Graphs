class Graph:
    def __init__(self) -> None:
        self.adj_matrix = []
        self.size = 0

    def add_node(self) -> None:
        """
        Method to add a node and its corresponding data to the adjacency matrix
        """
        self.size += 1
        new_node = []
        for _ in range(self.size):
            new_node.append(False)

        self.adj_matrix.append(new_node)

        if self.size > 1:
            self.update_nodes()

    def update_nodes(self) -> None:
        # Method for updating the size of adjacency matrix lists
        for node in self.adj_matrix:
            n = self.size - len(node)
            for _ in range(n):
                node.append(False)

    def add_edge(self, i, j):
        # Method to add an arist from one node to another node
        self.adj_matrix[i][j] = True

    """
    def remove_edge(self, i, j):
        self.adj_matrix[i][j] = False
    """

    def has_edge(self, i, j):
        # Method to verify if there is a connection between two nodes
        try:
            return self.adj_matrix[i][j]
        except:
            return True

    def __str__(self) -> str:
        return f'Graph Object'
