import os

def create_index(dir):
    index = {}
    for filename in os.listdir(dir):
        if filename.endswith((".txt", ".png", ".jpg", ".jpeg")):
            filepath = os.path.join(dir, filename)
            index[filename] = "Found!" 
    return index

index = create_index(r'C:\Users\nicholas.nesmith0001\Documents\Search Engine')
print(index)
input("Press Enter to exit...") 