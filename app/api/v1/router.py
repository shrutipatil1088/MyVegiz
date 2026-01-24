from fastapi import APIRouter
from app.api.v1.routes.users import router as user_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.categories import router as category_router
from app.api.v1.routes.products import router as product_router
from app.api.v1.routes.uoms import router as uom_router
from app.api.v1.routes.profile_update import router as profile_router
from app.api.v1.routes.email_settings import router as email_settings_router
from app.api.v1.routes.main_categories import router as main_category_router
from app.api.v1.routes.sub_categories import router as sub_category_router
from app.api.v1.routes.zones import router as zone_router
from app.api.v1.routes.product_variants import router as product_variant_router  # ✅ ADD THIS

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(category_router,prefix="/categories",tags=["Categories"])
api_router.include_router(product_router,prefix="/products",tags=["Products"])
api_router.include_router(uom_router,prefix="/uoms",tags=["UOMs"])
api_router.include_router(profile_router, prefix="/users", tags=["Users"])
api_router.include_router(email_settings_router,prefix="/email-settings",tags=["Email Settings"])
api_router.include_router(main_category_router,prefix="/main-categories",tags=["Main Categories"])
api_router.include_router(sub_category_router,prefix="/sub-categories",tags=["Sub Categories"])
api_router.include_router(zone_router,prefix="/zone",tags=["Zone"])

api_router.include_router(product_variant_router, prefix="/product-variants", tags=["Product Variants"])  # ✅
