from sqlmodel import SQLModel, Relationship
from sqlmodel import Field as SqlField
from pydantic import BaseModel
from pydantic import Field as PydField
from datetime import datetime


class ProductSpecs(SQLModel, table=True):
    product_id: int | None = SqlField(
        default=None, foreign_key="product.id", primary_key=True
    )
    spec_id: int | None = SqlField(
        default=None, foreign_key="spec.id", primary_key=True
    )
    value: str

    product: "Product" = Relationship(back_populates="spec_links")
    spec: "Spec" = Relationship(back_populates="product_links")

class Comments(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    product_id: int | None = SqlField(
        default=None, foreign_key="product.id"
    )
    user_id: int | None = SqlField(
        default=None, foreign_key="user.id"
    )
    rate: int = SqlField(ge=0, le=5)
    text: str

    product: "Product" = Relationship(back_populates="user_comment_links")
    user: "User" = Relationship(back_populates="product_comment_links")


class Cart(SQLModel, table=True):
    order_id: int | None = SqlField(
        default=None, foreign_key="order.id", primary_key=True
    )
    product_id: int | None = SqlField(
        default=None, foreign_key="product.id", primary_key=True
    )
    count: int

    order: "Order" = Relationship(back_populates="product_links")
    product: "Product" = Relationship(back_populates="order_links")


class Category(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str = SqlField(unique=True)

    products: list["Product"] = Relationship(
        back_populates="category", cascade_delete=True
    )

class Status(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str = SqlField(unique=True)

    orders: list["Order"] = Relationship(back_populates="status")

class Order(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    user_id: int = SqlField(foreign_key="user.id")
    is_available: bool = SqlField(default=False)
    status_id: int | None = SqlField(foreign_key="status.id", default=None)
    address: str | None = SqlField(default=None)
    date: datetime | None = SqlField(default=None)

    user: User = Relationship(back_populates="orders")
    status: Status = Relationship(back_populates="orders")
    product_links: list[Cart] = Relationship(back_populates="order", cascade_delete=True)


class Product(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str
    description: str | None = SqlField(default="Отсутствует")
    category_id: int = SqlField(foreign_key="category.id")
    price: float = SqlField(ge=0)
    quantity: int = SqlField(ge=0)

    category: Category = Relationship(back_populates="products")
    images: list["Image"] | None = Relationship(
        back_populates="product", cascade_delete=True
    )
    spec_links: list[ProductSpecs] = Relationship(
        back_populates="product", cascade_delete=True
    )
    order_links: list[Cart] = Relationship(back_populates="product")
    user_comment_links: list[Comments] = Relationship(back_populates="product")


class Image(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    image_link: str
    is_main: bool
    product_id: int = SqlField(foreign_key="product.id")

    product: Product = Relationship(back_populates="images")


class Role(SQLModel, table=True):
    id: int = SqlField(default=None, primary_key=True)
    name: str

    users: list["User"] = Relationship(back_populates="role", cascade_delete=True)


class User(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    login: str = SqlField(unique=True)
    password: str
    email: str = SqlField(unique=True)
    role_id: int = SqlField(foreign_key="role.id")
    refresh_token: str | None = SqlField(default=None)

    role: Role = Relationship(back_populates="users")
    # order_links: list[Order] = Relationship(back_populates="user")
    product_comment_links: list[Comments] = Relationship(back_populates="user", cascade_delete=True)
    orders: list["Order"] = Relationship(back_populates="user", cascade_delete=True)

class Spec(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str = SqlField(unique=True)

    product_links: list[ProductSpecs] = Relationship(
        back_populates="spec"
    )

class Table(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str = SqlField(unique=True)

    logs: list["Log"] = Relationship(back_populates="table", cascade_delete=True)

class Type(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str = SqlField(unique=True)

    logs: list["Log"] = Relationship(back_populates="type", cascade_delete=True)

class Log(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    user_id: int = SqlField(foreign_key="user.id")
    table_id: int = SqlField(foreign_key="table.id")
    type_id: int = SqlField(foreign_key="type.id")
    object_id: int
    old_data: str | None = SqlField(default=None)
    new_data: str | None = SqlField(default=None)
    date: datetime | None = SqlField(default=datetime.now())

    table: Table = Relationship(back_populates="logs")
    type: Type = Relationship(back_populates="logs")

# ПОЛЬЗОВАТЕЛИ
class RegUser(BaseModel):
    login: str = PydField(min_length=5)
    password: str = PydField(min_length=5)
    confirm_psw: str
    email: str = PydField(example="email@mail.ru", pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class LoginUser(BaseModel):
    login: str = PydField(example="Admin")
    password: str = PydField(example="Admin")

class ResponseUser(BaseModel):
    id: int
    login: str
    email: str
    role: Role
    refresh_token: str | None = PydField(default=None)
    access_token: str | None = PydField(default=None)

class UpdateUser(BaseModel):
    login: str | None = PydField(default="")
    old_password: str | None = PydField(default="")
    new_password: str | None = PydField(default="")
    email: str = PydField(default=None, example="email@mail.ru", pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    role: str | None = PydField(default=None)

# ТОВАРЫ

class ResponseProduct(BaseModel):
    id: int
    name: str
    description: str | None = PydField(default="Отсутствует")
    category: Category
    price: float
    quantity: int
    images: list[Image]
    spec_links: list[ProductSpecs]
    user_comment_links: list[Comments]

class ResponsePageProducts(BaseModel):
    id: int
    name: str
    description: str | None = PydField(default="Отсутствует")
    category: Category
    price: float
    quantity: int

class PageResponse(BaseModel):
    page: int
    elements_on_page: int
    total_pages: int
    products: list[ResponsePageProducts]

class NewProduct(BaseModel):
    name: str
    description: str | None = PydField(default="Отсутствует")
    category_id: int
    price: float = PydField(ge=0)
    quantity: int = PydField(ge=0)

class EditProduct(BaseModel):
    name: str | None = PydField(default="")
    description: str | None = PydField(default="")
    category_id: int | None = PydField(default=None)
    price: float | None = PydField(default=None, ge=0)
    quantity: int | None = PydField(default=None, ge=0)

# ЗАКАЗЫ

class ResponseOrder(BaseModel):
    id: int
    user_id: int
    is_available: bool
    status: Status | None = PydField(default=None)
    address: str | None = PydField(default=None)
    date: datetime | None = PydField(default=None)
    product_links: list[Cart]

class FullOrderResponse(BaseModel):
    order: ResponseOrder
    full_price: float

class OrderData(BaseModel):
    is_available: bool | None = PydField(default=None)
    status_id: int | None = PydField(default=None)
    address: str | None = PydField(default="")
    date: datetime | None = PydField(default=None)
    new_products_id: list[int] | None = PydField(default=None)
    delete_products_id: list[int] | None = PydField(default=None)

class AmountChange(BaseModel):
    product_id: int
    amount: int = PydField(ge=0)

# ОТЗЫВЫ

class NewComment(BaseModel):
    product_id: int
    rate: int = PydField(ge=0, le=5)
    text: str = PydField(min_length=3, max_length=200)

class EditComment(BaseModel):
    rate: int | None = PydField(default=None, ge=0, le=5)
    text: str | None = PydField(default=None, min_length=3, max_length=200)

class DeleteComment(BaseModel):
    reason: str | None = PydField(default=None)