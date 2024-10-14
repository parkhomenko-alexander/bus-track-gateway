import datetime
import socket
import threading


# Wialon Protocol Message Handler (example, parsing may vary depending on actual message format)
def handle_wialon_message(message):
    # Decode the message based on Wialon IPS protocol
    # Here, you would parse the binary or string data according to Wialon specs
    print(f"Received message: {message}")
    
    # Simulate response message (you would craft a proper response here)
    if "#L#" in message:
        response = "#AL#1\r\n"
    else:
        response = "#ACK;"
    return response

# Function to handle client connection
def handle_client_connection(client_socket):
    try:
        while True:
            # Receive the data from the client (GPS tracker)
            message = client_socket.recv(1024)
            
            if not message:
                print("Connection closed by client")
                break
            
            print(f"Received data: {message}")
            
            # Handle the incoming Wialon IPS message
            response = handle_wialon_message(message.decode())
            
            # Send an acknowledgment or response back to the device
            client_socket.send(response.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

# Main server function
def start_server(host='0.0.0.0', port=2020):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # Listen for up to 5 simultaneous connections
    print(f"Server started on {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        
        # Handle client connection in a separate thread
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    print("hello work")
    # Start the Wialon server
    start_server(port=2020)
