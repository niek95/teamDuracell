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

def countSort1(array):
    row = []

    for i in range(100):
        row.append([0, []])
    
    for i in array:
        length = int(i[0])
        row[length][0] += 1
        row[length][1].append(i[1])

    for i in range(len(row)):
        row[i] += row[i - 1]

    array = []

    for i in range(len(row)):
        if row[i] != row[i-1]:
            array.append((row[i][0],row[i][1]))
    
    return array