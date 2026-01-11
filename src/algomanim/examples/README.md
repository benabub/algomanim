# Examples for algomanim

## Where to find the examples folder

The examples/ module is included when you install algomanim via pip or poetry.

After installation, you can find the examples directory at:
```bash
.venv/lib/python3.x/site-packages/algomanim/examples/
```

## How to run an example

1. **Make scripts executable**  
    ```bash
    chmod +x rend_poetry.sh rend_no_poetry.sh
    ```

2. **Find the Example class**  
   Open `examples/examples.py` and look for the `Example<ClassName>` scene you want to render.  
   The part after `Example` (for example, `Array` in `ExampleArray`) is the class name you will use as an argument.

3. **Choose a script**  
   - Use `rend_poetry.sh` if you installed algomanim with Poetry.  
     _No need to activate a virtual environment manually; the script uses `poetry run`._
   - Use `rend_no_poetry.sh` if you installed algomanim with pip or are using a manually activated virtual environment.  
     _You must activate your venv before running this script._

4. **Run the script**

   ```sh
   # Usage: ./rend_poetry.sh -l|-m|-h class_name
   # (-l: low quality, -m: medium quality, -h: high quality)
   # (class_name: without 'Example_', case-insensitive, snake_case)
   ./rend_poetry.sh -l code_block
   ./rend_poetry.sh -m Code_Block
   ./rend_poetry.sh -h cOdE_BlOCK
   ```

   The rendered video will appear in the corresponding `video_output/<quality>/` folder.

## Output

- Videos are saved in `examples/video_output/<quality>/` (e.g., `low_quality/array.mp4`).
