import urllib.request
import re
import imghdr
from PIL import Image
import requests

def url_image_download(url, save_pass):
    """URL先の画像をダウンロード。"""
    response = requests.get(url, timeout=(3.0, 7.5))
    image = response.content
    with open(save_pass, "wb") as download_img:
        return download_img.write(image)

def tenpu_image_download(url, save_pass):
    """添付画像をダウンロード。"""
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, save_pass)
    return

def download_image_class(message, save_pass):
    """
    messageにhttpという文言が含まれていれば、httpに続く文字列をURLと解釈し、画像をダウンロード
    でなければ、messageに添付されたファイルをダウンロードする
    ダウンロード位置はsave_passでパスを指定する
    """
    words = ["http"]
    for word in words:
        if word in message.content:
            url = message.content
            url = re.search(r"http.*", url, flags=re.DOTALL)
            url = url.group(0)  # メッセージからhttpを含む、http以下の文字を取り出してURLにしている
            url_image_download(url, save_pass)
        else:
            url = message.attachments[0].url
            tenpu_image_download(url, save_pass)