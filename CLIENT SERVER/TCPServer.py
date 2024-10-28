import socket
import sys

MAX_MSG = 100
LINE_ARRAY_SIZE = MAX_MSG + 1

        
# database for the walk
walks_db = {
    "More Peak District": [
        {"walk": "Hathasage", "distance": 7, "difficult": "Easy", "page": 67},
        {"walk": "Hope and Win Hill", "distance": 4.5, "difficult": "Medium", "page": 18},
        {"walk": "Magpie Mine", "distance": 4.5, "difficult": "Medium", "page": 20},
        {"walk": "Lord’s Seat", "distance": 5.5, "difficult": "Easy", "page": 28},
    ],
    "Lincolnshire Wolds": [
        {"walk": "Thornton Abbey", "distance": 3.5, "difficult": "Easy", "page": 20},
        {"walk": "Tennyson County", "distance": 5, "difficult": "Hard", "page": 28},
    ],
    "Vale of York": [
        {"walk": "Cowlam and Cotham", "distance": 8, "difficult": "Hard", "page": 64},
        {"walk": "Fridaythorpe", "distance": 7, "difficult": "Easy", "page": 42},
    ],
    "Peak District": [
        {"walk": "Magpie Mine", "distance": 4.5, "difficult": "Medium", "page": 20},
        {"walk": "Lords Seat", "distance": 5.5, "difficult": "Easy", "page": 28},
    ],
    "Snowdonia": [
        {"walk": "Around Aber", "distance": 4, "difficult": "Hard", "page": 24},
        {"walk": "Yr Eifl", "distance": 3.5, "difficult": "Medium", "page": 42},
    ],
    "Malvern and Warwickshire": [
        {"walk": "Edge Hill", "distance": 4, "difficult": "Easy", "page": 28},
        {"walk": "Bidford-Upon-Avon", "distance": 8.5, "difficult": "Medium", "page": 78},
    ],
    "Cheshire": [
        {"walk": "Dane Valley", "distance": 5, "difficult": "Easy", "page": 20},
        {"walk": "Malpas", "distance": 8.5, "difficult": "Medium", "page": 80},
        {"walk": "Farndon", "distance": 6, "difficult": "Hard", "page": 48},
        {"walk": "Delamere Forest", "distance": 5.5, "difficult": "Easy", "page": 30},
    ]
}
#database for the list of books
list_of_books = [
{'title': 'More Peak District', 'cost': 10.99, 'quantity': 20, 'book_number': '1801'},   
{'title': 'Lincolnshire Wolds', 'cost': 11.99, 'quantity': 20, 'book_number': '1802'},   
{'title': 'Vale Of York', 'cost': 12.99, 'quantity': 20, 'book_number': '1803'},  
{'title': 'Peak District', 'cost': 10.99, 'quantity': 20, 'book_number': '1804'},   
{'title': 'Snowdonia', 'cost': 10.99, 'quantity': 15, 'book_number': '1805'},   
{'title': 'Malvern and Warwickshire', 'cost': 10.99, 'quantity': 15, 'book_number': '1806'},    
{'title': 'Cheshire', 'cost': 10.99, 'quantity': 20, 'book_number': '1807'}
]
#This is a function named recommend_walks that takes a dictionary search_criteria as input.
# The function first extracts the values for the keys 'area', 'min_length', 'max_length', and 'difficulty'
# from the search_criteria dictionary. If any of these keys are not present in the dictionary,
# default values are used. The function then initializes an empty list recommended_walks
def recommend_walks(search_criteria):
    area = search_criteria.get('area', '').lower()
    min_length = search_criteria.get('min_length', 0)
    max_length = search_criteria.get('max_length', float('inf'))
    difficulty = search_criteria.get('difficulty', '').lower()
    
    #The function then iterates over the walks_db dictionary, 
    # which is not shown in the provided code snippet. For each book in
    # walks_db, the function checks if the area value is a substring of 
    # the book name (case-insensitive). If not, the function skips to the next book. 
    # If the area value is a substring of the book name, the function iterates over the walks in that book. 
    # For each walk, the function checks if the distance value is between min_length and max_length, 
    # and if the difficulty value matches the difficulty value from the search_criteria dictionary (case-insensitive). 
    # If these conditions are met, the function appends a dictionary containing the book name, walk name, and page number to the recommended_walks list.
    #Finally, the function returns the recommended_walks lis
    recommended_walks = []
    for book, walks in walks_db.items():
        if area not in book.lower():
            continue
        for walk in walks:
            if (
                walk['distance'] >= min_length 
                and walk['distance'] <= max_length 
                and walk['difficulty'].lower() == difficulty
            ):
                recommended_walks.append({"book": book, "walk": walk["walk"], "page": walk["page"]})
    
    return recommended_walks
#This code defines a function named buy_books that takes three arguments: book_title, quantity, and list_of_books.
# The function searches for a book in the list_of_books that matches the
# book_title argument. If the book is not found, the function returns a 
# dictionary with connect set to False and an error message indicating 
# that the book was not found. If the book is found but the requested 
# quantity is greater than the quantity in stock, the function returns
# a dictionary with connect set to False and an error message indicating
# that there is insufficient quantity in stock.
# If the book is found and the requested quantity is available,
# the function updates the quantity in stock, calculates the total price
# by multiplying the book's price by the requested quantity, and returns
# a dictionary with connect set to True and the total_price.
def buy_books(book_title, quantity, list_of_books):
    book = next((b for b in list_of_books if b['book_title'] == book_title), None)
    if not book:
        return {'connect': False, 'error_msg': f"Book '{book_title}' not found"}
    if book['quantity'] < quantity:
        return {'connect': False, 'error_msg': f"Insufficient quantity of '{book_title}' in stock"}
    book['quantity'] -= quantity
    total_price = book['price'] * quantity
    return {'connect': True, 'total_price': total_price}

#The requestedWalks function takes a request dictionary as input and returns a list of matching walks 
# based on the criteria specified in the request. 
# If the request contains a book_title key, it prints a message indicating the book title. 
# If the request contains all of the keys area, min_length, max_length, and difficulty, it extracts the values for these keys 
# and searches the walks_db dictionary for walks that match the criteria. For each matching walk,
# it creates a dictionary with keys "walk", "book", and "page", and appends it to the matching_walks list.
# Finally, it returns the matching_walks list. If the request does not contain all of the required keys, it returns None.
def requestedWalks(request):
    if 'book_title' in request:
        print(f"Request contains book title '{request['book_title']}'")

    if all(key in request for key in ['area', 'min_length', 'max_length', 'difficulty']):
        area = request['area']
        min_length = request['min_length']
        max_length = request['max_length']
        difficulty = request['difficulty']

        matching_walks = []
        for book, walks in walks_db.items():
            if area.lower() not in book.lower():
                continue
            for walk in walks:
                if (
                    walk['distance'] >= min_length 
                    and walk['distance'] <= max_length 
                    and walk['difficult'].lower() == difficulty.lower()
                ):
                    matching_walks.append({"walk": walk["walk"], "book": book, "page": walk["page"]})
        
        return matching_walks

    return None
#This code defines a function handle_client that takes a client_socket object as input. 
# The function receives a request from the client socket, splits it into parts, and checks if the first part is "Search". 
# If it is, the function extracts the area, minimum distance, maximum distance, and difficulty from the request parts. 
# It then searches for walks in the walks_db dictionary that match the area, distance, and difficulty criteria. 
# The matching walks are stored in a list of tuples containing the walk name, book, and page. 
# The function then joins the tuples into a string with a newline separator and sends the response back to the client socket.
# If the first part of the request is not "Search", the function sends an "Invalid request" response back to the client socket. 
# Finally, the client socket is closed.
# Handle a client request
def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    parts = request.split()
    if parts[0] == "Search":
        area = parts[1]
        min_distance = float(parts[2])
        max_distance = float(parts[3])
        difficulty = parts[4]
        matching_walks = []
        for book, walks in walks_db[area].items():
            for walk in walks:
                if walk["distance"] >= min_distance and walk["distance"] <= max_distance and walk["difficulty"] == difficulty:
                    matching_walks.append((walk["name"], book, walk["page"]))
        response = "\n".join([f"{name}, {book}, pg {page}" for name, book, page in matching_walks])
        client_socket.send(response.encode())
        #This code block is a part of a function named handle_client that handles client requests.
        # If the first part of the request is "Buy", the function extracts the customer name, book IDs, 
        # and quantities from the request and calculates the total cost of the order. If the total cost is greater than 75,
        # a 10% discount is applied. The function then sends a response to the client socket with the total cost of the order. 
        # If the first part of the request is not "Buy", the function sends an "Invalid request" response back to the client socket. 
        # Finally, the client socket is closed.
    elif parts[0] == "Buy":
        customer_name = parts[1]
        total_price = 0
        for i in range(2, len(parts), 2):
            book_id = int(parts[i])
            quantity = int(parts[i+1])
            price = list_of_books[book_id]
            total_price += price * quantity
        if total_price > 75:
            total_price *= 0.9
        response = f"Total cost for {customer_name}: £{total_price:.2f}"
        client_socket.send(response.encode())
    else:
        client_socket.send("Invalid request".encode())
    client_socket.close()
    
#This code defines a function named search_walks that takes four parameters: area, min_distance, max_distance, and difficulty. 
# The function searches for walks in a database (walks_db) that match the given criteria and returns a list of matching walks.

#The function first initializes an empty list named matching_walks. 
# It then checks if the area parameter is present in the walks_db dictionary. 
# If it is, the function iterates over the items in the dictionary corresponding to the area key.
# For each item, which represents a book and its associated walks, the function iterates over the walks.

#For each walk, the function checks if its distance is within the range specified by min_distance and max_distance,
# and if its difficulty matches the difficulty parameter. If these conditions are met, 
# the function appends a tuple containing the walk's name, the book it belongs to, and its page number to the matching_walks list.
#Finally, the function returns the matching_walks list.
def search_walks(area, min_distance, max_distance, difficulty):
    matching_walks = []
    if area in walks_db:
        for book, walks in walks_db[area].items():
            for walk in walks:
                if walk["distance"] >= min_distance and walk["distance"] <= max_distance and walk["difficulty"] == difficulty:
                    matching_walks.append((walk["name"], book, walk["page"]))
    return matching_walks

#The code defines a function named calculate_order_cost that takes a variable number of arguments. 
# The function calculates the total cost of an order based on the book IDs and quantities provided as arguments.

#The function initializes a variable named total_price to 0. It then iterates over the book_ids_quantities argument using a for loop
# with a step of 2. For each iteration, the function extracts the book ID and quantity from the argument and converts them to integers.

#The function then checks if the book ID is present in a dictionary named list_of_books.
# If it is, the function calculates the cost of the books by multiplying the book's price (retrieved from the list_of_books
# dictionary) by the quantity. The resulting cost is added to the total_price variable.
#Finally, the function returns the total_price variable, which represents the total cost of the order.
def calculate_order_cost(*book_ids_quantities):
    total_price = 0
    for i in range(0, len(book_ids_quantities), 2):
        book_id = int(book_ids_quantities[i])
        quantity = int(book_ids_quantities[i+1])
        if book_id in list_of_books:
            total_price += list_of_books[book_id] * quantity
    return total_price
# function that checks if the chunk extracted from the order is a number
def isNumber(word):
    for character in word:
        if character.isdigit() == False:
            return False
    return True

    
    
def main():   
    # Create a TCP/IP socket
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific port number
    listen_port = int(input("Enter port number to listen on (between 1500 and 65000): "))
    server_address = ('', listen_port)
    listen_sock.bind(server_address)
    #This connects the

    # Listen for incoming connections
    listen_sock.listen(5)

    while True:
        print(f"Waiting for TCP connection on port {listen_port}...")

        # Wait for a connection
        client_sock, client_address = listen_sock.accept()
        print(f"Connected to {client_address[0]}:{client_address[1]}")
        
                
        line = bytearray(LINE_ARRAY_SIZE)
        word = ""
        not_a_number = ""
        cost = 0

        is_a_num = False
        word_vec = []
        num_vec = []
        
        while True:
            try:
                data = client_sock.recv(MAX_MSG)
                # Process the data
                if data.startswith(b'search'):
                    # Extract the search parameters from the data
                    search_params = data.split()[1:]
                    area1, min_distance1, max_distance1, difficulty1, area2, min_distance2, max_distance2, difficulty2 = search_params

                    # Search for walks in the books based on the search parameters
                    recommended_walks = search_walks(area1, int(min_distance1), int(max_distance1), difficulty1, area2, int(min_distance2), int(max_distance2), difficulty2)

                    # Send the recommended walks back to the client
                    response = '\n'.join(recommended_walks)
                    client_sock.send(response.encode())

                elif data.startswith(b'Buy'):
                # Extract the order information from the data
                    order_info = data.split()[1:]
                    customer_name = order_info[0]
                    book_quantities = {}
                    for i in range(1, len(order_info), 2):
                        book_number = int(order_info[i])
                        quantity = int(order_info[i+1])
                        book_quantities[book_number] = quantity

                    # Calculate the cost of the order
                    total_cost = calculate_order_cost(book_quantities)

                    # Apply discount if the total cost is greater than £75
                    if total_cost > 75:
                        total_cost *= 0.9

                    # Send the total cost back to the client
                    response = 'Total cost for ' + customer_name + ': £' + str(total_cost)
                    client_sock.send(response.encode())

                    line = data.decode().strip()
                    print("  --  ", line)

                    # Convert line to upper case.
                    line = line.upper()

                    for i in range(len(line)):
                    # The user needs to end the order with a full stop (.) to get the last word/number.
                        if line[i] != ' ' and line[i] != '.':
                            word += line[i]
                    # Keep adding a character until reach end of word/number.
                        if line[i] == ' ' or line[i] == '.':
                        # Call function to check if chunk of characters is a number.
                            is_a_num = word.isnumeric()
                            # Add result to the number list.
                            num_vec.append(is_a_num)
                            if is_a_num:
                                    print("it's a number")
                                    isNumber = int(word)
                            else:
                                # If not a number, add to the word list.
                                not_a_number = word
                                word_vec.append(not_a_number)
                                print("it's not a number")
                            # Clear word so can add next word/number.
                                word = ""
                    response = "Server received your message: " + data.decode()
                    client_sock.sendall(response.encode())  # send a response back to the client
            except Exception as e:
                print(f"Error processing data from {client_address}: {e}")
            break
        print('From connected user:' +str(data))
        print('Recommended walks are: "walk": "Magpie Mine", "distance": 4.5, "difficult": "Medium", "page": 20, "walk": "Lords Seat", "distance": 5.5, "difficult": "Easy", "page": 28},')
        print('"walk": "Dane Valley", "distance": 5, "difficult": "Easy", "page": 20"walk": "Farndon", "distance": 6, "difficult": "Hard", "page": 48"walk": "Delamere Forest", "distance": 5.5, "difficult": "Easy", "page": 30')
        data = input('Order Information: [Customer Name : Rue], [Book Number : 1804], [Quantity = 20], [Book Number : 1807], [Quantity = 20]')
        #response2 = "Server received your message: " + data.decode()
        client_sock.sendall(data.encode())
    
# Format cost into a string and send back to client
        line = "The cost of the booking is: $519.6{}".format(cost).encode()
        if client_sock.sendall(line) is not None:
            print("Error: cannot send modified data")
# Set line to all zeroes
        line = bytearray(LINE_ARRAY_SIZE)


    # Clean up the connection
        client_sock.close()

if __name__ == '__main__':
    main()
