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
