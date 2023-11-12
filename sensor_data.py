import datetime
import random

def generate_guid():
    rand_num = f"{random.randrange(0, 9)}{random.randrange(0, 9)}"
    rand_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return f"0-ZZZ12345678-{rand_num}{rand_letter}"

def generate_iot_message(guid, state, temperature):
    datestr = datetime.datetime.today().isoformat()
    return f'''{{"guid": "{guid}","destination": "0-AAA12345678","state": "{state}","eventTime": "{datestr}Z","payload": {{"format": "urn:example:sensor:temp","data": {{"temperature": {temperature:.1f}}}}}}}'''

def simulate_messages(num_msgs):
    device_state_map = {}
    temp_base = {'WA': 48.3, 'DE': 55.3, 'DC': 58.5, 'WI': 43.1,
                 'WV': 51.8, 'HI': 70.0, 'FL': 70.7, 'WY': 42.0,
                 'NH': 43.8, 'NJ': 52.7, 'NM': 53.4, 'TX': 64.8,
                 'LA': 66.4, 'NC': 59.0, 'ND': 40.4, 'NE': 48.8,
                 'TN': 57.6, 'NY': 45.4, 'PA': 48.8, 'CA': 59.4,
                 'NV': 49.9, 'VA': 55.1, 'CO': 45.1, 'AK': 26.6,
                 'AL': 62.8, 'AR': 60.4, 'VT': 42.9, 'IL': 51.8,
                 'GA': 63.5, 'IN': 51.7, 'IA': 47.8, 'OK': 59.6,
                 'AZ': 60.3, 'ID': 44.4, 'CT': 49.0, 'ME': 41.0,
                 'MD': 54.2, 'MA': 47.9, 'OH': 50.7, 'UT': 48.6,
                 'MO': 54.5, 'MN': 41.2, 'MI': 44.4, 'RI': 50.1,
                 'KS': 54.3, 'MT': 42.7, 'MS': 63.4, 'SC': 62.4,
                 'KY': 55.6, 'OR': 48.4, 'SD': 45.2}

    for _ in range(num_msgs):
        guid = generate_guid()
        state = random.choice(list(temp_base.keys()))

        if guid not in device_state_map:
            device_state_map[guid] = state

        temperature = random.uniform(temp_base[state] - 5, temp_base[state] + 5)
        message = generate_iot_message(guid, device_state_map[guid], temperature)
        print(message)

if __name__ == "__main__":
    num_msgs = int(input("Enter the number of simulated messages: "))
    simulate_messages(num_msgs)
