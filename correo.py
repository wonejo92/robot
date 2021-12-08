# Install Courier SDK: pip install trycourier
from trycourier import Courier

def send_email(email : str, token: str):
    client = Courier(auth_token="dk_prod_BYG6JKS8WD4503QQCH9T74J0RN8P")

    resp = client.send(
      event="KTF9WC1REMMNMCQY05E0Z4BS5R5D",
      recipient="debe4413-2695-48ec-b0ac-c49b194ea923",
      brand="QTG5PM1QQSMBT1HJGVBC9TEQ7SNP",
      profile={
        "email": email,
      },
      data={
        "codigo": token,
      },
    )

    #print(resp['messageId'])