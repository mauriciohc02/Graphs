from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils.graph import Graph


class AddRemoveEdgeWindow(QWidget):
    """
    class to display a pop-up window where 
    the origin and destination of the new edge are entered.
    """

    def __init__(self, type=1):
        super().__init__()
        self.center()
        self.error_message = QMessageBox()

        layouth = QHBoxLayout()
        layoutv = QVBoxLayout()
        self.label = QLabel("From:")
        self.input = QLineEdit()
        self.label2 = QLabel("To:")
        self.input2 = QLineEdit()
        self.buttonDo = QPushButton("")
        layouth.addWidget(self.label)
        layouth.addWidget(self.input)
        layouth.addWidget(self.label2)
        layouth.addWidget(self.input2)
        layoutv.addLayout(layouth)
        layoutv.addWidget(self.buttonDo)
        self.setLayout(layoutv)

        self.changeType(type)

    def changeType(self, type):
        text = "Add Edge" if type == 1 else "Remove Edge"
        self.setWindowTitle(text)
        self.buttonDo.setText(text)

    def center(self):
        """ 
            Method to center the window with respect 
            to the size of the screen from which the program is executed

            Args: None
            Returns: None    
        """

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class StartTraversalWindow(QWidget):
    """
    Class to display a pop-up window in which 
    the user enters the node where the traversal starts.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Start Traversal')
        self.center()

        layout = QVBoxLayout()
        self.label = QLabel("Which node do you want to start the traversal:")
        self.input = QLineEdit()
        self.buttonAdd = QPushButton("Start Traversal")
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.buttonAdd)
        self.setLayout(layout)

    def center(self):
        """ 
            Method to center the window with respect to the 
            size of the screen from which the program is executed

            Args: None
            Returns: None    
        """

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class GraphAnimation(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # Set icon size and initialize UI elements
        self.icon_size: int = 50
        self.init_UI()
        # A list with all the QPointF
        self.qPointsF: list = []
        # A list with all edges
        self.edges: list = []
        # An object of the graph class
        self.graph = Graph()

        # A list containing the points of the traversal
        self.dfs_traversal: list = []
        self.bfs_traversal: list = []

        self.start_animation = False
        self.active_traversal = None
        self.current_circle_index = -1
        self.paint = True

        # auxiliary list for the points that have already been painted orange
        self.painted_circles = []

        # timer to control that the points are painted every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCircle)
        self.timer.start(1000)

        self.tracking = None


    def init_UI(self) -> None:
        """
        Create each element and object of the Widget UI
        returns: None
        rtype: None
        """
        self.startTraversalWindow = StartTraversalWindow()


        self.button_reset = QPushButton(QIcon('./images/remove_all.png'), '', self)
        self.button_reset.setIconSize(QSize(self.icon_size, self.icon_size))
        self.button_reset.setToolTip('Reset Animation')
        self.button_reset.clicked.connect(self.reset)

        self.button_add_edge = QPushButton(QIcon('./images/add_edge.png'), '', self)
        self.button_add_edge.setIconSize(QSize(self.icon_size, self.icon_size))
        self.button_add_edge.setToolTip('Add Edge')
        self.button_add_edge.clicked.connect(self.add_edge)

        self.button_remove_edge = QPushButton(QIcon('./images/remove_edge.png'), '', self)
        self.button_remove_edge.setIconSize(QSize(self.icon_size, self.icon_size))
        self.button_remove_edge.setToolTip('Remove Edge')
        self.button_remove_edge.clicked.connect(self.remove_edge)

        self.button_bfs = QPushButton(QIcon('./images/bfs.png'), '', self)
        self.button_bfs.setIconSize(QSize(self.icon_size, self.icon_size))
        self.button_bfs.setToolTip('Breadth-First Search')
        self.button_bfs.clicked.connect(self.bfs_animation)

        self.button_dfs = QPushButton(QIcon('./images/dfs.png'), '', self)
        self.button_dfs.setIconSize(QSize(self.icon_size, self.icon_size))
        self.button_dfs.setToolTip('Depth-First Search')
        self.button_dfs.clicked.connect(self.dfs_animation)

        self.layout_aux = QHBoxLayout()
        self.layout_aux.addWidget(self.button_add_edge)
        self.layout_aux.addWidget(self.button_remove_edge)
        self.layout_aux.addWidget(self.button_reset)
        self.layout_aux.addWidget(self.button_bfs)
        self.layout_aux.addWidget(self.button_dfs)
        self.layout_aux.addStretch(1)

        self.layout_main = QVBoxLayout()
        self.layout_main.addLayout(self.layout_aux)
        self.layout_main.addStretch(1)
        self.setLayout(self.layout_main)

        self.welcome_message = QMessageBox(self)
        self.welcome_message.setWindowTitle('Welcome')
        self.welcome_message.setInformativeText(
            'Welcome to Graph!\nClick on the screen and see what happens!')


    def draw_points(self, painter) -> None:
        """
        Draw the points where the user has clicked
        returns: None
        rtype: None
        """
        painter.setBrush(QBrush(QColor('white')))        
        painter.setPen(QPen(QColor('black'), 3))

        for p in self.qPointsF:
            painter.drawEllipse(p, 20, 20)
            node_value = str(self.qPointsF.index(p))
            painter.drawText(int(p.x() - 5), int(p.y() + 5), node_value)


    def buttons_enabled(self, b):
        # method to deactivate or activate buttons
        self.button_dfs.setEnabled(b)
        self.button_bfs.setEnabled(b)
        self.button_add_edge.setEnabled(b)
        self.button_remove_edge.setEnabled(b)


    def updateCircle(self):
        # method to change every two seconds which points should be painted
        if self.start_animation:
            self.current_circle_index = self.current_circle_index + 1
            if self.current_circle_index >= len(self.active_traversal):
                self.paint = False
                self.buttons_enabled(True)
            else:
                circle = self.active_traversal[self.current_circle_index]
                self.painted_circles.append(circle)
                self.buttons_enabled(False)
        self.update()


    def draw_edges(self, painter):
        """
        Draw the edge that the user has wrote
        returns: None
        rtype: None
        """
        # painter.setBrush(QBrush(QColor('white')))
        painter.setPen(QPen(QColor('black'), 3))

        self.edges.clear()

        for i in range(len(self.graph.adj_matrix)):
            for j in range(len(self.graph.adj_matrix[i])):
                if self.graph.adj_matrix[i][j]:
                    edge = QLineF(QPointF(self.qPointsF[i]), QPointF(self.qPointsF[j]))
                    self.edges.append(edge)

        for l in self.edges:
            painter.drawLine(l)


    def getOriginDestination(self, type):
        # print(type)
        if self.graph.size == 0:
            self.AddRemoveEdgeWindow.hide()
            self.messageBox(QMessageBox.Information, "No hay nodos", "El grafo actual no cuenta con nodos")
            return

        # method to obtain the origin and destination points of the arrow
        origin = self.AddRemoveEdgeWindow.input.text()
        destination = self.AddRemoveEdgeWindow.input2.text()
        # the data must be numbers
        if origin.isdigit() and destination.isdigit():
            self.AddRemoveEdgeWindow.hide()
            # if there is not yet an edge between these nodes

            if type == 1:
                if self.graph.has_edge(int(origin), int(destination)) == False:
                    # if the origin and destination are not the same
                    if (origin != destination):
                        self.graph.add_edge(int(origin), int(destination))

                        p1 = self.qPointsF[int(origin)]
                        p2 = self.qPointsF[int(destination)]
                        edge = QLineF(p1, p2)

                        self.edges.append(edge)
                    else:
                        self.messageBox(QMessageBox.Critical, "Error!", "No se puede unir el nodo consigo mismo")
                elif self.graph.has_edge(int(origin), int(destination)) == True:
                    self.messageBox(QMessageBox.Information, "Hecho!", "El enlace ya ha sido creado")
                else:
                    self.messageBox(QMessageBox.Information, "No existe!", "Los nodos a unir no existen")

            elif type == 2:
                if (self.graph.has_edge(int(origin), int(destination)) == True):
                    self.graph.remove_edge(int(origin), int(destination))
                    index = 0
                    for i, edge in enumerate(self.edges):
                        if edge.p1() == self.qPointsF[int(origin)] and edge.p2() == self.qPointsF[int(destination)]:
                            index = i
                        elif edge.p1() == self.qPointsF[int(destination)] and edge.p2() == self.qPointsF[int(origin)]:
                            index = 1
                        else:
                            index = None

                        if index:
                            self.edges.pop(index)
                else:
                    self.messageBox(QMessageBox.Information, "No existe!", "El enlace que quiere eliminar no existe")

            self.update()


    def add_edge(self):
        # the window for adding an edge is activated
        self.AddRemoveEdgeWindow = AddRemoveEdgeWindow()
        self.AddRemoveEdgeWindow.changeType(1)
        self.AddRemoveEdgeWindow.buttonDo.clicked.connect(lambda _, type=1: self.getOriginDestination(type))
        self.AddRemoveEdgeWindow.show()
        

    def remove_edge(self):
        # the window for removing an edge is activated
        self.AddRemoveEdgeWindow = AddRemoveEdgeWindow()
        self.AddRemoveEdgeWindow.changeType(2)
        self.AddRemoveEdgeWindow.buttonDo.clicked.connect(lambda _, type=2: self.getOriginDestination(type))
        self.AddRemoveEdgeWindow.show()


    def dfs_animation(self):
        self.startTraversalWindow.show()
        self.startTraversalWindow.buttonAdd.clicked.connect(
            self.getFirstNodeDFS)


    def bfs_animation(self):
        self.startTraversalWindow.show()
        self.startTraversalWindow.buttonAdd.clicked.connect(
            self.getFirstNodeBFS)
        

    def getFirstNodeBFS(self):
        if self.graph.size == 0:
            return

        # method to obtain the list with bfs route
        node = self.startTraversalWindow.input.text()
        if node.isdigit():
            self.startTraversalWindow.hide()
            if int(node) <= self.graph.size:
                first_node = int(node)
                self.bfs(first_node)
                self.start_animation = True
                self.active_traversal = self.bfs_traversal


    def getFirstNodeDFS(self):
        if self.graph.size == 0:
            return

        # method to obtain the list with dfs route
        node = self.startTraversalWindow.input.text()
        if node.isdigit():
            self.startTraversalWindow.hide()
            if int(node) <= self.graph.size:
                first_node = int(node)
                visited = [False] * len(self.graph.adj_matrix)
                self.dfs(visited, first_node)
                self.start_animation = True
                self.active_traversal = self.dfs_traversal

    def bfs(self, start):
        visited = [False] * len(self.graph.adj_matrix)
        queue = [start]
        visited[start] = True

        while queue:
            node = queue.pop(0)
            self.bfs_traversal.append(self.qPointsF[node])

            for neighbor, connected in enumerate(self.graph.adj_matrix[node]):
                if connected and not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

    def dfs(self, visited, node):
        visited[node] = True
        self.dfs_traversal.append(self.qPointsF[node])
        self.update()
        for i, adyacente in enumerate(self.graph.adj_matrix[node]):
            if adyacente and not visited[i]:
                self.dfs(visited, i)

    def reset(self) -> None:
        """
        Reset animation to its initial state
        returns: None
        rtype: None
        """
        self.qPointsF.clear()
        self.edges.clear()
        self.dfs_traversal.clear()
        self.bfs_traversal.clear()
        self.graph.adj_matrix.clear()
        self.graph.size = 0
        self.start_animation = False
        self.active_traversal = None
        self.current_circle_index = -1
        self.painted_circles.clear()
        self.paint = True
        self.buttons_enabled(True)
        self.update()

    def paintEvent(self, event) -> None:
        """
        Draw the animation every time an event happen
        returns: None
        rtype: None
        """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        self.draw_edges(painter)
        self.draw_points(painter)

        if self.active_traversal is not None:
            for i, circle in enumerate(self.active_traversal):
                if self.paint:
                    painter.setBrush(QBrush(Qt.NoBrush))
                    if circle in self.painted_circles or i == self.current_circle_index:
                        painter.setPen(QPen(QColor('orange'), 4))
                    else:
                        painter.setPen(QPen(QColor('black'), 3))
                    painter.drawEllipse(circle, 20, 20)
                else:
                    self.dfs_traversal.clear()
                    self.bfs_traversal.clear()
                    self.current_circle_index = -1
                    self.paint = True
                    self.painted_circles.clear()
                    self.start_animation = False
                    self.active_traversal = None

    def mousePressEvent(self, event) -> None:
        """
        Selects the closest point when user click with its mouse
        returns: None
        rtype: None
        """
        if not self.start_animation:
            flag = True
            for z in self.qPointsF:
                d = ((event.x() - z.x())**2)+((event.y() - z.y())**2)
                if (d < 500):
                    flag = False
            if flag:
                p = QPointF(event.x(), event.y())
                self.graph.add_node()
                self.qPointsF.append(p)

            self.update()

    def mouseMoveEvent(self, event) -> None:
        """
        Update the position of the selected point
        returns: None
        rtype: None
        """
        if not self.start_animation:
            i = min(
                range(len(self.qPointsF)),
                key=lambda i: (
                    event.x() - self.qPointsF[i].x()) ** 2 + (event.y() - self.qPointsF[i].y()) ** 2
            )

            self.tracking = lambda p: self.qPointsF.__setitem__(i, p)
            self.tracking(QPointF(event.x(), event.y()))
            
            self.update()

    def mouseReleaseEvent(self, event) -> None:
        """
        Reset self.tracking when a mouseEvent is over
        returns: None
        rtype: None
        """
        self.tracking = None

    def messageBox(self, icon, title, text):
        msgBox = QMessageBox()
        msgBox.setIcon(icon)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Close)
        msgBox.exec()

    def __str__(self) -> str:
        return f'GraphAnimation Object'
