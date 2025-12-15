import ipywidgets as widgets
from IPython.display import display, Javascript
import base64
import os
import mimetypes


class ColabFileDownloader(widgets.VBox):
    """
    Download files from the kernel to the local machine via an ipywidgets button.

    **Parameters**

    file_path : str
        Path to the file to download from the kernel.

    **Usage**

    ColabFileDownloader("data/my_plot.png")

    **Notes**

    - Intended for small files only.
    - Large files are not recommended due to browser and kernel limitations.
    """

    def __init__(self, file_path, **kwargs):
        self.file_path = file_path

        # Validate file exists
        if not self.file_path or not os.path.exists(self.file_path):
            # File not found - disable button
            button_desc = "File Not Found"
            self.button = widgets.Button(description=button_desc, disabled=True)
            self.progress = widgets.IntProgress(
                value=0, min=0, max=100, description="Progress:", bar_style="info"
            )
            self.progress.layout.visibility = "hidden"
            super().__init__([self.button, self.progress])
            print(f"File not found: {self.file_path}")
            return

        # File exists - show info and enable button
        file_size = os.path.getsize(self.file_path)
        file_name = os.path.basename(self.file_path)
        print(f"File: {file_name} (Size: {file_size / (1024 * 1024):,.2f} Mb)")

        # Create button
        button_desc = kwargs.get("description", "Download File")
        self.button = widgets.Button(description=button_desc)
        self.button.on_click(self._handle_download)

        # Create progress bar (hidden initially)
        self.progress = widgets.IntProgress(
            value=0, min=0, max=100, description="Progress:", bar_style="info"
        )
        self.progress.layout.visibility = "hidden"

        # Create VBox with button and progress
        super().__init__([self.button, self.progress])

    def _handle_download(self, b):
        """
        Reads the file, encodes it, and sends it to the browser.
        """
        try:
            # 2. Update button text to show activity
            original_desc = self.button.description
            self.button.description = "Downloading..."
            self.button.disabled = True
            self.progress.layout.visibility = "visible"
            self.progress.value = 0

            # 3. Guess MIME type
            mime_type, _ = mimetypes.guess_type(self.file_path)
            if mime_type is None:
                mime_type = "application/octet-stream"
            self.progress.value = 10

            # 4. Read file and encode to Base64 with progress
            file_size = os.path.getsize(self.file_path)
            chunk_size = 1024 * 1024  # 1MB chunks
            file_data = bytearray()

            with open(self.file_path, "rb") as f:
                bytes_read = 0
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    file_data.extend(chunk)
                    bytes_read += len(chunk)
                    # Update progress 10-60%
                    self.progress.value = 10 + int((bytes_read / file_size) * 50)

            # 5. Encode to base64
            self.progress.value = 70
            b64_data = base64.b64encode(bytes(file_data)).decode()
            self.progress.value = 90

            filename = os.path.basename(self.file_path)

            # 6. Trigger Download using JS
            js_payload = f"""
            var a = document.createElement('a');
            a.href = 'data:{mime_type};base64,{b64_data}';
            a.download = '{filename}';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            """

            display(Javascript(js_payload))

            # 7. Restore button state
            self.progress.value = 100
            self.progress.bar_style = "success"
            self.button.description = original_desc
            self.button.disabled = False

        except Exception as e:
            self.button.description = "Failed"
            self.progress.bar_style = "danger"
            print(f"Download failed: {e}")
            self.button.disabled = False
