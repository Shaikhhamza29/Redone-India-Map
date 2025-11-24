import os
os.environ["VLC_VERBOSE"] = "-1"
os.environ["PYTHON_VLC_VERBOSE"] = "-1"


import matplotlib




matplotlib.use("TkAgg")
matplotlib.rcParams["toolbar"] = "none"
import matplotlib.font_manager as fm
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk
import tkinter as tk
import vlc   # VLC player


# ================== SCREEN SIZE ===================
root = tk.Tk()
root.withdraw()
SCREEN_W = root.winfo_screenwidth()
SCREEN_H = root.winfo_screenheight()
root.destroy()


# ================== IMAGE SLIDESHOW ===================
def open_slideshow(image_folder):
    images = [f for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not images:
        print("No images found!")
        return

    slideshow = Toplevel()
    slideshow.title("Image Slideshow")
    slideshow.attributes("-fullscreen", True)

    slideshow.focus_set()
    slideshow.grab_set()

    index = {"i": 0}
    img_label = Label(slideshow)
    img_label.pack(expand=True)

    def show_image():
        img_path = os.path.join(image_folder, images[index["i"]])
        img = Image.open(img_path)
        img = img.resize((SCREEN_W, SCREEN_H))
        photo = ImageTk.PhotoImage(img)
        img_label.config(image=photo)
        img_label.image = photo

    def next_img():
        index["i"] = (index["i"] + 1) % len(images)
        show_image()

    def autoplay():
        next_img()
        slideshow.after(4000, autoplay)

    def close_show(event=None):
        slideshow.grab_release()
        slideshow.destroy()

    Button(slideshow, text="Close", command=close_show,
           font=("Arial", 18), fg="white", bg="red").pack(side="bottom")

    slideshow.bind("<Escape>", close_show)

    show_image()
    autoplay()


# ================== VIDEO SLIDESHOW (VLC) ===================
# ================== VIDEO SLIDESHOW (VLC FIXED) ===================
# ================== VIDEO SLIDESHOW (VLC FIXED CLEAN) ===================
def open_video_slideshow(video_folder):
    videos = [f for f in os.listdir(video_folder) if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))]
    if not videos:
        print("No videos found!")
        return

    video_window = Toplevel()
    video_window.title("Video Slideshow")
    video_window.attributes("-fullscreen", True)
    video_window.focus_set()
    video_window.grab_set()

    instance = vlc.Instance(
        "--no-video-title-show",
        "--avcodec-hw=none",          # force software decoding
        "--no-plugins-cache",
        "--no-sub-autodetect-file",
        "--vout=opengl",              # <---- FIX: avoid direct3d11 crashes
        "--drop-late-frames",
        "--skip-frames"
    )

    player = instance.media_player_new()
    current = {"i": 0}

    def play_video():
        video_path = os.path.join(video_folder, videos[current["i"]])
        media = instance.media_new(video_path)
        player.set_media(media)

        # Delay attach to prevent SetThumbNailClip failure
        def attach():
            player.set_hwnd(video_window.winfo_id())
            player.play()

        video_window.after(250, attach)  # ensure window allocated fully

    def next_video():
        current["i"] = (current["i"] + 1) % len(videos)
        play_video()
        video_window.after(4000, next_video)

    def close_video(event=None):
        player.stop()
        video_window.grab_release()
        video_window.destroy()
    video_window.bind("<Escape>", close_video)

    play_video()
    video_window.after(4000, next_video)


def open_manual_gallery(folder):
    media_files = [f for f in os.listdir(folder)
                   if f.lower().endswith((".png", ".jpg", ".jpeg", ".mp4", ".avi", ".mov", ".mkv"))]

    if not media_files:
        print("No media found!")
        return

    gallery = Toplevel()
    gallery.title("Manual Viewer")
    gallery.attributes("-fullscreen", True)
    gallery.focus_set()
    gallery.grab_set()

    index = {"i": 0}
    player = None

    display_label = Label(gallery, bg="black")
    display_label.pack(fill="both", expand=True)

    def show_media():
        nonlocal player
        file_path = os.path.join(folder, media_files[index["i"]])

        # stop video if running
        if player:
            player.stop()
            player = None

        if file_path.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            instance = vlc.Instance("--no-video-title-show")
            player = instance.media_player_new()
            media = instance.media_new(file_path)
            player.set_media(media)

            def attach():
                try:
                    player.set_hwnd(display_label.winfo_id())
                    player.play()
                except:
                    pass

            gallery.after(200, attach)

        else:
            img = Image.open(file_path)
            img = img.resize((SCREEN_W, SCREEN_H))
            photo = ImageTk.PhotoImage(img)
            display_label.config(image=photo)
            display_label.image = photo

    def next_media(event=None):
        index["i"] = (index["i"] + 1) % len(media_files)
        show_media()

    def prev_media(event=None):
        index["i"] = (index["i"] - 1) % len(media_files)
        show_media()

    def close_gallery(event=None):
        if player:
            player.stop()
        gallery.grab_release()
        gallery.destroy()

    # Keyboard shortcuts only
    gallery.bind("<Right>", next_media)
    gallery.bind("<Left>", prev_media)
    gallery.bind("<Escape>", close_gallery)

    show_media()


# ===================== INDIA MAP =====================
shapefile_path = r"D:\Projects\India_map_hostpots\in_shp\in.shp"



STATE_COL = "name"
states = gpd.read_file(shapefile_path).to_crs(epsg=4326)
states[STATE_COL] = states[STATE_COL].str.encode('ascii', 'ignore').str.decode('ascii')

states["is_selected"] = False

fig, ax = plt.subplots()


def draw_map():
    ax.clear()
    colors = ["yellow" if sel else "#dddddd" for sel in states["is_selected"]]
    states.plot(ax=ax, edgecolor="black", facecolor=colors)

    for _, row in states.iterrows():
        centroid = row.geometry.centroid
        ax.text(centroid.x, centroid.y, row[STATE_COL],
                fontsize=8, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6))

    ax.set_axis_off()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.canvas.draw_idle()


draw_map()
try: plt.get_current_fig_manager().full_screen_toggle()
except: pass


STATE_ACTIONS = {
    "maharashtra": ("slideshow", r"D:\Projects\India_map_hostpots\media\Mumbai"),
    "delhi": ("video", r"D:\Projects\India_map_hostpots\media\Delhi"),
    "goa": ("manual", r"D:\Projects\India_map_hostpots\media\Goa"),
    "tamil nadu": ("video", r"D:\Projects\India_map_hostpots\media\Chennai"),
    "kerala": ("manual", r"D:\Projects\India_map_hostpots\media\Kerala"),
    "gujarat": ("slideshow", r"D:\Projects\India_map_hostpots\media\Gujarat"),
    "jammu and kashmir": ("video", r"D:\Projects\India_map_hostpots\media\Jammu_Kashmir"),
    "uttar pradesh": ("manual", r"D:\Projects\India_map_hostpots\media\Uttar_predesh"),
    "andaman and nicobar": ("slideshow", r"D:\Projects\India_map_hostpots\media\Andaman_and_Nicobar"),
    "karnataka": ("manual", r"D:\Projects\India_map_hostpots\media\Karnataka"),
}



def on_click(event):
    if event.inaxes is not ax:
        return

    pt = Point(event.xdata, event.ydata)
    mask = states.geometry.contains(pt)
    if not mask.any():
        return

    idx = states.index[mask][0]
    state_name = states.at[idx, STATE_COL]

    states["is_selected"] = False
    states.at[idx, "is_selected"] = True
    draw_map()

    key = state_name.lower().replace("&", "and").strip()
    if key in STATE_ACTIONS:
        action, folder = STATE_ACTIONS[key]
        if action == "image":
            open_slideshow(folder)
        elif action == "video":
            open_video_slideshow(folder)
        elif action == "manual":
            open_manual_gallery(folder)


fig.canvas.mpl_connect("button_press_event", on_click)


def map_escape(event):
    if event.key == "escape":
        print("Exiting map...")
        plt.close(fig)

fig.canvas.mpl_connect("key_press_event", map_escape)


plt.show()
