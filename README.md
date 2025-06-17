# MechCAD Stop ⚙️

**MechCAD Stop** is a one-stop, web-based **parametric CAD generator** that allows users to quickly create standard mechanical components.  
Built with [Streamlit](https://streamlit.io/) and powered by [CadQuery](https://github.com/CadQuery/cadquery?tab=readme-ov-file), this tool streamlines the generation of **gears**, **fasteners**, and **bearings**, offering ready-to-use **STEP files** for your CAD projects.

With a library of hundreds of standard **bearings**, **fasteners**, and fully **parametric gears**, MechCAD Stop can generate over **1000+ unique component combinations**, tailored to match your exact design requirements.

![MechCAD Stop Interface](https://github.com/user-attachments/assets/9886951a-09ee-46ba-a3b2-4b776de3e029)

---

## Features

Quickly generate 3D models for a wide variety of standard parts with just a few clicks.

### 🔩 Fasteners
Generate standard nuts, screws, and washers with optional threading.

- **Nuts**: Hex, Domed, Square, Heat-Set, and more  
- **Screws**: Socket Head, Counter-Sunk, Pan Head, and others  
- **Washers**: Plain and Chamfered

### ⚙️ Gears
Create parametric gears of different types.

- Spur Gear  
- Bevel Gear  
- Crossed Helical Gear  
- Rack Gear  
- Ring Gear  
- Worm Gear  

### 🧷 Bearings
Produce industry-standard bearings based on SKT specifications.

- Deep Groove  
- Capped  
- Angular Contact  
- and more...
  
![Generated Components](https://github.com/user-attachments/assets/16dd9447-3a78-4941-97c0-00aaa38388a3)

*Example of a generated CAD model. The web app supports creating many more types, all included within the interface.*


---

## 🛠️ How to Use

1. **Select a Component**  
   Choose between **"Bearing"**, **"Fastener"**, or **"Gear"** from the main dropdown menu.

2. **Specify Parameters**  
   Select the desired class, type, and size. Enter any required dimensions like length, bore diameter, etc.

3. **Generate**  
   Click the **"Generate"** button.

4. **Download**  
   Once the file is ready, a **"Download STEP"** button will appear. Click it to save your 3D model.

---

## 📦 Acknowledgements

This application is built on the shoulders of giants. Special thanks to the creators of these powerful open-source libraries:

- [`cq-warehouse`](https://github.com/gumyr/cq_warehouse) by **Gumyr** – for fastener and bearing generation  
- [`cq-gears`](https://github.com/meadiode/cq_gears) by **meadiode@github** – for parametric gear modeling  

---

## 📄 License

This project is licensed under the **Apache License 2.0**.  
See the [LICENSE](./LICENSE) file for details.

---

## 🌐 Live Demo

[https://mechcadstop.streamlit.app/](https://mechcadstop.streamlit.app/)

> **Note:** This app is hosted on Streamlit Community Cloud, which may go inactive after 12 hours of no use.  
> If the link appears invalid and you prefer not to clone and run it locally, feel free to drop me a request — I’ll reactivate it for you.


---

## 📬 Contact

For any questions, feedback, or collaboration ideas, feel free to reach out via GitHub Issues or open a Pull Request!

