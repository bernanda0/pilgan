import json
import os
import socket
import random
from dotenv import load_dotenv

load_dotenv()

def load_questions(filename):
    with open(filename, 'r') as f:
        questions = json.load(f)
    return questions

questions = load_questions('questions.json')

# Fungsi untuk memilih 10 soal secara acak
def select_random_questions(questions, n=10):
    return random.sample(questions, n)

# Fungsi untuk menjalankan server kuis
def run_quiz_server():
    host = '0.0.0.0'
    
    # Ambil port dari environment variable, default ke 12345 jika tidak ada
    port = 6969
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"Server listening on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        score = 0
        total_questions = 2
        
        # Pilih 10 soal acak
        random_questions = select_random_questions(questions, total_questions)

        # Simpan jawaban pengguna (ID soal dan status benar/salah)
        user_results = []

        for idx, q in enumerate(random_questions):
            attempts = 0  # Inisialisasi percobaan untuk tiap soal
            
            while attempts < 2:  # Memberikan maksimal 2 percobaan
                question_text = f"Q{q['id']}: {q['question']}\n"
                options_text = "\n".join(q["options"])
                full_text = question_text + options_text + f"\n\nPercobaan {attempts + 1} dari 2\nKetikkan jawaban Anda (A, B, C, atau D):\n"
                client_socket.send(full_text.encode())
                
                # Terima jawaban dari client
                answer = client_socket.recv(1024).decode().strip().upper()

                # Verifikasi jawaban
                if answer == q["answer"]:
                    feedback = "Benar!\n\n"
                    client_socket.send(feedback.encode())
                    score += 1
                    user_results.append((q['id'], "✅ Correct!"))  # Simpan status benar
                    break  # Jika benar, lanjut ke soal berikutnya
                else:
                    attempts += 1
                    if attempts < 2:
                        feedback = "Salah! Silakan coba lagi.\n\n"
                    else:
                        feedback = "Salah! Anda telah menggunakan semua percobaan.\n\n"
                        user_results.append((q['id'], "❌ Wrong"))  # Simpan status salah
                    client_socket.send(feedback.encode())
        
        # Akhiri dengan hasil akhir
        percentage_score = (score / total_questions) * 100
        
        # Tampilkan hasil skor dalam bentuk persentase
        result = f"Skor Anda: {percentage_score:.2f}%\n"
        client_socket.send(result.encode())

        # Tampilkan rekap soal yang sudah dijawab dengan status (benar/salah)
        client_socket.send(b"--------------------\n")
        for q_id, status in user_results:
            result = f"ID {q_id}: {status}\n"
            client_socket.send(result.encode())
        
        client_socket.send(b"--------------------\n")

        bendera = os.getenv('FLAG')
        client_socket.send(f"Berikut bendera sebagai hadiah : {bendera}".encode())

        # Tutup koneksi setelah kuis selesai
        client_socket.close()

# Jalankan server
if __name__ == "__main__":
    run_quiz_server()
