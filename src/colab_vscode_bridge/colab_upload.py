import os
import ipywidgets as widgets
from IPython.display import display, clear_output


def upload_to_colab(destination_folder: str = "/content/uploads"):
    """
    Upload files from local machine to Google Colab using an interactive widget.

    Args:
        destination_folder: Directory path in Colab where files will be saved (default: '/content/uploads')

    Returns:
        FileUploader: Widget instance that handles the upload

    Usage:
        upload_to_colab()
        upload_to_colab("/content/data")
    """

    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Create file uploader widget
    file_uploader = widgets.FileUpload(accept="*", multiple=True)

    upload_progress = widgets.IntProgress(
        value=0,
        min=0,
        max=100,
        description="Uploading:",
        bar_style="info",
        orientation="horizontal",
    )
    upload_progress.layout.visibility = "hidden"

    output_area = widgets.Output()

    # Container for all widgets
    container = widgets.VBox([file_uploader, upload_progress, output_area])

    def on_upload_change(change):
        """Handle file upload"""
        if not change["new"]:
            return

        try:
            uploaded_files = change["new"]
            file_count = len(uploaded_files)

            if file_count == 0:
                return

            # Show progress bar
            upload_progress.layout.visibility = "visible"
            upload_progress.value = 0
            upload_progress.bar_style = "info"

            with output_area:
                clear_output(wait=True)

                saved_paths = []

                for idx, (filename, file_info) in enumerate(uploaded_files.items()):
                    content = file_info["content"]

                    # Update progress description
                    upload_progress.description = f"File {idx + 1}/{file_count}:"

                    # Save file to destination folder
                    file_path = os.path.join(destination_folder, filename)

                    with open(file_path, "wb") as f:
                        f.write(content)

                    saved_paths.append(file_path)

                    # Update progress
                    upload_progress.value = int(((idx + 1) / file_count) * 100)

                # Complete
                upload_progress.bar_style = "success"
                upload_progress.description = "Complete:"

                # Display results
                print(
                    f"Successfully uploaded {file_count} file(s) to: {destination_folder}\n"
                )
                print("Uploaded files:")
                for file_path in saved_paths:
                    file_size = os.path.getsize(file_path)
                    print(f"  - {file_path} ({file_size / 1024:.2f} KB)")

            # Clear the file uploader to reset it
            file_uploader.value.clear()
            file_uploader._counter = 0

        except Exception as e:
            upload_progress.bar_style = "danger"
            upload_progress.description = "Failed:"
            with output_area:
                clear_output(wait=True)
                print(f"Error during upload: {e}")

    # Attach event handler
    file_uploader.observe(on_upload_change, names="value")

    return container
