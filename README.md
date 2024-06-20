# Audio Streaming Server-Client Project with VLC
This project demonstrates a simple server-client architecture for streaming audio files. The server hosts audio files and streams them to clients upon request. Clients can interact with the audio playback using VLC..

## Requirements
### Software Dependencies
Python 3 - The server and client are implemented in Python. <br>
VLC Media Player - Used for audio playback on the client side. <br>

### Python Libraries
Ensure you have the following Python libraries installed:

vlc <br>
socket <br>
threading <br>
You can install the required VLC Python library via pip: <br>
```sh
pip install python-vlc
```

## Running the code

To run the code, you first need to open the server
### Run the server
```sh
python3 main.py
```


### Run the client(s)
To run the client, you need to execute this command:
```sh
python3 client.py
```
