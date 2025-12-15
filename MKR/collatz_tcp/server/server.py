import os
import socket
from typing import Dict

HOST = "0.0.0.0"
PORT = int(os.getenv("SERVER_PORT", "9000"))

def collatz_steps(n: int, cache: Dict[int, int]) -> int:
    original = n
    steps = 0
    path = []

    while n != 1 and n not in cache:
        path.append(n)
        if n & 1:
            n = 3 * n + 1
        else:
            n //= 2
        steps += 1

    tail = cache.get(n, 0)
    total_steps = steps + tail

    for x in reversed(path):
        cache[x] = total_steps
        total_steps -= 1

    return cache.get(original, steps + tail)

def compute_average_steps(N: int) -> float:
    cache = {1: 0}
    total = 0
    for i in range(1, N + 1):
        total += collatz_steps(i, cache)
    return total / N

def recv_line(conn: socket.socket, max_bytes: int = 1024) -> str:
    data = b""
    while b"\n" not in data and len(data) < max_bytes:
        chunk = conn.recv(64)
        if not chunk:
            break
        data += chunk
    return data.decode("utf-8", errors="replace").strip()

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[server] Listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print(f"[server] Client connected: {addr}")
            line = recv_line(conn)

            try:
                N = int(line)
                if N <= 0:
                    raise ValueError("N must be positive")
            except Exception:
                msg = "ERROR: expected positive integer N\n"
                conn.sendall(msg.encode("utf-8"))
                print("[server] Invalid input:", repr(line))
                return

            avg = compute_average_steps(N)
            response = f"{avg}\n"
            conn.sendall(response.encode("utf-8"))
            print(f"[server] Sent average steps for N={N}: {avg}")

        print("[server] Connection closed. Server stops (single client).")

if __name__ == "__main__":
    main()
