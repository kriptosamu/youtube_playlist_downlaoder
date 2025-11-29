import os
import yt_dlp
import sys
from pathlib import Path

class YouTubePlaylistDownloader:
    def __init__(self):
        self.qualita_audio = {
            '1': '128',
            '2': '192', 
            '3': '256',
            '4': '320'
        }
    
    def scarica_playlist_mp3(self, url_playlist, cartella_output, qualita='192'):
        """
        Scarica l'intera playlist YouTube e CONVERTE in MP3
        """
        
        Path(cartella_output).mkdir(parents=True, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            
            'outtmpl': os.path.join(cartella_output, '%(title)s.%(ext)s'),
            
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',           
                    'preferredquality': qualita,       
                },
                {
                    'key': 'FFmpegMetadata',           
                    'add_metadata': True,
                }
            ],
            
            'postprocessor_args': [
                '-acodec', 'libmp3lame',             
                '-b:a', f'{qualita}k',      
            ],
            
            'writethumbnail': False,      
            'embedthumbnail': False,
            'ignoreerrors': True,       
            'no_warnings': False,
            'quiet': False,
            'nooverwrites': True,
            
            'progress_hooks': [self.progress_hook],
        }
        
        try:
            print("🎵 Analizzo la playlist...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_playlist, download=False)
                
                if 'entries' in info:
                    playlist_title = info.get('title', 'Sconosciuta')
                    num_tracce = len([e for e in info['entries'] if e is not None])
                    
                    print(f"📋 Playlist: {playlist_title}")
                    print(f"🎶 Tracce trovate: {num_tracce}")
                    print(f"📁 Salvataggio in: {os.path.abspath(cartella_output)}")
                    print(f"🎧 Formato: MP3 ({qualita} kbps)")
                    print("=" * 50)
                    
                    conferma = input("Vuoi procedere con il download? (s/n): ").lower()
                    if conferma != 's':
                        print("❌ Download annullato.")
                        return
                
                print("🚀 Avvio download e conversione MP3...")
                ydl.download([url_playlist])
                
                print("\n" + "=" * 50)
                print("✅ DOWNLOAD COMPLETATO!")
                print(f"📀 Tutti i file sono stati convertiti in MP3")
                print(f"💾 Cartella: {os.path.abspath(cartella_output)}")
                print("🎧 Pronto per la meditazione! 🧘‍♀️")
                
        except Exception as e:
            print(f"❌ Errore durante il download: {str(e)}")
            if "FFmpeg" in str(e):
                print("💡 Assicurati che FFmpeg sia installato correttamente")

    def progress_hook(self, d):
        """Mostra il progresso del download e conversione"""
        if d['status'] == 'downloading':
            filename = os.path.basename(d.get('filename', 'N/A'))
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'N/A')
            print(f"\r⬇️  Scaricando: {percent} | Velocità: {speed} | {filename[:30]}...", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\r✅ Completato: {os.path.basename(d['filename'])}")
        elif d['status'] == 'postprocessing':
            print(f"\r🔄 Convertendo in MP3...", end='', flush=True)

def verifica_dipendenze():
    """Verifica che le dipendenze siano installate"""
    try:
        import yt_dlp
        return True
    except ImportError:
        print("❌ yt-dlp non installato!")
        print("💡 Installa con: pip install yt-dlp")
        return False

def verifica_ffmpeg():
    """Verifica che FFmpeg sia disponibile"""
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    """Funzione principale"""
    print("🎧" + "=" * 50)
    print("           DOWNLOADER PLAYLIST YOUTUBE MP3")
    print("                 PER MEDITAZIONE")
    print("=" * 50)
    
    if not verifica_dipendenze():
        sys.exit(1)
    
    if not verifica_ffmpeg():
        print("⚠️  FFmpeg non trovato. La conversione MP3 potrebbe non funzionare.")
        print("💡 Installa FFmpeg:")
        print("   Windows: https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
        print()
    
    downloader = YouTubePlaylistDownloader()
    
    while True:
        url = input("🔗 Incolla l'URL della playlist YouTube: ").strip()
        if url:
            break
        print("❌ Inserisci un URL valido")
    
    cartella = input("📁 Cartella di output [meditazione_mp3]: ").strip()
    if not cartella:
        cartella = "meditazione_mp3"
    
    print("\n🎚️  Seleziona qualità MP3:")
    print("1 - 128 kbps (dimensione ridotta)")
    print("2 - 192 kbps (buon bilanciamento) ★")
    print("3 - 256 kbps (alta qualità)")
    print("4 - 320 kbps (qualità massima)")
    
    scelta_qualita = input("Scelta [2]: ").strip()
    qualita = downloader.qualita_audio.get(scelta_qualita, '192')
    
    print("\n⚙️  RIEPILOGO IMPOSTAZIONI:")
    print(f"   📋 Playlist: {url[:50]}...")
    print(f"   📁 Cartella: {cartella}")
    print(f"   🎧 Formato: MP3 {qualita} kbps")
    print("=" * 50)
    
    downloader.scarica_playlist_mp3(url, cartella, qualita)

if __name__ == "__main__":
    main()