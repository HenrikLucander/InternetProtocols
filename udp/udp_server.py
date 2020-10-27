import socket
import random


class UDPServer:
    """Class for representing the UDP server.

        :param host: The hostname of the server
        :param serverPort: The port of the server to send data
        :param serverSocket: UDP Socket object for the server

        :type host: str
        :type serverPort: str
        :type serverSocket: Object of type <socket.socket>
        """
    def __init__(self, host, port_name):
        self.host = host
        self.serverPort = port_name
        self.serverSocket = None

    def create_and_bind_socket(self):
        """Method to create a UDP socket object and instantiate the class variable serverSocket
        and bind the created socket to the hostname (host) and port (serverPort).

        """
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.serverSocket.bind((self.host, self.serverPort))
        except socket.error as e:
            print(f"Error creating socket: {e}")

    def receive_message(self):
        """Class method to receive a message from client

        :returns:
            - result - The received result of type integer
            - address - The address of the server
        """

        result, address = self.serverSocket.recvfrom(2048)
        return result, address

    def send_message(self, message, client_address):
        """Class method to send a message from server to client

        :param message: The message to be send to the client
        :param client_address: The ip address of the client
        """
        self.serverSocket.sendto(message.encode('utf-8'), client_address)

    def start_game(self):
        """Method representing the game logics and mechanics at the server side.

        """
        print("The server has guessed an integer number.\n")
        number_in_mind = random.randint(0, 100)
        breakout = True
        tries = 10  # 0
        while breakout:
            number, client_address = self.receive_message()
            try:
                user_input = int(number)
                if 100 < user_input < 0:
                    message = "The input number is invalid! The input number should be between [0,100] (including both)"
                    self.send_message(message, client_address)
                    continue
            except ValueError:
                message = "The received number is not an int!"
                self.send_message(message, client_address)
                continue

            print(f"Successfully received value {user_input} from the client")

            if user_input == number_in_mind:
                message = "Success, You have guessed the right number. The correct number was " + str(number_in_mind)
                self.send_message(message, client_address)
                breakout = False
            elif user_input > number_in_mind:
                tries = tries + 1
                if tries == 10:
                    message = "Failure, You have failed to guess the correct number. The correct number was " + str(
                        number_in_mind)
                    self.send_message(message, client_address)
                else:
                    message = f"Your guess {user_input} is higher than what server had in mind. Try guessing a lower " \
                              f"number "
                    self.send_message(message, client_address)
            else:
                tries = tries + 1
                if tries == 10:
                    message = "Failure, You have failed to guess the correct number. The correct number was " + str(
                        number_in_mind)
                    self.send_message(message, client_address)
                else:
                    message = f"Your guess {user_input} is lower than the value server had in mind. Try guessing a " \
                              f"higher number "
                    self.send_message(message, client_address)

    def close_socket(self):
        self.serverSocket.close()


if __name__ == '__main__':
    port = 12000
    hostname = ''
    server = UDPServer(hostname, port)
    server.create_and_bind_socket()
    server.start_game()
    server.close_socket()
