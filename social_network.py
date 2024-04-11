import random
import faker

from graph import Graph  # Import the Graph class from the graph2 module

follow_graph = Graph()  # Create a graph to represent the follow relationships
likes_graph = Graph()  # Create a graph to represent the likes relationships
comment_graph = Graph()  # Create a graph to represent the comment relationships
influence_graph = Graph()  # Create a graph to represent the influence relationships
names = []  # Initialize an empty list to store the names

def set_random_names():
    # Generate a list of random names
    fake = faker.Faker()
    for _ in range(10):
        names.append(fake.name())

    for name in names:
        # Add random names to the follow, likes, comment, and user graphs
        follow_graph.add_vertex(name)
        likes_graph.add_vertex(name)
        comment_graph.add_vertex(name)
        influence_graph.add_vertex(name)

        # Randomly create follow relationships
        num_follows = random.randint(0, len(names) - 1)
        followed_names = random.choices(names, k=num_follows)
        for followed_name in followed_names:
            follow_graph.add_edge(name, followed_name)

        # Randomly create likes relationships
        num_likes = random.randint(0, len(names) - 1)
        num_likes_of_each_name = random.randint(1, 10)
        liked_names = random.choices(names, k=num_likes)
        for liked_name in liked_names:
            likes_graph.add_edge(name, liked_name, num_likes_of_each_name)

        # Randomly create comment relationships
        num_comments = random.randint(0, len(names) - 1)
        num_comments_of_each_name = random.randint(1, 10)
        commented_names = random.choices(names, k=num_comments)
        for commented_name in commented_names:
            comment_graph.add_edge(name, commented_name, num_comments_of_each_name)

# Calculate the engagement rate for a given name
def calculate_engagement_rate(name):
    follows = follow_graph.get_number_of_edges(name)
    likes = get_total_likes(name)
    comments = get_total_comments(name)
    engagement_rate = (likes + comments) / follows if follows != 0 else 0
    return engagement_rate

# Calculate the influence between two names
def calculate_influence(ida, idb):
    likes = 0
    comments = 0
    engagement_rate = calculate_engagement_rate(ida)
    likes = likes_graph.get_weight(ida, idb)
    comments = comment_graph.get_weight(ida, idb)
    influence = (likes + comments) / engagement_rate if engagement_rate != 0 else 0
    return influence

# Create the influence graph based on the likes and comments relationships
def create_influence_graph():
    for name in names:
        for liked_name in likes_graph.get_edges(name):
            if name != liked_name:  # Check if the name is not the same as the liked_name
                influence_likes = calculate_influence(name, liked_name)
                if liked_name not in comment_graph.get_edges(name):
                    influence_graph.add_edge(name, liked_name, influence_likes)
                else:
                    for commented_name in comment_graph.get_edges(name):
                        influence_comments = calculate_influence(name, commented_name)
                        total_influence = influence_likes + influence_comments
                        influence_graph.add_edge(name, commented_name, total_influence)

# Find the highest engagement path between two names
def highest_engagement_path(start, destination):
    # Initialize variables
    current_node = start
    path = [current_node]
    total_engagement = 0

    # Traverse the graph until the destination is reached
    while current_node != destination:
        # Get the neighbors of the current node
        neighbors = influence_graph.get_edges(current_node)

        # Calculate the engagement of each neighbor
        neighbor_engagement = {}
        for neighbor in neighbors:
            engagement = calculate_engagement_rate(neighbor)
            neighbor_engagement[neighbor] = engagement

        # Sort the neighbors based on their engagement in descending order
        sorted_neighbors = sorted(neighbor_engagement.items(), key=lambda x: x[1], reverse=True)

        # Choose the neighbor with the highest engagement as the next node
        next_node = sorted_neighbors[0][0]
        next_engagement = sorted_neighbors[0][1]

        # Update the total engagement and path
        total_engagement += next_engagement
        path.append(next_node)

        # Move to the next node
        current_node = next_node

    return path, total_engagement

# Get the total number of likes for a given name
def get_total_likes(name):
    total_likes = 0
    for e in likes_graph.get_edges(name):
        total_likes += likes_graph.get_weight(name, e)
    return total_likes

# Get the total number of comments for a given name
def get_total_comments(name):
    total_comments = 0
    for e in comment_graph.get_edges(name):
        total_comments += comment_graph.get_weight(name, e)
    return total_comments

# Display the total number of likes, comments, and follows for each name
def display_total_likes_comments_follows():
    print("\nLikes, Comments, and Follows\n")
    for name in names:
        print(f"{name}:")
        followed_names = follow_graph.get_edges(name)
        print(f"Total Follows: {len(followed_names)}")
        print(f"Total Likes: {get_total_likes(name)}")
        print(f"Total Comments: {get_total_comments(name)}\n")

# Display the engagement rate for each name
def display_engagement_rate():
    print("\nEngagement rate")
    for name in names:
        engagement_rate = calculate_engagement_rate(name)
        print(f"{name}: {engagement_rate:.2f}")

# Display the influence between each pair of names
def display_influence():
    create_influence_graph()
    print("\nInfluence")
    for name in names:
        print(f"{name}:")
        for e in influence_graph.get_edges(name):
            print(f"{e}: {influence_graph.get_weight(name, e):.2f}")
        print()

# Display the shortest paths for follows
def display_shortest_paths_for_follows():
    start = input("Enter the starting name: ")
    dest = input("Enter the destination name: ")
    follow_graph.bfs(start)
    follow_graph.print_shortest_path(start, dest)
    print(f"{follow_graph.path}\n")

# Display the shortest paths for likes
def display_shortest_paths_for_likes():
    start = input("Enter the starting name: ")
    dest = input("Enter the destination name: ")
    likes_graph.bfs(start)
    likes_graph.print_shortest_path(start, dest)
    print(f"{likes_graph.path}\n")

# Display the shortest paths for comments
def display_shortest_paths_for_comments():
    start = input("Enter the starting name: ")
    dest = input("Enter the destination name: ")
    comment_graph.bfs(start)
    comment_graph.print_shortest_path(start, dest)
    print(f"{comment_graph.path}\n")

# Display the engagement path for follows
def display_engagement_path_for_follows():
    start = input("Enter the starting name: ")
    dest = input("Enter the destination name: ")
    follow_graph.dijkstra(start)
    follow_graph.print_shortest_path(start, dest)
    print("\nEngagement Path for Follows")
    print(f"{follow_graph.path}\n")

# Display the engagement path for likes
def display_engagement_path_for_likes():
    start = input("Enter the starting name: ")
    dest = input("Enter the destination name: ")
    likes_graph.dijkstra(start)
    likes_graph.print_shortest_path(start, dest)
    print("\nEngagement Path for Likes")
    print(f"{likes_graph.path}\n")

# Display the engagement path for comments
def display_engagement_path_for_comments():
    start = input("Enter the starting name: ")
    dest = input("Enter the destination name: ")
    comment_graph.dijkstra(start)
    comment_graph.print_shortest_path(start, dest)
    print("\nEngagement Path for Comments")
    print(f"{comment_graph.path}\n")

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Display all follows, likes, and comments")
        print("2. Display Engagement Rate")
        print("3. Display Influence")
        print("4. Display Shortest Paths")
        print("5. Find Highest Engagement Path")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_total_likes_comments_follows()
        elif choice == "2":
            display_engagement_rate()
        elif choice == "3":
            display_influence()
        elif choice == "4":
            display_shortest_paths_submenu()
        elif choice == "5":
            display_engagement_path_submenu()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def display_shortest_paths_submenu():
    while True:
        print("Shortest Paths Submenu")
        print("1. Display Shortest Paths for Follows")
        print("2. Display Shortest Paths for Likes")
        print("3. Display Shortest Paths for Comments")
        print("4. Go back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            follow_graph.display_edges()
            display_shortest_paths_for_follows()
        elif choice == "2":
            likes_graph.display_edges()
            display_shortest_paths_for_likes()
        elif choice == "3":
            comment_graph.display_edges()
            display_shortest_paths_for_comments()
        elif choice == "4":
            main_menu()
        else:
            print("Invalid choice. Please try again.")

def display_engagement_path_submenu():
    while True:
        print("Engagement Path Submenu")
        print("1. Display Engagement Path for Follows")
        print("2. Display Engagement Path for Likes")
        print("3. Display Engagement Path for Comments")
        print("4. Go back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            follow_graph.display_edges()
            display_engagement_path_for_follows()
        elif choice == "2":
            likes_graph.display_edges()
            display_engagement_path_for_likes()
        elif choice == "3":
            comment_graph.display_edges()
            display_engagement_path_for_comments()
        elif choice == "4":
            main_menu()
        else:
            print("Invalid choice. Please try again.")

def main():
    set_random_names()
    main_menu()


main()
