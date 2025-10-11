
# Lab: Getting Familiar With Ollama CLI


1 / 9
info

Ollama Labs

The Ollama service is running on the ollama-server.

To access the server, use the following SSH command:

ssh ai-engineer@$IP_ADDRESS




2 / 9

Ollama Labs

Which one of the following models is present on the ollama-server right now?

A. duckyblender/danube3:0.5b
B. tinyllama:latest
C. llama3.2:1b
D. mistral:latest


~ ✖ ssh ai-engineer@$IP_ADDRESS
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1031-azure x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Sun Aug 31 17:32:34 UTC 2025

  System load:  0.45               Processes:             121
  Usage of /:   21.7% of 28.89GB   Users logged in:       0
  Memory usage: 5%                 IPv4 address for eth0: 10.0.0.4
  Swap usage:   0%


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
New release '24.04.3 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


ai-engineer@ollama-server-1756661287:~$ ollama ls
NAME                         ID              SIZE      MODIFIED           
llama3.2:1b                  baf6a787fdff    1.3 GB    53 seconds ago        
tinyllama:latest             2644915ede35    637 MB    About a minute ago    
duckyblender/danube3:0.5b    13292586951b    317 MB    About a minute ago    
ai-engineer@ollama-server-1756661287:~$ 
ai-engineer@ollama-server-1756661287:~$ date
Sun Aug 31 17:32:59 UTC 2025
ai-engineer@ollama-server-1756661287:~$ 




3 / 9

Ollama Labs

Get the qwen:0.5b model on the ollama-server.

Is the qwen:0.5b model pulled into the ollama-server?


ollama pull qwen:0.5b

ai-engineer@ollama-server-1756661287:~$ ollama pull qwen:0.5b
pulling manifest 
pulling fad2a06e4cc7: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏ 394 MB                         
pulling 41c2cf8c272f: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏ 7.3 KB                         
pulling 1da0581fd4ce: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏  130 B                         
pulling f02dd72bb242: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏   59 B                         
pulling ea0a531a015b: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏  485 B                         
verifying sha256 digest 
writing manifest 
success 
ai-engineer@ollama-server-1756661287:~$ ollama ls
NAME                         ID              SIZE      MODIFIED      
qwen:0.5b                    b5dc5e784f2a    394 MB    9 seconds ago    
llama3.2:1b                  baf6a787fdff    1.3 GB    2 minutes ago    
tinyllama:latest             2644915ede35    637 MB    2 minutes ago    
duckyblender/danube3:0.5b    13292586951b    317 MB    2 minutes ago    
ai-engineer@ollama-server-1756661287:~$ date
Sun Aug 31 17:34:06 UTC 2025
ai-engineer@ollama-server-1756661287:~$ 




4 / 9

Ollama Labs

Run the pulled qwen:0.5b model on ollama-server.

Press Ctrl + D to detach from the model.

Is the qwen:0.5b model running on ollama-server?


ollama run qwen:0.5b


ai-engineer@ollama-server-1756661287:~$ ollama run qwen:0.5b
>>> Send a message (/? for help)

ai-engineer@ollama-server-1756661287:~$ ollama ps
NAME                         ID              SIZE      PROCESSOR    CONTEXT    UNTIL               
tinyllama:latest             2644915ede35    827 MB    100% CPU     4096       28 minutes from now    
duckyblender/danube3:0.5b    13292586951b    675 MB    100% CPU     4096       28 minutes from now    
qwen:0.5b                    b5dc5e784f2a    1.0 GB    100% CPU     4096       4 minutes from now     
ai-engineer@ollama-server-1756661287:~$ 





5 / 9

Ollama Labs

What is the current number of models available on the ollama-server?


ai-engineer@ollama-server-1756661287:~$ ollama ls
NAME                         ID              SIZE      MODIFIED           
qwen:0.5b                    b5dc5e784f2a    394 MB    About a minute ago    
llama3.2:1b                  baf6a787fdff    1.3 GB    3 minutes ago         
tinyllama:latest             2644915ede35    637 MB    4 minutes ago         
duckyblender/danube3:0.5b    13292586951b    317 MB    4 minutes ago         
ai-engineer@ollama-server-1756661287:~$ 




6 / 9

Ollama Labs

How many models are running on the ollama-server right now?



ai-engineer@ollama-server-1756661287:~$ ollama ps
NAME                         ID              SIZE      PROCESSOR    CONTEXT    UNTIL               
tinyllama:latest             2644915ede35    827 MB    100% CPU     4096       27 minutes from now    
duckyblender/danube3:0.5b    13292586951b    675 MB    100% CPU     4096       27 minutes from now    
qwen:0.5b                    b5dc5e784f2a    1.0 GB    100% CPU     4096       3 minutes from now     
ai-engineer@ollama-server-1756661287:~$ 




7 / 9

Ollama Labs

Stop the running tinyllama model on ollama-server.

Is the tinyllama model stopped?


ai-engineer@ollama-server-1756661287:~$ ollama stop tinyllama:latest
ai-engineer@ollama-server-1756661287:~$ ollama ps
NAME                         ID              SIZE      PROCESSOR    CONTEXT    UNTIL               
duckyblender/danube3:0.5b    13292586951b    675 MB    100% CPU     4096       26 minutes from now    
qwen:0.5b                    b5dc5e784f2a    1.0 GB    100% CPU     4096       3 minutes from now     
ai-engineer@ollama-server-1756661287:~$ date
Sun Aug 31 17:36:40 UTC 2025
ai-engineer@ollama-server-1756661287:~$ 





8 / 9

Ollama Labs

Remove the tinyllama model present on the ollama-server.

Is the tinyllama model removed from ollama-server?

ai-engineer@ollama-server-1756661287:~$ ollama ls
NAME                         ID              SIZE      MODIFIED      
qwen:0.5b                    b5dc5e784f2a    394 MB    3 minutes ago    
llama3.2:1b                  baf6a787fdff    1.3 GB    5 minutes ago    
tinyllama:latest             2644915ede35    637 MB    5 minutes ago    
duckyblender/danube3:0.5b    13292586951b    317 MB    5 minutes ago    
ai-engineer@ollama-server-1756661287:~$ ollama rm tinyllama:latest
deleted 'tinyllama:latest'
ai-engineer@ollama-server-1756661287:~$ 
ai-engineer@ollama-server-1756661287:~$ ollama ls
NAME                         ID              SIZE      MODIFIED      
qwen:0.5b                    b5dc5e784f2a    394 MB    3 minutes ago    
llama3.2:1b                  baf6a787fdff    1.3 GB    5 minutes ago    
duckyblender/danube3:0.5b    13292586951b    317 MB    5 minutes ago    
ai-engineer@ollama-server-1756661287:~$ date
Sun Aug 31 17:37:14 UTC 2025
ai-engineer@ollama-server-1756661287:~$ 



9 / 9

Ollama Labs

Stop all running models on the ollama-server.

Have all the models stopped?


ai-engineer@ollama-server-1756661287:~$ ollama stop duckyblender/danube3:0.5b
ai-engineer@ollama-server-1756661287:~$ ollama stop qwen:0.5b
ai-engineer@ollama-server-1756661287:~$ 
ai-engineer@ollama-server-1756661287:~$ ollama ps
NAME    ID    SIZE    PROCESSOR    CONTEXT    UNTIL 
ai-engineer@ollama-server-1756661287:~$ 