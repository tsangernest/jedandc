import ollama
import sys
from PIL import Image
import pymupdf
from pydantic import BaseModel
from pytesseract import image_to_string, image_to_data

from pprint import pprint


DOCS_DIR: str = f"../data"


class Receipt(BaseModel):
    attributes: dict


def query_ollama():
    doc_receipt = pymupdf.open(filename=f"{DOCS_DIR}/receipt-from-costco-ca-website.pdf")

    if not doc_receipt.page_count:
        print(f"\nNo Image found! Bailing hard")
        sys.exit(0)

    name = (
        doc_receipt
        .name
        .rsplit(sep="/", maxsplit=1)[-1]
        .split(sep=".", maxsplit=1)[0]
    )
    for page in doc_receipt:
        pic_receipt = page.get_pixmap(dpi=300)
        pic_receipt.save(f"{DOCS_DIR}/{name}-page-%i.png" % page.number)

    # print(image_to_data(image=f"{DOCS_DIR}/{name}.png", lang="eng"))
    print(image_to_string(Image.open(f"{DOCS_DIR}/{name}-page-0.png"), lang="eng"))

    breakpoint()

    # print(f"\n***\nQuerying Ollama\n***\n")
    # content = "Describe image as accurately as possible. Use and lean on OCR more than yourself."
    #
    # format_req = ".\nReturn as JSON. without newline characters."
    # response = ollama.chat(
    #     model="gemma3:12b",
    #     format=Receipt.model_json_schema(),
    #     messages=[{
    #         "role": "user",
    #         "content": f"{content}{format_req}",
    #         "images": [f"{DOCS_DIR}/receipt-low-film.png",],
    #     }],
    # )
    #
    # print(f"\nOllama response")
    # ollama_response = Receipt.model_validate_json(response.message.content)
    # pprint(ollama_response)
    # print(f"\n{response['total_duration']=}\n\n")


if __name__ == "__main__":
    query_ollama()
    print(f"\n***\nEnd of Processing\n***\n")

