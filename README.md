# 🎞️ GIF to ASCII Animation Converter

A Python program to convert animated `.gif` files into animated ASCII art in the terminal.

---

## 📦 Features

- Convert GIFs to ASCII while preserving the original aspect ratio
- Two conversion modes:
  - **Standard (interactive)** — `converter.py`
  - **Multithreaded (faster)** — `converter-multithreaded.py`
- Outputs animation as:
  - A `.txt` file (`frames.txt`)
  - Plaintext copied to your clipboard
- Terminal-based ASCII animation player — `ascii_player.py`

---

## 🗂️ File Overview

| File/Folder                 | Description |
|-----------------------------|-------------|
| `converter.py`              | Standard interactive converter: select a GIF and generate ASCII frames. |
| `converter-multithreaded.py`| Faster, multithreaded version of the converter for large GIFs. |
| `ascii_player.py`           | Terminal-based player for displaying ASCII animations from `frames.txt`. |
| `frames.txt`                | Output text file containing all ASCII frames (newline-separated format). |
| `gifs/`                     | Folder containing input `.gif` files for conversion. |

---

## 🧾 How the Frames Are Stored

The converted ASCII frames are stored in a plain text file called `frames.txt`.  
Each frame is separated by **two newlines (`\n\n`)** — similar to how CSV stores comma-separated values, this file uses **newline-separated blocks**.

```txt
[ASCII frame 1]

[ASCII frame 2]

[ASCII frame 3]
...
````

This makes it easy to parse and display each frame in sequence.

---

## 🚀 Quickstart

### 1. Install dependencies

```bash
pip install pillow pyperclip
```

### 2. Add your `.gif` files to the `gifs/` folder.

### 3. Convert your GIF to ASCII

#### Option 1: Standard converter

```bash
python3 converter.py
```

#### Option 2: Faster, multithreaded converter

```bash
python3 converter-multithreaded.py
```

* The script will prompt you to select a `.gif` file from the `gifs/` folder.
* It will generate ASCII frames and:

  * Copy the entire animation to your clipboard
  * Save the output to `frames.txt`

---

### 4. Play the ASCII Animation

```bash
python3 ascii_player.py
```

* You'll be prompted to enter the **FPS** (frames per second).
* Press `<Enter>` at any time to stop the animation.
* Make sure `frames.txt` exists in the same directory.

---

## 🛠️ Configuration

You can tweak the following settings in the `.py` files:

| Variable     | Description                                                 |
| ------------ | ----------------------------------------------------------- |
| `MAX_WIDTH`  | Max width (in characters) for the ASCII output              |
| `CHAR_RATIO` | Adjusts the pixel aspect ratio (height/width of characters) |
| `PALETTE`    | The character set used, from darkest to lightest            |

---

## 📎 Example Output (ASCII Frame)

```
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;::::::;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;:,,,..,;+;::, .,.:+,,:,,,,,,,,:,,:,,,,,,,:;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;,.,,;;?%%?++;:;+*?%%%$%%?*;;;;;. ????**;;;;;,,,,,::;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;,.:*%%$$$$;,:+?%$$$$$$$$$$$$$$$*,,+$$$$$$$$$$$%%%*+:,..::;;;;;;;;;;;;;;
;;;;;;;;;;;;;..?$$$$$$$% *%;*%$$$$$$$$$$$$?:,;*%$$$$$$$$$$$$$$$$$$$?*,,.,;;;;;;;;;;;;
;;;;;;;;;;;;,.?$$$$$$$$%;:*?::;??%$$$$$?+:,+?$$$$$$$$$$$$$$$$$$$$$$$$$%+:.,;;;;;;;;;;
;;;;;;;;;;;: *$$$$$$$$$$%;:;;*+++*%%%*;,;?%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$?: ,;;;;;;;;
;;;;;;;;;;;,.%$$$$$$$$$$$$$?+;,;;;;,:;*%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$*,.;;;;;;;
;;;;;;;;;;;, *?%$$$$$$$$$$$$$$%?+++%%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%: ;;;;;;
;;;;;;;;;;,..::;:,*$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$,.;;;;;
;;;;;;;;;.,?$$$%*+.,$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%..;;;;
;;;;;;;;. %$%%%?%*.:$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%* :;;;
;:;;;;;;:.+%???+::+$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%?????:.,,,
;;;;;;;;;;,,.... :%%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%?????????+  ..
;;;;;;;;;;;;;;;;, +%%$$$$%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%????????????+ .,,
;;;;;;;;;;;;;;;;;, *%%%$%%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%????????????????+    
;;;;;;;;;;;;;;;;;;, +??%?%%$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%????????????????????%..,,,
:;;;;;;;;;;;;;;;;;;, ;????%%%$$$$$$$$$$$$$$%%%%%%%%%%?????????????????????????%: ,::,
:;;;;;;;;;;;;;;;;;;;: ,?%???%%%%%%%%%%%%%%%?????????????????????????????????%%; *$$$+
:;;;;;;;;;;;;;;;;;;;;:.:*%?????????????????????????????????????????????????%*:.*#%%%+
::;;;;;;;;;;;;;;:::,.,. .;%%????????????????????????????????????????????%%%;. ,+;::,.
;:;;;;;;;:::,... .....,,. :?%???????????????????????????????????????%%%%*;,  ......,,
;,,:,.... ....,,,,,,,,...  ,?%???????????????????????????????????%%%??+:   .,,:;+++**
.......,,,,,,.......   ......;%?????????????????????????????%%%%??+;...:+++********++
,,,,,...... .   ...,,,,:::::, +%?????%%%%%??????????%%%%%%%?**;;,.;; .+****++++++++++
..  .....,,,,,,:;;+**:,::::::..*???*+++++*?%%%%%%%%%*++++::,.::+;+*,,;;;;;;;;++++++**
.,,,,::::::,+?%$$$###%;::::::: ;%????**:,:,,,,,,,,,,,...,:: .,,:..,:;;;;;;;++********
,::::::::::,*$$$%???+:::::::,,. +???%%%%%%: ;;;;:::;;;;;;;;,,:::;;;++++++++**********
;,:::::::::,::;;:,,,,.......,,:.,???%%%%??.,++;;;;;;;;;;;;;+++++++++++++++********+++
?,,:::::::,,,........:::;++****; ???*;;;.,,;;;;;;;;;;++++++++++++++++++++++++++++++++
:::,,,....,..,::;+********++++++,,...,,:;;+;;++++++++++++++++++;+++;++++++++++++++++*
 ..,.,:;;;********+++++++++++++;;;;;;++++++++++++++++++;;;;;;;;;++++++++++++*********
+++*******+++++++++++++++++****++++++++++++++++;;;;;;;;;;;;;++++++++*****************
***++++++++++++++++************+++++;;;;;;;;;;;;;;;;+++++++******************++++++++
+++++++++++********************++;;;;;;;;;;;;++++++******************++++++++++++++++
```

---

## 📄 License

MIT License – use freely, modify proudly, and share generously.

---

## 🙏 Credits

Created by Me with help from ChatGPT ❤️

Built using:
* [`Pillow`](https://python-pillow.org/) – for image and GIF processing
* [`pyperclip`](https://pypi.org/project/pyperclip/) – for clipboard support



