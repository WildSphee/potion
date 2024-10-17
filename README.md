# Potion: A Gen-AI Tool to Create PowerPoint Presentations

Potion is a generative AI tool designed to create PowerPoint presentations (PPTX files) based on user input. It helps you:

- **Boost Creativity**: Generate presentation skeletons to kickstart your ideas.
- **Accelerate Development**: Save time by automating slide creation.
- **Enhance Productivity**: Quickly produce presentations that are easily customizable.
- **Flexibility**: Easily replicable and adaptable to different platforms.

## Features

- Generate PowerPoint presentations from text descriptions.
- Use AI to design slides and compose content.
- Start a FastAPI server for API access.
- Analyze and dissect PPTX files for development purposes.

## Installation

1. **Clone the Repository**

```
git clone https://github.com/WildSphee/potion
cd potion
```

2. **Install Poetry**

```
pip install poetry
```

3. **Install Dependencies**

```
poetry install
```

4. **Start the API Server**

To run the API server, execute:

```sh
sh scripts/start.sh
```

## Configuration

Create a `.env` file in the root directory with the following format:

```py
OPENAI_API_KEY=<start with sk-> 

# Replicate Image Generation
REPLICATE_API_TOKEN= 

# PPT Output folder
PPT_OUTPUT_FOLDER=output/
# Image Output folder
IMAGE_OUTPUT_FOLDER=output/
```

Replace the placeholders with your actual API keys and desired output folders.

## Usage

### Generate a PowerPoint Presentation

You can generate a PowerPoint presentation first by selecting a predefined potion object, in this example `ncsgpt_potion` is used:

```py
from ncsgpt_potion import ncspotion
from potion import DesignSchema

user_input = ```Your presentation content here.```

design = await ncspotion.design(user_input, 1)
await ncspotion.compose(design)
path = ncspotion.save(design[0].desc)

print(path)
```

This will start a FastAPI server on port 8888. Access it at `<IP>:8888/create-ppt/` to create presentations via the API.

### Development Tools

- **Linting**

For code linting, run:

```sh
sh scripts/lint.sh
```

- **Dissecting PPTX Files**

To analyze the shapes and format of a PPTX object, use:

```sh
python scripts/dissect_pptx.py --<file_path>
```

## Contributing

Contributions are welcome! Please follow these guidelines:

- **Fork the Repository**: Create a personal fork of the project.
- **Create a Feature Branch**: Work on your feature or bugfix in a new branch.
- **Write Clear Commit Messages**: Keep your commit messages concise and descriptive.
- **Code Style and Linting**: Ensure your code adheres to the project's coding standards.

### Linting Practices

We use linting to maintain code quality and consistency. Before submitting a pull request, run the linter:

```sh
sh scripts/lint.sh
```

This script checks the code for stylistic errors and enforces coding standards.

### Pull Requests

- **Submit PRs to the `master` Branch**: Make sure your pull request targets the `master` branch.
- **Describe Your Changes**: Provide a clear description of your changes and the problem they solve.
- **Review Process**: Your pull request will be reviewed by maintainers. Please address any feedback promptly.

## Contact

For any questions or suggestions, feel free to open an issue or contact the maintainers.
