INSTRUCOES DE COMPILACAO E EXECUCAO

Requisitos:
- Python 3.x
- protobuf (pip install protobuf)
- protoc (compilador Protocol Buffers)

1. Compilacao do Protocol Buffers (Parte 4):
   protoc --python_out=. calculator.proto

2. Execucao Parte 1 - UDP:
   # Servidor (defina a taxa de perda desejada):
   python3 server_udp.py --loss-rate 0.0
   python3 server_udp.py --loss-rate 0.1
   python3 server_udp.py --loss-rate 0.3

   # Cliente:
   python3 client_udp.py

3. Execucao Parte 2 - TCP Textual:
   # Servidor:
   python3 server_tcp.py

   # Cliente:
   python3 client_tcp.py

4. Execucao Parte 4 - TCP Protobuf:
   # Servidor:
   python3 server_proto.py

   # Cliente:
   python3 client_proto.py
