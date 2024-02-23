# qrlogo

Create QR codes for URLs and automatically add the favicon logo to the QR code

## Installation

```bash
git clone git@github.com:RhetTbull/qrlogo.git
cd qrlogo
pip install -r requirements.txt
```

## Usage

```
Usage: qrlogo.py [OPTIONS]

  Create QR codes with logos.

  If no logo is provided, try to fetch the favicon from the provided URL.

  Logo may also be added to the QR code using the --logo option.

  Use --no-logo to create a regular QR code without a logo.

Options:
  --url TEXT     URL to encode into the QR code  [required]
  --logo PATH    Path to the logo file
  --no-logo      No logo on QR code
  --output TEXT  Output filename  [required]
  --help         Show this message and exit.
```

## Example

```bash
python3 qrlogo.py --url https://github.com/RhetTbull/qrlogo --output qrlogo.png
```

Produces a QR code with the GitHub favicon in the center:

![qrlogo](qrlogo.png)

## License

MIT License
