class Environment:

    def __init__(self, vehicles: list, num_of_assets: int, communications: dict, shot_down: list):
        """
        Initialize the environment with the given parameters

        :param vehicles: the vehicles in the environment
        :param num_of_assets: the number of assets in the environment
        :param communications: a dictionary that represents the connections between the vehicles
        :param shot_down: a list of the vehicles that were shot down
        """
        self.vehicles = vehicles
        self.num_of_assets = num_of_assets
        self.communications = communications
        self.shot_down = shot_down

    def get_children(self, position):
        """
        Find the children of the given position (the positions we can travel to from the given position)

        :param position: the given position
        :return: the possible states we can go to from the given position
        """
        # K = {}
        # for a_index, a in enumerate(self.assets):
        #     K[a] = []
        #     for v_index, v in enumerate(self.vehicles):
        #         if position[a_index * len(self.vehicles) + v_index] == 1:
        #             K[a].append(v)
        
        children = []
        for a_index in range(self.num_of_assets):
            for v1 in self.communications.keys():
                v1_index = self.vehicles.index(v1)
                for v2 in self.communications[v1]:
                    v2_index = self.vehicles.index(v2)
                    if position[a_index * len(self.vehicles) + v1_index] == 1 and position[a_index * len(self.vehicles) + v2_index] == 0:
                        child = list(position)
                        child[a_index * len(self.vehicles) + v1_index], child[a_index * len(self.vehicles) + v2_index] = 0, 1
                        if child not in children:
                            children.append(child)
                    if position[a_index * len(self.vehicles) + v2_index] == 1 and position[a_index * len(self.vehicles) + v1_index] == 0:
                        child = list(position)
                        child[a_index * len(self.vehicles) + v2_index], child[a_index * len(self.vehicles) + v1_index] = 0, 1
                        if child not in children:
                            children.append(child)
        
        return children
