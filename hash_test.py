import os
import json
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk

# Directory where videos are located
VIDEO_DIRECTORY = "/Users/seherova/Downloads/VIDEO_DIRECTORY"
DATABASE_FILE = "database_file.json"


def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    else:
        return {}


def save_database(database):
    with open(DATABASE_FILE, "w") as file:
        json.dump(database, file, indent=4)


def get_video_files():
    if not os.path.exists(VIDEO_DIRECTORY):
        messagebox.showerror("Error", f"{VIDEO_DIRECTORY} directory not found.")
        return []
    return [f for f in os.listdir(VIDEO_DIRECTORY) if f.endswith((".mp4", ".avi", ".mov"))]


def search_videos_by_tag(tag):
    database = load_database()
    result = [video for video, tags in database.items() if tag in tags]
    return result


def get_videos_by_tags(tags):
    database = load_database()
    result = [video for video, video_tags in database.items() if any(tag in video_tags for tag in tags)]
    return result


def show_video_tags(video_name):
    database = load_database()
    if video_name in database:
        return database[video_name]
    else:
        return None


def hash_video_size(video_path):
    """Verilen videonun boyutunu hash'le ve çıktı olarak döndür."""
    size = os.path.getsize(video_path)  # Dosyanın boyutunu al
    return hashlib.sha256(str(size).encode()).hexdigest()  # Hash'le


def rename_video_with_hash(video_name):
    """Video adını hash değerine göre değiştir."""
    video_path = os.path.join(VIDEO_DIRECTORY, video_name)
    hash_name = hash_video_size(video_path) + os.path.splitext(video_name)[1]  # Uzantıyı koru
    new_path = os.path.join(VIDEO_DIRECTORY, hash_name)
    os.rename(video_path, new_path)  # Dosyayı yeniden adlandır
    return hash_name


def add_tags_to_video(video_name, new_tags):
    database = load_database()

    if video_name not in database:
        database[video_name] = []

    current_tags = database[video_name]
    for tag in new_tags:
        if tag not in current_tags:
            current_tags.append(tag)

    # Videoyu hash ile yeniden adlandır
    new_video_name = rename_video_with_hash(video_name)

    # Veritabanında eski adı yeni adla güncelle
    database[new_video_name] = database.pop(video_name)

    save_database(database)
    messagebox.showinfo("Success", f"Tags {new_tags} added to {new_video_name}.")


def is_video_in_directory(video_name):
    return video_name in get_video_files()


def search_videos():
    search_window = tk.Toplevel(root)
    search_window.title("Search Videos by Tags")
    search_window.geometry("400x200")

    tag_label = tk.Label(search_window, text="Enter tags to search (comma separated):")
    tag_label.pack(pady=5)

    tag_entry = tk.Entry(search_window, width=50)
    tag_entry.pack(pady=5)

    def perform_search():
        user_input = tag_entry.get()
        if user_input:
            tags_to_search = [tag.strip() for tag in user_input.split(",")]
            videos_found = get_videos_by_tags(tags_to_search)
            if videos_found:
                result_text = "\n".join(videos_found)
                messagebox.showinfo("Videos Found", f"Videos with {tags_to_search}:\n{result_text}")
            else:
                messagebox.showinfo("No Videos Found", "No matching videos found.")
        search_window.destroy()

    search_button = tk.Button(search_window, text="Search", command=perform_search)
    search_button.pack(pady=10)


def show_tags():
    tags_window = tk.Toplevel(root)
    tags_window.title("Show Video Tags")
    tags_window.geometry("400x200")

    video_list = get_video_files()
    if not video_list:
        messagebox.showinfo("No Videos", "No videos found in the directory.")
        tags_window.destroy()
        return

    video_name_label = tk.Label(tags_window, text="Select a video to view tags:")
    video_name_label.pack(pady=5)

    video_combobox = ttk.Combobox(tags_window, values=video_list, width=40)
    video_combobox.pack(pady=5)

    def display_tags():
        selected_video = video_combobox.get()
        if selected_video:
            tags = show_video_tags(selected_video)
            if tags is not None:
                messagebox.showinfo("Video Tags", f"Tags for {selected_video}:\n{tags}")
            else:
                messagebox.showinfo("Not Found", "No tags found for the selected video.")
        tags_window.destroy()

    show_button = tk.Button(tags_window, text="Show Tags", command=display_tags)
    show_button.pack(pady=10)


def add_tags():
    add_window = tk.Toplevel(root)
    add_window.title("Add Tags to Video")
    add_window.geometry("400x250")

    video_list = get_video_files()
    if not video_list:
        messagebox.showinfo("No Videos", "No videos found in the directory.")
        add_window.destroy()
        return

    video_name_label = tk.Label(add_window, text="Select a video to add tags:")
    video_name_label.pack(pady=5)

    video_combobox = ttk.Combobox(add_window, values=video_list, width=40)
    video_combobox.pack(pady=5)

    tag_label = tk.Label(add_window, text="Enter tags to add (comma separated):")
    tag_label.pack(pady=5)

    tag_entry = tk.Entry(add_window, width=50)
    tag_entry.pack(pady=5)

    def perform_add_tags():
        selected_video = video_combobox.get()
        new_tags_input = tag_entry.get()
        if selected_video and new_tags_input:
            new_tags = [tag.strip() for tag in new_tags_input.split(",")]
            add_tags_to_video(selected_video, new_tags)
        add_window.destroy()

    add_button = tk.Button(add_window, text="Add Tags", command=perform_add_tags)
    add_button.pack(pady=10)


def main():
    global root
    root = tk.Tk()
    root.title("Video Tag Manager")
    root.geometry("500x400")

    label = tk.Label(root, text="Video Tag Manager", font=("Arial", 16))
    label.pack(pady=20)

    search_button = tk.Button(root, text="Search Video by Tag", command=search_videos, width=30)
    search_button.pack(pady=10)

    show_tags_button = tk.Button(root, text="Show Video's Tags", command=show_tags, width=30)
    show_tags_button.pack(pady=10)

    add_tags_button = tk.Button(root, text="Add Tag to Video", command=add_tags, width=30)
    add_tags_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, width=30)
    exit_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
