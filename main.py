import os
import json

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
        print(f"Error: {VIDEO_DIRECTORY} directory not found.")
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

def add_tags_to_video(video_name, new_tags):
    database = load_database()

    # Initialize with an empty list of tags if the video is not yet in the database
    if video_name not in database:
        database[video_name] = []

    # Add new tags to the existing tags
    current_tags = database[video_name]
    for tag in new_tags:
        if tag not in current_tags:
            current_tags.append(tag)

    # Save the updated database
    save_database(database)
    print(f"Tags {new_tags} added to {video_name}.")

def is_video_in_directory(video_name):
    # Check if the video exists in VIDEO_DIRECTORY
    return video_name in get_video_files()

def main():
    while True:
        choice = input("1. Search video by tag\n2. Show video's tags\n3. Add tag to video\n4. Exit\nMake your selection: ")

        if choice == "1":
            user_input = input("Enter the tag(s) you want to search for, separated by commas (e.g., rocket, F16, Akıncı): ")
            tags_to_search = [tag.strip() for tag in user_input.split(",")]
            videos_found = get_videos_by_tags(tags_to_search)

            if videos_found:
                print(f"Videos with {tags_to_search} tag(s): {videos_found}")
            else:
                print(f"No videos found with {tags_to_search} tag(s).")

        elif choice == "2":
            video_name = input("Enter the name of the video to view its tags (e.g., video1.mp4): ")
            tags = show_video_tags(video_name)
            if tags is not None:
                print(f"Tags for {video_name}: {tags}")
            else:
                print(f"{video_name} not found.")

        elif choice == "3":
            # Check if the video exists in the VIDEO_DIRECTORY before proceeding
            video_name = input("Enter the name of the video to add tags (e.g., video1.mp4): ")
            if is_video_in_directory(video_name):
                # Proceed with adding tags
                new_tags_input = input("Enter the tags to add, separated by commas (e.g. nature, landscape): ")
                new_tags = [tag.strip() for tag in new_tags_input.split(",")]
                add_tags_to_video(video_name, new_tags)
            else:
                print(f"Error: {video_name} not found in {VIDEO_DIRECTORY}. Please enter a valid video name.")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
