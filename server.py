import socket
import threading

class RTSPServer:
    def __init__(self, port):
        self.server_port = port
        self.rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtsp_socket.bind(("0.0.0.0", self.server_port))
        self.rtsp_socket.listen(5)
        print(f"RTSP Server started on port {self.server_port}... Waiting for client.")

    def start(self):
        while True:
            client_conn, client_addr = self.rtsp_socket.accept()
            print(f"✅ Client connected from {client_addr}")
            threading.Thread(target=self.handle_client, args=(client_conn,)).start()

    def handle_client(self, client_conn):
        """ Handle RTSP commands from the client """
        print("🟢 Waiting to receive RTSP requests...")
        while True:
            try:
                request = client_conn.recv(1024).decode()
                if not request.strip():
                    print("❌ Empty RTSP request received. Closing connection.")
                    break
                print(f"✅ RTSP Request Received:\n{request}")

                self.process_rtsp_request(request, client_conn)

            except ConnectionResetError:
                print("❌ Client disconnected unexpectedly.")
                break
            except Exception as e:
                print(f"❌ Error in handle_client: {e}")
                break

        client_conn.close()
        print("❌ Client disconnected.")

    def process_rtsp_request(self, request, client_conn):
        """ Process RTSP client commands and ensure responses are sent """
        lines = request.strip().split("\n")
        if len(lines) < 2:
            print("❌ Invalid RTSP request. Skipping processing.")
            return

        command_parts = lines[0].split(" ")
        if len(command_parts) < 2:
            print("❌ Invalid RTSP command format. Skipping.")
            return

        command = command_parts[0]  # Extract command (SETUP, PLAY, etc.)
        seq_line = lines[1].split(" ")

        if len(seq_line) < 2:
            print("❌ Missing sequence number. Skipping.")
            return
        
        seq_num = seq_line[1]  # Extract sequence number
        response = f"RTSP/1.0 200 OK\nCSeq: {seq_num}\nSession: 123456\n"

        if command == "SETUP":
            if len(lines) < 3 or "Transport" not in lines[2]:
                print("❌ Invalid SETUP request. No RTP port specified!")
                return

            try:
                self.rtp_port = int(lines[2].split("client_port=")[1])
            except IndexError:
                print("❌ RTP port extraction failed.")
                return

            response += "Transport: RTP/UDP\n"
            print(f"✅ SETUP processed. RTP port: {self.rtp_port}")

        elif command == "PLAY":
            print("✅ PLAY request received. Starting stream...")
            response += "Playing stream...\n"

        elif command == "PAUSE":
            print("✅ PAUSE request received. Stopping stream.")
            response += "Stream paused.\n"

        elif command == "TEARDOWN":
            print("✅ TEARDOWN request received. Closing connection.")
            client_conn.close()
            return

        # Send RTSP response
        print(f"✅ Sending RTSP Response:\n{response}")
        client_conn.send(response.encode())

if __name__ == "__main__":
    server = RTSPServer(8554)
    server.start()

