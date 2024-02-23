"""Create QR codes with logos."""

from __future__ import annotations

import re
import urllib.parse
from io import BytesIO

import click
import qrcode
import requests
from bs4 import BeautifulSoup
from PIL import Image


def fetch_icon(url: str) -> Image.Image | None:
    """Fetch favicon from the provided URL."""
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        icon_link = soup.find("link", attrs={"rel": re.compile(r"\bicon\b")})
        if icon_link is not None:
            logo_url = urllib.parse.urljoin(url, icon_link["href"])
            logo_res = requests.get(logo_url)
            return Image.open(BytesIO(logo_res.content))
    except Exception:
        return None


@click.command()
@click.option("--url", required=True, help="URL to encode into the QR code")
@click.option(
    "--logo", "logo_path", default=None, type=click.Path(), help="Path to the logo file"
)
@click.option("--no-logo", is_flag=True, default=False, help="No logo on QR code")
@click.option("--output", required=True, help="Output filename")
def qrlogo(url, logo_path, no_logo, output):
    """Create QR codes with logos.
    
    If no logo is provided, try to fetch the favicon from the provided URL.
    
    Logo may also be added to the QR code using the --logo option.
    
    Use --no-logo to create a regular QR code without a logo.
    """
    if no_logo and logo_path is not None:
        raise click.UsageError(
            "Invalid option: --logo_path cannot be used together with --no-logo."
        )

    logo_image = None

    # Get favicon if logo is not provided
    if not no_logo and logo_path is None:
        logo_image = fetch_icon(url)
        if logo_image is None:
            base_url = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(url))
            logo_image = fetch_icon(base_url)

        if logo_image is None:
            print(
                "Warning: Favicon not found for the provided URL. Outputting a regular QR code without logo."
            )

    if logo_path is not None:
        logo_image = Image.open(logo_path)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Adding logo
    if logo_image is not None:
        base = img.copy()

        # Calculate width and height of the QR code
        qr_width, qr_height = base.size

        # Calculate width and height of the logo
        logo_width, logo_height = logo_image.size

        factor = 4
        size_width = qr_width // factor
        size_height = qr_height // factor

        if logo_width > logo_height:
            logo_height = logo_height * size_width // logo_width
            logo_width = size_width
        else:
            logo_width = logo_width * size_height // logo_height
            logo_height = size_height

        logo_image = logo_image.resize((logo_width, logo_height))
        position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)
        base.paste(logo_image, position, logo_image)
        img = base

    # Save file
    img.save(output)


if __name__ == "__main__":
    qrlogo()

