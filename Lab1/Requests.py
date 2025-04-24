# -------------------------------------------------------- Requests ---------------------------------------------------------- #
'''
Requests is a simple and elegant HTTP , is used to make (POST , GET , PUT ,PATCH ,DELETE)
'''
import requests
from pydantic import BaseModel

class Product(BaseModel):
    id : int
    title : str
    price: float
    description: str
    category: str
    image: str

res = requests.get("https://fakestoreapi.com/products") # example of a get request to fakestoreapi to bring products
content = res.json()  # Parse the JSON content from the response

for prod in content:
    curr = Product(**prod)  # Create a Product instance using the parsed data
    print(curr.id)
    print(curr.title)
    print(curr.price)
    print(curr.description)
    print(curr.category)
    print(curr.image)


data = {"id" : 21,
    "title" : "just for test",
    "price": 18.2,
    "description": "alkjvboiuxcv",
    "category": "test",
    "image": 21
}
url = "https://fakestoreapi.com/products"

res = requests.post(url, json=data)

print(res.status_code) # if the post request pass fine the responce status code will be 200

url = "https://httpbin.org/delay/10"
try:
    res = requests.get(url,timeout=5) # timeout function is used to make some delay
except requests.exceptions.Timeout as err:
    print(err)
# this is used to make sure that request spent short util response

# # if you to send headers like authentication token just inject it as header in the request param
# auth_token = "XXXXXXXX"
# # here we set the authorization header with the 'bearer token' for authentication purposes.
# headers = {
#     "Authorization": f"Bearer {auth_token}"
# }

# url = "https://httpbin.org/headers"
# response = requests.get(url, headers=headers)
# print(response.json())


from bs4 import BeautifulSoup
#Web Scraping using requests 
url = "https://webscraper.io/test-sites/e-commerce/allinone/computers"

response = requests.get(url)
# print(response.content) # it prints all bundled html css and js code


# we usually use BeautifulSoup to parse html
soup = BeautifulSoup(response.content, "html.parser")
title = soup.title.text
content = soup.find("p").text
print(title, content)# it extract the element from the dom like javascript do

'''
developers usually use Requests instead of urllib despite it is built in
because it is easy to use
'''