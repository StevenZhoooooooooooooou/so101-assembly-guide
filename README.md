# SO-101 Assembly and LeRobot Setup Guide (English Draft)

This guide is for readers assembling an SO-101 Leader and Follower from parts. Install LeRobot and configure the servos one at a time, assemble joints J1 through J6, wire the arms, calibrate them, and test teleoperation. Each assembly section has an image placeholder for photos you can add later. If you are building only a Follower, skip the Leader-specific steps.

> Scope: the SO-101 design using Feetech STS3215 bus servos. Printed parts, controllers, and power supplies vary by kit; check the markings on your actual components. Software commands were checked against the LeRobot `main` documentation and local source on 2026-09-30. Recheck the CLI when upgrading LeRobot.

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

Order: install software → find ports → configure each servo ID and baud rate → clean printed parts → J1 → J2 → J3 → J4 → J5 → J6 → wiring → calibration → teleoperation. For each joint, add a parts layout photo, a servo/horn orientation photo, and an assembled view showing the cable path.

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

macOS ports often look like `/dev/cu.usbmodem...` or `/dev/tty.usbmodem...`. If you already have a local LeRobot checkout, run the install command inside that checkout instead of cloning it again.

### 2.3 Windows (native PowerShell or Miniforge Prompt)

Choose the Windows installer from the [Miniforge download page](https://conda-forge.org/download/). Open Miniforge Prompt and make sure `git --version` works:

```powershell
conda create -y -n lerobot python=3.12
conda activate lerobot
git clone https://github.com/huggingface/lerobot.git
cd lerobot
python -m pip install -e ".[core_scripts,feetech]"
```

Find the controller's COM number in Device Manager under **Ports (COM & LPT)**, such as `COM3` or `COM4`. Windows commands later in this guide are single-line PowerShell commands; Bash's `\` line continuation does not work in PowerShell. The official installation page covers Windows environment activation. The Windows hardware connection flow in this draft still needs testing on the target PC.

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

The joint sections provide the text structure for later photos. Check orientations, screw counts, and horn details against your printed parts and kit BOM. Test-fit each joint, confirm smooth movement, then tighten screws. Screws that are too long can damage a servo. The M2×6 mm and M3×6 mm sizes below follow the [Hugging Face joint guide](https://huggingface.co/docs/lerobot/main/en/so101).

Each servo comes with two metal horns. The photo shows the output shaft and both horns so you can identify them before assembling the joints.

![Leader servo output shaft with two round metal horns](images/onedrive-IMG_6529.jpg)

Each servo also comes with three types of screws. The next photo shows the two horns and the three groups of screws; use the fasteners specified for each joint.

![Two metal servo horns and three screw types supplied with each servo](images/servo-horns-and-three-screw-types-cw90.jpg)

### J1 Base rotation / Shoulder Pan

Use `F1` or `L1`. Fit the upper and lower servo horns, securing the upper horn with an M3×6 mm screw. Put the servo in the base and fasten it with four M2×6 mm screws, two above and two below. Slide on the first motor holder and secure it with one M2×6 mm screw on each side. Attach the shoulder piece with four M3×6 mm screws on top and four below, then add the shoulder motor holder. Confirm that the base is secure and the cable cannot be pinched during rotation.

> 📷 Photo to add: inserting the J1 servo into the base, bottom screws, and cable exit.

### J2 Shoulder lift

Use `F2` or `L2`. Fit the horns and secure the upper horn. Slide the servo into the shoulder holder from above and fasten it with four M2×6 mm screws. Align the upper arm with the horn and support side, then use four M3×6 mm screws on each side. Leave adjustable cable slack and check that shoulder movement does not wind the cable tightly around the axis.

These photos of the black Leader parts show shoulder joint J2: its servo sits beside the base with the metal horn facing outward. The next views show fastening from inside the base and fitting the upper-arm holder.

![J2 servo beside the base, with metal horn and shoulder printed parts](images/onedrive-IMG_6532.jpg)

![Side view of the J2 servo aligned with the shoulder printed part](images/onedrive-IMG_6533.jpg)

![Tightening a shoulder connection screw from inside the base](images/onedrive-IMG_6534.jpg)

![Close-up of a shoulder connection screw](images/onedrive-IMG_6535.jpg)

![Side view after fitting the J2 upper-arm holder to the base](images/onedrive-IMG_6536.jpg)

![Another side view of the fitted J2 upper-arm holder](images/onedrive-IMG_6537.jpg)

> 📷 Photo to add: fasteners on the other side of the J2 upper arm and shoulder movement check.

### J3 Elbow flex

Use `F3` or `L3`. Fit the horns and secure the upper horn. Place the servo at the end of the upper arm and fasten it with four M2×6 mm screws. Attach the forearm to J3 with four M3×6 mm screws on each side. Slowly flex the elbow and check for shell contact or tension on the three-pin plug.

The first photo shows the J3 servo and metal horn at the end of the upper arm. The second shows the forearm attached and the three-pin cable routed alongside it.

![J3 servo at the end of the upper arm, with its metal horn facing outward](images/onedrive-IMG_6538.jpg)

![Side view after attaching the J3 forearm, showing the three-pin lead](images/onedrive-IMG_6539.jpg)

> 📷 Photo to add: J3 connection screws and elbow motion range.

### J4 Wrist flex

Use `F4` or `L4`. Slide the J4 motor holder into place, then slide in the servo. Fit the horns, secure the upper horn with an M3×6 mm screw, and fasten the servo with four M2×6 mm screws. Check the orientation of the surface that will carry the wrist, and leave a path for the J5/J6 cables.

This side view shows the assembly through the forearm. Another servo and its metal horn are visible at the far end; the wrist connection is not yet shown.

![Servo and metal horn at the end of the forearm, with the assembled base-to-forearm structure](images/onedrive-IMG_6540.jpg)

> 📷 Photo to add: fitting the J4 motor holder, wrist connection, and cable exit.

### J5 Wrist roll

Use `F5` or `L5`. Insert the servo into the wrist holder and secure it with two front M2×6 mm screws. Fit only one horn here, held by one M3×6 mm screw. Attach the wrist assembly to J4 using M3×6 mm screws on both sides at the printed mounting holes. Check motion by hand before routing the J4 and J5 cables.

> 📷 Photo to add: J5 single horn; connection to J4; cable slack during wrist rotation.

### J6 Follower gripper / Leader handle and trigger

**Follower:** Use `F6`. Attach the gripper body to the J5 horn with four M3×6 mm screws. Insert the gripper servo and secure it with two M2×6 mm screws on each side. Fit the horns, fastening the upper one with an M3×6 mm screw. Attach the moving jaw to the horn/support side with four M3×6 mm screws on each side. Check that the jaws open and close without binding.

**Leader:** Use `L6`. Secure the handle holder to the wrist with four M3×6 mm screws, then attach the handle with one M2×6 mm screw. Insert the trigger servo and secure it with two M2×6 mm screws on each side. Fit and fasten its horn with an M3×6 mm screw, then attach the trigger to the horn with four M3×6 mm screws. Check that the trigger moves smoothly under finger pressure.

> 📷 Photo to add: Follower gripper exploded view and open/closed positions; Leader handle and trigger assembly.

### 4.7 Wiring and final mechanical check

Insert brass standoffs into the four holes in the white printed mounting plate, checking that each sits straight and secure. Align the controller's four mounting holes with the standoffs and fasten it using the kit screws. The side photo shows clearance between the board and plate, with the USB-C connector and supply lead still accessible. Before fastening the plate in the reserved base position, confirm that its connectors can still be reached.

![First brass standoff in the mounting plate, with controller and fasteners nearby](images/mount-plate-first-standoff.jpg)

![Four brass standoffs installed in the white mounting plate](images/mount-plate-four-standoffs.jpg)

![Side view of the controller attached to the white mounting plate](images/controller-on-mount-plate.jpg)

These two photos show the controller mounted on a black printed plate. Brass standoffs raise the board; the side and top views show the connectors and power lead.

![Controller mounted on a black printed plate, side view showing standoffs and connectors](images/onedrive-IMG_6530.jpg)

![Controller mounted on a black printed plate, top view showing USB-C and red-black power wires](images/onedrive-IMG_6531.jpg)

Then daisy-chain the three-pin leads by servo ID 1→6, with J1 connected to the controller. Use the printed cable clips and guides. Slowly move every unpowered joint through its range and look for pulled leads, pinched cables, or loose plugs. Clamp the base securely and clear the arm's working area before connecting the correct power supply. Disconnect power immediately if you notice unusual heat, odor, or noise.

> 📷 Photo to add: final location of the mounting plate in the base; full cable route; finished Leader and Follower.

## 5. Calibrate and test teleoperation

Calibrate each assembled arm separately. First place every joint near the middle of its travel. After pressing Enter, slowly move each joint through its full range as instructed. The calibration ID names a local record; use the same ID during teleoperation. Replace the example ports below.

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
