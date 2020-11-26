from resources_allocator import *


class DynamicEnvironment:

    def __init__(self, resources_allocator: ResourcesAllocator):
        """
        Initialize the environment with the given parameters

        :param vehicles: the vehicles in the environment
        :param num_of_assets: the number of assets in the environment
        :param communications: a dictionary that represents the connections between the vehicles
        :param shot_down: a list of the vehicles that were shot down
        """
        self.resources_allocator = resources_allocator
        self.vehicles = resources_allocator.V
        self.num_of_assets = len(resources_allocator.A)
        self.communications = resources_allocator.Comm
        self.shot_down = resources_allocator.shot_down

    def get_children(self, position):
        """
        Find the children of the given position (the positions we can travel to from the given position)

        :param position: the given position
        :return: the possible states we can go to from the given position
        """
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

    def is_feasible(self, position):
        is_feasible = True

        # Constraint 3 - if a resource is encrypted, the encryption key
        # must not be allocated on the drone on which the resource is allocated
        for v in range(len(self.vehicles)):
            for a in range(self.num_of_assets):
                encrypted_index = v * self.num_of_assets * len(I) + a * len(I) + LOCAL_ENCRYPTED
                key_index = self.num_of_assets * len(self.vehicles) * len(I) + a * len(self.vehicles) + v
                is_feasible = is_feasible and position[encrypted_index] + position[key_index] <= 1

        # Constraint 5 - the amount of data (in Bytes) that can be transferred
        # at once is limited by MaxComm
        is_feasible = is_feasible and sum(
            position[v * self.num_of_assets * len(I) + a * len(I) + REMOTE] * self.resources_allocator.A_net[
                a] +
            position[
                self.num_of_assets * len(self.vehicles) * len(I) + a * len(self.vehicles) + v] * KEY_PACKET_SIZE
            for a in range(self.num_of_assets) for v in
            range(len(self.vehicles))) <= self.resources_allocator.MaxComm

        # Constraint 6 - if a resource on vehicle v is encrypted, then the v can
        # communicate with at least r vehicles that hold the key
        for v in range(len(self.vehicles)):
            for a in range(self.num_of_assets):
                is_feasible = is_feasible and sum(
                    position[self.num_of_assets * len(self.vehicles) * len(I) + a * len(self.vehicles) + v1] *
                    (1 if self.vehicles[v1] in self.resources_allocator.Comm[self.vehicles[v]] else 0)
                    for v1 in range(len(self.vehicles)) if v1 != v) \
                              - position[v * self.num_of_assets * len(I) + a * len(I) + LOCAL_ENCRYPTED] \
                              * self.resources_allocator.r >= 0

        return is_feasible
