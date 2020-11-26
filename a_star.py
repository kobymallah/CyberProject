import scipy.spatial.distance as dist
import numpy as np


class Node:

    def __init__(self, parent, position):
        """
        Initializing a new node with a parent and position and initialize the g, h and f values
        :param parent:
        :param position:
        """
        self.parent = parent
        self.position = np.array(position)

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        """
        Compares the positions of this node and the other node
        :param other: the other node
        :return: True if the positions are equal and False otherwise
        """
        return np.array_equal(self.position, other.position)


def a_star(env, start):
    """
    Finds the shortest path from start to goal and returns a list of tuples that represents the path

    :param env: the environment
    :param start: start position
    :param end: goal position
    :return: the path from start to end as a list
    """
    start_node = Node(None, start)

    open_list = []
    closed_list = []
    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0

        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)

        if env.is_feasible(current_node.position):
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = [Node(current_node, child) for child in env.get_children(current_node.position)]
        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = env.risk(current_node.position)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)