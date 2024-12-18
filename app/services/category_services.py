from typing import List
from fastapi import HTTPException
from config.prsma_config import prisma
from prisma.errors import UniqueViolationError
from schemas.category_schema import (
    Category as categorySchema,
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:

    # get all categories
    async def get_categories(self) -> List[categorySchema]:
        categories = await prisma.category.find_many()
        return [categorySchema(**category.model_dump()) for category in categories]

    # get category by id
    async def get_category(self, id: int) -> categorySchema:
        category = await prisma.category.find_unique(where={"id": id})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return categorySchema(**category.model_dump())

    # get category by name
    async def get_category_by_name(self, name: str) -> categorySchema:
        category = await prisma.category.find_unique(where={"name": name})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return categorySchema(**category.model_dump())

    # create category
    async def create_category(self, category: CategoryCreate) -> categorySchema:
        try:
            category = await prisma.category.create(data=category.model_dump())
            return categorySchema(**category.model_dump())
        except UniqueViolationError:
            raise HTTPException(status_code=409, detail="Category already exists")

    # update category
    async def update_category(
        self, id: int, category: CategoryUpdate
    ) -> categorySchema:
        category = await prisma.category.update(
            where={"id": id}, data=category.model_dump()
        )
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return categorySchema(**category.model_dump())

    # delete category
    async def delete_category(self, id: int) -> categorySchema:
        category = await prisma.category.delete(where={"id": id})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return categorySchema(**category.model_dump())

    # search category
    async def search_category(self, name: str) -> List[categorySchema]:
        categories = await prisma.category.find_many(where={"name": {"contains": name}})
        if not categories:
            raise HTTPException(status_code=404, detail="Category not found")
        return [categorySchema(**category.model_dump()) for category in categories]
