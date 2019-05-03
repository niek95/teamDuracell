from route import Route

MAX_DISTANCE = 100


# alphabetical order
def countSort(arr):

    # The output character array that will have sorted arr
    output = [0 for i in range(256)]

    # Create a count array to store count of inidividul
    # characters and initialize count array as 0
    count = [0 for i in range(256)]

    # For storing the resulting answer since the
    # string is immutable
    ans = ["" for _ in arr]

    # Store count of each character
    for i in arr:
        count[ord(i)] += 1

    # Change count[i] so that count[i] now contains actual
    # position of this character in output array
    for i in range(256):
        count[i] += count[i-1]

    # Build the output character array
    for i in range(len(arr)):
        output[count[ord(arr[i])]-1] = arr[i]
        count[ord(arr[i])] -= 1

    # Copy the output array to arr, so that arr now
    # contains sorted characters
    for i in range(len(arr)):
        ans[i] = output[i]
    return ans


def countSort2(houses):
    """
    Takes a list containing tuples containing the length to a battery and
    the corresponding house. Returns the same list ordered by length
    """
    count = []
    for i in range(0, MAX_DISTANCE):
        count.append([0, []])

    for tuple in houses:
        length = tuple[0]
        count[length-1][0] += 1
        count[length-1][1].append(tuple)
        
    for i in range(1, len(count)):
        count[i][0] += count[i - 1][0]

    sorted = []

    for i in range(1, len(count)):
        if count[i][0] != count[i-1][0]:
            for house in count[i][1]:
                sorted.append(house)
    return sorted

def switch(route1, route2):
    battery1 = route1.get_battery()
    battery2 = route2.get_battery()
    battery1.remove_route(route1)
    battery2.remove_route(route2)
    house1 = route1.get_house()
    house2 = route2.get_house()
    house1.add_route(battery2)
    house2.add_route(battery1)
    battery1.connect_house(house2)
    battery2.connect_house(house1)
    return house1.get_route(), house2.get_route()

def check_switch(route1, route2):
    battery1 = route1.get_battery()
    battery2 = route2.get_battery()
    house1 = route1.get_house()
    house2 = route2.get_house()
    length1 = route1.get_length()
    length2 = route2.get_length()
    total_length1 = length1 + length2
    route1 = Route(house2, battery1)
    route2 = Route(house1, battery2)
    length1 = route1.get_length()
    length2 = route2.get_length()
    total_length2 = length1 + length2
    if total_length2 < total_length1:
        return True
    else:
        return False