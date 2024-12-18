from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from services.product_services import ProductService
from schemas.product_schema import (
    Product as productSchema,
    ProductCreate,
    ProductUpdate,
)
from config.prsma_config import prisma
from prisma.errors import UniqueViolationError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


# Get all products
@router.get("/", response_model=List[productSchema], status_code=status.HTTP_200_OK)
async def get_products(product_service: ProductService = Depends()):
    products = await product_service.get_products()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Products not found"
        )
    return products


# Get product by id
@router.get("/{id}", response_model=productSchema, status_code=status.HTTP_200_OK)
async def get_product(id: int, product_service: ProductService = Depends()):
    product = await product_service.get_product(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


# Get product by name
@router.get(
    "/name/{name}", response_model=productSchema, status_code=status.HTTP_200_OK
)
async def get_product_by_name(name: str, product_service: ProductService = Depends()):
    product = await product_service.get_product_by_name(name)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


# Get product by category
@router.get(
    "/category/{category}",
    response_model=List[productSchema],
    status_code=status.HTTP_200_OK,
)
async def get_product_by_category(
    category: str, product_service: ProductService = Depends()
):
    products = await product_service.get_product_by_category(category)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return products


# Search product by name
@router.get(
    "/search/{name}", response_model=List[productSchema], status_code=status.HTTP_200_OK
)
async def search_product(name: str, product_service: ProductService = Depends()):
    products = await product_service.search_product(name)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return products


# Create product
@router.post("/", response_model=productSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, product_service: ProductService = Depends()
):
    product = await product_service.create_product(product)
    logger.info(f"Product created: {product}")
    return product


# Update product
@router.put("/{id}", response_model=productSchema, status_code=status.HTTP_200_OK)
async def update_product(
    id: int, product: ProductUpdate, product_service: ProductService = Depends()
):
    product = await product_service.update_product(id, product)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    logger.info(f"Product updated: {product}")
    return product


# Delete product
@router.delete("/{id}", response_model=productSchema, status_code=status.HTTP_200_OK)
async def delete_product(id: int, product_service: ProductService = Depends()):
    product = await product_service.delete_product(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    logger.info(f"Product deleted: {product}")
    return product
