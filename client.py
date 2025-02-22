import socket
import threading

class RTSPClient:
    def __init__(self, server_ip, server_port, filename):
        self.server_ip = server_ip
        self.server_port = server_port
        self.filename = filename
        self.rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtsp_socket.connect((self.server_ip, self.server_port))
        print(f"✅ Connected to RTSP server at {server_ip}:{server_port}")

    def send_rtsp_request(self, command):
        """ Sends RTSP commands to the server """
        request = f"{command} {self.filename} RTSP/1.0\nCSeq: 1\n"
        if command == "SETUP":
            request += "Transport: RTP/UDP; client_port=25000\n"
        print(f"\n📤 Sending RTSP Request:\n{request.strip()}")

        self.rtsp_socket.send(request.encode())
        response = self.rtsp_socket.recv(1024).decode()
        print(f"\n📩 Received RTSP Response:\n{response}")

    def start(self):
        """ Main loop to send RTSP commands """
        while True:
            command = input("\nEnter command (setup, play, pause, teardown): ").strip().upper()
            if command in ["SETUP", "PLAY", "PAUSE", "TEARDOWN"]:
                self.send_rtsp_request(command)
                if command == "TEARDOWN":
                    self.rtsp_socket.close()
                    break
            else:
                print("❌ Invalid command. Try again.")

if __name__ == "__main__":
    client = RTSPClient("127.0.0.1", 8554, "movie.Mjpeg")
    client.start()

