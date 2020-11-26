import json
import random


class RandomScenario:

    @staticmethod
    def generate_random_scenario(n_drones, n_assets, redundancy):
        """
        Generate a random scenario with n_drones amount of drones and n_assets amount of assets and the given redundancy.
        The drones and assets attributes are generated randomly.
        The communications between the drones are created randomly (the chance that two drones will can communicate is 1/3).
        The requests of assets by the drones are created randomly (the chance that a drone will request an asset is 1/4).
        The access factors for each asset are generated randomly.
        The max communications is generated randomly.

        The scenario is saved to a json file named 'random.json'.

        :param n_drones: the number of drones
        :param n_assets: the number of assets
        :param redundancy: the redundancy factor
        """
        scenario_data = dict()
        scenario_data['Vehicles'] = []
        for drone_index in range(n_drones):
            scenario_data['Vehicles'].append({
                'name': f'v{drone_index}',
                'likelihood': random.randint(0, 10),
                'cpu': random.randint(10, 20),
                'mem': random.randint(10, 20)
            })
        
        scenario_data['Assets'] = []
        for asset_index in range(n_assets):
            scenario_data['Assets'].append({
                'name': f'a{asset_index}',
                'sensitivity': random.randint(0, 10),
                'cpu': random.randint(1, 3),
                'mem': random.randint(1, 3),
                'net': random.randint(1, 3)
            })
        
        scenario_data['Communication'] = []
        for v1 in range(n_drones):
            for v2 in range(v1 + 1, n_drones):
                if scenario_data['Vehicles'][v1]['name'] != scenario_data['Vehicles'][v2]['name'] and random.choice([True, False, False]):
                    scenario_data['Communication'].append([scenario_data['Vehicles'][v1]['name'], scenario_data['Vehicles'][v2]['name']])
        
        scenario_data['Requests'] = []
        for v in range(n_drones):
            for a in range(len(scenario_data['Assets'])):
                if random.choice([True, False, False, False]):
                    scenario_data['Requests'].append({scenario_data['Vehicles'][v]['name']: scenario_data['Assets'][a]['name']})
        
        scenario_data['Factors'] = []
        for a in range(len(scenario_data['Assets'])):
            scenario_data['Factors'].append({scenario_data['Assets'][a]['name']: [0, random.uniform(1, 5), random.uniform(0.01, 0.05), random.uniform(0.001, 0.005)]})
        
        scenario_data['MaxComm'] = random.randint(n_drones * 100, n_drones * 200)
        scenario_data['r'] = redundancy

        with open('random.json', 'w+') as f:
            json.dump(scenario_data, f)
