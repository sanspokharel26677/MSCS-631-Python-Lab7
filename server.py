import socket
import threading
import cv2
import struct
import time

class RTSPServer:
    def __init__(self, port, video_file):
        self.server_port = port
        self.video_file = video_file
        self.rtsp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtsp_socket.bind(("0.0.0.0", self.server_port))
        self.rtsp_socket.listen(5)
        self.client_conn = None
        self.client_addr = None
        self.streaming = False
        self.rtp_socket = None
        self.rtp_port = None

    def start(self):
        print(f"RTSP Server started on port {self.server_port}... Waiting for client.")
        while True:
            self.client_conn, self.client_addr = self.rtsp_socket.accept()
            print(f"✅ Client connected from {self.client_addr}")
            threading.Thread(target=self.handle_client).start()

    def handle_client(self):
        """ Handle RTSP commands from the client """
        print("🟢 Waiting to receive RTSP requests...")
        while True:
            try:
                request = self.client_conn.recv(1024).decode()
                if not request.strip():
                    print("❌ Empty RTSP request received. Closing connection.")
                    break
                print(f"✅ RTSP Request Received:\n{request}")

                self.process_rtsp_request(request)

            except ConnectionResetError:
                print("❌ Client disconnected unexpectedly.")
                break
            except Exception as e:
                print(f"❌ Error in handle_client: {e}")
                break

        self.client_conn.close()
        print("❌ Client disconnected.")

    def process_rtsp_request(self, request):
        """ Process RTSP client commands and send responses """
        lines = request.strip().split("\n")
        if len(lines) < 2:
            print("❌ Invalid RTSP request. Skipping processing.")
            return

        command_parts = lines[0].split(" ")
        if len(command_parts) < 2:
            print("❌ Invalid RTSP command format. Skipping.")
            return

        command = command_parts[0]  # Extract command (SETUP, PLAY, etc.)
        seq_num = lines[1].split(" ")[1]
        response = f"RTSP/1.0 200 OK\nCSeq: {seq_num}\nSession: 123456\n"

        if command == "SETUP":
            try:
                self.rtp_port = int(lines[2].split("client_port=")[1])
                self.rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print(f"✅ SETUP processed. RTP port: {self.rtp_port}")
            except Exception as e:
                print(f"❌ Failed to extract RTP port: {e}")
                return

        elif command == "PLAY":
            print("✅ PLAY request received. Starting stream...")
            self.streaming = True
            threading.Thread(target=self.stream_video, daemon=True).start()

        elif command == "PAUSE":
            print("✅ PAUSE request received. Stopping stream.")
            self.streaming = False

        elif command == "TEARDOWN":
            print("✅ TEARDOWN request received. Closing connection.")
            self.streaming = False
            self.client_conn.close()
            self.rtsp_socket.close()
            return

        # Send RTSP response
        print(f"✅ Sending RTSP Response:\n{response}")
        self.client_conn.send(response.encode())

    def stream_video(self):
        """ Stream video frames over RTP """
        cap = cv2.VideoCapture(self.video_file)
        if not cap.isOpened():
            print(f"❌ Error: Unable to open video file {self.video_file}")
            return
        
        print(f"🎥 Streaming video from {self.video_file}...")
        frame_id = 0

        while self.streaming and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("✅ Video streaming completed.")
                break

            _, frame_encoded = cv2.imencode('.jpg', frame)
            frame_data = frame_encoded.tobytes()

            # Create RTP Packet
            header = struct.pack("!BBHII", 0x80, 26, frame_id, 0, 0)
            rtp_packet = header + frame_data

            # Send RTP Packet
            self.rtp_socket.sendto(rtp_packet, (self.client_addr[0], self.rtp_port))
            print(f"📩 Sent RTP packet {frame_id} (size: {len(rtp_packet)} bytes)")
            
            frame_id += 1
            time.sleep(1 / 30)  # Simulate 30 FPS

        cap.release()

if __name__ == "__main__":
    server = RTSPServer(8554, "movie.Mjpeg")
    server.start()

