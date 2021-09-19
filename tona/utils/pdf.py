import os
import subprocess
import base64

def build_pdf(storage, name, header, body, footer, **kwargs):
    fpath = storage
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    fheader = header
    fbody = body
    ffooter = footer
    contents = {'header': header, 'body': body, 'footer': footer}
    for content in contents:
        if not os.path.exists(contents.get(content)):
            ptmp = os.path.join(fpath, f"pdf_{content}.html")
            with open(ptmp, "w", encoding='utf-8') as f:
                f.write(contents.get(content))
                f.close()
            if content == 'header':
                fheader = ptmp
            elif content == 'body':
                fbody = ptmp
            elif content == 'footer':
                ffooter = ptmp
    fpath = os.path.join(fpath, name)
    args = [
        "wkhtmltopdf", fbody,
        "--footer-html", ffooter,
        "--header-html", fheader,
        fpath
    ]
    subprocess.run(args)
    is_base64 = kwargs.get("b64", False)
    if is_base64:
        with open(fpath, 'rb') as csvfile:
            return base64.b64encode(csvfile.read())
    return fpath
