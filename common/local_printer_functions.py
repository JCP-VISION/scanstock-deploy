import logging
import platform
import subprocess
import tempfile
# ADD get_priority_config HERE!
from PIL import Image, ImageDraw, ImageFont, ImageWin
import barcode
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")

def get_target_printer_name():
    """
    Finds the target printer name. 
    First checks get_priority_config for 'local_printer_name'.
    If not found, searches available printers and skips common virtual printers.
    Falls back to the default printer.
    """
    from common.project_config import get_priority_config

    # 1. Check config
    config_printer = get_priority_config(
        path="tool.configs",
        key="local_printer_name",
        default=None,
        data_type=str
    )  # NOTE: NOT ADDED DELETE!
    if config_printer:
        return config_printer

    system = platform.system()
    if system == "Windows":
        try:
            import win32print

            # 2. Try to find a real printer (skip virtual ones)
            flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            printers = win32print.EnumPrinters(flags)

            skip_keywords = ["pdf", "xps", "onenote", "fax"]

            for printer in printers:
                # printer is a tuple, printer[2] is the printer name
                p_name = printer[2]
                is_virtual = any(kw in p_name.lower() for kw in skip_keywords)
                if not is_virtual:
                    logging.info(f"Auto-selected non-virtual printer: {p_name}")
                    return p_name

            # 3. Fallback to default
            return win32print.GetDefaultPrinter()
        except Exception as e:
            logging.error(f"Error enumerating printers: {e}")

    return None

def get_all_printers():
    """
    Returns a list of all available physical printers connected to the local server.
    Filters out common virtual drivers (PDF, XPS, etc.) to keep the list clean.
    """
    system = platform.system()
    printers_list = []

    if system == "Windows":
        try:
            import win32print
            flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            printers = win32print.EnumPrinters(flags)

            skip_keywords = ["pdf", "xps", "onenote", "fax"]

            for printer in printers:
                p_name = printer[2]
                is_virtual = any(kw in p_name.lower() for kw in skip_keywords)
                if not is_virtual:
                    printers_list.append(p_name)

        except Exception as e:
            logging.error(f"Error enumerating printers for list: {e}")

    elif system == "Linux":
        try:
            output = subprocess.check_output(["lpstat", "-a"], text=True)
            for line in output.splitlines():
                if line:
                    p_name = line.split()[0]
                    printers_list.append(p_name)
        except Exception as e:
            logging.error(f"Error enumerating Linux printers: {e}")

    return sorted(printers_list)

def get_local_printer_size(printer_name=None):
    """
    Detect the specified printer (or target printer) and return its printable width and height.

    On Windows, this uses win32print and win32ui to query the printer
    device context and determine the printable area.

    Returns
    -------
    tuple[int, int]
        Printable width and height in pixels.
    """
    system = platform.system()

    if system == "Windows":
        try:
            import win32print
            import win32ui

            if not printer_name:
                printer_name = get_target_printer_name() or win32print.GetDefaultPrinter()

            logging.info(f"Printer selected for sizing: {printer_name}")

            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)

            width = hDC.GetDeviceCaps(8)
            height = hDC.GetDeviceCaps(10)

            logging.info(f"Printable width: {width}")
            logging.info(f"Printable height: {height}")

            hDC.DeleteDC()

            if width > 0 and height > 0:
                return width, height

        except Exception as e:
            logging.error(f"Printer size detection failed: {e}")

    return 812, 1218  # DEFAULT_WIDTH, DEFAULT_HEIGHT

def is_qr_data(data):
    """
    Detect whether the data should be encoded as a QR code
    rather than a 1D barcode.

    Returns True if the data contains the AUTH:JCV marker
    (user login QR codes, delimited by commas or pipes).
    """
    return 'AUTH:JCV' in data

def create_barcode(data):
    """
    Generate a Code128 barcode image from a given string value.

    Parameters
    ----------
    data : str
        The value to encode into the barcode.

    Returns
    -------
    str
        File path of the generated barcode image.

    Notes
    -----
    Uses python-barcode with ImageWriter to create a PNG file.
    The text rendering below the barcode is disabled so only
    the barcode graphic is produced.
    """

    writer = ImageWriter()
    writer.write_text = False

    code128 = barcode.get("code128", data, writer=writer)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    filename = temp_file.name
    temp_file.close()

    saved = code128.save(filename)

    return saved

def create_barcode_image(barcode_data, custom_subtitle=None):
    """
    Render a Code128 barcode as a PIL image, optionally with custom subtitle text.
    """
    my_barcode = Code128(barcode_data, writer=ImageWriter())

    if custom_subtitle is not None:
        my_barcode.get_fullcode = lambda: custom_subtitle

    return my_barcode.render()

def create_barcode_with_subtitle(data, custom_subtitle):
    """
    Generate a Code128 barcode image file with explicit subtitle text.
    """
    barcode_img = create_barcode_image(data, custom_subtitle=custom_subtitle)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    filepath = temp_file.name
    temp_file.close()

    barcode_img.save(filepath)
    logging.info(f"Code128 barcode with subtitle created: {filepath}")
    return filepath

def create_qrcode(data):
    """
    Generate a QR code image from a given string value.

    Parameters
    ----------
    data : str
        The value to encode into the QR code.

    Returns
    -------
    str
        File path of the generated QR code PNG image.
    """
    qr = qrcode.QRCode(
        version=None,  # auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    filepath = temp_file.name
    temp_file.close()

    img.save(filepath)
    logging.info(f"QR code created: {filepath}")
    return filepath

def is_login_barcode_override_enabled():
    """
    Returns True when login barcode override is enabled in config.
    """
    try:
        from common.project_config import get_priority_config
        return get_priority_config(
            path="tool.configs",
            key="login_barcode_override",
            default=False,
            data_type=bool,
        )
    except Exception as e:
        logging.error(f"Unable to read login_barcode_override config: {e}")
        return False

def create_code_image(data, code_type=None, custom_subtitle=None, login_barcode_override=None):
    """
    Auto-detect and generate the appropriate code image
    (QR code or 1D barcode) based on the data content.
    """
    normalized_code_type = (code_type or "auto").strip().lower()

    if normalized_code_type == "barcode":
        if custom_subtitle:
            logging.info("Explicit code_type=barcode with custom subtitle")
            return create_barcode_with_subtitle(data, custom_subtitle=custom_subtitle)
        logging.info("Explicit code_type=barcode")
        return create_barcode(data)

    if normalized_code_type == "qr":
        logging.info("Explicit code_type=qr")
        return create_qrcode(data)

    if login_barcode_override is None:
        login_barcode_override = is_login_barcode_override_enabled()

    if login_barcode_override and is_qr_data(data):
        logging.info("login_barcode_override enabled: forcing Code128 for QR-style data")
        return create_barcode_with_subtitle(data, custom_subtitle="LOGIN CREDENTIALS")

    if is_qr_data(data):
        return create_qrcode(data)
    return create_barcode(data)

def create_label(barcode_path, printer_w, printer_h):
    """
    Create a printable label image containing the barcode.

    Parameters
    ----------
    barcode_path : str
        Path to the generated barcode image.
    printer_w : int
        Printable width of the target printer.
    printer_h : int
        Printable height of the target printer.

    Returns
    -------
    str
        File path to the generated label image.

    Notes
    -----
    The barcode is rotated only when the printer is in portrait
    orientation so the bars align with the printer feed direction.
    The barcode is then scaled and centered on the label.
    """

    WIDTH = printer_w
    HEIGHT = printer_h

    logging.info(f"Label canvas: {WIDTH} x {HEIGHT}")

    label = Image.new("RGB", (WIDTH, HEIGHT), "white")

    barcode_img = Image.open(barcode_path)

    img_w, img_h = barcode_img.size
    is_square = abs(img_w - img_h) < max(img_w, img_h) * 0.1  # QR codes are square

    if is_square:
        # QR code: keep it square, fit within the label
        max_size = int(min(WIDTH, HEIGHT) * 0.85)
        barcode_img = barcode_img.resize((max_size, max_size))
        barcode_x = (WIDTH - max_size) // 2
        barcode_y = (HEIGHT - max_size) // 2
    else:
        # 1D barcode: original stretch logic
        if printer_h > printer_w:
            barcode_img = barcode_img.rotate(90, expand=True)

        barcode_height = int(HEIGHT * 0.65)
        barcode_width = int(WIDTH * 0.6)
        barcode_img = barcode_img.resize((barcode_width, barcode_height))
        barcode_x = (WIDTH - barcode_width) // 2
        barcode_y = (HEIGHT - barcode_height) // 2

    label.paste(barcode_img, (barcode_x, barcode_y))

    temp_label = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    label_path = temp_label.name
    temp_label.close()

    label.save(label_path)

    logging.info(f"Label created: {label_path}")

    return label_path

def print_local_label(file_path, printer_name=None):
    """
    Send the generated label image to the default printer.

    Parameters
    ----------
    file_path : str
        Path to the label image file that should be printed.
    printer_name: str, optional
        Name of the printer to use.

    Notes
    -----
    On Windows this uses the Win32 printing API through
    win32print and win32ui. The image is drawn onto the
    printer device context using ImageWin.Dib.

    On Linux, the function falls back to using the `lp`
    command to submit the print job.
    """

    system = platform.system()

    if system == "Windows":

        try:
            import win32print
            import win32ui

            if not printer_name:
                printer_name = get_target_printer_name() or win32print.GetDefaultPrinter()

            logging.info(f"Printing using Windows GDI to: {printer_name}")

            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)

            printable_w = hDC.GetDeviceCaps(8)
            printable_h = hDC.GetDeviceCaps(10)

            bmp = Image.open(file_path)

            img_w, img_h = bmp.size

            logging.info(f"Printer area: {printable_w} x {printable_h}")
            logging.info(f"Image size: {img_w} x {img_h}")

            x = int((printable_w - img_w) / 2)
            y = int((printable_h - img_h) / 2)

            hDC.StartDoc("ScanStock Label")
            hDC.StartPage()

            dib = ImageWin.Dib(bmp)

            dib.draw(
                hDC.GetHandleOutput(),
                (x, y, x + img_w, y + img_h)
            )

            hDC.EndPage()
            hDC.EndDoc()

            hDC.DeleteDC()

            logging.info("Print job completed")

        except Exception as e:
            logging.error(f"Windows printing failed: {e}")

    elif system == "Linux":

        try:
            if printer_name:
                subprocess.run(["lp", "-d", printer_name, file_path])
            else:
                subprocess.run(["lp", file_path])
        except Exception as e:
            logging.error(f"Linux printing failed: {e}")

def print_local_barcode_label(barcode_value, printer_name=None, code_type=None, custom_subtitle=None):
    """
    High-level function to generate and print a barcode/QR label.

    Parameters
    ----------
    barcode_value : str
        Value to encode in the barcode or QR code.
    printer_name: str
        Target valid printer instance string. Optional override.

    Workflow
    --------
    1. Detect printer printable area.
    2. Generate barcode or QR code image (auto-detected).
    3. Build a label image with correct orientation.
    4. Send the label to the printer.
    """

    target_printer = printer_name if printer_name else get_target_printer_name()
    width, height = get_local_printer_size(target_printer)

    code_path = create_code_image(
        barcode_value,
        code_type=code_type,
        custom_subtitle=custom_subtitle,
    )

    label_path = create_label(
        code_path,
        width,
        height
    )

    print_local_label(label_path, target_printer)
