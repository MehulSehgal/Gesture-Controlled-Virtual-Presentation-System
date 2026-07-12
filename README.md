# Virtual Presentation Controller ✋

Control slide presentations and draw on-screen using only hand gestures, tracked live through your webcam with MediaPipe and OpenCV.

## Features

- **Draw** — hold your index finger up (keep your middle finger down) to draw on the video feed.
- **Next Slide** — swipe your hand to the right.
- **Previous Slide** — swipe your hand to the left.
- **Clear Canvas** — press `c`.
- **Quit** — press `q`.

Slide navigation is simulated via keyboard input (`pyautogui`), so it works with any presentation software that responds to the arrow keys (PowerPoint, Google Slides, Keynote, PDF viewers, etc.) — just make sure the presentation window is focused.

## Demo

![gesture-demo-placeholder](docs/demo.gif)

## Requirements

- Python 3.8+
- A webcam

## Installation

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
pip install -r requirements.txt
```

## Usage

```bash
python hand_gesture_control.py
```

Open your presentation software first, then run the script. Keep the presentation window focused so the simulated arrow-key presses reach it.

## How it works

1. **MediaPipe Hands** detects 21 hand landmarks per frame from the webcam feed.
2. **Drawing gesture**: if the index fingertip is significantly above the middle fingertip, the current position is recorded and drawn as a trail.
3. **Swipe gesture**: the wrist's horizontal position is tracked frame-to-frame. A large enough jump left or right (past `swipe_threshold`) triggers a simulated arrow-key press, with a short cooldown to prevent duplicate triggers.

## Known limitations

- Works best with one hand and good, even lighting.
- Swipe detection is based on raw pixel movement, so results depend on webcam resolution and distance from the camera — tune `swipe_threshold` in the script if it's too sensitive or not sensitive enough.
- `pyautogui` sends OS-level key presses, so it does not target a specific window — keep your presentation app focused.

## License

[MIT](LICENSE)
