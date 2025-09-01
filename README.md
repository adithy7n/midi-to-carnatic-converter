
# 🎶 MIDI to Carnatic Converter  

Ever played around with a MIDI file and wondered what it would sound like if expressed in **Carnatic swaras** instead of plain Western notes?  
That’s exactly what this project does.  

It’s a Python-powered desktop app that takes a **MIDI sequence**, translates it into **Carnatic notation (Sa, Ri, Ga, Ma… etc.)**, optionally guesses a **matching raga**, and even lets you **play the file back** with controls like pause, resume, and stop — all wrapped up in a clean Tkinter GUI with dark mode support.  

Think of it as a mini translator between **Western digital music** and **South Indian classical tradition**.  

---

## ✨ What You Can Do With It  
- 🔄 **Convert MIDI → Carnatic Swaras**  
- 🎼 **Identify a Raga (basic matching)**  
- ▶️ **Play your MIDI file with controls** (play, pause, resume, stop)  
- 🌗 **Toggle Dark Mode** because code deserves aesthetics too  
- 💾 **Export results** (swaras, durations, and identified raga) into a `.txt` file  
- 🎹 **Choose your tonic (root note)** so you’re not stuck in just “C”  

---

## 📂 How It’s Built  

The project glues together a few moving parts:  

- **MIDI Parsing** → using [`mido`](https://mido.readthedocs.io/)  

- **Note Mapping** → converts Western notes into Carnatic swaras with a lookup table 

- **Duration Tracking** → captures note lengths relative to MIDI ticks  

- **Raga Recognition** → compares sequences to a tiny built-in database (Mohanam, Kalyani, etc.) 

- **Audio Engine** → playback handled by `pygame`  

- **Interface** → Tkinter GUI with file picker, tonic input, playback buttons, and dark mode toggle  

All in pure Python, no external DAWs or plugins required.  

---

## 🚀 Getting Started  

Clone the repo:  
```bash
git clone https://github.com/your-username/midi-to-carnatic-converter.git
cd midi-to-carnatic-converter
````

Install dependencies:

```bash
pip install mido pygame
```

Run the app:

```bash
python converter.py
```

---

## 🖥️ Usage

1. Launch the program.
2. Use the **Browse** button to pick a `.midi` or `.mid` file.
3. Enter your **tonic (root note)** — defaults to C.
4. Click **Play MIDI** to listen, or use **Pause / Resume / Stop** for control.
5. Toggle **Dark Mode** if you’re a night owl 🌙.
6. Save results with **Export Output** → gives you a `.txt` file with swaras, durations, and the identified raga.

---

## 📝 Example Output

Carnatic Swaras:
Ga1 Ga1 Ma2 Ni1 Ni1 Ri1 Ri1 Ma1 Dha1 Ni1 Ni1 Ga1 Ma2 Dha1 Ni1 Dha1 Dha1 Ri1 Ma1 Ga1 Ga1 Ga1 Ma2 Ni1 Ni1 Ri1 Ri1 Ma1 Dha1 Ma2 Ma1 Ga1 Ni1 Ga1 Ma2 Dha1 Ni1 Ma1 Dha1 Ri1 Ga1 Ri1

Note Durations:
0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 4.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.75

```
---

## 📂 Project Structure

```
midi-to-carnatic-converter/
│── converter.py       # Main application (GUI + logic)
│── README.md          # Project documentation
│── requirements.txt   # Dependencies
```

---

## 🤝 Contributing

Contributions are welcome!

* Add more **ragas** to the recognition database
* Improve **note duration tracking**
* Polish the **UI/UX**
* Or just open an issue if something breaks 🎵

---

## 📜 License

This project is licensed under the MIT License.
Feel free to use, modify, and share — just keep the credits intact.

---

## 💡 Inspiration

This project started out as a fun experiment:

> “What if we could take a digital MIDI file and hear it through the lens of Carnatic music theory?”

It’s for:

* Students learning Carnatic theory
* Musicians curious about mapping MIDI to swaras
* Coders who just like hacking on music projects

---

```

✅ Now everything (including **Inspiration**) is in one copy block — you can drop this directly into your `README.md`.  

Do you also want me to generate a **`requirements.txt`** file so people can install everything with a single `pip install -r requirements.txt`?
```
