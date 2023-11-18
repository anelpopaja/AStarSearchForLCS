import heapq
import os

def heuristic(state, exclusion_constraints):
    return 0  # Trenutno koristimo trivijalnu heuristiku

def is_excluded(x, y, exclusion_constraints):
    return any(constraint in [x, y] for constraint in exclusion_constraints)

def a_star_search(X, Y, exclusion_constraints):
    start_state = (0, 0, [])  # Početno stanje: indeksi u X i Y, trenutni LCS je prazan niz
    priority_queue = [(0, start_state)]  # Prioritetni red: (f(n), stanje)
    visited_states = set()

    while priority_queue:
        _, current_state = heapq.heappop(priority_queue)

        if current_state[:2] in visited_states:
            continue

        visited_states.add(current_state[:2])

        if current_state[0] == len(X) or current_state[1] == len(Y):
            # Dostigli smo kraj jedne od sekvenci
            return current_state[2]

        for action in [(1, 0), (0, 1), (1, 1)]:
            next_state = (current_state[0] + action[0], current_state[1] + action[1], current_state[2])
            if (
                next_state[0] < len(X) and
                next_state[1] < len(Y) and
                not is_excluded(X[next_state[0]], Y[next_state[1]], exclusion_constraints)
            ):
                next_state = (next_state[0], next_state[1], next_state[2] + [X[next_state[0]]])

                cost = len(next_state[2]) + heuristic(next_state, exclusion_constraints)
                heapq.heappush(priority_queue, (cost, next_state))

    return []

def read_instance_file(file_path):
    with open(file_path, 'r') as file:
        # Čitanje prvog reda datoteke
        num_instances, alphabet_size, num_constrained_strings = map(int, file.readline().split())

        instances = []
        constrained_sequences = []

        # Čitanje instanci
        for _ in range(num_instances):
            length, instance = file.readline().split()
            instances.append((int(length), instance))

        # Čitanje constrained sekvenci
        for _ in range(num_constrained_strings):
            length, constrained_sequence = file.readline().split()
            constrained_sequences.append((int(length), constrained_sequence))

    return num_instances, alphabet_size, num_constrained_strings, instances, constrained_sequences

"""Znaci ne kontam sta se desava al sam nesto pokusavala, vise nmg radim 3h i nikaoko haha pokusacu kascije nadam se da cu uspjesno pushat"""
def find_combined_lcs(X, Y, exclusion_constraints_1, exclusion_constraints_2):
    result_1 = a_star_search(X, Y, exclusion_constraints_1)
    result_2 = a_star_search(X, Y, exclusion_constraints_2)

    return result_1, result_2

def compare_instances(file_path_1, file_path_2):
    num_instances_1, alphabet_size_1, num_constrained_strings_1, instances_1, constrained_strings_1 = read_instance_file(file_path_1)
    num_instances_2, alphabet_size_2, num_constrained_strings_2, instances_2, constrained_strings_2 = read_instance_file(file_path_2)

    for i in range(min(num_instances_1, num_instances_2)):
        seq_length_1, sequence_1 = instances_1[i]
        seq_length_2, sequence_2 = instances_2[i]

        print(f"\nInstance {i + 1} - Seq Length 1: {seq_length_1}\nSequence 1: {sequence_1}")
        print(f"Instance {i + 1} - Seq Length 2: {seq_length_2}\nSequence 2: {sequence_2}")

        for length_1, constrained_sequence_1 in constrained_strings_1:
            exclusion_constraints_1 = list(constrained_sequence_1)

            for length_2, constrained_sequence_2 in constrained_strings_2:
                exclusion_constraints_2 = list(constrained_sequence_2)

                combined_result = find_combined_lcs(sequence_1, sequence_2, exclusion_constraints_1, exclusion_constraints_2)

                print(f"Exclusion Constraints 1: {exclusion_constraints_1}")
                print(f"Exclusion Constraints 2: {exclusion_constraints_2}")

                print(f"Combined Longest Common Subsequence with Exclusion Constraints: {combined_result}")

                # Ovde možete dodati dodatne analize ili poređenja između rezultata
                print("\n---")


if __name__ == '__main__':
    main_path = os.path.dirname(__file__)
    file_path_1 = os.path.join(main_path, 'instances\\10_100_4_0.txt')
    file_path_2 = os.path.join(main_path, 'instances\\10_100_4_1.txt')
    compare_instances(file_path_1, file_path_2)


