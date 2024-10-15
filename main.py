import datetime
import socket
import threading


def extract_data_fields(message):
    message = message.strip()  
    if message.startswith("#D#"):
        message_content = message[3:-2]  # Remove the "#D#" prefix
    else:
        return None  # Not a valid #D# message

    # Split the message by semicolons
    fields = message_content.split(';')
    
    # Extract the relevant fields
    try:
        date = fields[0] if fields[0] != "NA" else None
        time = fields[1] if fields[1] != "NA" else None
        lat1 = fields[2] if fields[2] != "NA" else None
        lat2 = fields[3] if fields[3] != "NA" else None
        lon1 = fields[4] if fields[4] != "NA" else None
        lon2 = fields[5] if fields[5] != "NA" else None
        speed = fields[6] if fields[6] != "NA" else None
        course = fields[7] if fields[7] != "NA" else None
        
        # Return extracted values
        return {
            "date": date,
            "time": time,
            "lat1": lat1,
            "lat2": lat2,
            "lon1": lon1,
            "lon2": lon2,
            "speed": speed,
            "course": course
        }
        
    except IndexError:
        print("Error: Message does not contain enough fields.")
        return None
    


def handle_wialon_message(message):
    response_body = ""
    print(message[:3])
    match message[:3]:
        case "#L#":
            print(f"Login message: {message}")
            response_body = "#AL#1\r\n"
            return response_body
        case "#D#":
            print(f"Data message: {message}")
            exd = extract_data_fields(message)
            print(exd)
            response_body = "#AD#1\r\n"
            return response_body
        case _:
            print("ERROR")
            response_body = "#ERROR#1\r\n"

    return response_body



def handle_client_connection(client_socket):
    # try:
    #     buffer_size = 1024
    #     data = b''

    #     while True:
    #         print("Waiting to receive data...")
    #         chunk = client_socket.recv(buffer_size)

    #         # If the chunk is empty, the connection is closed
    #         if not chunk:
    #             print("Connection closed by client")
    #             break

    #         # Accumulate the chunk of data
    #         data += chunk

    #         # Check if the message ends with the delimiter (e.g., '\r\n')
    #         if b'\r\n' in data:
    #             print(f"Complete message received: {data.decode()}")

    #             # Process the message and send the response
    #             response = handle_wialon_message(data.decode())
    #             print(response)
    #             client_socket.send(response.encode())

    #             # Clear the buffer for future messages if needed
    #             data = b''  # Reset the buffer for the next message
    #             break  # Stop after processing the message

    # except Exception as e:
    #     print(f"Error handling client: {e}")
    # finally:
    #     client_socket.close()
    
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
    print(f"Server started on {host}:{port}\n")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server(port=2020)
