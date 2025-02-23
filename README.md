# MSCS-631-Python-Lab7# RTSP Video Streaming and RTP Analysis - Lab 7

## 📌 Overview  
This project implements a **Real-Time Streaming Protocol (RTSP) server and client** to stream a video over **RTP (Real-Time Transport Protocol)**. The implementation allows the client to send RTSP commands (`SETUP`, `PLAY`, `PAUSE`, `TEARDOWN`) to control the video stream, while the server processes these commands and transmits the video as RTP packets.

## 📂 Files in This Project  
- **`server.py`** - RTSP server that streams video over RTP.  
- **`client.py`** - RTSP client that sends commands and plays the streamed video.  
- **`VideoStream.py`** - Handles video file reading and frame extraction.  

## 🚀 Features Implemented  
✅ RTSP command handling (`SETUP`, `PLAY`, `PAUSE`, `TEARDOWN`)  
✅ RTP packet streaming  
✅ RTP packet reception and video playback using OpenCV  
✅ Packet capture and analysis using `tcpdump` and `tshark`  
✅ Performance metrics calculation (frame rate, data rate, packet loss)  

## 🎥 How to Run the Project  

### 1️⃣ **Start the RTSP Server**  
Run the server on a specific port (e.g., `8554`):  
```bash
python3 server.py 8554

The server will wait for a client connection.

### 2️⃣ Start the Client
	Run the client and connect to the server:
  python3 client.py 127.0.0.1 8554 movie.Mjpeg
  
You will be prompted to enter RTSP commands.

### 3️⃣ Send RTSP Commands
	Once the client is running, enter any of the following:

	setup      # Initializes the streaming session  
	play       # Starts video playback  
	pause      # Pauses the video stream  
	teardown   # Ends the session and disconnects  

## Dependencies
Ensure you have the required dependencies installed:
	pip install opencv-python numpy


📌 Notes
The video file (movie.Mjpeg) is required for streaming. If not provided, download and convert a video to MJPEG format.
The server and client must be running on the same network for proper communication.
Wireshark or tshark can be used for further RTP analysis.

👨‍💻 Author
Sandesh Pokharel
Master’s in Computer Science (MSCS)
Advanced Computer Networks - Lab 7
