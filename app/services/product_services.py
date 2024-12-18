from typing import List
from fastapi import HTTPException
from config.prsma_config import prisma
from prisma.errors import UniqueViolationError
from schemas.product_schema import (
    Product as productSchema,
    ProductCreate,
    ProductUpdate,
)


class ProductService:

    # get all products
    async def get_products(self) -> List[productSchema]:
        products = await prisma.product.find_many()
        return [productSchema(**product.model_dump()) for product in products]

    # get product by id
    async def get_product(self, id: int) -> productSchema:
        product = await prisma.product.find_unique(where={"id": id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return productSchema(**product.model_dump())

    # get product by name
    async def get_product_by_name(self, name: str) -> productSchema:
        product = await prisma.product.find_unique(where={"name": name})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return productSchema(**product.model_dump())

    # get product by category
    async def get_product_by_category(self, category: str) -> List[productSchema]:
        products = await prisma.product.find_many(where={"category": category})
        if not products:
            raise HTTPException(status_code=404, detail="Product not found")
        return [productSchema(**product.model_dump()) for product in products]

    # create product
    async def create_product(self, product: ProductCreate) -> productSchema:
        try:
            product = await prisma.product.create(data=product.model_dump())
            return productSchema(**product.model_dump())
        except UniqueViolationError:
            raise HTTPException(status_code=409, detail="Product already exists")

    # update product
    async def update_product(self, id: int, product: ProductUpdate) -> productSchema:
        product = await prisma.product.update(
            where={"id": id}, data=product.model_dump()
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return productSchema(**product.model_dump())

    # delete product
    async def delete_product(self, id: int) -> productSchema:
        product = await prisma.product.delete(where={"id": id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return productSchema(**product.model_dump())

    # search product
    async def search_product(self, name: str) -> List[productSchema]:
        products = await prisma.product.find_many(where={"name": {"contains": name}})
        if not products:
            raise HTTPException(status_code=404, detail="Product not found")
        return [productSchema(**product.model_dump()) for product in products]
