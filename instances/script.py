import os
import random
import string

# Read the instances from the file given the file path
def read_lcs_instances(file_path):
    instances = []

    # Read the first line containing the number of instances and the alphabet
    with open(file_path, 'r') as file:
        # Read the first line and extract values
        first_line_values = list(map(int, file.readline().strip().split('\t')))
        num_instances, num_alphabet = first_line_values[:2]

        # Read the instances themselves
        for _ in range(num_instances):
            instance_length, instance_string = file.readline().strip().split('\t')
            instances.append((int(instance_length), instance_string))


    return num_instances, num_alphabet, instances

# Function to generate a string of given length using the given alphabet
def generate_random_string(alphabet, length):
    return ''.join(random.choice(alphabet) for _ in range(length))

# Function to generate an alphabet from the alphabet size and then generate 10 random strings and write them to the end of the file

def generate_strings(file_path, num_alphabet, num_instances, num_strings):
    alphabet = ''.join([chr(i) for i in range(97, 97 + num_alphabet)])
    random_strings = [generate_random_string(alphabet, random.randint(2, 10)) for _ in range(num_strings)]

    with open(file_path, 'w') as file:
        # Write the first line with the three values
        file.write(f"{num_instances}\t{num_alphabet}\t{num_strings}\n")

        # Write the lines of instances
        for instance_length, instance_string in instances:
            file.write(f"{instance_length}\t{instance_string}\n")

        # Write the generated strings
        for random_string in random_strings:
            file.write(f"{len(random_string)}\t{random_string}\n")


# Function to remove previously randomly generated strings at the end of the file (if they exist)        



def clean_file(file_path):
    with open(file_path, 'r') as file:
        # Read the first line to check if num_strings is present
        first_line = file.readline().strip()

        # Extract values from the first line
        first_line_values = list(map(int, first_line.split('\t')))

        file.seek(0)
        
        # Remove the third value and corresponding lines
        lines = file.readlines()
        del lines[0]  # Remove the first line
        del lines[-int(first_line_values[2]):]  # Remove the last lines

        # Write back the first line and the modified lines  
        with open(file_path, 'w') as file:
            file.write('\t'.join(map(str, first_line_values[:2])) + '\n')
            file.writelines(lines)

# Get a list of all files in the current directory
directory = os.getcwd()
files = [f for f in os.listdir(directory) if f.endswith(".txt")]

# Process each file
for file_name in files:
    if file_name.startswith("10_100"):
        num_strings = 10

        file_path = os.path.join(directory, file_name)
        num_instances, num_alphabet, instances = read_lcs_instances(file_path)

        print(f"File: {file_name}")
        print(f"Number of instances: {num_instances}")
        print(f"Number of alphabet characters: {num_alphabet}")
        print("Instances:")
        for instance_length, instance_string in instances:
            print(f"Length: {instance_length}, String: {instance_string}")
        print("="*30)

        #if num_strings is not None:
            # Clean up previously generated values
            #clean_file(file_path)
        

        # Generate and append random strings
        generate_strings(file_path, num_alphabet, num_instances, num_strings)