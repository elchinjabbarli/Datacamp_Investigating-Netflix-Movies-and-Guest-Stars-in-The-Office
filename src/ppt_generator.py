import os
from pptx import Presentation
from pptx.util import Inches, Pt
from typing import Dict, Any, List, Optional
import logging

class PPTGenerator:
    """
    Handles PowerPoint generation using a master template.
    """
    def __init__(self, template_path: Optional[str] = None):
        if template_path and os.path.exists(template_path):
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()
            logging.warning("Template not found or not provided. Using default layout.")

    def _get_layout_by_name(self, name: str):
        """
        Tries to find a slide layout by name, defaults to index 1 if not found.
        """
        for layout in self.prs.slide_layouts:
            if name.lower() in layout.name.lower():
                return layout
        return self.prs.slide_layouts[1] # Default to Title and Content

    def create_presentation(self, structure: Dict[str, Any], images: List[str], output_path: str):
        """
        Creates a .pptx file based on the provided structure and images.
        """
        # If there's a title slide in structure
        title_text = structure.get("presentation_title", "Yeni Sunum")

        for slide_data in structure.get("slides", []):
            layout_name = slide_data.get("layout", "Title and Content")
            layout = self._get_layout_by_name(layout_name)
            slide = self.prs.slides.add_slide(layout)

            # Set Title
            title_placeholder = slide.shapes.title
            if title_placeholder:
                title_placeholder.text = slide_data.get("title", "")

            # Set Content (Bullet points)
            body_placeholder = None
            for shape in slide.placeholders:
                if shape.placeholder_format.type == 2: # Body/Object placeholder
                    body_placeholder = shape
                    break

            if body_placeholder:
                tf = body_placeholder.text_frame
                content = slide_data.get("content", [])
                if isinstance(content, list):
                    for i, line in enumerate(content):
                        if i == 0:
                            tf.text = line
                        else:
                            p = tf.add_paragraph()
                            p.text = line
                            p.level = 0
                else:
                    tf.text = str(content)

            # Add Image if specified
            img_index = slide_data.get("image_index")
            if img_index is not None and 0 <= img_index < len(images):
                img_path = images[img_index]
                self._add_image_to_slide(slide, img_path)

        self.prs.save(output_path)
        return output_path

    def _add_image_to_slide(self, slide, img_path):
        """
        Adds an image to a slide. Tries to find a picture placeholder,
        otherwise places it in a default position.
        """
        # Try to find a picture placeholder
        placeholder = None
        for shape in slide.placeholders:
            if "picture" in shape.name.lower() or shape.placeholder_format.type == 18: # Picture placeholder
                placeholder = shape
                break

        if placeholder:
            # Replace placeholder with image
            placeholder.insert_picture(img_path)
        else:
            # Add image to a default position (e.g., right side or bottom)
            # This is a fallback
            left = Inches(5)
            top = Inches(2)
            width = Inches(4)
            slide.shapes.add_picture(img_path, left, top, width=width)
