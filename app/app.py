import os
import json


class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}"

    def to_dict(self):
        """Convert the Post instance to a dictionary."""
        return {"title": self.title, "content": self.content}

    @staticmethod
    def from_dict(data):
        """Create a Post instance from a dictionary."""
        return Post(data["title"], data["content"])


class PostManager:
    DEFAULT_FOLDER = "saved_posts"
    DEFAULT_FILE = "posts.json"

    def __init__(self):
        self.posts = {}

    def save_to_json(self, folder_path=None):
        """Save all posts to a JSON file."""
        folder_path = folder_path or self.DEFAULT_FOLDER
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, self.DEFAULT_FILE)

        try:
            with open(file_path, "w") as file:
                json.dump({title: post.to_dict() for title, post in self.posts.items()}, file, indent=4)
            print(f"Posts saved to '{file_path}'.")
        except Exception as e:
            print(f"Error saving posts: {e}")

    def load_from_json(self, folder_path=None):
        """Load posts from a JSON file."""
        folder_path = folder_path or self.DEFAULT_FOLDER
        file_path = os.path.join(folder_path, self.DEFAULT_FILE)

        try:
            with open(file_path, "r") as file:
                self.posts = {title: Post.from_dict(data) for title, data in json.load(file).items()}
            print(f"Posts loaded from '{file_path}'.")
        except FileNotFoundError:
            print(f"No posts found at '{file_path}'.")
        except Exception as e:
            print(f"Error loading posts: {e}")

    def create_post(self, title, content, folder_path=None):
        """Create a new post."""
        if not title.strip() or not content.strip():
            print("Title and content cannot be empty.")
            return

        if title in self.posts:
            print(f"A post with the title '{title}' already exists.")
            return

        self.posts[title] = Post(title, content)
        print(f"Post '{title}' created successfully.")
        self.save_to_json(folder_path)

    def read_post(self, title):
        """Read a post by title."""
        post = self.posts.get(title)
        if post:
            print(post)
        else:
            print(f"No post found with the title '{title}'.")

    def update_post(self, title, new_content, folder_path=None):
        """Update the content of an existing post."""
        if title in self.posts:
            self.posts[title].content = new_content
            print(f"Post '{title}' updated successfully.")
            self.save_to_json(folder_path)
        else:
            print(f"No post found with the title '{title}'.")

    def delete_post(self, title, folder_path=None):
        """Delete a post by title."""
        if title in self.posts:
            del self.posts[title]
            print(f"Post '{title}' deleted successfully.")
            self.save_to_json(folder_path)
        else:
            print(f"No post found with the title '{title}'.")

    def search_posts(self, keyword):
        """Search posts by a keyword."""
        results = [post for post in self.posts.values() if keyword.lower() in post.title.lower() or keyword.lower() in post.content.lower()]
        if results:
            print(f"Posts matching '{keyword}':")
            for post in results:
                print(f"- {post.title}")
        else:
            print(f"No posts found matching '{keyword}'.")

    def show_all_posts(self):
        """Display all post titles."""
        if self.posts:
            print("All Posts:")
            for title in self.posts.keys():
                print(f"- {title}")
        else:
            print("No posts available.")

    def main(self):
        """Main loop for the Post Manager."""
        self.load_from_json()

        while True:
            print("\nPost Manager")
            print("1. Create Post")
            print("2. Read Post")
            print("3. Update Post")
            print("4. Delete Post")
            print("5. Search Posts")
            print("6. Show All Posts")
            print("7. Exit")

            choice = input("Choose an option (1-7): ").strip()

            if choice == "1":
                title = input("Enter the post title: ").strip()
                content = input("Enter the post content: ").strip()
                self.create_post(title, content)
            elif choice == "2":
                title = input("Enter the title of the post to read: ").strip()
                self.read_post(title)
            elif choice == "3":
                title = input("Enter the title of the post to update: ").strip()
                if title in self.posts:
                    new_content = input(f"Enter new content for '{title}': ").strip()
                    self.update_post(title, new_content)
                else:
                    print(f"No post found with the title '{title}'.")
            elif choice == "4":
                title = input("Enter the title of the post to delete: ").strip()
                self.delete_post(title)
            elif choice == "5":
                keyword = input("Enter a keyword to search: ").strip()
                self.search_posts(keyword)
            elif choice == "6":
                self.show_all_posts()
            elif choice == "7":
                print("Exiting Post Manager. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    PostManager().main()
