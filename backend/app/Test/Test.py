from app.models import Sold, User, Shop, Product, Gender, Category, QuantityStatus, Color, Size, Order, OrderStatus
from werkzeug.security import generate_password_hash
import os
from PIL import Image
import uuid
import random
import pandas as pd
from datetime import datetime

DESCRIPTION = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
PATH = 'app/Test/Images'
IMAGE_FOLDER = 'IMAGE_FOLDER'

# default number of products to be created
PRODUCTS_MAX = 100

# default min/max product price
PRICE_MIN = 100
PRICE_MAX = 1000

# default stock quantity
QUANTITY = 1000

# default order quantity per purchase
ORDER_MIN = 1
ORDER_MAX = 5

# default range of dates for purchases
START = '2022-1-1'
END = datetime.now()

def createUser(email, password, usertype):
    user = User(
        firstName = "Lorem",
        lastName = "Ipsum",
        email = email,
        password = generate_password_hash(password),
        address = "Lorem Ipsum, Iloilo",
        number = 639123456789,
        age = 1,
        gender = 1,
        userType = usertype,
    )

    result = user.create()

    if result:
        if user.userType == 'Seller':
            image = getRandomImage()
            shop = Shop(
                user=user.id,
                shopName="Lorem Ipsum Shop",
                address ="Lorem Ipsum, Iloilo",
                description=DESCRIPTION,
                image=save_img(os.path.join(PATH, image))
            )
            shop.create()

        return user.id

def createCategory(id, categoryList):
    shop = Shop.query.filter_by(user=id).first()
    for category in categoryList:
        cat = Category(name=category, shop=shop.id)
        cat.create()

def createColors(id, colors):
    for color in colors:
        c = Color(color=color, product=id)
        c.create()

def createSizes(id, sizes):
    for size in sizes:
        s = Size(size=size, product=id)
        s.create()

def createProducts(id, num):
    print(f"Creating {num} products...")
    shop = Shop.query.filter_by(user=id).first()
    categoryList = Category.query.filter_by(shop=shop.id).all()
    genderList = Gender.query.all()

    for i in range(0, num):
        gender = random.choice(genderList)
        category = random.choice(categoryList)
        image = getRandomImage()

        product = Product(
            shop=shop.id,
            productName= f"Product {i}",
            description = DESCRIPTION,
            price = random.randint(PRICE_MIN, PRICE_MAX),
            image = save_img(os.path.join(PATH, image)),
            gender=gender.id,
            category=category.id
        )

        product.create()

        quantityStatus = QuantityStatus(
            product=product.id,
            quantity = QUANTITY,
            status = True
        )

        sold = Sold(
            product=product.id,
            quantity = 0
        )

        createColors(product.id,
        ["White", "Black", "Red", "Blue"] 
        )

        createSizes(product.id,
            ["S", "M", "L","XL"] 
        )
        sold.create()
        quantityStatus.create()
    
    print("Done!!!")

def getRandomImage():
    images = os.listdir(PATH)
    return random.choice(images)

def save_img(img_path):
    WIDTH = 800

    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    name = str(uuid.uuid4())
    path = IMAGE_FOLDER + "/" + name + '.png'

    im = Image.open(img_path)
    newHeight = int(WIDTH * im.height/im.width)
    im = im.resize((WIDTH, newHeight), resample=Image.LANCZOS)
    im.save(path, 'PNG')

    return name

def purchaseProduct(id, perday, start, end):
    print('Creating sample for purchased products...')
    fullname = "Full Name"
    num = 99999999
    address = "Location, Iloilo City"

    products = Product.query.join(QuantityStatus.query.filter_by(status=True)).all()

    dates = createDates(start, end)

    for date in dates:
        for i in range(perday):
            product = random.choice(products).id
            quantity = random.randint(ORDER_MIN, ORDER_MAX)
            quantityStatus = QuantityStatus.query.filter_by(product=product).first()
            color = random.choice(Color.query.filter_by(product=product).all())
            size = random.choice(Size.query.filter_by(product=product).all())

            if quantityStatus.quantity - quantity > 0:
                status = OrderStatus.query.filter_by(name='COMPLETE').first()
                order = Order(
                    user=id,
                    product=product,
                    quantity=quantity,
                    fullname=fullname,
                    number=num,
                    address=address,
                    status = status.id,
                    color=color.id,
                    size=size.id,
                    dateCreated = date
                )

                order.create()

                quantityStatus.quantity -= quantity
                quantityStatus.update()

                sold = Sold.query.filter_by(product=product).first()
                sold.quantity += quantity
                sold.update()

    print('Done!!!')

def createDates(start, end):
    dates = pd.date_range(start, end)

    return dates

def start():
    # clean image folder
    if os.path.exists(IMAGE_FOLDER):
        for f in os.listdir(IMAGE_FOLDER):
            os.remove(os.path.join(IMAGE_FOLDER,f))

    user = createUser(
        email="test@gmail.com",
        password="test",
        usertype='Seller'
    )

    createCategory(user, 
        ["Jeans", "T-Shirt", "Shorts", "Pants", "Polo", "Shoes", "Dress"]
    )

    createProducts(user, PRODUCTS_MAX)

    buyer = createUser(
        email="buyer@gmail.com",
        password="test",
        usertype='Buyer'
    )

    purchaseProduct(buyer, 1, START, END)

      


