# Initializing a Git Repository and Pushing to GitHub

## Initializing a Local Repository

1.  **Navigate to your project directory:**
    Open your terminal and use the `cd` command to move into the directory you want to turn into a Git repository.

    ```bash
    cd /path/to/your/project
    ```

2.  **Initialize the repository:**
    Run the following command.

    ```bash
    git init
    ```

    This command creates a new `.git` subdirectory in your current directory, which contains all the necessary repository files. After running this command, you can start using Git to track your project's files.

## Pushing to GitHub

After initializing the repository, here are the steps to add your files to GitHub:

1.  **Stage your files for the first commit.** This tells Git which files to include in the commit. To add all files in the current directory, use:
    ```bash
    git add .
    ```

2.  **Commit the staged files.** This saves a snapshot of your files to your local repository.
    ```bash
    git commit -m "Initial commit"
    ```

3.  **Create a new repository on GitHub.**
    *   Go to [https://github.com/new](https://github.com/new).
    *   Give your repository a name (usually the same as your project folder).
    *   You can add a description.
    *   **Important:** Do *not* initialize the repository with a README, .gitignore, or license file on GitHub at this stage, as you already have a local repository.
    *   Click "Create repository".

4.  **Link your local repository to the one on GitHub.**
    On the next page on GitHub, you'll see a repository URL. Copy it. Then, in your terminal, run this command, replacing `<repository_url>` with the URL you copied:
    ```bash
    git remote add origin <repository_url>
    ```
    This sets up a "remote" named `origin` that points to your GitHub repository.

5.  **Push your local commits to GitHub.**
    This sends your committed files to your GitHub repository.
    ```bash
    git push -u origin main
    ```
    (Note: Your default branch might be named `master` instead of `main`. If `main` doesn't work, try `master`.)

After these steps, your files will be on GitHub.
