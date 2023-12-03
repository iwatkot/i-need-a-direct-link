# I need a direct link

Simple Flask app to upload files and download them with a direct link.


<p align="center">
  <a href="https://ineedadirectlink.site">Website</a> •
  <a href="https://www.buymeacoffee.com/iwatkot0">Buy me a coffee</a> 
</p>

## Features

- Upload files, you will get a link and a file ID after upload.
- Download a file with its direct link.
- Delete a file with its file ID.


## Installation

1. Clone the repository.
2. Run `sh create_venv.sh` to create a virtual environment and install the dependencies.
3. VSCode launch configuration is included, so you can run the app with the debugger.
4. Edit image name in `sh create_docker.sh`.
5. Run `sh create_docker.sh` to create a Docker image.
6. Deploy the image to your server with `docker run -d -p 80:80 --name <container-name> <image-name>`.

### Example

![Example of uploading file](https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/287507244-bc97bcb7-6e8e-41f5-9034-f8a39bef622b.gif)