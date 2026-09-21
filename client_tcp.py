import socket
import time
import random

HOST = '127.0.0.1'
PORT = 5001
N_REQUESTS = 20
OPS = ['+', '-', '*', '/']

def run_tcp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    rtts = []
    total_bytes_sent = 0
    total_bytes_recv = 0
    start_total_time = time.time()

    for seq in range(N_REQUESTS):
        op1 = round(random.uniform(1, 100), 1)
        op2 = round(random.uniform(0, 10), 1) if random.random() > 0.2 else 0
        op = random.choice(OPS)

        payload = f"CALC:{seq}:{op1}:{op}:{op2}\n"
        payload_bytes = payload.encode('utf-8')
        total_bytes_sent += len(payload_bytes)

        start_rtt = time.time()
        sock.sendall(payload_bytes)

        response_bytes = b""
        while b'\n' not in response_bytes:
            chunk = sock.recv(1024)
            if not chunk: break
            response_bytes += chunk

        end_rtt = time.time()
        total_bytes_recv += len(response_bytes)

        rtt = (end_rtt - start_rtt) * 1000
        rtts.append(rtt)

        resp = response_bytes.decode('utf-8').strip()
        print(f"[Seq {seq}] Resp: {resp} | RTT: {rtt:.2f} ms")

    total_time = time.time() - start_total_time
    sock.close()

    avg_rtt = sum(rtts) / len(rtts) if rtts else 0
    max_rtt = max(rtts) if rtts else 0
    avg_msg_size = (total_bytes_sent + total_bytes_recv) / (N_REQUESTS * 2)

    print("\n--- ESTATÍSTICAS (TCP Textual) ---")
    print(f"Tempo total: {total_time:.2f} s")
    print(f"RTT Médio: {avg_rtt:.2f} ms")
    print(f"RTT Máximo: {max_rtt:.2f} ms")
    print(f"Tamanho médio das mensagens: {avg_msg_size:.2f} bytes")

if __name__ == '__main__':
    run_tcp_client()
