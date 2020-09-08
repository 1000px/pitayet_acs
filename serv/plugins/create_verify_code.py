import random, string
from PIL import Image, ImageDraw, ImageFont
def gene_text():
  # 生成4位验证码
  return ''.join(random.sample(string.ascii_letters + string.digits, 4))

def rnd_color():
  # 随机颜色
  return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
def draw_lines(draw, num, width, height):
  for num in range(num):
    x1 = random.randint(0, width / 2)
    y1 = random.randint(0, height / 2)
    x2 = random.randint(0, width)
    y2 = random.randint(height / 2, height)
    draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

def create_verify_code():
  # 生成验证码图形
  code = gene_text()
  # 图片大小
  width, height = 120, 48
  # 新图片对象
  img = Image.new('RGB', (width, height), 'white')
  # 字体
  font = ImageFont.truetype('app/static/arial.ttf', 40)
  # draw对象
  draw = ImageDraw.Draw(img)
  # 绘制字符串
  for item in range(4):
    draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
      text=code[item], fill=rnd_color(), font=font)
  draw_lines(draw, 6, width, height)
  return img, code
