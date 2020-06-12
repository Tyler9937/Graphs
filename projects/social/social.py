import random
from collections import deque

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:


    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        self.count = 0

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        self.count += 1

        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            
    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.friendships[vertex_id]

    def populate_graph(self, num_users, avg_friendships):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        for i in range(0, num_users):
            self.add_user(f'User {i}')

        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])


    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = deque()
        q.append([starting_vertex])

        visited = set()

        while q:
            path = q.popleft()
            v = path[-1]
            if v not in visited:
                if v == destination_vertex:
                    return path
                visited.add(v)
                for n in self.get_neighbors(v):
                    q.append([*path, n])
        return None


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        
        for user in self.users:
            path = self.bfs(user_id, user)
            visited[user] = path

        return visited

'''
 3. Question
    1. To create 100 users with an average of 10 friends each, how many times would you need to call add_friendship()? Why?
    
        - In this case it would take 500 function calls. In any case it would be the number of users * the desired average // 2.
        This is because: Firstly, the divided by 2 part just accounts for the fact that when when user makes a friendship its actully
        new friendships occuring. So lets drop the // 2 for understanding. We have 100 users and we want an avaarge of 10 friends per user.
        that means we would have to create 1000 friendships from a randomly distributied source so that so that each user has chance of
        gaining 10 friends (1000frindships / 100 users = 10friends / user). Since its random some people will have more than 10 and some
        people will have less but the average will work out to be 10.

    2. near 100% average 500 degrees of seperation
'''

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
    print(sg.count)
