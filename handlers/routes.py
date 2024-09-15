import os
import logging
from flask import render_template, request, redirect, url_for
from modules import constants, utils, claude_client
import anthropic

def configure_routes(app):
    @app.route("/", methods=['GET'])
    def index():
        return render_template("index.html")

    @app.route("/process", methods=['POST'])
    def process():
        try:
            # Retrieve form data
            question = request.form['question']
            images = request.files.getlist('images')

            # Ensure the images directory exists
            constants.IMAGE_DIR.mkdir(parents=True, exist_ok=True)

            # Save uploaded images temporarily
            image_paths = []
            for image in images:
                if image.filename == '':
                    continue  # Skip if no file is selected
                image_path = constants.IMAGE_DIR / image.filename
                image.save(image_path)
                image_paths.append(image_path)

            # Load system prompt and instructions
            system_prompt = utils.load_file_content(constants.SYSTEM_PROMPT_PATH)

            # Prepare message content
            message_content = claude_client.prepare_claude_message(
                system_prompt, question, image_paths, constants.MEDIA_TYPES
            )

            # Create client and query Claude
            env_vars = utils.load_environment(['ANTHROPIC_API_KEY'])
            client = anthropic.Client(api_key=env_vars['ANTHROPIC_API_KEY'])
            result = claude_client.query_claude(
                client, "claude-3-5-sonnet-20240620", 8024, message_content
            )

            # Clean up temporary images
            for path in image_paths:
                if path.exists():
                    path.unlink()

            return render_template("result.html", result=result)
        except Exception as e:
            logging.error(f"Processing failed: {str(e)}")
            return render_template("error.html", error=str(e))

