import socket
import threading
import struct
import calculator_pb2

def evaluate_calc(op1, op_str, op2):
    if op_str == '+': return True, op1 + op2
    elif op_str == '-': return True, op1 - op2
    elif op_str == '*': return True, op1 * op2
    elif op_str == '/':
        if op2 == 0: return False, "divisao por zero"
        return True, op1 / op2
    else: return False, f"operacao invalida: {op_str}"

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

def handle_client(conn, addr):
    print(f"[Proto Server] Conectado por {addr}")
    try:
        while True:
            data = recv_msg(conn)
            if not data:
                break

            req = calculator_pb2.CalcRequest()
            req.ParseFromString(data)

            success, res = evaluate_calc(req.operand1, req.op, req.operand2)

            resp = calculator_pb2.CalcResponse()
            resp.seq = req.seq
            resp.success = success
            if success:
                resp.result = res
            else:
                resp.error_message = str(res)

            send_msg(conn, resp.SerializeToString())
    except Exception as e:
        print(f"[Proto Server] Erro no cliente {addr}: {e}")
    finally:
        conn.close()
        print(f"[Proto Server] Conexao encerrada com {addr}")

def start_proto_server(host='127.0.0.1', port=5002):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[Proto Server] Escutando na porta {port}...")

    while True:
        conn, addr = sock.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == '__main__':
    start_proto_server()
