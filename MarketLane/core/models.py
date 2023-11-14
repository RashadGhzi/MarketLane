from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES=(
    ('SG', 'Sun Glass'),
    ('SH', 'Shoes'),
    ('CL', 'Cloth'),
)
GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    product_image = models.ImageField(upload_to='product images')

    def __str__(self) -> str:
        return f"{self.id} : {self.title}"


    
class CustomerAddress(models.Model):
    STATE_CHOICES = [
        ('Rajshahi', (
                ('Bogura', 'Bogura'),
                ('Joypurhat', 'Joypurhat'),
                ('Naogaon', 'Naogaon'),
                ('Natore', 'Natore'),('Chapainawabganj', 'Chapainawabganj'),
                ('Pabna', 'Pabna'),('Rajshahi', 'Rajshahi'),
                ('Sirajganj', 'Sirajganj'),
            )
        ),
        ('Rangpur', (
                ('Dinajpur', 'Dinajpur'),
                ('Gaibandha', 'Gaibandha'),
                ('Kurigram', 'Kurigram'),
                ('Lalmonirhat', 'Lalmonirhat'),
                ('Nilphamari', 'Nilphamari'),('Panchagarh', 'Panchagarh'),
                ('Rangpur', 'Rangpur'),('Thakurgaon', 'Thakurgaon'),
            ) 
        ),
        ('Sylhet', (
                ('Habiganj', 'Habiganj'),
                ('Maulvibazar', 'Maulvibazar'),
                ('Sunamganj', 'Sunamganj'),('Sylhet', 'Sylhet'),
            ) 
        ),
        ('Barisal', (
                ('Barguna', 'Barguna'),
                ('Barisal', 'Barisal'),
                ('Bhola', 'Bhola'),
                ('Jhalokati', 'Jhalokati'),
                ('Patuakhali', 'Patuakhali'),
                ('Pirojpur', 'Pirojpur'),
            )
        ),
        ('Chittagong', (
                ('Bandarban', 'Bandarban'),
                ('Brahmanbaria', 'Brahmanbaria'),
                ('Chandpur', 'Chandpur'),
                ('Chittagong', 'Chittagong'),
                ('Comilla', 'Comilla'),
                ('Cox\'s Bazar', 'Cox\'s Bazar'),
                ('Feni', 'Feni'),
                ('Khagrachhari', 'Khagrachhari'),
                ('Lakshmipur', 'Lakshmipur'),
                ('Noakhali', 'Noakhali'),
                ('Rangamati', 'Rangamati'),
            )
        ),
        ('Dhaka', (
                ('Dhaka', 'Dhaka'),
                ('Faridpur', 'Faridpur'),
                ('Gazipur', 'Gazipur'),
                ('Gopalganj', 'Gopalganj'),
                ('Kishoreganj', 'Kishoreganj'),
                ('Madaripur', 'Madaripur'),
                ('Manikganj', 'Manikganj'),
                ('Munshiganj', 'Munshiganj'),
                ('Narayanganj', 'Narayanganj'),
                ('Narsingdi', 'Narsingdi'),
                ('Rajbari', 'Rajbari'),
                ('Shariatpur', 'Shariatpur'),
                ('Tangail', 'Tangail'),
            )
        ),
        ('Khulna', (
                ('Bagerhat', 'Bagerhat'),
                ('Chuadanga', 'Chuadanga'),
                ('Jessore', 'Jessore'),
                ('Jhenaidah', 'Jhenaidah'),
                ('Khulna', 'Khulna'),
                ('Kushtia', 'Kushtia'),
                ('Magura', 'Magura'),
                ('Meherpur', 'Meherpur'),
                ('Narail', 'Narail'),
                ('Satkhira', 'Satkhira'),
            )
        ),
        ('Mymensingh',(
                ('Jamalpur', 'Jamalpur'),
                ('Mymensingh', 'Mymensingh'),
                ('Netrakona', 'Netrakona'),
                ('Sherpur', 'Sherpur'),
            )
        ),
        ('Rajshahi', (
                ('Bogra', 'Bogra'),
                ('Chapainawabganj', 'Chapainawabganj'),
                ('Joypurhat', 'Joypurhat'),
                ('Naogaon', 'Naogaon'),
                ('Natore', 'Natore'),
                ('Pabna', 'Pabna'),
            )
        ),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES, max_length=15)
    zip_code = models.CharField(max_length=20)
    phone = models.IntegerField()

    def __str__(self):
        return self.address


class ProductCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.user.username}'s Cart"
    
    def get_total_cost(self):
        return self.quantity * self.product.selling_price



class Order(models.Model):
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_loc = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')

    def get_total_price(self):
        return self.product.selling_price * self.quantity