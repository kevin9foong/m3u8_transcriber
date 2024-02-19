import argparse
import subprocess

def check_filename_exists(filename):
    try:
        with open(filename, 'r') as f:
            return True
    except FileNotFoundError:
        return False

def generate_wav(link, filename):
    return subprocess.run(['ffmpeg', '-i', link, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', filename], check = True)

def run_transcription_task(model_path, wav_output_filename, output_filename):
    subprocess.run(['./main', '-m', model_path, '-f', wav_output_filename, '-otxt', '-of', output_filename])

parser = argparse.ArgumentParser(
    description='Download HLS stream and convert to wav')
parser.add_argument('-l', '--link', type=str, help='m3u8 link')
parser.add_argument('-wav', '--wav_name', type=str, help='Name of the file')
parser.add_argument('-o', '--output', type=str, help='Output transcribed file name')

args = parser.parse_args()

link = args.link
wav_output_filename = args.wav_name + '.wav'
output_filename = args.output + '.txt'

result = None

if (not check_filename_exists(wav_output_filename)):
    print('Generating wav from m3u8 link...')
    result = generate_wav(link, wav_output_filename)
    print('Wav file generated successfully')

if (not result or result.returncode == 0) and not check_filename_exists(output_filename):
    # transcribe the file
    print('Transcribing the file...')
    run_transcription_task('models/ggml-base.en.bin', wav_output_filename, output_filename)




