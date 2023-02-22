from django.db import models
from django.contrib.auth.models import User

# Create your models here.

###################################################################
# db_index=True, because Client will search against a title field using db_index
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return f"{self.title}"

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT) # MenuItem belongs to Category.

######### Cart class is a temp storage
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE) # A menuitem can be in serveral Carts. If a menuitem is deleted, so are they in carts.
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        # unique_together = ('menuitem', 'user') # An user can only have one cart at a time.
        constraints = [
            models.UniqueConstraint(fields=['menuitem', 'user'], # Only one menuitem for an user.
                                    name='Unique_insted_of_unuiqe_together')
        ]

class Oreder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, # user & delivery fields are reffering to 'user id' in User table.
                                      related_name="delivery_crew", # So, one of them must use 'related_name'.
                                      null=True)
    status = models.BooleanField(db_index=True, default=0) # To mark an order is done or not.
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

#### All the items from Cart will be moved here.
#    with a link to newly created order ID.
#    And then the Cart will be empty.

class OrderItem(models.Model):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'menuitem'], # Only one menu item for an order.
                                    name='order_item')
        ]

