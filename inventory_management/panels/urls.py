from django.urls import path
from. import views

urlpatterns = [
   path("",views.dashboard,name="dashboard"),
   path("branch",views.branch_table,name="list_branch"),
   path("branch-json",views.branch_table_json,name="list_branch_json"),
   path("add-branch",views.add_branch,name="add_branch"),
   path("add-product",views.add_product,name="add_product"),
   path("add-manager",views.add_manager,name="add_manager"),
   path("edit_branch/<int:id>",views.edit_branch,name="edit_branch"),
   path("show_products/<int:id>",views.show_products_in_branch,name="show_branch"),
   path("product-json/<int:id>",views.product_table_json,name="list_product_json"),
   path("show_branches/<int:id>",views.show_branch_under_dealer,name="list_branch_under_dealer"),
   path("show_branches_json/<int:id>",views.show_branch_under_dealer_table_json,name="list_branch_under_dealer_json"),
   path("dealer",views.dealer_table,name="list_dealer"),
   path("dealer-json",views.dealer_table_json,name="list_dealer_json"),
   path("cart-view",views.cart_view,name="cart_view"),
   path("list_product",views.product_list,name="product_list"),
   path("add-to-cart/<int:product_id>",views.add_to_cart,name="add_to_cart"),
   path("update-cart/<int:product_id>",views.update_cart,name="update_cart"),
   path("delete-cart/<int:product_id>",views.remove_from_cart,name="delete_cart"),
   path("checkout/",views.process_checkout,name="checkout"),
]
