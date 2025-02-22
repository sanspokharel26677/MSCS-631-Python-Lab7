class VideoStream:
    def __init__(self, filename):
        """ Open the video file """
        try:
            self.file = open(filename, "rb")
            print(f"✅ Video file '{filename}' opened successfully.")
        except Exception as e:
            print(f"❌ Error opening video file: {e}")
            self.file = None

    def next_frame(self):
        """ Read the next frame from the video file """
        try:
            if not self.file:
                print("❌ No video file loaded.")
                return None

            frame_size = 2048  # Read smaller chunks instead of large frames
            frame_data = self.file.read(frame_size)

            if not frame_data:
                print("🎬 End of video file reached.")
                return None  # End of file

            return frame_data

        except Exception as e:
            print(f"❌ Error reading frame: {e}")
            return None

