app.mount(
    "/images",
    StaticFiles(directory=image_dir),
    name="images"
)