import vlc
import time

instance = vlc.Instance()



# Create a MediaPlayer with the default instance
player = instance.media_player_new()



cmd = [
       "file:///home/sensey/Projects/VideoStream/test.mp4",
       "sout=#transcode{vcodec=mp4v}:rtp{dst=127.0.0.1,port=1234,sdp=rtsp://localhost:8000/test.sdp}"
];

# cmd = [
#        "screen://",
#        "sout=#transcode{vcodec=mp4v}:rtp{dst=127.0.0.1,port=1234,sdp=rtsp://localhost:8000/test.sdp}"
# ];
# 
# 
#   s = "sout=#duplicate{"
#         for ip,port in self.destinations:
#             s+="dst=rtp{dst=%s,port=%s}," %(ip,port)
#         s = s[:-1]
#         s+="}"

# Load the media file
# media = instance.media_new("file:///home/sensey/Projects/VideoStream/test.mp4")
# media = instance.media_new('rtsp://localhost:8000/test.sdp')
media = instance.media_new(*cmd)


# cvlc screen:// --sout '#transcode{vcodec=mp4v}:rtp{dst=127.0.0.1,port=1234,sdp=rtsp://localhost:8000/test.sdp}'


# Add the media to the player
player.set_media(media)

# Play for 10 seconds then exit
player.play()
time.sleep(1000)


