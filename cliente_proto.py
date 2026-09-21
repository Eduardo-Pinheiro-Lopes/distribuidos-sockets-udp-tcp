import socket
import time
import random
import struct
import calculator_pb2

HOST = '127.0.0.1'
PORT = 5002
N_REQUESTS = 20
OPS = ['+', '-', '*', '/']

def recv_all(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)

def recv_msg(sock):
    raw_len = recv_all(sock, 4)
    if not raw_len:
        return None
    msg_len = struct.unpack('>I', raw_len)[0]
    return recv_all(sock, msg_len)

def send_msg(sock, msg_bytes):
    length_prefix = struct.pack('>I', len(msg_bytes))
    sock.sendall(length_prefix + msg_bytes)

def run_proto_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    rtts = []
    total_bytes = 0
    start_total_time = time.time()

    for seq in range(N_REQUESTS):
        req = calculator_pb2.CalcRequest()
        req.seq = seq
        req.operand1 = round(random.uniform(1, 100), 1)
        req.operand2 = round(random.uniform(0, 10), 1) if random.random() > 0.2 else 0.0
        req.op = random.choice(OPS)

        serialized_req = req.SerializeToString()
        total_bytes += len(serialized_req)

        start_rtt = time.time()
        send_msg(sock, serialized_req)

        resp_bytes = recv_msg(sock)
        rtt = (time.time() - start_rtt) * 1000

        if resp_bytes:
            total_bytes += len(resp_bytes)
            resp = calculator_pb2.CalcResponse()
            resp.ParseFromString(resp_bytes)
            rtts.append(rtt)
            status = f"RESULT: {resp.result}" if resp.success else f"ERROR: {resp.error_message}"
            print(f"[Seq {seq}] Resp: {status} | RTT: {rtt:.2f} ms")

    total_time = time.time() - start_total_time
    sock.close()

    avg_rtt = sum(rtts) / len(rtts) if rtts else 0
    max_rtt = max(rtts) if rtts else 0
    avg_msg_size = total_bytes / (N_REQUESTS * 2)

    print("\n--- ESTATÍSTICAS (TCP Protobuf) ---")
    print(f"Tempo total: {total_time:.2f} s")
    print(f"RTT Médio: {avg_rtt:.2f} ms | RTT Máximo: {max_rtt:.2f} ms")
    print(f"Tamanho médio da mensagem: {avg_msg_size:.2f} bytes")

if __name__ == '__main__':
    run_proto_client()
