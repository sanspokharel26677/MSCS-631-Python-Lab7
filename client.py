import socket
import threading
import cv2
import struct
import numpy as np

class RTSPClient:
    def __init__(self, server_ip, server_port, filename):
        self.server_ip = server_ip
        self.server_port = server_port
        self.filename = filename
        self.rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtsp_socket.connect((self.server_ip, self.server_port))
        self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rtp_socket.bind(("0.0.0.0", 25000))
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

        if command == "PLAY":
            threading.Thread(target=self.receive_rtp_stream, daemon=True).start()

    def receive_rtp_stream(self):
        """ Receives and decodes RTP stream """
        print("\n🎥 Receiving RTP stream...")
        while True:
            try:
                data, _ = self.rtp_socket.recvfrom(65535)
                if not data:
                    continue

                header = data[:12]
                frame_data = data[12:]

                frame_array = np.frombuffer(frame_data, dtype=np.uint8)
                frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

                if frame is not None:
                    cv2.imshow("RTSP Video Stream", frame)
                    cv2.waitKey(1)
                else:
                    print("⚠️ Skipping invalid frame.")

            except Exception as e:
                print(f"❌ Error receiving RTP stream: {e}")
                break

    def start(self):
        """ Main loop to send RTSP commands """
        while True:
            command = input("\nEnter command (setup, play, pause, teardown): ").strip().upper()
            if command in ["SETUP", "PLAY", "PAUSE", "TEARDOWN"]:
                self.send_rtsp_request(command)
                if command == "TEARDOWN":
                    self.rtsp_socket.close()
                    cv2.destroyAllWindows()
                    break
            else:
                print("❌ Invalid command. Try again.")

if __name__ == "__main__":
    client = RTSPClient("127.0.0.1", 8554, "movie.Mjpeg")
    client.start()

