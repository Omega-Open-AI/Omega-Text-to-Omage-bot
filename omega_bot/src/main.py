import click
import asyncio
import dotenv
import os
from pathlib import Path
from .image_generator import ImageGenerator
from .async_generator import AsyncImageGenerator
from .utils import save_image, display_image, sanitize_path
from .exceptions import ImageGenerationError, SecurityError

dotenv.load_dotenv()

@click.group()
def cli():
    """Omega Text-to-Image Generator"""
    pass

@cli.command()
@click.option("--prompt", required=True, help="Text prompt for image generation")
@click.option("--output", default="output.png", help="Output file path")
@click.option("--no-display", is_flag=True, help="Skip image preview")
@click.option("--async", "async_flag", is_flag=True, help="Use async API")
def generate(prompt, output, no_display, async_flag):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise click.ClickException("OPENAI_API_KEY not found in .env")
    
    try:
        if async_flag:
            generator = AsyncImageGenerator(api_key)
            url = asyncio.run(generator.generate_batch([prompt]))[0]
        else:
            generator = ImageGenerator(api_key)
            url = generator.generate_image(prompt)
        
        save_image(url, output)
        if not no_display:
            display_image(output)
    except (ImageGenerationError, SecurityError) as e:
        raise click.ClickException(str(e))

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output-dir", default="./outputs", help="Output directory")
def batch(input_file, output_dir):
    """Process multiple prompts from a file"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise click.ClickException("OPENAI_API_KEY not found in .env")

    with open(input_file, 'r') as f:
        prompts = [line.strip() for line in f if line.strip()]

    generator = AsyncImageGenerator(api_key)
    urls = asyncio.run(generator.generate_batch(prompts))
    
    for idx, (prompt, url) in enumerate(zip(prompts, urls)):
        try:
            output_path = Path(output_dir) / f"output_{idx}.png"
            save_image(url, output_path)
            click.echo(f"Generated: {output_path}")
        except Exception as e:
            click.echo(f"Failed to save {prompt}: {str(e)}")

if __name__ == "__main__":
    cli()
