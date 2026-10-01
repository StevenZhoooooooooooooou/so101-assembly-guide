# SO-101 Assembly and LeRobot Setup Guide

This guide was created by Aleks Santari, Yinzhe Zhou, Xinyi Yin, and Professor Krishna Murthy Jatavallabhula for **Hands-on Robot Learning** (EN.601.498 / EN.601.698) at Johns Hopkins University in Fall 2026. It covers assembling an SO-101 Leader and Follower from parts and bringing the two arms into teleoperation.

## 1. Before you start

### 1.1 Parts and tools

- Per arm: six servos of the specified models, one bus controller, three-pin servo cables, a USB data cable, a separate power supply matched to the servos, printed base and links, servo horns, and fasteners.
- Tools: drivers for M2 and M3 screws, a tool for removing print supports, and labels. Remove supports and clear the holes before assembly.

![Kit overview with black Leader printed parts, white Follower printed parts, servo boxes, controllers, cables, and clamps](images/parts-overview.jpg)

The black and white bags in the photo are labeled Leader and Follower printed parts. Servo boxes, two controllers, cables, mounting clamps, and a small fastener bag are also visible.

| Position | LeRobot motor name | Follower servo in this kit | Leader servo in this kit |
| --- | --- | --- | --- |
| J1 Base rotation | `shoulder_pan` | C047, 12 V, 1:345 | C044, 7.4 V, 1:191 |
| J2 Shoulder lift | `shoulder_lift` | C047, 12 V, 1:345 | C001, 7.4 V, 1:345 |
| J3 Elbow flex | `elbow_flex` | C047, 12 V, 1:345 | C044, 7.4 V, 1:191 |
| J4 Wrist flex | `wrist_flex` | C047, 12 V, 1:345 | C046, 7.4 V, 1:147 |
| J5 Wrist roll | `wrist_roll` | C047, 12 V, 1:345 | C046, 7.4 V, 1:147 |
| J6 Gripper or trigger | `gripper` | C047, 12 V, 1:345 | C046, 7.4 V, 1:147 |

All six Follower servos are the same model, `ST-3215-C047`. Label them `1`–`6` yourself. The Leader servo boxes are already numbered; see the table for their models. Gear ratios follow the [Hugging Face SO-101 guide](https://huggingface.co/docs/lerobot/main/en/so101) and [Seeed Studio SO-ARM10x Wiki](https://wiki.seeedstudio.com/lerobot_so100m_new/).

![Six C047 12 V Follower servo boxes marked F](images/follower-servos-c047.jpg)

![Six Leader servo boxes numbered 1 through 6 with their model codes](images/leader-servos-numbered.jpg)

### 1.2 Power supplies for this kit

**Connect 5 V to the Leader and 12 V to the Follower.**

![5 V 3 A supply label for the Leader](images/leader-5v-supply.jpg)

![12 V 2 A supply label for the Follower](images/follower-12v-supply.jpg)

### 1.3 Build order and photo list

Order: install software → find ports → configure each servo ID and baud rate → clean printed parts → J1 → J2 → J3 → J4 → J5 → J6 → wiring → mount and focus the camera → calibration → teleoperation.

## 2. Install LeRobot (Linux, Windows, macOS)

These instructions use a Miniforge Conda environment, Python 3.12, and a LeRobot source install. Install [Git](https://git-scm.com/downloads) and [Miniforge](https://conda-forge.org/download/) first, then open a new terminal. On Windows, use Miniforge Prompt or a PowerShell session initialized for Conda. On Linux and macOS, use a terminal. If `conda activate` says initialization is needed, run `conda init` as directed and reopen the terminal. If you already have a working `lerobot` environment, try Section 2.4 before reinstalling. If a `lerobot` source directory already exists in your current directory, skip `git clone` and enter the existing directory.

### 2.1 Linux

```bash
conda create -y -n lerobot python=3.12
conda activate lerobot
git clone https://github.com/huggingface/lerobot.git
cd lerobot
python -m pip install -e ".[core_scripts,feetech]"
```

On Ubuntu or Debian, if opening the serial port fails with `Permission denied`, check the device's group, add your account to it, and log in again. A common group name is `dialout`:

```bash
ls -l /dev/ttyACM*
sudo usermod -aG dialout "$USER"
```

For WSL, the LeRobot installation guide also requires `evdev`; after activating the environment, run `conda install evdev -c conda-forge`. The USB controller must be visible inside WSL. If it appears only as a Windows COM port, use the native Windows route to complete the build. `/dev/ttyACM0` and `/dev/ttyACM1` are example Linux ports, not fixed names.

### 2.2 macOS

```bash
conda create -y -n lerobot python=3.12
conda activate lerobot
git clone https://github.com/huggingface/lerobot.git
cd lerobot
python -m pip install -e ".[core_scripts,feetech]"
```

macOS ports often look like `/dev/cu.usbmodem...` or `/dev/tty.usbmodem...`. If you already have a local LeRobot checkout, run the install command inside that checkout instead of cloning it again. This workspace also contains a [Mac-specific quick-start](SO101_使用说明.md) using a local `so101.sh` wrapper; readers on other machines should use the standard CLI commands below.

### 2.3 Windows (native PowerShell or Miniforge Prompt)

Choose the Windows installer from the [Miniforge download page](https://conda-forge.org/download/). Open Miniforge Prompt and make sure `git --version` works:

```powershell
conda create -y -n lerobot python=3.12
conda activate lerobot
git clone https://github.com/huggingface/lerobot.git
cd lerobot
python -m pip install -e ".[core_scripts,feetech]"
```

Find the controller's COM number in Device Manager under **Ports (COM & LPT)**, such as `COM3` or `COM4`. Windows commands later in this guide are single-line PowerShell commands; Bash's `\` line continuation does not work in PowerShell. The official installation page covers Windows environment activation. The Windows hardware connection flow still needs testing on the target PC.

### 2.4 Verify the installation on any platform

Activate the environment with `conda activate lerobot` in each new terminal. From the source directory, run:

```text
python -c "import lerobot; import scservo_sdk; print('LeRobot and Feetech OK')"
python -c "import shutil; names=('lerobot-find-port','lerobot-setup-motors','lerobot-calibrate','lerobot-teleoperate'); print({name: shutil.which(name) for name in names}); assert all(shutil.which(name) for name in names)"
lerobot-setup-motors --help
lerobot-calibrate --help
```

`lerobot-find-port` has no help option; run it only with a controller connected when you are ready to unplug and reconnect USB as prompted. If the SDK import fails, check the environment with `python -m pip show feetech-servo-sdk` and inspect the install error. Video recording is outside this build stage. When you need recording, you can first run `conda install ffmpeg -c conda-forge` in the environment, then check the platform requirements for FFmpeg/TorchCodec in the [LeRobot installation guide](https://huggingface.co/docs/lerobot/main/en/installation). That guide also lists system packages for install failures.

## 3. Find ports and configure servos

### 3.1 Identify the controller and connect its power lead

The first photo shows a controller, USB data cable, and an adapter lead with a DC socket at one end and bare red/black wires at the other. With power disconnected, check the board's polarity markings, connect the **red wire to positive and black wire to negative**, and tighten the green terminal screws. Do not infer polarity solely from which wire appears above the other in a photo. Plug the correct 5 V or 12 V supply into the DC socket; connect USB-C to the board and the other end to the computer. Before connecting the servo bus, check that exposed wire strands cannot touch each other.

**1. Prepare the controller, USB data cable, and DC socket to red-black wire lead.**

![Controller, USB data cable, and DC socket to red-black wire lead](images/controller-kit.jpg)

**2. Loosen the screw above the terminal opening.**

![Loosening the green terminal screw before wiring](images/controller-terminal-before-wiring.jpg)

**3. Insert the positive and negative power wires: black on the outside, red on the inside.**

![Rear view showing how to insert the red and black power wires](images/controller-back-polarity.jpg)

**4. Check how the wires look after insertion.**

![Red and black supply wires seated in the controller's green terminal](images/controller-power-wires.jpg)

**5. Tighten the screw above the terminal opening.**

![Tightening the controller power-terminal screws](images/controller-terminal-screws.jpg)

**6. Connect the matching power supply and the USB-C data cable: 5 V for the Leader, 12 V for the Follower.**

### 3.2 Identify Leader and Follower ports

Connect each controller to a power supply matched to its servos and to USB. Run:

```text
lerobot-find-port
```

When prompted, briefly unplug the **controller's USB cable**, record the identified port, and plug it back in. Record `FOLLOWER_PORT` and `LEADER_PORT` separately. Common port formats: Linux `/dev/ttyACM0`, macOS `/dev/cu.usbmodem...`, Windows `COM3`.

### 3.3 Set each servo's ID and baud rate

New servos often share the same default ID. During setup, connect the controller to USB, the red-black power lead, and **only one servo at a time**, with no other servo daisy-chained to it. After connecting the servo, make sure the controller's red indicator **stays on continuously**; if it flickers, check that the power supply is connected correctly. Run the setup process once for each arm. The program will ask for each motor by name and write its ID and communication settings. An already configured arm does not need this step again.

![One servo connected to the controller by a three-pin lead, with USB and a red-black power lead attached](images/onedrive-IMG_6527.jpg)

Linux/macOS:

```bash
lerobot-setup-motors --robot.type=so101_follower --robot.port=/dev/ttyACM0
lerobot-setup-motors --teleop.type=so101_leader --teleop.port=/dev/ttyACM1
```

Windows PowerShell:

```powershell
lerobot-setup-motors --robot.type=so101_follower --robot.port=COM3
lerobot-setup-motors --teleop.type=so101_leader --teleop.port=COM4
```

Replace the ports above with your actual ports, and connect each motor as named on screen. After assigning the motor IDs, mark each motor clearly; every motor has a designated position on the arm. If the order gets mixed up, check each motor's ID again and relabel it.

## 4. Mechanical assembly

The following sections cover joints J1–J6. We strongly recommend following these steps alongside the [Hugging Face SO-101 assembly guide](https://huggingface.co/docs/lerobot/main/en/so101).

**Joints J1–J5 are assembled the same way on the Leader and Follower.** Before each step, choose the motor labeled for that position. `L` means Leader; `F` means Follower.

| Position | Follower motor | Leader motor |
| --- | --- | --- |
| J1 Base rotation | `F1` | `L1` |
| J2 Shoulder lift | `F2` | `L2` |
| J3 Elbow flex | `F3` | `L3` |
| J4 Wrist flex | `F4` | `L4` |
| J5 Wrist roll | `F5` | `L5` |

Each servo comes with two metal horns. The photo shows the output shaft and both horns so you can identify them before assembling the joints.

![Leader servo output shaft with two round metal horns](images/onedrive-IMG_6529.jpg)

Each servo also comes with three types of screws. The next photo shows the two horns and the three groups of screws; use the fasteners specified for each joint.

![Two metal servo horns and three screw types supplied with each servo](images/servo-horns-and-three-screw-types-cw90.jpg)

#### Installing the two servo horns

1. Align the splined horn with the motor's gold output spline. Press it on with the raised hub facing the motor.

   ![Splined horn fitted to the motor's gold output spline](images/servo-splined-horn-installed.jpg)

2. Insert the other horn into the black mounting hole at the opposite end of the motor, again with its raised hub facing the motor.

   ![Other horn beside the black mounting hole at the opposite end of the motor](images/servo-rear-horn-before-install.jpg)

3. Secure the horn at the opposite end with the separate pointed screw.

   ![Side view of the opposite horn secured with the pointed screw](images/servo-rear-horn-pointed-screw.jpg)

#### Cable routing and part orientation

Except at J5, you can connect each motor's cables before inserting the motor into its printed part. **The two ports on each motor are interchangeable; either one can take the incoming cable.** Use the other port when daisy-chaining to the next motor. As you test-fit the printed connectors, keep their cable holes roughly on the same side of the arm so the cables have a smooth path. Use the hole positions to check each connector's orientation. For J5, follow its separate steps: insert the motor into its printed part, connect cables to both ports, and then attach the assembly to the arm.

### J1 Base rotation / Shoulder Pan

1. Prepare the pictured base parts and motor `F1` (Follower) or `L1` (Leader).

   ![J1 base parts and the matching motor labeled 1](images/onedrive-IMG_6533.jpg)

2. Insert the motor into its position in the base part, oriented as shown.

   ![Inserting the J1 motor into the base part in the specified orientation](images/onedrive-IMG_6532.jpg)

3. Use the small screws to fasten the printed part to the motor from underneath the base.

   ![Fastening the J1 motor to the printed part from underneath with a small screw](images/onedrive-IMG_6534.jpg)

4. Continue fastening the other side with the small screws, checking that the motor sits flush against the printed part.

   ![Tightening a small screw on the other side of the J1 motor](images/onedrive-IMG_6535.jpg)

5. Insert the second connector piece at the position shown, then drive a small screw in from the side to join and secure the two printed parts.

   ![Where to insert the second J1 connector piece](images/onedrive-IMG_6536.jpg)

### J2 Shoulder lift

First, align the second connector from J1 with the horn holes on both ends of motor `F1` or `L1`. Fasten it with the larger screws (M3×6 mm), four above and four below. We recommend fastening the **non-splined side, where the horn can rotate freely**, first.

![Second connector attached to the J1 base assembly](images/onedrive-IMG_6537.jpg)

Next, fit the rectangular shell-shaped printed part onto the previous assembly, then insert motor `F2` or `L2`. Do not confuse it with the similar-looking part: **choose the one with the cable opening on the slanted edge, rather than on the side face.** Secure the motor with the smaller screws and check its position against the photo.

![J2 rectangular shell with its motor installed](images/onedrive-IMG_6538.jpg)

Before attaching the long connector, check its orientation and cable path against the next photo. Align the connector with the horn holes and secure it without reversing the printed part.

![J2 long connector orientation and cable routing](images/onedrive-IMG_6539.jpg)

### J3 Elbow flex

Insert motor `F3` or `L3` into the holder at the end of the long connector, then secure the motor and its horn. Match the motor, metal horn, and cable orientation to the photo before attaching the next forearm part.

![J3 motor at the end of the long connector](images/onedrive-IMG_6540.jpg)

### J4 Wrist flex

Use `F4` or `L4`. Slide the J4 motor holder into place, then insert the servo. Fit the horns, secure the upper horn with an M3×6 mm screw, and fasten the servo with four M2×6 mm screws. Check the orientation of the surface that will carry the wrist, and leave a path for the J5/J6 cables. The photo shows the assembled J4 position.

![J4 motor, horn, and forearm end after assembly](images/j4-wrist-flex-assembled.jpg)

### J5 Wrist roll

1. **We strongly recommend removing the horn from the splined side of motor `F5` or `L5` before inserting the motor into the J5 printed part.** Secure the motor with the small screws, then reinstall and fasten the horn on the splined side. J5 **uses only this one horn**; do not fit a horn on the opposite side.

   ![J5 motor in its printed holder with one horn on the splined side](images/j5-motor-horn-side.jpg)

2. Check the motor and holder orientation from the other side, and leave a route for the cables.

   ![Opposite side of the J5 motor holder and cable exit](images/j5-motor-cable-side.jpg)

3. **Connect cables to both ports on the J5 motor before attaching this assembly to the arm.** Route the cables through the printed part and leave slack for movement. Both ports are difficult to reach after attachment. The photo shows the cable path through the printed part.

   ![J5 cable path through the printed part before attaching the assembly to the arm](images/j5-cable-routing-before-attachment.jpg)

4. Align the mounting holes and attach the J5 assembly to the end of the J4 forearm. After attachment, move the wrist by hand to check for binding or cable tension.

   ![J5 assembly attached to the forearm](images/j5-attached-to-arm.jpg)

### J6 Follower gripper / Leader handle and trigger

**Follower:** Use `F6` and assemble the gripper in this order:

1. Align the gripper body with the J5 horn and fasten it with four M3×6 mm screws. The first photo shows the four fasteners from inside the gripper body.

   ![Four screws securing the Follower J6 gripper body to the J5 horn](images/follower-j6-gripper-body-mounted.jpg)

2. You can connect the `F6` gripper servo cable before inserting the servo into the body. Secure it with two M2×6 mm screws on each side. Fit the horns. Check the motor and visible metal horn orientation against the second photo.

   ![Follower J6 gripper servo installed with its metal horn exposed](images/follower-j6-servo-installed.jpg)

3. Align the moving jaw with the horn and support-side holes, then fasten it with four M3×6 mm screws on each side. Slowly open and close the gripper to check that the jaw does not bind.

   ![Follower J6 moving jaw installed on the gripper](images/follower-j6-moving-jaw-mounted.jpg)

**Leader:** Use `L6` and assemble the handle, trigger motor, and trigger in this order:

1. Fasten the handle to its holder with one M2×6 mm screw, then secure the holder to the wrist with four M3×6 mm screws. The photo shows the assembled handle and holder.

   ![Leader J6 handle attached to its holder](images/leader-j6-handle-assembled.jpg)

2. You can connect the `L6` trigger motor cable before inserting the motor into the holder. Secure it with two M2×6 mm screws on each side. Fit the metal horn. The photo shows the installed motor, cable, and exposed horn.

   ![Leader J6 trigger motor, cable, and metal horn](images/leader-j6-trigger-motor-installed.jpg)

3. Align the loop-shaped trigger with the horn holes and fasten it with four M3×6 mm screws. Check that the trigger moves smoothly under finger pressure.

   ![Leader J6 loop trigger fastened to the horn](images/leader-j6-trigger-mounted.jpg)

### 4.7 Wiring and final mechanical check

Insert brass standoffs into the four holes in the white printed mounting plate, checking that each sits straight and secure. Align the controller's four mounting holes with the standoffs and fasten it using the kit screws. The side photo shows clearance between the board and plate, with the USB-C connector and supply lead still accessible. Before fastening the plate in the reserved base position, confirm that its connectors can still be reached.

![First brass standoff in the mounting plate, with controller and fasteners nearby](images/mount-plate-first-standoff.jpg)

![Four brass standoffs installed in the white mounting plate](images/mount-plate-four-standoffs.jpg)

![Side view of the controller attached to the white mounting plate](images/controller-on-mount-plate.jpg)

These two photos show the controller mounted on a black printed plate. Brass standoffs raise the board; the side and top views show the connectors and power lead.

![Controller mounted on a black printed plate, side view showing standoffs and connectors](images/onedrive-IMG_6530.jpg)

![Controller mounted on a black printed plate, top view showing USB-C and red-black power wires](images/onedrive-IMG_6531.jpg)

Finally, complete the 1→6 daisy-chain with the three-pin leads and connect the J1 lead to the controller. Use the printed cable clips and guides. Slowly move every unpowered joint through its range and look for pulled leads, pinched cables, or loose plugs. Clamp the base securely and clear the arm's working area before connecting the correct power supply. Disconnect power immediately if you notice unusual heat, odor, or noise.

The photo shows both completed arms: the white Follower on the left and the black Leader on the right.

![Completed white Follower and black Leader arms](images/assembled-leader-follower.jpg)

### 4.8 Mount and focus the Follower camera

1. Prepare the Innomaker camera, white printed mount, camera cable, four M2 screws and nuts, and two screws for attaching the mount. The first photo has been rotated 90° counterclockwise to show the parts clearly.

   ![Camera, printed mount, cable, four M2 screws and nuts, and two mount screws](images/camera-kit-ccw90.jpg)

2. Align the camera board with the square opening in the mount. Insert four M2 screws from the back of the board and secure four nuts on the lens side. The next photos show the lens side and the back of the board.

   ![Lens side of the camera secured to its mount with four nuts](images/camera-mounted-front.jpg)

   ![Back of the camera board with four M2 screws through the mount](images/camera-mounted-back.jpg)

3. Use the two mounting screws to attach the camera mount above the Follower gripper. Plug the camera cable into the connector on the back of the board, leaving slack for joint movement.

   ![Camera mount attached above the Follower gripper](images/camera-on-follower.jpg)

Use the [OpenCV camera preview script](preview_innomaker.py) to focus the image. The LeRobot version used in this guide depends on headless OpenCV. For a preview window, create a separate desktop environment and run these commands from the folder containing the script:

```bash
conda create -y -n so101-camera python=3.12
conda activate so101-camera
python -m pip install opencv-python
python preview_innomaker.py
```

Change `CAMERA_PORT` at the top of the script to the Innomaker video device port on your computer. The default camera input is **1920×1080 at 30 fps**. `DISPLAY_WIDTH` and `DISPLAY_HEIGHT` set a **960×540 preview window**; they do not change the camera input resolution. These values can be adjusted in the script:

```python
CAMERA_PORT = 0
INPUT_WIDTH = 1920
INPUT_HEIGHT = 1080
DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540
FPS = 30
```

**Slowly turn the lens until an object at the gripper position is clearly visible in the preview.** Click below to watch the focus adjustment.

[![Preview of turning the camera lens to focus an object at the gripper](images/camera-focus-preview.jpg)](https://stevenzhoooooooooooooou.github.io/so101-assembly-guide/#camera-focus)

## 5. Calibrate and test teleoperation

Calibrate each assembled arm separately. First place every joint near the middle of its travel. After pressing Enter, slowly move each joint through its full range as instructed. The calibration ID names a local record; use the same ID during teleoperation. Replace the example ports below.

Use these photos as references for the initial calibration poses: the white Follower first, then the black Leader.

![White Follower pose for calibration](images/calibration-pose-follower.jpg)

![Black Leader pose for calibration](images/calibration-pose-leader.jpg)

These two videos show how to move several joints by hand during calibration. Click a preview to watch it in the browser.

[![Preview of the white Follower joint movement video](images/calibration-joint-motion-follower.jpg)](https://stevenzhoooooooooooooou.github.io/so101-assembly-guide/#follower-joints)

[![Preview of the black Leader joint movement video](images/calibration-joint-motion-leader.jpg)](https://stevenzhoooooooooooooou.github.io/so101-assembly-guide/#leader-joints)

Linux/macOS:

```bash
lerobot-calibrate --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=so101_follower_arm
lerobot-calibrate --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 --teleop.id=so101_leader_arm
lerobot-teleoperate --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=so101_follower_arm --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 --teleop.id=so101_leader_arm
```

Windows PowerShell:

```powershell
lerobot-calibrate --robot.type=so101_follower --robot.port=COM3 --robot.id=so101_follower_arm
lerobot-calibrate --teleop.type=so101_leader --teleop.port=COM4 --teleop.id=so101_leader_arm
lerobot-teleoperate --robot.type=so101_follower --robot.port=COM3 --robot.id=so101_follower_arm --teleop.type=so101_leader --teleop.port=COM4 --teleop.id=so101_leader_arm
```

Move the Leader a small amount first and confirm that the Follower's J1–J5 and gripper respond in the expected direction. Press `Ctrl+C` to stop if motion looks wrong, then check servo labels, assembly orientation, calibration, and cables. Cameras, datasets, and model training are not required for this check.

After teleoperation starts successfully, the Follower should move with the Leader. Click the preview to watch the example in the browser.

[![Preview of successful Leader-to-Follower teleoperation](images/teleoperation-success.jpg)](https://stevenzhoooooooooooooou.github.io/so101-assembly-guide/#teleoperation)

## 6. Troubleshooting

| Symptom | Check first |
| --- | --- |
| No serial port | USB data cable, controller power, Windows Device Manager or Linux/macOS device nodes, Waveshare jumpers. |
| Communication error during servo setup | Only one servo connected, supply voltage, three-pin cable orientation and seating, whether another program is using the port. |
| A joint does not move or moves the wrong way | F/L label, ID, gear ratio, horn orientation, and calibration record. |
| A cable unplugs during movement | Turn off power, reroute it with slack through the full J2–J5 range, then secure it in clips. |
| `lerobot-*` command not found | Run `conda activate lerobot` again and confirm you installed from the LeRobot source directory. |

## References

- [Hugging Face: SO-101 assembly, setup, and calibration](https://huggingface.co/docs/lerobot/main/en/so101)
- [Hugging Face: LeRobot installation](https://huggingface.co/docs/lerobot/main/en/installation)
- [Hugging Face: teleoperating a real robot](https://huggingface.co/docs/lerobot/main/en/il_robots)
- [Seeed Studio: SO-ARM100/SO-ARM101 tutorial](https://wiki.seeedstudio.com/lerobot_so100m_new/)
- [TheRobotStudio: SO-ARM100/SO-101 parts and print files](https://github.com/TheRobotStudio/SO-ARM100)
