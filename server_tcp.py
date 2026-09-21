import socket
import threading

def evaluate_calc(op1, op_str, op2):
    try:
        val1, val2 = float(op1), float(op2)
        if op_str == '+': return True, val1 + val2
        elif op_str == '-': return True, val1 - val2
        elif op_str == '*': return True, val1 * val2
        elif op_str == '/':
            if val2 == 0: return False, "divisao por zero"
            return True, val1 / val2
        else: return False, f"operacao invalida: {op_str}"
    except ValueError:
        return False, "operandos invalidos"

def handle_client(conn, addr):
    print(f"[TCP Server] Cliente conectado: {addr}")
    buffer = ""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8')
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':')
                if len(parts) == 5 and parts[0] == 'CALC':
                    _, seq, op1, op, op2 = parts
                    success, res = evaluate_calc(op1, op, op2)
                    resp = f"RESULT:{seq}:{res}\n" if success else f"ERROR:{seq}:{res}\n"
                    conn.sendall(resp.encode('utf-8'))
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print(f"[TCP Server] Conexão encerrada: {addr}")

def start_tcp_server(host='127.0.0.1', port=5001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[TCP Server] Escutando em {host}:{port}")

    while True:
        conn, addr = sock.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    start_tcp_server()
