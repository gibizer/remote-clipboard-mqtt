A small tool to share the clipboard between multiple machines via a public
mqtt server.

The content of the clipboard is encrypted end to end. So the mqtt server 
does not see the content shared between the machines.

Usage
-----
Install and start the proxy server:
```shell script
$ git clone https://github.com/gibizer/remote-clipboard-mqtt.git
$ cd remote-clipboard-mqtt
$ pip install .
$ remote-clipboard
```

The ``remote-clipboard`` command will create a new shared clipboard and prints
the command line that you can use on another machine to join to this shared 
clipboard instance.

For more information see the builtin help:

```shell script
$ remote-clipboard --help
usage: Connect to a shared, remote clipboard.

If called without parameter then a new shared clipboard is created and 
instruction is printed to connect to it from another machine.

optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     The encryption key the clipboard uses. If not
                        provided a new is generated and printed.
  -n NAME, --name NAME  The name of the shared clipboard to join to. If
                        not provided a new shared clipboard with a
                        random name is created and printed.
  -d, --debug           Print more logs
```