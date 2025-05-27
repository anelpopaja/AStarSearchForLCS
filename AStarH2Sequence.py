from collections import Counter
import os
import heapq
import time

class Node:
    def __init__(self, subsequence, position_vector, l, p, g, h, patterns):
        self.subsequence = subsequence
        self.position_vector = position_vector
        self.l = l
        self.p = p
        self.g = g
        self.h = h
        self.f = g + h
        self.patterns = patterns

    def __str__(self):
        return f"Node(subsequence='{self.subsequence}', position_vector={self.position_vector}, l={self.l}, p={self.p}, g={self.g}, h={self.h}, f={self.f}, patterns='{self.patterns}')"

    def __lt__(self, other):
        """Compares nodes based on priority for heap ordering."""
        if self.f != other.f:
            return self.f < other.f  # Prioritize smaller f values
        elif self.g != other.g:
            return self.g > other.g  # Prioritize larger g values (reversed for __lt__)
        else:
            # Compare indexes of patterns
            for self_p, other_p in zip(self.p, other.p):
                if self_p != other_p:
                    return self_p > other_p  # Prioritize larger p values (reversed for __lt__)
            return False

    def check_exclusion_patterns(self, c, P):
        for p in P:
            if is_subsequence(self.subsequence+c, p):
                return False
        return True

    def is_dominated(self, node):
        if self is not node and node.l >= self.l:

            for self_p, other_p in zip(self.p, node.p):
                if self_p >= other_p:
                    return True
            return False
        return False  # Node is not dominated

    def generate_child_nodes(self, X, Y, patterns, alphabet):
        
        child_nodes = []
        
        # Create new nodes by appending a letter of alphabet to each of the new nodes' subsequence

        for c in alphabet:

            # Find the next index in X and Y for the newly appended letter of alphabet

            new_index_x = X.find(c, self.position_vector[0])
            new_index_y = Y.find(c, self.position_vector[1])
            
            # If the new c letter is not in one of the X or Y strings, or if the added c letter generates one of the p patterns discard the node

            if new_index_x != -1 and new_index_y != -1 and self.check_exclusion_patterns(c, self.patterns):
                # Create a new child node
                child_node = self._create_child_node(X, Y, c, patterns, alphabet, new_index_x, new_index_y)
                child_nodes.append(child_node)
        return child_nodes

    def _create_child_node(self, X, Y, c, patterns, alphabet, new_index_x, new_index_y):

        # Generate a new subsequence with the letter c
        new_subsequence = self.subsequence + c
        
        # Determine the longest matches for each pattern (List p)
        longest_matches = find_longest_pattern_matches(new_subsequence, patterns)

        count_x = Counter(X[:new_index_x+1])
        count_y = Counter(Y[:new_index_y+1])

        child_node = Node(
            subsequence=new_subsequence,
            position_vector=(new_index_x + 1, new_index_y + 1),
            l=self.l + 1,
            p=longest_matches,
            g=self.g + 1,
            h=calculate_heuristic(count_x, count_y, alphabet),
            patterns=self.patterns
        )

        return child_node

    def is_goal_state(self, X, Y):
        return self.l == min(len(X), len(Y))
    
def calculate_heuristic(count_x, count_y, alphabet):
    sum = 0

    for c in alphabet:
        temp1 = count_x[c]
        temp2 = count_y[c]
        sum += min(temp1, temp2)

    return sum    
    # h = sum(min(count_x[c], count_y[c]) for c in alphabet)
    

def find_longest_pattern_matches(subsequence, patterns):
    longest_matches = [0] * len(patterns)

    for i, pattern in enumerate(patterns):
        max_match_length = 0
        subseq_index = 0
        for char in pattern:
            while subseq_index < len(subsequence):
                if(subsequence[subseq_index] != char):
                    subseq_index += 1
                else:
                    max_match_length += 1
                    subseq_index += 1
                    break
        longest_matches[i] = max_match_length

    return longest_matches


# Function to check if target
# is a subsequence of string S
def is_subsequence(S, target):

	# Declare a stack to store the target sequence
	stack = []

	# Push the characters of
	# target into the stack
	for i in range(len(target)):
		stack.append(target[i])

	# Traverse the string S in reverse
	for i in range(len(S) - 1, -1, -1):

		# If the stack is empty
		# ie. if we have exhausted all the characters of the target
		if (len(stack) == 0):
			# print("Stack is empty")
			return True

		# If S[i] is same as the
		# top of the stack
		# ie. we have found a matching character in S and target
		if (S[i] == stack[-1]):

			# Pop the top of stack
			stack.pop()

	# Stack s is empty
	# We have found all of the characters
	if (len(stack) == 0):
		return True
	else:
		return False


def a_star(X, Y, P, alphabet):
    
    start_time = time.time()
    starting_node = Node(
        subsequence="",
        position_vector=(0, 0),
        l=0,
        p=0,
        g=0,
        h=calculate_heuristic(Counter(X[:0]), Counter(Y[:0]), alphabet),
        patterns=P
    )

    N = {}
    Nrel = {}
    Q = []
    heapq.heappush(Q, starting_node)

    while Q:
        current_node = heapq.heappop(Q)
        # print(current_node)

        # Check if the subsequence of a node is equal to the length of one of the input strings
        if current_node.is_goal_state(X, Y):
            print("goal state found")
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")
            return current_node
        
        

        children = current_node.generate_child_nodes(X, Y, P, alphabet)

        for child in children:
            child_key = (child.position_vector)

            # Maintain a hashmap of all the created nodes
            # And add the child to the Queue if no node exists that has the same positional vectors for X and Y

            if child_key not in N:
                N[child_key] = child
                heapq.heappush(Q, child)
            else:
                # If there is a node with same positional vectors for X and Y check if the new node is dominated by it
                # Add the new node to Nrel where the key are the positional vectors

                if child_key not in Nrel:
                    Nrel[child_key] = [N[child_key]]
                
                Nrel[child_key].append(child)
                Nrel[child_key].sort(key=lambda n: n.l, reverse=True)

                is_dominated = False
                for related_node in Nrel[child_key]:
                    if child.is_dominated(related_node):
                        # print(f"{child} is dominated by: {related_node}")
                        is_dominated = True
                        break

                if not is_dominated:
                    N[child_key] = child
                    heapq.heappush(Q, child)
                    
    
    if N:
        best_node = max(N.values(), key=lambda node: node.l)
        print(best_node)
        return best_node
    else:
        return None
    
def process_file(file_path):
    with open(file_path, 'r') as file:


        # Skip the first line
        next(file)
        
        # Read X and Y strings from the second and third lines respectively
        X = file.readline().split()[1].strip()
        Y = file.readline().split()[1].strip()
        
        
        # Initialize list to store exclusion patterns P
        P = []
        
        # Read exclusion patterns from the rest of the file
        for line in file:
            pattern = line.split()[1].strip()
            P.append(pattern)
        
        return X, Y, P

def get_alphabet(X, Y):
    alphabet = set()
    alphabet.update(X)
    alphabet.update(Y)
    return alphabet

def main():

    # Directory containing the files
    directory = "C:/Users/User/Desktop/instances/Dp_optimal_sequences"
    print(directory)

    # For every instance:
    
    for file_name in os.listdir(directory):
        if file_name == 'results.txt':
            continue  # Skip the results file

        if file_name.endswith(".txt"):
                
            # Process each file
            file_path = os.path.join(directory, file_name)
            X, Y, P = process_file(file_path)
            print(file_name)
                
            
            # print(X, Y, P)
            alphabet = get_alphabet(X, Y)

            # Call a_star function
            start_time = time.time()
            solution = a_star(X, Y, P, alphabet)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")

            with open(os.path.join(directory, 'resultsH2.txt'), 'a') as results_file:
                if solution != None:
                    results_file.write(f"File: {file_name}, Solution: {solution.subsequence}, Length: {solution.l}, Time: {elapsed_time}\n")            
                else:
                    results_file.write(f"File: {file_name}, No solution found\n")
        
        else:
            continue
        
    

    

if __name__ == "__main__":
    main()