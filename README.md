
#  IN-PROGRESSISH | USE AT RISK | LIMITED ERROR HANDLING | REQUIRES MACOS


An extension to remotely manipulate iterm2 sessions. 

<br>

<video controls>
  <source src="assets/iterm2-remote-example-video.mp4" type="video/mp4">
</video>
(the delay is what I am trying to fix right now)

---
### How to use (currently)  

To run server
```
python -m server.server
```  
To create new terminal session:
```

python -m client spawn --name <name> [--focus] [--shell <shell>] [--command <cmd>]

python -m client spawn -h (for help)

<name> → required, the name of the terminal session
[--focus | -f] → optional, keep focus on the new terminal
[--shell <shell>] → optional, specify shell (default zsh)
[--command <cmd>] → optional, run a command after launch

``` 

To send a command or text to an existing terminal session:
```
python -m client send (--name <name> | --id <id>) (--command <cmd> | --text <text>)

python -m client send -h (for help)

--name <name> → send to a session by name
--id <id> → send to a session by ID (not recommended nor implemented properly)
--command <cmd> → send a command to execute
--text <text> → send raw text
| = mutually exclusive option
```