from PIL import Image
import io


def image_to_byte_array(image: Image) -> bytes: # Pillow 이미지를 bytes로 변환하는 함수
  # BytesIO is a file-like buffer stored in memory
  imgByteArr = io.BytesIO()
  # image.save expects a file-like as a argument
  image.save(imgByteArr, format=image.format)
  # Turn the BytesIO object back into a bytes object
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


def get_pd_price(split_result_list, name_idx): # 가격 추출
  for block in split_result_list[name_idx:]:
    # if any(temp.isdigit() for temp in block): # 1000원 이하 가격 추출
    if (',' in block or '.' in block) and (2 < len(block) < 16):  # 1000원 이상 가격 추출
      price = ""
      for letter in block:
        if letter.isdigit():
          price += letter
      try:
        price = int(price)
        return price
      except:
        continue
    else:
      continue
  return 'fail'