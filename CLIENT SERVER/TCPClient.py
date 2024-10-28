import socket
import sys

MAX_LINE = 100
MAX_MSG = 100
LINE_ARRAY_SIZE = MAX_MSG + 1

def send_message(sock, message):
    # Sends a message to the server
    sock.send(message.encode())

def receive_message(sock):
    # Receives a message from the server
    message = sock.recv(LINE_ARRAY_SIZE)
    return message.decode()

def display_welcome_message():
    # Displays a welcome message
    print("Welcome to the walking books recommendation system!")
    print("You can use this system to find circular walks and buy books.")

def get_user_choice():
    # Gets the user's choice
    print("\nWhat would you like to do?")
    print("1. Find a walk")
    print("2. Buy a book")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")
    return choice

def get_walk_criteria():
    # Gets the criteria for the walk recommendation
    area = input("Enter the area you want to walk in: ")
    min_length = input("Enter the minimum length (in miles) of the walk: ")
    max_length = input("Enter the maximum length (in miles) of the walk: ")
    difficulty = input("Enter the difficulty level (Easy/Medium/Hard) of the walk: ")
    return {"area": area, "min_length": min_length, "max_length": max_length, "difficulty": difficulty}

def display_walks(walks):
    # Displays the recommended walks
    print("\nThe recommended walks are:")
    for walk in walks:
        print(f"- {walk['walk']} in {walk['book']}, page {walk['page']}")

def get_book_choice():
    # Gets the user's book choice
    book_title = input("Enter the title of the book you want to buy: ")
    quantity = input("Enter the quantity you want to buy: ")
    return {"book_title": book_title, "quantity": quantity}

def display_purchase_result(result):
    # Displays the result of the book purchase
    if result["connect"]:
        print(f"\nSuccessfully bought {result['quantity']} copies of {result['book_title']}.")
    else:
        print(f"\nError: {result['error_msg']}")

def display_exit_message():
    # Displays an exit message
    print("\nThank you for using the walking books recommendation system. Goodbye!")


try:
    # Prompt the user for the server hostname or IP address.
    hostname = '127.0.0.1'
    
    # Resolve the server hostname to an IP address.
    server_ip = socket.gethostbyname(hostname)

    # Prompt the user for the server port number.
    server_port = int(input("Enter server port number: "))

    # Create a TCP socket.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server.
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)



    buf = input()
    #This code block creates an infinite loop that prompts the user to input various parameters related to buying books 
    # and searching for walking areas. The user is prompted to enter their name, book numbers they want to buy, 
    # and the corresponding quantities. They are then prompted to enter two areas where they want to walk, the minimum and 
    # maximum distances they want to walk in each area, and the level of difficulty for each area.
    # The inputs are stored in variables for later use.
    while True:
        customer_name = input('Enter your name: ')
        book_numbers = input('Enter the book numbers you want to buy (separated by spaces): ')
        quantities = input('Enter the quantities you want to buy (separated by spaces): ')
        print('/n')
        area1 = input("Enter the area where you want to walk: ")
        area2 = input("Enter the another area where you want to walk: ")
        min_distance1 = input("Enter the minimum distance in miles: ")
        min_distance2 = input("Enter the another minimum distancein miles: ")
        max_distance1 = input("Enter the maximum distance in miles: ")
        max_distance2 = input("Enter the another maximum distance in miles: ")
        difficulty1 = input("Enter the level of difficulty: ")
        difficulty2 = input("Enter the another level of difficulty: ")
        
        # send search parameters to server
        buf = f"search {area1} {min_distance1} {max_distance1} {difficulty1} {area2} {min_distance2}, {max_distance2}, {difficulty2}" 
        
        # Construct the order message and send it to the server
        order = f"Buy {customer_name} {book_numbers} {quantities}\n".encode()
        socket.sendall(order)
        response = client_socket.recv(1024).decode()
        print(response)
        #This code block checks if the value of the variable buf is equal to a period (".") 
        #and if it is, it breaks out of the loop. This is commonly used to exit a loop when a certain condition is met.
        if buf == ".":
            break
        
        
        # Send the line to the server.
        client_socket.sendall(bytes(buf, 'utf-8'))
        

        # Zero out the buffer.
        buf = bytearray(MAX_LINE)

        # Read the modified line back from the server.
        recv_size = client_socket.recv_into(buf, MAX_LINE)
        #This code block checks if the value of the variable recv_size is less than zero.
        # If it is, it means that the client did not receive a response from the server. In this case, 
        # the code prints a message indicating that there was no response from the server, 
        # closes the client socket, and exits the program with an error code of 1
        if recv_size < 0:
            print("didn't get response from server?")
            client_socket.close()
            sys.exit(1)
        
        # Convert the bytes received to a string and display it.
        modified_buf = buf.decode('utf-8')
        print("Modified: ", modified_buf.strip())
        #This code block receives data from the server using the recv() method of the client_socket object.
        # The 1024 argument specifies the maximum amount of data to be received at once. The received data is in bytes format,
        # so it is decoded using the decode() method to convert it to a string. 
        # The decoded data is then printed to the console with a message indicating that it was r
        data = client_socket.recv(1024).decode()
        print(f"Message received from server: {data}")
        
        
   
    print("just a dot, and nothing else.")
    print("If a line is more than", MAX_LINE, "characters, then")
    print("only the first", MAX_LINE, "characters will be used.\n")
    
    #This code block is a part of a try-except block that handles exceptions. 
    # The KeyboardInterrupt exception is raised when the user presses the Ctrl+C keys on the keyboard. 
    # When this exception is caught, the code prints a message to the console indicating that a KeyboardInterrupt was received 
    # and then closes the client socket. Finally, the sys.exit(1) statement is used to exit the program with a non-zero status code,
    # indicating that an error occurred.
except KeyboardInterrupt:
    print("\nKeyboardInterrupt received. Closing the client socket.")
    client_socket.close()
    sys.exit(1)
    
    #This code block is a part of a try-except block that handles exceptions. 
    # It catches the socket.gaierror exception which is raised when the hostname could not be resolved. 
    # If this exception is caught, the code prints a message to the console indicating that the 
    # hostname could not be resolved and then exits the program with a non-zero status code, indicating that an error occurred.
except socket.gaierror:
    print("Hostname could not be resolved. Exiting.")
    sys.exit(1)

    #This code block is a part of a try-except block that handles exceptions. 
    # It catches the socket.error exception which is raised when a socket error occurs. 
    # If this exception is caught, the code prints a message to the console indicating that a socket error occurred and
    # then exits the program with a non-zero status code, indicating that an error occurred. 
    # The exception object is assigned to the variable 'e' and is printed along with the error message to provide more information
except socket.error as e:
    print("Socket error occurred: ", e)
    sys.exit(1)

    #This code block is a part of a try-except block that handles exceptions. 
    # It catches any exception that is not caught by the previous except blocks. 
    # If this exception is caught, the code prints a message to the console indicating that an error occurred and 
    # then exits the program with a non-zero status code, indicating that an error occurred. 
    # The exception object is assigned to the variable 'e'
    # and is printed along with the error message to provide more information about the error that occurred.
except Exception as e:
    print("An error occurred: ", e)
    sys.exit(1)
    #This line of code calls the exit() function from the sys module with an argument of 0. 
    # This function terminates the program and returns the specified exit code to the operating system
sys.exit(0)
