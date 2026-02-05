import os
import subprocess
import json

def get_video_info(file_path):
    """Mendeteksi codec video secara offline menggunakan ffprobe."""
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json', 
        '-show_streams', file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    for stream in data.get('streams', []):
        if stream.get('codec_type') == 'video':
            return stream.get('codec_name') # Contoh: 'hevc' atau 'h264'
    return None

def convert_to_h264(input_path, output_path):
    """Proses konversi menggunakan ffmpeg."""
    print(f"--- Memulai konversi: {os.path.basename(input_path)} ---")
    cmd = [
        'ffmpeg', '-i', input_path, 
        '-c:v', 'libx264',   # Codec tujuan H.264
        '-crf', '23',        # Kualitas (18-28, makin kecil makin bagus tapi file besar)
        '-preset', 'medium', # Kecepatan encode (ultrafast, medium, slow)
        '-c:a', 'copy',      # Audio tidak di-encode ulang (biar cepat)
        output_path,
        '-y'                 # Overwrite jika file sudah ada
    ]
    subprocess.run(cmd)

def main():
    input_dir = './input'
    output_dir = './output'

    # Pastikan folder output ada
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        
        # Filter hanya file video (bisa ditambah extensionnya)
        if filename.lower().endswith(('.mp4', '.mkv', '.mov')):
            codec = get_video_info(input_path)
            
            print(f"File: {filename} | Codec Terdeteksi: {codec}")

            if codec == 'hevc':
                output_path = os.path.join(output_dir, f"converted_{filename}")
                convert_to_h264(input_path, output_path)
                print(f"Selesai! Disimpan di: {output_path}")
            else:
                print("Skip: Bukan H.265/HEVC.")
            print("-" * 30)

if __name__ == "__main__":
    main()
