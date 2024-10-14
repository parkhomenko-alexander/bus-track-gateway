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
        buffer_size = 8192  # Increase the buffer size to a larger value, e.g., 8192 bytes
        data = b''  # Use this to accumulate data
        
        while True:
            # Receive data from the client
            chunk = client_socket.recv(buffer_size)
            
            if not chunk:
                print("Connection closed by client")
                break
            
            # Append the received chunk to the data buffer
            data += chunk
            
            print(f"Received chunk: {chunk}")
            
            # Check if the message ends with the delimiter (e.g., '\r\n')
            if b'\r\n' in data:
                # Split the data at the delimiter to process the message
                messages = data.split(b'\r\n')
                
                # Process each complete message (before the last delimiter)
                for message in messages[:-1]:
                    decoded_message = message.decode()
                    print(f"Complete message: {decoded_message}")
                    
                    # Handle the message (Wialon, in this case)
                    response = handle_wialon_message(decoded_message)
                    
                    # Send an acknowledgment or response back to the client
                    client_socket.send(response.encode())
                
                # Keep any data after the last delimiter in the buffer (in case of additional messages)
                data = messages[-1]  # Reset data to the remaining incomplete part (if any)
                
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
