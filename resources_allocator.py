import json
import math
import numpy
from event import Event
from environment import Environment
from a_star import a_star

I = ['None', 'LocalCleartext', 'LocalEncrypted', 'Remote']
NONE = 0
LOCAL_CLEARTEXT = 1
LOCAL_ENCRYPTED = 2
REMOTE = 3

KEY_PACKET_SIZE = 3


class ResourcesAllocator:
    
    def __init__(self, data_file: str):
        """
        Saves the data file path, initializes an empty MIP model and defines the required varibles

        :param data_file: the path to the file that contains the data for the model
        """
        # self.data_file = data_file
        # self.model = Model('ResourcesAllocator')
        # self.model.verbose = 0
        #
        # self.V = []
        # self.Likelihood = []
        # self.V_cpu = []
        # self.V_mem = []
        #
        # self.A = []
        # self.Sensitivity = []
        # self.A_cpu = []
        # self.A_mem = []
        # self.A_net = []
        #
        # self.K = None
        #
        # self.Comm = {}
        # self.Req = {}
        #
        # self.X = None
        # self.F = {}
        #
        # self.MaxComm = None
        # self.r = None
        #
        # self.assets_instances = None
        # self.keys_instances = None
        #
        # self.previous_keys_positions = None
        # self.current_keys_positions = None
        # self.shot_down = []
        #
        # self.load()
        #
        # self.build_model()
        pass
    
    def load(self):
        """
        Loads the data from the data file and assigns the values to the variables accordingly
        """
        # with open(self.data_file) as data:
        #     data_json = json.load(data)
        #
        #     vehicles = data_json['Vehicles']
        #     for v in vehicles:
        #         self.V.append(v['name'])
        #         self.Likelihood.append(v['likelihood'])
        #         self.V_cpu.append(v['cpu'])
        #         self.V_mem.append(v['mem'])
        #         self.Req[v['name']] = []
        #         self.Comm[v['name']] = []
        #
        #     assets = data_json['Assets']
        #     for a in assets:
        #         self.A.append(a['name'])
        #         self.Sensitivity.append(a['sensitivity'])
        #         self.A_cpu.append(a['cpu'])
        #         self.A_mem.append(a['mem'])
        #         self.A_net.append(a['net'])
        #
        #     communication = data_json['Communication']
        #     for c in communication:
        #         self.Comm[c[0]].append(c[1])
        #         self.Comm[c[1]].append(c[0])
        #
        #     requests = data_json['Requests']
        #     for r in requests:
        #         v = list(r.keys())[0]
        #         a = r[v]
        #         self.Req[v].append(a)
        #
        #     factors = data_json['Factors']
        #     for f in factors:
        #         a = list(f.keys())[0]
        #         a_index = [a1 for a1 in range(len(self.A))if self.A[a1] == a][0]
        #         self.F[a_index] = f[a]
        #
        #     self.MaxComm = data_json['MaxComm']
        #     self.r = data_json['r']
        pass
                
    def assignment_after_event(self, event: Event):
        """
        Finds a new assignment after an event

        :param event: the event that happened during the mission
        """
        # if event.type == Event.LOST_COMMUNICATION:
        #     v1, v2 = event.entities[0], event.entities[1]
        #     self.Comm[v1].remove(v2)
        #     self.Comm[v2].remove(v1)
        # elif event.type == Event.RISK_CHANGE:
        #     v = event.entities[0]
        #     v_index = self.V.index(event.entities[0])
        #     self.Likelihood[v_index] = event.entities_attributes[v]['likelihood']
        # elif event.type == Event.DAMAGED:
        #     v = event.entities[0]
        #     v_index = self.V.index(event.entities[0])
        #     self.Likelihood[v_index] = math.inf
        #     self.Req.pop(v)
        # elif event.type == Event.SHOT_DOWN:
        #     v = event.entities[0]
        #     v_index = self.V.index(event.entities[0])
        #     self.shot_down.append(v_index)
        #     # del self.V[v_index]
        #     # del self.V_cpu[v_index]
        #     # del self.V_mem[v_index]
        #     self.Comm.pop(v)
        #     [self.Comm[v_tag].remove(v) for v_tag in self.Comm.keys()]
        #     for a in self.A:
        #         if v in self.assets_instances[a]:
        #             self.assets_instances[a].remove(v)
        #         if v in self.keys_instances[a]:
        #             self.keys_instances[a].remove(v)
        # else:
        #     print(f'Illegal event type: {event.type}')
        # self.build_model_in_mission()
        # self.solve()
        pass
    
    def build_model(self):
        """
        Builds the model based on the target function and the constraints
        """

        # self.X = [[[self.model.add_var(var_type=BINARY) for i in I] for a in self.A] for v in self.V]
        #
        # self.K = [[self.model.add_var(var_type=BINARY) for v in self.V] for a in self.A]
        #
        # self.model.objective = minimize(xsum(self.Likelihood[v] * self.Sensitivity[a] * (self.X[v][a][i] * self.F[a][i] + self.K[a][v] * self.F[a][REMOTE]) for i in range(len(I)) for a in range(len(self.A)) for v in range(len(self.V))))
        #
        # # Constraint 1 - each resource is implemented with one access method only on each drone
        # for v in range(len(self.V)):
        #     for a in range(len(self.A)):
        #         self.model += xsum(self.X[v][a][i] for i in range(len(I))) == 1
        #
        # # Constraint 2 - if a drone needs access to a resource, the access
        # # method for this resource on this drone cannot be None (0)
        # for v in range(len(self.V)):
        #     for a in range(len(self.A)):
        #         v_requested_a = 1 if self.A[a] in self.Req[self.V[v]] else 0
        #         if v_requested_a:
        #             self.model += v_requested_a + self.X[v][a][NONE] <= 1
        #
        # # Constraint 3 - if a resource is encrypted, the encryption key
        # # must not be allocated on the drone on which the resource is allocated
        # for v in range(len(self.V)):
        #     for a in range(len(self.A)):
        #         self.model += self.X[v][a][LOCAL_ENCRYPTED] + self.K[a][v] <= 1
        #
        # # Constraint 4 - if a resource's access method is remote on a drone,
        # # then the drone can communicate with at least r drones that access
        # # the resource with either LocalCleartext or LocalEncrypted
        # for v in range(len(self.V)):
        #     for a in range(len(self.A)):
        #         v_requested_a = 1 if self.A[a] in self.Req[self.V[v]] else 0
        #         self.model += xsum((self.X[v1][a][LOCAL_CLEARTEXT] + self.X[v1][a][LOCAL_ENCRYPTED]) * (1 if self.V[v1] in self.Comm[self.V[v]] else 0) for v1 in range(len(self.V)) if v1 != v) - self.X[v][a][REMOTE] * self.r >= 0
        #
        # # Constraint 5 - the amount of data (in Bytes) that can be transferred
        # # at once is limited by MaxComm
        # self.model += xsum(self.X[v][a][REMOTE] * self.A_net[a] + self.K[a][v] * KEY_PACKET_SIZE for a in range(len(self.A)) for v in range(len(self.V))) <= self.MaxComm
        #
        # # Constraint 6 - if a resource on vehicle v is encrypted, then the v can
        # # communicate with at least r vehicles that hold the key
        # for v in range(len(self.V)):
        #     for a in range(len(self.A)):
        #         self.model += xsum(self.K[a][v1] * (1 if self.V[v1] in self.Comm[self.V[v]] else 0) for v1 in range(len(self.V)) if v1 != v) - self.X[v][a][LOCAL_ENCRYPTED] * self.r >= 0
        #
        # # Constraint 7 - the CPU usage of drone v is limited by its max CPU usage
        # for v in range(len(self.V)):
        #     self.model += xsum(self.A_cpu[a] * (self.X[v][a][LOCAL_CLEARTEXT] + self.X[v][a][LOCAL_ENCRYPTED]) for a in range(len(self.A))) <= self.V_cpu[v]
        #
        # # Constraint 8 - the memory usage of drone v is limited by its max memory usage
        # for v in range(len(self.V)):
        #     self.model += xsum(self.A_mem[a] * (self.X[v][a][LOCAL_CLEARTEXT] + self.X[v][a][LOCAL_ENCRYPTED]) for a in range(len(self.A))) <= self.V_mem[v]

        # Constraint 9 - the amount of assets has to be constant during the mission
        # if self.assets_instances != None:
        #     for a in range(len(self.A)):
        #         self.model += xsum(self.X[v][a][LOCAL_ENCRYPTED] for v in range(len(self.V))) + xsum(self.X[v][a][LOCAL_CLEARTEXT] for v in range(len(self.V))) == len(self.assets_instances[self.A[a]])
        
        # Constraint 10 - the amount of keys has to be constant during the mission
        # if self.keys_instances != None:
        #     for a in range(len(self.A)):
        #         self.model += xsum(self.K[a][v] for v in range(len(self.V))) == len(self.keys_instances[self.A[a]])        
        pass

    def build_model_in_mission(self):
        """
        Builds the model during the mission based on the target function and the constraints, solve only for keys
        """
        # self.K = [[self.model.add_var(var_type=BINARY) for v in self.V] for a in self.A]
        #
        # # Constraint 3 - if a resource is encrypted, the encryption key
        # # must not be allocated on the drone on which the resource is allocated
        # for v in range(len(self.V)):
        #     if v not in self.shot_down:
        #         for a in range(len(self.A)):
        #             self.model += self.X[v][a][LOCAL_ENCRYPTED].x + self.K[a][v] <= 1
        #
        # # Constraint 5 - the amount of data (in Bytes) that can be transferred
        # # at once is limited by MaxComm
        # self.model += xsum(self.X[v][a][REMOTE].x * self.A_net[a] + self.K[a][v] * KEY_PACKET_SIZE for a in range(len(self.A)) for v in range(len(self.V)) if v not in self.shot_down) <= self.MaxComm
        #
        # # Constraint 6 - if a resource on vehicle v is encrypted, then the v can
        # # communicate with at least r vehicles that hold the key
        # for v in range(len(self.V)):
        #     if v not in self.shot_down:
        #         for a in range(len(self.A)):
        #             self.model += xsum(self.K[a][v1] * (1 if self.V[v1] in self.Comm[self.V[v]] else 0) for v1 in range(len(self.V)) if v1 != v) - self.X[v][a][LOCAL_ENCRYPTED].x * self.r >= 0
        #
        # # Constraint 10 - the amount of keys has to be constant during the mission
        # if self.keys_instances is not None:
        #     for a in range(len(self.A)):
        #         self.model += xsum(self.K[a][v] for v in range(len(self.V))) == len(self.keys_instances[self.A[a]])
        #
        # for v in self.shot_down:
        #     self.model += xsum(self.K[a][v] for a in range(len(self.A))) == 0
        pass
        
    def solve(self, output_file_name='allocation.json'):
        """
        Solves the problem, prints the solution to the screen and saves
         the solution to a json file named 'allocations.json'

        :param output_file_name: the json file in which we write the new allocation
        """
        # self.model.threads = -1
        # self.model.optimize()
        #
        # assets_allocations = {}
        #
        # initial_allocation = self.current_keys_positions is None
        # self.previous_keys_positions = numpy.array(self.current_keys_positions)
        # self.current_keys_positions = [0] * (len(self.A) * len(self.V))
        #
        # # print('***Assets allocations***')
        # if self.assets_instances is None:
        #     self.assets_instances = {}
        # for v in range(len(self.V)):
        #     if v not in self.shot_down:
        #         assets_allocations[self.V[v]] = {}
        #         for a in range(len(self.A)):
        #             if self.A[a] not in self.assets_instances.keys():
        #                 self.assets_instances[self.A[a]] = []
        #             for i in range(len(I)):
        #                 if self.X[v][a][i].x >= 0.99:
        #                     assets_allocations[self.V[v]][self.A[a]] = I[i]
        #                     if (i == LOCAL_CLEARTEXT or i == LOCAL_ENCRYPTED) and self.V[v] not in self.assets_instances[self.A[a]]:
        #                         self.assets_instances[self.A[a]].append(self.V[v])
        #                     if i == REMOTE and self.V[v] in self.assets_instances[self.A[a]]:
        #                         self.assets_instances[self.A[a]].remove(self.V[v])
        #
        # keys_allocations = {}
        # if self.keys_instances is None:
        #     self.keys_instances = {}
        # for a in range(len(self.A)):
        #     keys_allocations[self.A[a]] = {}
        #     if self.A[a] not in self.keys_instances.keys():
        #         self.keys_instances[self.A[a]] = []
        #     for v in range(len(self.V)):
        #         if self.K[a][v].x >= 0.99:
        #             keys_allocations[self.A[a]][self.V[v]] = 1
        #             if self.V[v] not in self.keys_instances[self.A[a]]:
        #                 self.keys_instances[self.A[a]].append(self.V[v])
        #             self.current_keys_positions[a * len(self.V) + v] = 1
        #         else:
        #             if self.V[v] in self.keys_instances[self.A[a]]:
        #                 self.keys_instances[self.A[a]].remove(self.V[v])
        #
        # allocations = {'Assets': assets_allocations, 'Keys': keys_allocations}
        # with open(output_file_name, 'w+') as allocations_file:
        #     json.dump(allocations, allocations_file)
        #
        # self.current_keys_positions = numpy.array(self.current_keys_positions)
        # key_transfers = None if initial_allocation else self.get_keys_transfers()
        # if key_transfers is not None:
        #     with open('keys_transfers.txt', 'w+') as allocations_file:
        #         [allocations_file.write(str(transfer) + '\n') for transfer in key_transfers]
        pass

    def get_keys_transfers(self):
        """
        Finds the smallest amount of keys transfers possible to  get to the new allocation

        :return: the list of transfers, each element is a tuple in the form: (from_vehicle, to_vehicle, the_key's_asset)
        """
        # env = Environment(self.V, len(self.A), self.Comm, self.shot_down)
        #
        # path = a_star(env, self.previous_keys_positions, self.current_keys_positions)
        #
        # transfers = []
        # for p1_index, p1 in enumerate(path[:-1]):
        #     p2 = path[p1_index + 1]
        #     diff = p2 - p1
        #     from_index = int(numpy.where(diff == -1)[0])
        #     from_v = self.V[from_index]
        #     to_index = int(numpy.where(diff == 1)[0])
        #     to_v = self.V[to_index]
        #     a_index = int(from_index / len(self.V))
        #     a = self.A[a_index]
        #     transfers.append((from_v, to_v, a))
        #
        # return transfers
        pass
