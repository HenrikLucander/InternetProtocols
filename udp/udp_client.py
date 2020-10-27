import socket


def set_port_ip():
    server_port_ = 12000  # TODO: Complete the port here
    server_name = socket.gethostname()  # TODO: Get the server name
    ip_address_ = socket.gethostbyname(server_name)  # TODO: Get the server ip address
    return server_port_, ip_address_


def encode_utf(message):
    """Encodes a given message to utf-8 encoding

    :param message: The message to be encoded to utf-8
    :type message: str
    :return: The utf-8 encoded message
    """
    return str(message).encode('utf-8')


def decode_utf(message):
    """Decodes a given message from utf-8 encoding

    :param message: The message to be decoded to utf-8
    :return: The utf-8 decoded message
    """
    return message.decode('utf-8')


class UDPClient:
    """Class for representing the UDP client.

    :param serverAddress: The ip address of the server to send data
    :param serverPort: The port of the server to send data
    :param clientSocket: UDP Socket object for the client
    :param total_tries: The number of tries to guess the correct number
    :param user_input: The user input/ guessed value fo the client

    :type serverAddress: str
    :type serverPort: str
    :type clientSocket: Object of type <socket.socket>
    :type total_tries: int
    :type user_input: int
    """

    def __init__(self, host, port, tries, ui):
        self.serverAddress = host
        self.serverPort = port
        self.clientSocket = None
        self.total_tries = tries
        self.user_input = ui

    def create_socket(self):
        """Class method to create a UDP socket object and instantiates the clientSocket class variable

        """
        try:
            # TODO: Remove empty string and create a new UDP socket here
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        except socket.error as e:
            print(f"Error creating socket: {e}")

    def send_message(self, message):
        """Class method to send a message from client to server using the socket, ip_address, and port

        :param message: The message (the number guessed by client) that needs to be transmitted
        """
        try:
            message = encode_utf(message)
            # TODO: Use the created clientSocket, ip_address, and port to send the above given decoded message
            self.clientSocket.sendto(message,(self.serverAddress,self.serverPort))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def receive_message(self):
        """Class method to receive a message from server

        :returns:
            - result - The received result of type integer
            - address - The address of the server
        """
        try:
            result, address = self.clientSocket.recvfrom(1024)  # TODO: Utilize the clientSocket to receive the message from the server.
            return result, address
        except socket.error as e:
            print(f"Error receiving data: {e}")

    def guess_game(self):
        """The game mechanics method, that has the entire game logic.

        :return: The decoded message received from the server
        """
        tries = 0
        next_round = True
        result_message = None
        if self.total_tries is None:
            self.total_tries = 10
        if self.user_input is None:
            print("Welcome to the integer guessing game. You need to guess the integer between 0 and 100 that has been "
                  "selected by the server")
            print(
                "-----------------------------------------------------------------------------------------------------"
                "----------------------")
        while tries < self.total_tries and next_round:  # or if the answer is correct
            if self.user_input is None:

                try:
                    self.user_input = int(input("\nInput your guess for the number (integer between 0 and 100): "))
                except ValueError:
                    print("Invalid input! That's not an int!")
                    continue

                if self.user_input > 100 or self.user_input < 0:
                    print("Invalid input! The input number should be between 0 and 100")
                    continue

            self.send_message(self.user_input)
            result_message, server_address = self.receive_message()

            print(decode_utf(result_message))
            tries = tries + 1

            if "Success" in str(result_message):
                next_round = False

            if tries < self.total_tries and next_round is True:
                print(f"You have {self.total_tries - tries} tries remaining.")
            self.user_input = None
        return decode_utf(result_message)

    def close_socket(self):
        """Method to close the created socket

        """
        self.clientSocket.close()


if __name__ == '__main__':
    server_port, ip_address = set_port_ip()
    client = UDPClient(ip_address, server_port, None, None)
    client.create_socket()
    client.guess_game()
    client.close_socket()
