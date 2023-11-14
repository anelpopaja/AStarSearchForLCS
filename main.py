# Funkcija za čitanje i obradu podataka iz datoteke
import os


def read_instance_file(file_path):
    with open(file_path, 'r') as file:
        # Čitanje prvog reda datoteke
        num_instances, alphabet_size, num_constrained_strings = map(int, file.readline().split())

        instances = []
        constrained_strings = []

        # Čitanje instanci
        for _ in range(num_instances):
            length, instance = file.readline().split()
            instances.append((int(length), instance))

        # Čitanje constrained stringova
        for _ in range(num_constrained_strings):
            length, constrained_string = file.readline().split()
            constrained_strings.append((int(length), constrained_string))

    return num_instances, alphabet_size, num_constrained_strings, instances, constrained_strings


# Primer korišćenja funkcije
main_path = os.path.dirname(__file__)
file_path = os.path.join(main_path, 'instances\\10_100_4_0.txt')

num_instances, alphabet_size, num_constrained_strings, instances, constrained_strings = read_instance_file(file_path)

# Prikaz dobijenih podataka
print("Broj instanci:", num_instances)
print("Veličina azbuke:", alphabet_size)
print("Broj constrained stringova:", num_constrained_strings)
print("\nInstance:")
for length, instance in instances:
    print(f"Duzina: {length}, Instanca: {instance}")

print("\nConstrained stringovi:")
for length, constrained_string in constrained_strings:
    print(f"Duzina: {length}, Constrained string: {constrained_string}")
