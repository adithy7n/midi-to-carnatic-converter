import mido
import pygame
from tkinter import Tk, Label, Button, filedialog, Text
import threading
import time
from tkinter import PhotoImage

# MIDI to Western note mapping
midi_to_western = {
    0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"
}

# Western to Carnatic swara mapping
western_to_carnatic = {
    "C": "Sa",
    "C#": "Ri1",
    "D": "Ri2",
    "D#": "Ga1",
    "E": "Ga2",
    "F": "Ma1",
    "F#": "Ma2",
    "G": "Pa",
    "G#": "Dha1",
    "A": "Dha2",
    "A#": "Ni1",
    "B": "Ni2",
}

# Simple raga database
raga_patterns = {
    "Sa R2 G3 M1 P D2 N3": "Mohanam",
    "Sa R1 G3 M2 P D1 N2": "Kalyani",
}

def midi_note_to_western(note_number, tonic="C"):
    """Convert MIDI note number to a Western note relative to the tonic."""
    tonic_offset = list(midi_to_western.values()).index(tonic.upper())
    note_index = (note_number - tonic_offset) % 12
    return midi_to_western[note_index]

def convert_midi_to_carnatic(midi_file_path, tonic="C"):
    """Convert a MIDI file's notes to Carnatic swaras."""
    carnatic_swaras = []
    note_durations = []
    
    try:
        mid = mido.MidiFile(midi_file_path)
        ticks_per_beat = mid.ticks_per_beat  # Get ticks per beat
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    western_note = midi_note_to_western(msg.note, tonic)
                    carnatic_swara = western_to_carnatic.get(western_note, f"Unknown({western_note})")
                    carnatic_swaras.append(carnatic_swara)
                    note_durations.append(msg.time / ticks_per_beat)  # Duration in beats
    except Exception as e:
        raise RuntimeError(f"Error processing MIDI file: {e}")
    
    return carnatic_swaras, note_durations

def identify_raga(swaras):
    """Identify the raga based on a simple database."""
    swara_sequence = " ".join(swaras)
    for pattern, raga in raga_patterns.items():
        if pattern in swara_sequence:
            return raga
    return "Unknown"

def save_output_to_file(swaras, durations, raga):
    """Save output to a text file with a file dialog.""" 
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write("Carnatic Swaras:\n")
            f.write(" ".join(swaras) + "\n\n")
            f.write("Note Durations:\n")
            f.write(" ".join(map(str, durations)) + "\n\n")
            f.write(f"Identified Raga: {raga}\n")
        print(f"Output saved to {file_path}")
    else:
        print("File save cancelled.")

def play_midi(midi_file_path, pause_flag, stop_flag, root, ticks_per_beat):
    """Play the MIDI file with pause, stop functionality."""
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(midi_file_path)
    pygame.mixer.music.play()

    def update_playback():
        """Update playback control (pause, stop) while the music is playing."""
        if pygame.mixer.music.get_busy() and not stop_flag[0]:
            if not pause_flag[0]:
                threading.Timer(0.1, update_playback).start()  # Keeps updating every 100ms
        else:
            pygame.mixer.music.stop()  # Stop music if paused or stopped

    update_playback()

# GUI for the converter
def gui():
    pause_flag = [False]
    stop_flag = [False]
    swaras, durations, raga = [], [], []
    ticks_per_beat = 1

    # Dark Mode Toggle Flag
    dark_mode = [False]

    def toggle_dark_mode():
        """Toggle dark mode for the application."""
        if dark_mode[0]:
            root.config(bg="white")
            output_text.config(bg="white", fg="black")
            for widget in root.winfo_children():
                widget.config(bg="white", fg="black")
            dark_mode[0] = False
        else:
            root.config(bg="#2e2e2e")
            output_text.config(bg="#333333", fg="white")
            for widget in root.winfo_children():
                widget.config(bg="#333333", fg="white")
            dark_mode[0] = True

    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid *.midi")])
        if file_path:
            label_file_path.config(text=file_path)
            process_midi(file_path)

    def process_midi(file_path):
        nonlocal swaras, durations, raga, ticks_per_beat
        try:
            tonic = entry_tonic.get("1.0", "end-1c").strip().upper()
            if tonic not in midi_to_western.values():
                output_text.insert("end", "Error: Invalid tonic. Please enter a valid note (e.g., C, D#).\n")
                return

            swaras, durations = convert_midi_to_carnatic(file_path, tonic)
            ticks_per_beat = mido.MidiFile(file_path).ticks_per_beat  # Get ticks per beat from MIDI file
            if not swaras:
                output_text.insert("end", "Error: No valid notes found in the MIDI file.\n")
                return

            raga = identify_raga(swaras)
            output_text.delete("1.0", "end")
            output_text.insert("end", "Carnatic Swaras:\n" + " ".join(swaras) + "\n\n")
            output_text.insert("end", "Note Durations:\n" + " ".join(map(str, durations)) + "\n\n")
            output_text.insert("end", f"Identified Raga: {raga}\n")

            # Play MIDI in a separate thread to avoid freezing the GUI
            threading.Thread(target=play_midi, args=(file_path, pause_flag, stop_flag, root, ticks_per_beat), daemon=True).start()

        except Exception as e:
            output_text.insert("end", f"Error: {e}\n")

    def play_selected_file():
        """Play the selected MIDI file."""
        file_path = label_file_path.cget("text")
        if file_path and file_path != "No file selected":
            try:
                play_midi(file_path, pause_flag, stop_flag, root, ticks_per_beat)
            except Exception as e:
                output_text.insert("end", f"Error: {e}\n")
        else:
            output_text.insert("end", "Error: No file selected for playback.\n")

    def pause_playback():
        """Pause the MIDI playback."""
        pause_flag[0] = True
        pygame.mixer.music.pause()

    def resume_playback():
        """Resume the MIDI playback."""
        pause_flag[0] = False
        pygame.mixer.music.unpause()

    def stop_playback():
        """Stop the MIDI playback."""
        stop_flag[0] = True
        pygame.mixer.music.stop()

    root = Tk()
    root.title("MIDI to Carnatic Converter")

    # Dark Mode Toggle Button
    Button(root, text="Toggle Dark Mode", command=toggle_dark_mode).pack(pady=10)

    Label(root, text="Select MIDI File:").pack()
    Button(root, text="Browse", command=select_file).pack()

    label_file_path = Label(root, text="No file selected")
    label_file_path.pack()

    Label(root, text="Enter Tonic (Default: C):").pack()
    entry_tonic = Text(root, height=1, width=10)
    entry_tonic.insert("end", "C")
    entry_tonic.pack()

    output_text = Text(root, height=10, width=80)
    output_text.pack()

    Button(root, text="Play MIDI", command=play_selected_file, bg="#3A3A3A", fg="white").pack(pady=5)
    Button(root, text="Pause", command=pause_playback, bg="#3A3A3A", fg="white").pack(pady=5)
    Button(root, text="Resume", command=resume_playback, bg="#3A3A3A", fg="white").pack(pady=5)
    Button(root, text="Stop", command=stop_playback, bg="#3A3A3A", fg="white").pack(pady=5)

    Button(root, text="Save Output", command=lambda: save_output_to_file(swaras, durations, raga), bg="#3A3A3A", fg="white").pack(pady=5)
    Button(root, text="Close", command=root.quit, bg="#3A3A3A", fg="white").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    try:
        gui()
    except Exception as e:
        print(f"Error: {e}")
