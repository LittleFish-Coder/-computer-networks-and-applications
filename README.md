# COMP3331/9331 Computer Networks and Applications

## Usage

1. Run the server

```bash
python server.py <port>
```

2. Run the client

```bash
python client.py <server_port> <qname> <qtype> <timeout>
```

## Example

```bash
python server.py 12345
```

```bash
python client.py 12345 example.com. A 5
```

you can also run the bash script to test the program

1. Run the server

```bash
bash run_server.sh
```

2. Run the client

```bash
bash run_client.sh
```
