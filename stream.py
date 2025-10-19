import streamlit as st
import cadquery as cq
import numpy as np
from cq_gears import SpurGear
from cq_gears import BevelGear
from cq_gears import CrossedHelicalGear
from cq_gears import RackGear
from cq_gears import RingGear
from cq_gears import Worm
from cq_warehouse.fastener import (Nut, Screw, Washer,
    HexNut, DomedCapNut, SquareNut, HeatSetNut,
    SocketHeadCapScrew, CounterSunkScrew, PanHeadScrew, HexHeadScrew, SetScrew,
    PlainWasher, ChamferedWasher)
from cq_warehouse.bearing import (Bearing, SingleRowDeepGrooveBallBearing,
    SingleRowCappedDeepGrooveBallBearing,SingleRowAngularContactBallBearing,
    SingleRowCylindricalRollerBearing,SingleRowTaperedRollerBearing)
import tempfile
import os


st.markdown("""<style>.stApp {background: linear-gradient(135deg, #000000, #0f2027, #2c5364);background-attachment: fixed;}</style>""",unsafe_allow_html=True)
st.markdown("""<style>[data-testid="stDecoration"] {background-image: linear-gradient(90deg, rgb(0, 102, 204), rgb(102, 255, 255));}</style>""",unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: gray;'><i>MechCAD Stop</h1>", unsafe_allow_html=True)
st.divider()


if 'generated_file' not in st.session_state:
    st.session_state.generated_file = None
def clear_download_state():
    st.session_state.generated_file = None


option = st.selectbox("Select your component",("Bearing", "Gear","Fastener"),index=None, placeholder="Select a component type...",on_change=clear_download_state)

#-----------------------------------------------Bearing------------------------------------------------------------------

if option == "Bearing":
    st.subheader("Bearing Specifications")
    BEARING_CLASSES = {
        "Single Row Deep Groove Ball Bearing": SingleRowDeepGrooveBallBearing,
        "Single Row Capped DeepGrooveBall Bearing": SingleRowCappedDeepGrooveBallBearing,
        "Single Row Angular Contact BallBearing": SingleRowAngularContactBallBearing,
        "Single Row Cylindrical Roller Bearing": SingleRowCylindricalRollerBearing,
        "Single Row Tapered Roller Bearing": SingleRowTaperedRollerBearing
    }

    cols = st.columns(2)
    class_name = cols[0].selectbox("Bearing Class", list(BEARING_CLASSES.keys()), index=None, key="bearing_class")

    bearing_sizes = []
    if class_name:
        try:
            bearing_sizes = list(BEARING_CLASSES[class_name].sizes("SKT"))
        except Exception:
            st.error(f"Could not load sizes for {class_name}")

    bearing_size = cols[1].selectbox("Bearing Size", bearing_sizes, index=None, key="bearing_size",
                                     disabled=not class_name)

    st.caption("(All bearings are as per SKT standard)")

    btn_cols = st.columns(2)
    with btn_cols[0]:
        if st.button(f"Generate Bearing", disabled=not bearing_size):
            try:
                instance = BEARING_CLASSES[class_name](size=bearing_size, bearing_type="SKT")
                temp_dir = tempfile.gettempdir()
                file_name = f"{class_name}_{bearing_size}.step"
                temp_path = os.path.join(temp_dir, file_name)
                cq.exporters.export(instance.cq_object, temp_path)

                with open(temp_path, "rb") as f:
                    st.session_state.generated_file = {
                        "data": f.read(), "name": file_name, "label": f"Download STEP File"
                    }
                st.success("File ready!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                clear_download_state()
            finally:
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    os.remove(temp_path)
    with btn_cols[1]:
        if st.session_state.generated_file:
            st.download_button(
                label=st.session_state.generated_file["label"],
                data=st.session_state.generated_file["data"],
                file_name=st.session_state.generated_file["name"],
                mime="application/octet-stream"
            )
        else:
            st.button("Download STEP File", disabled=True)

#-----------------------------------------------------------Gear----------------------------------------------------------------------------
if option == "Gear":
    gear_type = st.selectbox("Select type of gear",("Spur Gear", "Bevel Gear", "Crossed Helical Gear", "Rack Gear", "Ring Gear", "Worm Gear"),index=None,placeholder="Select a gear type...",on_change=clear_download_state)
    st.header("  ", divider="gray")


    if gear_type == "Spur Gear":
        st.subheader("Spur Gear Specifications")
        cols = st.columns(4)
        module = cols[0].number_input("Module", value=1.0, min_value=0.1, step=0.1)
        teeth_number = cols[1].number_input("Number of Teeth", value=19, min_value=3, step=1)
        width = cols[2].number_input("Thickness (mm)", value=5.0, min_value=0.1, step=0.5)
        bore_d = cols[3].number_input("Bore Diameter (mm)", value=5.0, min_value=0.0, step=0.5)

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Generate Gear"):
                max_bore_d = module * (teeth_number - 2.5)
                if bore_d >= max_bore_d:
                    st.error(f"Bore Diameter is too large. Maximum is {max_bore_d:.2f} mm.")
                    clear_download_state()
                else:
                    temp_dir = tempfile.gettempdir()
                    temp_path = os.path.join(temp_dir, "spur_gear.step")
                    try:
                        spur_gear = SpurGear(module=module, teeth_number=teeth_number, width=width, bore_d=bore_d)
                        wp = cq.Workplane('XY').gear(spur_gear)
                        cq.exporters.export(wp, temp_path, 'STEP')
                        with open(temp_path, "rb") as f:
                            st.session_state.generated_file = {
                                "data": f.read(),
                                "name": "spur_gear.step",
                                "label": "Download STEP File"
                            }
                        st.success("File ready!")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        clear_download_state()
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)


    elif gear_type == "Bevel Gear":
        st.subheader("Bevel Gear Specifications")
        cols = st.columns(5)
        module = cols[0].number_input("Module", value=1.0, min_value=0.1, step=0.1)
        teeth_number = cols[1].number_input("Number of Teeth", value=25, min_value=5, step=1)
        cone_angle = cols[2].number_input("Cone Angle (°)", value=45.0, min_value=1.0, max_value=179.0, step=1.0)
        face_width = cols[3].number_input("Face Width (mm)", value=8.0, min_value=1.0, step=0.5)
        bore_d = cols[4].number_input("Bore Diameter (mm)", value=5.0, min_value=0.0, step=0.5)

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Generate Gear"):
                try:
                    gamma_p = np.radians(cone_angle)
                    rp = module * teeth_number / 2.0
                    gs_r = rp / np.sin(gamma_p)

                    if face_width >= gs_r:
                        st.error(f"Face Width is too large. Must be less than {gs_r:.2f} mm.")
                        clear_download_state()
                    else:
                        temp_dir = tempfile.gettempdir()
                        temp_path = os.path.join(temp_dir, "bevel_gear.step")
                        try:
                            bevel_gear = BevelGear(module=module, teeth_number=teeth_number,
                                                   cone_angle=cone_angle, face_width=face_width)
                            gear_body = bevel_gear.build(bore_d=bore_d)
                            wp = cq.Workplane('XY').add(gear_body)
                            cq.exporters.export(wp, temp_path, 'STEP')
                            with open(temp_path, "rb") as f:
                                st.session_state.generated_file = {
                                    "data": f.read(),
                                    "name": "bevel_gear.step",
                                    "label": "Download STEP File"
                                }
                            st.success("File ready!")
                        except Exception as e:
                            st.error(f"An error occurred during generation: {e}")
                            clear_download_state()
                        finally:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                except Exception as e:
                    st.error(f"A validation error occurred: {e}")
                    clear_download_state()
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)


    elif gear_type == "Crossed Helical Gear":
        st.subheader("Crossed Helical Gear Specifications")
        cols = st.columns(5)
        module = cols[0].number_input("Module", value=1.0, min_value=0.1, step=0.1)
        teeth_number = cols[1].number_input("Number of Teeth", value=20, min_value=3, step=1)
        width = cols[2].number_input("Width (mm)", value=10.0, min_value=1.0, step=0.5)
        helix_angle = cols[3].number_input("Helix Angle (°)", value=45.0, min_value=-89.0, max_value=89.0, step=1.0)
        bore_d = cols[4].number_input("Bore Diameter (mm)", value=5.0, min_value=0.0, step=0.5)

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Generate Gear"):
                try:
                    h_angle_rad = np.radians(helix_angle)
                    transverse_module = module / np.cos(h_angle_rad)
                    max_bore_d = transverse_module * (teeth_number - 2.5)
                    if bore_d >= max_bore_d:
                        st.error(f"Bore Diameter is too large. Maximum is {max_bore_d:.2f} mm.")
                        clear_download_state()
                    else:
                        temp_dir = tempfile.gettempdir()
                        temp_path = os.path.join(temp_dir, "crossed_helical_gear.step")
                        try:
                            ch_gear = CrossedHelicalGear(module=module, teeth_number=teeth_number,
                                                         width=width, helix_angle=helix_angle)
                            gear_body = ch_gear.build(bore_d=bore_d)
                            wp = cq.Workplane('XY').add(gear_body)
                            cq.exporters.export(wp, temp_path, 'STEP')
                            with open(temp_path, "rb") as f:
                                st.session_state.generated_file = {
                                    "data": f.read(),
                                    "name": "crossed_helical_gear.step",
                                    "label": "Download STEP File"
                                }
                            st.success("File ready!")
                        except Exception as e:
                            st.error(f"An error occurred during generation: {e}")
                            clear_download_state()
                        finally:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                except Exception as e:
                    st.error(f"A validation error occurred: {e}")
                    clear_download_state()
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)


    elif gear_type == "Ring Gear":
        st.subheader("Ring Gear Specifications")
        cols = st.columns(4)
        module = cols[0].number_input("Module", value=1.0, min_value=0.1, step=0.1)
        teeth_number = cols[1].number_input("Number of Teeth", value=60, min_value=10, step=1)
        width = cols[2].number_input("Width (mm)", value=10.0, min_value=1.0, step=0.5)
        rim_width = cols[3].number_input("Rim Width (mm)", value=5.0, min_value=1.0, step=0.5,
                                         help="The thickness of the solid outer ring.")

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Generate Gear"):
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, "ring_gear.step")
                try:
                    ring_gear = RingGear(module=module,
                                         teeth_number=teeth_number,
                                         width=width,
                                         rim_width=rim_width)
                    gear_body = ring_gear.build()
                    wp = cq.Workplane('XY').add(gear_body)
                    cq.exporters.export(wp, temp_path, 'STEP')
                    with open(temp_path, "rb") as f:
                        st.session_state.generated_file = {
                            "data": f.read(),
                            "name": "ring_gear.step",
                            "label": "Download STEP File"
                        }
                    st.success("File ready!")
                except Exception as e:
                    st.error(f"An error occurred during generation: {e}")
                    clear_download_state()
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)


    elif gear_type == "Rack Gear":
        st.subheader("Rack Gear Specifications")
        cols = st.columns(4)
        module = cols[0].number_input("Module", value=1.0, min_value=0.1, step=0.1)
        length = cols[1].number_input("Length (mm)", value=100.0, min_value=10.0, step=1.0)
        width = cols[2].number_input("Width (mm)", value=10.0, min_value=1.0, step=0.5)
        height = cols[3].number_input("Height (mm)", value=5.0, min_value=1.0, step=0.5,
                                      help="The total height of the rack base, excluding teeth.")
        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Generate Gear"):
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, "rack_gear.step")
                try:
                    rack_gear = RackGear(module=module,
                                         length=length,
                                         width=width,
                                         height=height)
                    gear_body = rack_gear.build()
                    wp = cq.Workplane('XY').add(gear_body)
                    cq.exporters.export(wp, temp_path, 'STEP')
                    with open(temp_path, "rb") as f:
                        st.session_state.generated_file = {
                            "data": f.read(),
                            "name": "rack_gear.step",
                            "label": "Download STEP File"
                        }
                    st.success("File ready!")
                except Exception as e:
                    st.error(f"An error occurred during generation: {e}")
                    clear_download_state()
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)


    elif gear_type == "Worm Gear":
        st.subheader("Worm Gear Specifications")
        cols = st.columns(5)
        module = cols[0].number_input("Module", value=1.0, min_value=0.1, step=0.1)
        lead_angle = cols[1].number_input("Lead Angle (°)", value=10.0, min_value=1.0, max_value=89.0, step=1.0)
        n_threads = cols[2].number_input("Number of Threads", value=1, min_value=1, step=1)
        length = cols[3].number_input("Length (mm)", value=50.0, min_value=5.0, step=1.0)
        bore_d = cols[4].number_input("Bore Diameter (mm)", value=8.0, min_value=0.0, step=0.5)

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Generate Gear"):
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, "worm_gear.step")
                try:
                    worm_gear = Worm(module=module,
                                     lead_angle=lead_angle,
                                     n_threads=n_threads,
                                     length=length)
                    gear_body = worm_gear.build(bore_d=bore_d)
                    wp = cq.Workplane('XY').add(gear_body)
                    cq.exporters.export(wp, temp_path, 'STEP')
                    with open(temp_path, "rb") as f:
                        st.session_state.generated_file = {
                            "data": f.read(),
                            "name": "worm_gear.step",
                            "label": "Download STEP File"
                        }
                    st.success("File ready!")
                except Exception as e:
                    st.error(f"An error occurred during generation: {e}")
                    clear_download_state()
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)


#----------------------------------FASTNER-------------------------------------------------------------------------------
if option == "Fastener":

    fastener_category = st.selectbox(
        "Select Fastener Category",
        ("Nut", "Screw", "Washer"),
        index=None,
        placeholder="Select category...",
        on_change=clear_download_state
    )
    st.header("  ", divider="gray")


    if fastener_category == "Nut":
        st.subheader("Nut Specifications")
        NUT_CLASSES = {"Hex Nut": HexNut, "Domed Cap Nut": DomedCapNut, "Square Nut": SquareNut, "Heat Set Nut": HeatSetNut}

        cols = st.columns(3)
        class_name = cols[0].selectbox("Nut Class", list(NUT_CLASSES.keys()), index=None, key="nut_class")

        nut_types = []
        if class_name:
            try:
                nut_types = list(NUT_CLASSES[class_name].types())
            except Exception:
                st.error(f"Could not load types for {class_name}")

        nut_type = cols[1].selectbox("Nut Type", nut_types, index=None, key="nut_type", disabled=not class_name)

        nut_sizes = []
        if class_name and nut_type:
            try:
                nut_sizes = list(NUT_CLASSES[class_name].sizes(nut_type))
            except Exception:
                st.error(f"Could not load sizes for {nut_type}")

        nut_size = cols[2].selectbox("Nut Size", nut_sizes, index=None, key="nut_size", disabled=not nut_type)

        show_threads = st.checkbox("Show Threads (slower)", value=False)

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button(f"Generate Nut", disabled=not nut_size):
                try:
                    instance = NUT_CLASSES[class_name](size=nut_size, fastener_type=nut_type, simple=not show_threads)
                    temp_dir = tempfile.gettempdir()
                    file_name = f"{class_name}_{nut_size.replace('/', '_')}.step"
                    temp_path = os.path.join(temp_dir, file_name)
                    cq.exporters.export(instance, temp_path)

                    with open(temp_path, "rb") as f:
                        st.session_state.generated_file = {
                            "data": f.read(), "name": file_name, "label": f"Download STEP file"
                        }
                    st.success("File ready!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    clear_download_state()
                finally:
                    if 'temp_path' in locals() and os.path.exists(temp_path):
                        os.remove(temp_path)
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)


    elif fastener_category == "Screw":
        st.subheader("Screw Specifications")
        SCREW_CLASSES = {"Socket Head Cap Screw": SocketHeadCapScrew, "Counter Sunk Screw": CounterSunkScrew,
                         "Pan Head Screw": PanHeadScrew, "Hex Head Screw": HexHeadScrew, "Set Screw": SetScrew}

        cols = st.columns(3)
        class_name = cols[0].selectbox("Screw Class", list(SCREW_CLASSES.keys()), index=None, key="screw_class")

        screw_types = []
        if class_name:
            try:
                screw_types = list(SCREW_CLASSES[class_name].types())
            except Exception:
                st.error(f"Could not load types for {class_name}")

        screw_type = cols[1].selectbox("Screw Type", screw_types, index=None, key="screw_type", disabled=not class_name)

        screw_sizes = []
        if class_name and screw_type:
            try:
                screw_sizes = list(SCREW_CLASSES[class_name].sizes(screw_type))
            except Exception:
                st.error(f"Could not load sizes for {screw_type}")

        screw_size = cols[2].selectbox("Screw Size", screw_sizes, index=None, key="screw_size", disabled=not screw_type)

        length = st.number_input("Length (mm)", value=10.0, min_value=1.0, step=1.0, disabled=not screw_size)
        show_threads = st.checkbox("Show Threads (slower)", value=False)

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button(f"Generate Screw", disabled=not screw_size):
                try:
                    instance = SCREW_CLASSES[class_name](size=screw_size, fastener_type=screw_type, length=length,
                                                         simple=not show_threads)
                    temp_dir = tempfile.gettempdir()
                    file_name = f"{class_name}_{screw_size.replace('/', '_')}_x{length}.step"
                    temp_path = os.path.join(temp_dir, file_name)
                    cq.exporters.export(instance, temp_path)

                    with open(temp_path, "rb") as f:
                        st.session_state.generated_file = {
                            "data": f.read(), "name": file_name, "label": f"Download STEP File"
                        }
                    st.success("File ready!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    clear_download_state()
                finally:
                    if 'temp_path' in locals() and os.path.exists(temp_path):
                        os.remove(temp_path)
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)


    elif fastener_category == "Washer":
        st.subheader("Washer Specifications")
        WASHER_CLASSES = {"Plain Washer": PlainWasher, "Chamfered Washer": ChamferedWasher}

        cols = st.columns(3)
        class_name = cols[0].selectbox("Washer Class", list(WASHER_CLASSES.keys()), index=None, key="washer_class")

        washer_types = []
        if class_name:
            try:
                washer_types = list(WASHER_CLASSES[class_name].types())
            except Exception:
                st.error(f"Could not load types for {class_name}")

        washer_type = cols[1].selectbox("Washer Type", washer_types, index=None, key="washer_type",
                                        disabled=not class_name)

        washer_sizes = []
        if class_name and washer_type:
            try:
                washer_sizes = list(WASHER_CLASSES[class_name].sizes(washer_type))
            except Exception:
                st.error(f"Could not load sizes for {washer_type}")

        washer_size = cols[2].selectbox("Washer Size", washer_sizes, index=None, key="washer_size",
                                        disabled=not washer_type)

        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button(f"Generate Washer", disabled=not washer_size):
                try:

                    instance = WASHER_CLASSES[class_name](size=washer_size, fastener_type=washer_type)
                    temp_dir = tempfile.gettempdir()
                    file_name = f"{class_name}_{washer_size.replace('/', '_')}.step"
                    temp_path = os.path.join(temp_dir, file_name)
                    cq.exporters.export(instance, temp_path)

                    with open(temp_path, "rb") as f:
                        st.session_state.generated_file = {
                            "data": f.read(), "name": file_name, "label": f"Download STEP File"
                        }
                    st.success("File ready!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    clear_download_state()
                finally:
                    if 'temp_path' in locals() and os.path.exists(temp_path):
                        os.remove(temp_path)
        with btn_cols[1]:
            if st.session_state.generated_file:
                st.download_button(
                    label=st.session_state.generated_file["label"],
                    data=st.session_state.generated_file["data"],
                    file_name=st.session_state.generated_file["name"],
                    mime="application/octet-stream"
                )
            else:
                st.button("Download STEP File", disabled=True)
