
# Lab: Build Your Own AI Application

1 / 2
info

Ollama Labs

The Ollama service is running on the ollama-server.

To access the server, use the following SSH command:

ssh ai-engineer@$IP_ADDRESS



2 / 2
info

Ollama Labs

Develop an application which interacts that the Ollama API running at http://localhost:11434/v1 in ollama-server. Use the previous video as a reference for interacting with the API. Use the qwen:0.5b model, which is already running for you with the help of ollama server.

To get the exact name of ollama server , You can use command hostname , in this example , the hostname is ollama-server-1755523044.

ai-engineer@ollama-server-1755523044:~$ hostname
ollama-server-1755523044

NOTE: All ports from 80 to 8080 are open on the ollama-server. Run the application on any of these ports, then access it in your browser using the IP_ADDRESS.
