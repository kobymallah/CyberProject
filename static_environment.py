import numpy as np
from resources_allocator import *


class StaticEnvironment:

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
        for a in range(self.num_of_assets):
            for v in range(len(self.vehicles)):
                first_access_method = v * len(I) * self.num_of_assets + a * len(I)
                for i in range(4):
                    child = np.array(position)
                    child[first_access_method + i] = 1 - child[first_access_method + i]
                    children.append(child)
                child = np.array(position)
                key_index = self.num_of_assets * len(self.vehicles) * len(I) + a * len(self.vehicles) + v
                child[key_index] = 1 - child[key_index]
                children.append(child)

        return children

    def is_feasible(self, position):
        is_feasible = True

        # Constraint 1 - each resource is implemented with one access method only on each drone
        for v in range(len(self.vehicles)):
            for a in range(self.num_of_assets):
                base_index = v * self.num_of_assets * len(I) + a * len(I)
                is_feasible = is_feasible and sum(position[base_index + i] for i in range(len(I))) == 1

        # Constraint 2 - if a drone needs access to a resource, the access
        # method for this resource on this drone cannot be None (0)
        for v in range(len(self.vehicles)):
            for a in range(self.num_of_assets):
                v_requested_a = 1 if self.resources_allocator.A[a] in self.resources_allocator.Req[self.vehicles[v]] else 0
                if v_requested_a:
                    none_index = v * self.num_of_assets * len(I) + a * len(I)
                    is_feasible = is_feasible and v_requested_a + position[none_index] <= 1

        # Constraint 3 - if a resource is encrypted, the encryption key
        # must not be allocated on the drone on which the resource is allocated
        for v in range(len(self.vehicles)):
            for a in range(self.num_of_assets):
                encrypted_index = v * self.num_of_assets * len(I) + a * len(I) + LOCAL_ENCRYPTED
                key_index = self.num_of_assets * len(self.vehicles) * len(I) + a * len(self.vehicles) + v
                is_feasible = is_feasible and position[encrypted_index] + position[key_index] <= 1

        # Constraint 4 - if a resource's access method is remote on a drone,
        # then the drone can communicate with at least r drones that access
        # the resource with either LocalCleartext or LocalEncrypted
        for v in range(len(self.vehicles)):
            for a in range(self.num_of_assets):
                remote_index = v * self.num_of_assets * len(I) + a * len(I) + REMOTE
                is_feasible = is_feasible and \
                              sum((position[v1 * self.num_of_assets * len(I) + a * len(I) + LOCAL_CLEARTEXT] +
                                   position[v1 * self.num_of_assets * len(I) + a * len(I) + LOCAL_ENCRYPTED]) *
                                  (1 if self.vehicles[v1] in self.resources_allocator.Comm[self.vehicles[v]] else 0)
                                  for v1 in range(len(self.vehicles)) if v1 != v) \
                              - position[remote_index] * self.resources_allocator.r >= 0

        # Constraint 5 - the amount of data (in Bytes) that can be transferred
        # at once is limited by MaxComm
        is_feasible = is_feasible and sum(
            position[v * self.num_of_assets * len(I) + a * len(I) + REMOTE] * self.resources_allocator.A_net[a] +
            position[self.num_of_assets * len(self.vehicles) * len(I) + a * len(self.vehicles) + v] * KEY_PACKET_SIZE
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
                              - position[v * self.num_of_assets * len(I) + a * len(I) + LOCAL_ENCRYPTED]\
                              * self.resources_allocator.r >= 0

        # Constraint 7 - the CPU usage of drone v is limited by its max CPU usage
        for v in range(len(self.vehicles)):
            is_feasible = is_feasible and \
                          sum(self.resources_allocator.A_cpu[a] *
                              (position[v * self.num_of_assets * len(I) + a * len(I) + LOCAL_CLEARTEXT]
                               + position[v * self.num_of_assets * len(I) + a * len(I) + LOCAL_ENCRYPTED])
                              for a in range(self.num_of_assets)) <= self.resources_allocator.V_cpu[v]

        # Constraint 8 - the memory usage of drone v is limited by its max memory usage
        for v in range(len(self.vehicles)):
            is_feasible = is_feasible and \
                          sum(self.resources_allocator.A_mem[a] *
                              (position[v * self.num_of_assets * len(I) + a * len(I) + LOCAL_CLEARTEXT]
                               + position[v * self.num_of_assets * len(I) + a * len(I) + LOCAL_ENCRYPTED])
                              for a in range(self.num_of_assets)) <= self.resources_allocator.V_mem[v]

        return is_feasible
