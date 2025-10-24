# Examples for algomanim

## Where to find the examples folder

The `examples/` folder is **not included** when you install algomanim via pip or poetry.  
It is available only in the source repository.

To access the examples, clone the full repository from GitHub **inside the same environment** where you installed algomanim:

```sh
git clone https://github.com/benabub/algomanim.git
```

This will create an `algomanim/` folder with the `examples/` directory inside it.  
Make sure to run the example scripts from within this cloned folder, and that your Python environment has algomanim installed.

> **Note:**  
> You do not actually need the entire repository for running examples — only the `examples/` folder is required.  
> As long as the `examples/` folder is located somewhere within your Python environment (where algomanim is installed), the examples will work.

## How to run an example

1. **Find the Example class**  
   Open `examples/examples.py` and look for the `Example<ClassName>` scene you want to render.  
   The part after `Example` (for example, `Array` in `ExampleArray`) is the class name you will use as an argument.

2. **Choose a script**  
   - Use `rend_poetry.sh` if you installed algomanim with Poetry.  
     _No need to activate a virtual environment manually; the script uses `poetry run`._
   - Use `rend_no_poetry.sh` if you installed algomanim with pip or are using a manually activated virtual environment.  
     _You must activate your venv before running this script._

3. **Run the script**

   ```sh
   # Usage: ./rend_poetry.sh -l|-m|-h class_name
   # (-l: low quality, -m: medium quality, -h: high quality)
   # (class_name: without 'Example', case-insensitive)
   ./rend_poetry.sh -l array
   ./rend_poetry.sh -m Array
   ./rend_poetry.sh -h aRrAy
   ```

   The rendered video will appear in the corresponding `video_output/<quality>/` folder.

## Output

- Videos are saved in `examples/video_output/<quality>/` (e.g., `low_quality/array.mp4`).
