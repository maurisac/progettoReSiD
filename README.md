# Audio Streaming Server-Client Project with VLC
This project demonstrates a simple server-client architecture for streaming audio files. The server hosts audio files and streams them to clients upon request. Clients can interact with the audio playback using VLC..

## Requirements
### Software Dependencies
Python 3 - The server and client are implemented in Python. <br>
VLC Media Player - Used for audio playback on the client side. <br>

### Python Libraries
Ensure you have the following Python libraries installed:

*vlc <br>
socket <br>
threading <br>
subprocess <br>
time <br>
os* <br>

You can install the required, and not pre-installed, VLC Python library via apt: <br>
```sh
apt install python3-vlc
```

## Running the code

To run the code, you first need to open the server
### Run the server
```sh
python3 server.py
```


### Run the client(s)
To run the client, you need to execute this command:
```sh
python3 client.py
```

## Project Structure

>├── client.py           # Client script <br>
>├── main.py             # Server script <br>
>├── authuser.py         # Authentication handler <br>
>├── fileHandler.py      # File handling utilities <br>
>├── files/              # Directory for audio files <br>
>└── README.md           # This file <br>
>
## Troubleshooting
<ul>
<li>VLC Not Opening: Ensure VLC is correctly installed and accessible via the command line. </li>
<li>Permission Issues: Check that the files directory and its contents are readable. </li>
<li>Network Issues: Verify that the server and client are on the same network and that the server's IP address and port are correctly specified in the client script. </li>
</ul>
