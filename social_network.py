class Person:
    '''
    A class representing a person in a social network.
    Attributes:
        name (str): The name of the person.
        friends (list): A list of friends (Person objects).
    Methods:
        add_friend(friend): Adds a friend to the person's friend list.
    '''

    def __init__(self, name):
        self.name = name
        self.friends = []

    def add_friend(self, friend):
        if friend is not self and friend not in self.friends:
            self.friends.append(friend)


class SocialNetwork:
    '''
    A class representing a social network.
    Attributes:
        people (dict): A dictionary mapping names to Person objects.
    Methods:
        add_person(name): Adds a new person to the network.
        add_friendship(person1_name, person2_name): Creates a friendship between two people.
        print_network(): Prints the names of all people and their friends.
    '''

    def __init__(self):
        self.people = {}

    def add_person(self, name):
        if name in self.people:
            print(f"{name} already exists in the network!")
            return
        self.people[name] = Person(name)

    def add_friendship(self, person1_name, person2_name):
        if person1_name not in self.people:
            print(f"Friendship not created. {person1_name} doesn't exist!")
            return
        if person2_name not in self.people:
            print(f"Friendship not created. {person2_name} doesn't exist!")
            return
        if person1_name == person2_name:
            print("Friendship not created. A person can't befriend themselves!")
            return

        person1 = self.people[person1_name]
        person2 = self.people[person2_name]

        if person2 in person1.friends:
            print(f"{person1_name} and {person2_name} are already friends!")
            return

        person1.add_friend(person2)
        person2.add_friend(person1)

    def print_network(self):
        for name, person in self.people.items():
            friend_names = ", ".join(friend.name for friend in person.friends)
            print(f"{name} is friends with: {friend_names}")


# Test your code here
network = SocialNetwork()

# 6 people
for name in ["Alex", "Jordan", "Morgan", "Taylor", "Casey", "Riley"]:
    network.add_person(name)

# Edge case: duplicate person
network.add_person("Alex")  # "Alex already exists in the network!"

# 8 friendships
network.add_friendship("Alex", "Jordan")
network.add_friendship("Alex", "Morgan")
network.add_friendship("Jordan", "Taylor")
network.add_friendship("Morgan", "Casey")
network.add_friendship("Taylor", "Riley")
network.add_friendship("Casey", "Riley")
network.add_friendship("Morgan", "Riley")
network.add_friendship("Alex", "Taylor")

# Edge cases
network.add_friendship("Jordan", "Johnny")  # Johnny doesn't exist
network.add_friendship("Alex", "Jordan")    # duplicate friendship
network.add_friendship("Casey", "Casey")    # self-friendship

network.print_network()

# Edge case: a person with no friends prints an empty list
network.add_person("Sam")
network.print_network()


#Design Memo
#A graph is the right structure because friendship is a many-to-many, bidirectional relationship with no hierarchy. Any person can connect to any other, and each connection is symmetric, which is exactly what undirected edges between nodes express. A graph also supports the questions a social platform cares about, like how many hops separate two users, which is how Facebook's 3.57 degrees of separation figure was found.
#A list fails because it stores people but not who relates to whom; I would need a second structure of pairs and would scan it to find someone's friends. A tree fails because it forbids cycles and gives each node one parent. In my test network, Alex, Jordan, and Taylor form a cycle, and so do Morgan, Casey, and Riley. A tree cannot represent either without dropping friendships.
#I used an adjacency list inside a dictionary. Looking up a person by name is O(1) on average, and add_person is O(1). add_friendship is O(1) for the lookups, plus O(d) for the duplicate check, where d is the number of friends a person has. Memory is O(V + E), which suits sparse networks, since most people know a tiny fraction of all users. An adjacency matrix would answer "are these two friends?" in O(1) but needs O(V^2) space, impractical at millions of users. Printing is O(V + E) because every person and every friendship is visited, each friendship appearing twice. The trade-off is that checking one specific friendship costs O(d), and storing each friendship on both sides doubles the writes and requires keeping both lists in sync.
